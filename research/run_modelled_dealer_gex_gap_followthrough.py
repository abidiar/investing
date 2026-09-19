#!/usr/bin/env python3
"""Frozen Investing OS experiment: modelled dealer-GEX gap follow-through v1.0.

Rules are frozen in research/modelled_dealer_gex_gap_followthrough_v1.md.
Do not change sample, sign convention, features, models, outcomes, or gates after results.
"""
from __future__ import annotations

import os
from pathlib import Path
from datetime import datetime, timezone

import numpy as np
import pandas as pd
from scipy.stats import spearmanr
from sklearn.linear_model import LogisticRegression, Ridge
from sklearn.metrics import brier_score_loss, mean_absolute_error

DATA_DIR = Path(os.environ.get("GEX_PROXY_DATA_DIR", "/tmp/modelled_gex_proxy"))
OUT = Path("research/results")
OUT.mkdir(parents=True, exist_ok=True)

SYMBOLS = ["SPY", "IWM"]
TRAIN_YEARS = [2008]
TEST_YEARS = [2009, 2010]
ALL_YEARS = TRAIN_YEARS + TEST_YEARS
GAP_MIN = 0.0025

BASE_COLS = [
    "abs_gap",
    "gap_atr20",
    "gap_up",
    "day_abs_oc",
    "day_range",
    "rv5",
    "rv20",
    "median20_range",
    "atr20",
    "range20_ratio",
    "log_adv20_dollar",
    "prior_cc_aligned",
    "prior_oc_aligned",
]
GEX_COL = "signed_gex_to_adv"


def _lower_columns(df: pd.DataFrame) -> pd.DataFrame:
    x = df.copy()
    x.columns = [str(c).strip().lower().replace(" ", "_") for c in x.columns]
    return x


def load_prices(symbol: str) -> pd.DataFrame:
    fp = DATA_DIR / f"{symbol.lower()}_underlying_prices.parquet"
    if not fp.exists():
        raise RuntimeError(f"Missing underlying file: {fp}")
    p = _lower_columns(pd.read_parquet(fp))

    aliases = {
        "date": ["date", "datetime", "timestamp"],
        "open": ["open", "o"],
        "high": ["high", "h"],
        "low": ["low", "l"],
        "close": ["close", "c", "adj_close", "adjclose"],
        "volume": ["volume", "v"],
    }
    resolved = {}
    for target, choices in aliases.items():
        hit = next((c for c in choices if c in p.columns), None)
        if hit is None:
            raise RuntimeError(f"{symbol} price file missing {target}; columns={list(p.columns)}")
        resolved[target] = hit
    p = p.rename(columns={v: k for k, v in resolved.items()})
    p = p[["date", "open", "high", "low", "close", "volume"]].copy()
    p["date"] = pd.to_datetime(p["date"], errors="coerce").dt.tz_localize(None).dt.normalize()
    for c in ["open", "high", "low", "close", "volume"]:
        p[c] = pd.to_numeric(p[c], errors="coerce")
    p = p.dropna().drop_duplicates("date").sort_values("date").set_index("date")

    p["prev_close"] = p["close"].shift(1)
    p["cc"] = p["close"].pct_change()
    p["oc"] = p["close"] / p["open"] - 1.0
    p["day_abs_oc"] = p["oc"].abs()
    p["day_range"] = (p["high"] - p["low"]) / p["open"]
    p["rv5"] = p["cc"].rolling(5).std(ddof=1)
    p["rv20"] = p["cc"].rolling(20).std(ddof=1)
    p["median20_range"] = p["day_range"].rolling(20).median()
    tr = pd.concat([
        p["high"] - p["low"],
        (p["high"] - p["prev_close"]).abs(),
        (p["low"] - p["prev_close"]).abs(),
    ], axis=1).max(axis=1)
    p["norm_true_range"] = tr / p["prev_close"]
    p["atr20"] = p["norm_true_range"].rolling(20).mean()
    p["range20_ratio"] = p["day_range"] / p["median20_range"]
    p["dollar_volume"] = p["close"] * p["volume"]
    p["adv20_dollar"] = p["dollar_volume"].rolling(20).mean()
    p["log_adv20_dollar"] = np.log(p["adv20_dollar"].where(p["adv20_dollar"] > 0))

    p["next_date"] = pd.Series(p.index, index=p.index).shift(-1).values
    p["next_open"] = p["open"].shift(-1)
    p["next_high"] = p["high"].shift(-1)
    p["next_low"] = p["low"].shift(-1)
    p["next_close"] = p["close"].shift(-1)
    return p


def load_options(symbol: str, year: int) -> pd.DataFrame:
    fp = DATA_DIR / f"{symbol.lower()}_options_{year}.parquet"
    if not fp.exists():
        raise RuntimeError(f"Missing options file: {fp}")
    cols = ["date", "expiration", "type", "open_interest", "gamma"]
    x = pd.read_parquet(fp, columns=cols)
    x = _lower_columns(x)
    x["date"] = pd.to_datetime(x["date"], errors="coerce").dt.tz_localize(None).dt.normalize()
    x["expiration"] = pd.to_datetime(x["expiration"], errors="coerce").dt.tz_localize(None).dt.normalize()
    x["open_interest"] = pd.to_numeric(x["open_interest"], errors="coerce")
    x["gamma"] = pd.to_numeric(x["gamma"], errors="coerce")
    x["type"] = x["type"].astype(str).str.lower().str.strip()
    x["dte"] = (x["expiration"] - x["date"]).dt.days
    x = x[(x["date"].dt.year == year) & (x["dte"] >= 1)]
    x = x[x["open_interest"].notna() & (x["open_interest"] >= 0)]
    x = x[x["gamma"].notna() & np.isfinite(x["gamma"]) & (x["gamma"] > 0)]
    x["is_call"] = x["type"].str.startswith("c")
    x["is_put"] = x["type"].str.startswith("p")
    x = x[x["is_call"] | x["is_put"]]
    return x


def day_gex(chain: pd.DataFrame, spot: float) -> dict:
    if chain.empty or not np.isfinite(spot) or spot <= 0:
        return {}
    base = chain["gamma"].to_numpy(float) * chain["open_interest"].to_numpy(float) * 100.0 * spot * spot * 0.01
    calls = chain["is_call"].to_numpy(bool)
    puts = chain["is_put"].to_numpy(bool)
    call_d = float(base[calls].sum())
    put_d = float(base[puts].sum())
    return {
        "eligible_contracts": int(len(chain)),
        "call_dgamma": call_d,
        "put_dgamma": put_d,
        "signed_dgex": call_d - put_d,
        "gross_dgex": call_d + put_d,
    }


def build_panel() -> tuple[pd.DataFrame, dict]:
    prices = {s: load_prices(s) for s in SYMBOLS}
    rows = []
    exclusions = {s: {"no_price": 0, "no_next": 0, "no_history": 0, "no_gex": 0, "small_gap": 0} for s in SYMBOLS}

    for symbol in SYMBOLS:
        p = prices[symbol]
        for year in ALL_YEARS:
            opt = load_options(symbol, year)
            for d, chain in opt.groupby("date", sort=True):
                d = pd.Timestamp(d).normalize()
                if d not in p.index:
                    exclusions[symbol]["no_price"] += 1
                    continue
                q = p.loc[d]
                if any(pd.isna(q[c]) for c in ["next_open", "next_high", "next_low", "next_close"]):
                    exclusions[symbol]["no_next"] += 1
                    continue
                needed = ["day_abs_oc", "day_range", "rv5", "rv20", "median20_range", "atr20", "range20_ratio", "adv20_dollar", "log_adv20_dollar", "cc", "oc"]
                if any(pd.isna(q[c]) or not np.isfinite(float(q[c])) for c in needed):
                    exclusions[symbol]["no_history"] += 1
                    continue
                if float(q["atr20"]) <= 0 or float(q["adv20_dollar"]) <= 0:
                    exclusions[symbol]["no_history"] += 1
                    continue

                spot = float(q["close"])
                gx = day_gex(chain, spot)
                if not gx or gx["eligible_contracts"] <= 0 or gx["gross_dgex"] <= 0:
                    exclusions[symbol]["no_gex"] += 1
                    continue

                o = float(q["next_open"]); h = float(q["next_high"]); l = float(q["next_low"]); c = float(q["next_close"])
                gap = o / spot - 1.0
                if not np.isfinite(gap) or abs(gap) < GAP_MIN or gap == 0:
                    exclusions[symbol]["small_gap"] += 1
                    continue
                direction = 1.0 if gap > 0 else -1.0
                follow = direction * (c / o - 1.0)
                if direction > 0:
                    mfe = max(h / o - 1.0, 0.0)
                    mae = max(1.0 - l / o, 0.0)
                else:
                    mfe = max(1.0 - l / o, 0.0)
                    mae = max(h / o - 1.0, 0.0)
                denom = mfe + mae
                eff = mfe / denom if denom > 0 else np.nan
                rth_range = (h - l) / o

                row = {
                    "symbol": symbol,
                    "year": int(d.year),
                    "date": d,
                    "next_date": pd.Timestamp(q["next_date"]).normalize(),
                    "gap": gap,
                    "abs_gap": abs(gap),
                    "gap_atr20": abs(gap) / float(q["atr20"]),
                    "gap_up": float(gap > 0),
                    "day_abs_oc": float(q["day_abs_oc"]),
                    "day_range": float(q["day_range"]),
                    "rv5": float(q["rv5"]),
                    "rv20": float(q["rv20"]),
                    "median20_range": float(q["median20_range"]),
                    "atr20": float(q["atr20"]),
                    "range20_ratio": float(q["range20_ratio"]),
                    "adv20_dollar": float(q["adv20_dollar"]),
                    "log_adv20_dollar": float(q["log_adv20_dollar"]),
                    "prior_cc_aligned": direction * float(q["cc"]),
                    "prior_oc_aligned": direction * float(q["oc"]),
                    "signed_gex_to_adv": gx["signed_dgex"] / float(q["adv20_dollar"]),
                    "gross_gex_to_adv": gx["gross_dgex"] / float(q["adv20_dollar"]),
                    "followthrough_oc": follow,
                    "continued": float(follow > 0),
                    "mfe": mfe,
                    "mae": mae,
                    "excursion_efficiency": eff,
                    "rth_range": rth_range,
                    **gx,
                }
                rows.append(row)
            del opt

    panel = pd.DataFrame(rows).replace([np.inf, -np.inf], np.nan).dropna()
    panel = panel.sort_values(["date", "symbol"]).reset_index(drop=True)
    return panel, exclusions


def matrix(df: pd.DataFrame, cols: list[str], mu=None, sd=None):
    X = df[cols].to_numpy(float)
    if mu is None:
        mu = X.mean(axis=0)
        sd = X.std(axis=0)
        sd = np.where(sd == 0, 1.0, sd)
    Xs = (X - mu) / sd
    iwm = (df["symbol"].to_numpy() == "IWM").astype(float).reshape(-1, 1)
    return np.column_stack([Xs, iwm]), mu, sd


def predict_logistic(train, test, cols):
    Xtr, mu, sd = matrix(train, cols)
    Xte, _, _ = matrix(test, cols, mu, sd)
    y = train["continued"].astype(int).to_numpy()
    if len(np.unique(y)) < 2:
        return np.full(len(test), float(np.mean(y)))
    m = LogisticRegression(C=1.0, penalty="l2", solver="lbfgs", class_weight=None, max_iter=3000, random_state=0)
    m.fit(Xtr, y)
    return m.predict_proba(Xte)[:, 1]


def predict_ridge(train, test, cols, target):
    Xtr, mu, sd = matrix(train, cols)
    Xte, _, _ = matrix(test, cols, mu, sd)
    y = train[target].to_numpy(float)
    m = Ridge(alpha=1.0)
    m.fit(Xtr, y)
    return m.predict(Xte)


def walk_forward(panel: pd.DataFrame) -> pd.DataFrame:
    test_all = panel[panel["year"].isin(TEST_YEARS)].copy()
    if len(panel[panel["year"].isin(TRAIN_YEARS)]) < 100:
        raise RuntimeError("Too few 2008 seed candidates")
    out = []
    for current_date in sorted(test_all["date"].unique()):
        train = panel[panel["date"] < current_date]
        test = test_all[test_all["date"] == current_date]
        if test.empty:
            continue
        pa = predict_logistic(train, test, BASE_COLS)
        pb = predict_logistic(train, test, BASE_COLS + [GEX_COL])
        fta = predict_ridge(train, test, BASE_COLS, "followthrough_oc")
        ftb = predict_ridge(train, test, BASE_COLS + [GEX_COL], "followthrough_oc")
        efa = predict_ridge(train, test, BASE_COLS, "excursion_efficiency")
        efb = predict_ridge(train, test, BASE_COLS + [GEX_COL], "excursion_efficiency")
        for j, (_, r) in enumerate(test.iterrows()):
            row = r.to_dict()
            row.update({
                "p_cont_price": float(pa[j]),
                "p_cont_gex": float(pb[j]),
                "pred_ft_price": float(fta[j]),
                "pred_ft_gex": float(ftb[j]),
                "pred_eff_price": float(efa[j]),
                "pred_eff_gex": float(efb[j]),
            })
            out.append(row)
    return pd.DataFrame(out).sort_values(["date", "symbol"]).reset_index(drop=True)


def corr_row(df: pd.DataFrame, label: str) -> dict:
    def sp(x, y):
        if len(x) < 5 or x.nunique() < 2 or y.nunique() < 2:
            return (np.nan, np.nan)
        r = spearmanr(x, y, nan_policy="omit")
        return float(r.statistic), float(r.pvalue)
    r_ft, p_ft = sp(df[GEX_COL], df["followthrough_oc"])
    r_eff, p_eff = sp(df[GEX_COL], df["excursion_efficiency"])
    return {"sample": label, "n": len(df), "rho_ft": r_ft, "p_ft": p_ft, "rho_eff": r_eff, "p_eff": p_eff}


def pred_metrics(df: pd.DataFrame, label: str) -> dict:
    if df.empty:
        return {"sample": label, "n": 0}
    def rel_improve(a, b):
        return (a - b) / a if a > 0 else np.nan
    brier_a = brier_score_loss(df["continued"], df["p_cont_price"])
    brier_b = brier_score_loss(df["continued"], df["p_cont_gex"])
    ft_a = mean_absolute_error(df["followthrough_oc"], df["pred_ft_price"])
    ft_b = mean_absolute_error(df["followthrough_oc"], df["pred_ft_gex"])
    eff_a = mean_absolute_error(df["excursion_efficiency"], df["pred_eff_price"])
    eff_b = mean_absolute_error(df["excursion_efficiency"], df["pred_eff_gex"])
    ft_rho_a = spearmanr(df["followthrough_oc"], df["pred_ft_price"], nan_policy="omit").statistic
    ft_rho_b = spearmanr(df["followthrough_oc"], df["pred_ft_gex"], nan_policy="omit").statistic
    eff_rho_a = spearmanr(df["excursion_efficiency"], df["pred_eff_price"], nan_policy="omit").statistic
    eff_rho_b = spearmanr(df["excursion_efficiency"], df["pred_eff_gex"], nan_policy="omit").statistic
    return {
        "sample": label,
        "n": len(df),
        "brier_a": brier_a,
        "brier_b": brier_b,
        "brier_improvement_rel": rel_improve(brier_a, brier_b),
        "ft_mae_a": ft_a,
        "ft_mae_b": ft_b,
        "ft_mae_improvement_rel": rel_improve(ft_a, ft_b),
        "eff_mae_a": eff_a,
        "eff_mae_b": eff_b,
        "eff_mae_improvement_rel": rel_improve(eff_a, eff_b),
        "ft_pred_rho_a": float(ft_rho_a),
        "ft_pred_rho_b": float(ft_rho_b),
        "eff_pred_rho_a": float(eff_rho_a),
        "eff_pred_rho_b": float(eff_rho_b),
    }


def regime_stats(df: pd.DataFrame) -> pd.DataFrame:
    rows = []
    for label, x in [("NEGATIVE_PROXY", df[df[GEX_COL] < 0]), ("POSITIVE_PROXY", df[df[GEX_COL] >= 0])]:
        rows.append({
            "regime": label,
            "n": len(x),
            "mean_gex_to_adv": x[GEX_COL].mean(),
            "continuation_rate": x["continued"].mean(),
            "mean_followthrough_oc": x["followthrough_oc"].mean(),
            "mean_mfe": x["mfe"].mean(),
            "mean_mae": x["mae"].mean(),
            "mean_efficiency": x["excursion_efficiency"].mean(),
            "mean_rth_range": x["rth_range"].mean(),
        })
    return pd.DataFrame(rows)


def pct(x):
    return "nan" if pd.isna(x) else f"{100*x:.2f}%"


def main():
    panel, exclusions = build_panel()
    panel.to_csv(OUT / "modelled_dealer_gex_gap_followthrough_v1_panel.csv", index=False)
    preds = walk_forward(panel)
    preds.to_csv(OUT / "modelled_dealer_gex_gap_followthrough_v1_predictions.csv", index=False)

    hold = preds.copy()
    corr_rows = [corr_row(hold, "FULL")]
    for s in SYMBOLS:
        corr_rows.append(corr_row(hold[hold["symbol"] == s], f"SYMBOL_{s}"))
    for y in TEST_YEARS:
        corr_rows.append(corr_row(hold[hold["year"] == y], f"YEAR_{y}"))
    corrs = pd.DataFrame(corr_rows)
    corrs.to_csv(OUT / "modelled_dealer_gex_gap_followthrough_v1_correlations.csv", index=False)

    metric_rows = [pred_metrics(hold, "FULL")]
    for s in SYMBOLS:
        metric_rows.append(pred_metrics(hold[hold["symbol"] == s], f"SYMBOL_{s}"))
    for y in TEST_YEARS:
        metric_rows.append(pred_metrics(hold[hold["year"] == y], f"YEAR_{y}"))
    metrics = pd.DataFrame(metric_rows)
    metrics.to_csv(OUT / "modelled_dealer_gex_gap_followthrough_v1_metrics.csv", index=False)

    regimes = regime_stats(hold)
    regimes.to_csv(OUT / "modelled_dealer_gex_gap_followthrough_v1_regimes.csv", index=False)

    fullc = corrs[corrs["sample"] == "FULL"].iloc[0]
    fullm = metrics[metrics["sample"] == "FULL"].iloc[0]
    subgroup = corrs[corrs["sample"].isin(["SYMBOL_SPY", "SYMBOL_IWM", "YEAR_2009", "YEAR_2010"])]
    stable_count = int(((subgroup["rho_ft"] < 0) & (subgroup["rho_eff"] < 0)).sum())

    gate1 = bool(fullc["rho_ft"] < 0 and fullc["rho_eff"] < 0)
    gate2 = stable_count >= 3
    gate3 = bool(fullm["brier_improvement_rel"] >= 0.02)
    gate4 = bool(fullm["ft_mae_improvement_rel"] >= 0.02)
    gate5 = bool(fullm["eff_mae_improvement_rel"] >= -0.01)

    if gate1 and gate2 and gate3 and gate4 and gate5:
        verdict = "SUPPORTED FOR FURTHER DEALER-DATA REPLICATION"
    elif gate1 and gate2 and not (gate3 and gate4):
        verdict = "MECHANISM-CONSISTENT / INCREMENTAL UTILITY NOT SUPPORTED"
    else:
        verdict = "PROXY FAILED / NOT SUPPORTED"

    neg = regimes[regimes["regime"] == "NEGATIVE_PROXY"].iloc[0]
    pos = regimes[regimes["regime"] == "POSITIVE_PROXY"].iloc[0]
    generated = datetime.now(timezone.utc).isoformat()
    md = f"""# Modelled Dealer-GEX Gap Follow-Through v1.0 — Frozen Results

Generated: {generated}

## Measurement warning
This experiment uses a **MODELLED DEALER-GEX PROXY**, not observed dealer inventory. Calls are assumed dealer-long-gamma and puts dealer-short-gamma, following the frozen published proxy convention.

## Coverage
- Total panel rows (2008-2010): **{len(panel)}**
- 2008 seed candidates: **{len(panel[panel['year'] == 2008])}**
- Untouched 2009-2010 holdout candidates: **{len(hold)}**
- SPY holdout: **{len(hold[hold['symbol'] == 'SPY'])}**
- IWM holdout: **{len(hold[hold['symbol'] == 'IWM'])}**
- Exclusions: `{exclusions}`

## Frozen mechanism tests
- Signed GEX/ADV -> gap-direction open-to-close follow-through: **rho={fullc['rho_ft']:.4f}, p={fullc['p_ft']:.4g}** (expected <0)
- Signed GEX/ADV -> excursion efficiency: **rho={fullc['rho_eff']:.4f}, p={fullc['p_eff']:.4g}** (expected <0)
- Prespecified subgroups with both expected signs: **{stable_count}/4**

### Subgroup correlations
{corrs.to_markdown(index=False)}

## Negative vs positive modelled proxy states
| metric | Negative proxy | Positive proxy |
|---|---:|---:|
| n | {int(neg['n'])} | {int(pos['n'])} |
| continuation rate | {pct(neg['continuation_rate'])} | {pct(pos['continuation_rate'])} |
| mean gap-direction O/C follow-through | {pct(neg['mean_followthrough_oc'])} | {pct(pos['mean_followthrough_oc'])} |
| mean MFE | {pct(neg['mean_mfe'])} | {pct(pos['mean_mfe'])} |
| mean MAE | {pct(neg['mean_mae'])} | {pct(pos['mean_mae'])} |
| mean excursion efficiency | {pct(neg['mean_efficiency'])} | {pct(pos['mean_efficiency'])} |
| mean RTH range | {pct(neg['mean_rth_range'])} | {pct(pos['mean_rth_range'])} |

## Incremental predictive value
- Continuation Brier A (price/vol/liquidity): **{fullm['brier_a']:.6f}**
- Continuation Brier B (+ modelled GEX): **{fullm['brier_b']:.6f}**
- Relative Brier improvement: **{pct(fullm['brier_improvement_rel'])}**
- Follow-through MAE A: **{pct(fullm['ft_mae_a'])}**
- Follow-through MAE B: **{pct(fullm['ft_mae_b'])}**
- Relative follow-through MAE improvement: **{pct(fullm['ft_mae_improvement_rel'])}**
- Excursion-efficiency MAE A: **{fullm['eff_mae_a']:.6f}**
- Excursion-efficiency MAE B: **{fullm['eff_mae_b']:.6f}**
- Relative efficiency-MAE improvement: **{pct(fullm['eff_mae_improvement_rel'])}**

### Robustness metrics
{metrics.to_markdown(index=False)}

## Frozen gates
- Full-sample expected sign for both primary outcomes: **{'PASS' if gate1 else 'FAIL'}**
- Expected sign in >=3/4 prespecified subgroups: **{'PASS' if gate2 else 'FAIL'}**
- Continuation Brier improvement >=2%: **{'PASS' if gate3 else 'FAIL'}**
- Follow-through MAE improvement >=2%: **{'PASS' if gate4 else 'FAIL'}**
- Efficiency MAE not worse by >1%: **{'PASS' if gate5 else 'FAIL'}**

## Overall frozen verdict
**{verdict}**

## Interpretation constraint
This is an old-regime (2009-2010), daily-OHLC proxy study using an assumed dealer sign. Even a positive result cannot authorize an Investing OS scanner change. It can only justify replication with stronger participant/signed-flow data and modern intraday outcomes.
"""
    (OUT / "modelled_dealer_gex_gap_followthrough_v1_results.md").write_text(md)
    (OUT / "modelled_dealer_gex_gap_followthrough_v1_run.log").write_text(md)
    print(md)


if __name__ == "__main__":
    main()
