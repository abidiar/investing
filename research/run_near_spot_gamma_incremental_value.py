#!/usr/bin/env python3
"""Frozen Investing OS experiment: near-spot unsigned gamma incremental value v1.0.

Rules are frozen in research/near_spot_gamma_incremental_value_v1.md.
Do not change controls, thresholds, sample, or promotion gates after results.
"""
from __future__ import annotations

import math
import os
from pathlib import Path
from datetime import datetime, timezone

import numpy as np
import pandas as pd
from scipy import stats
import statsmodels.api as sm
import yfinance as yf

DATA_DIR = Path(os.environ.get("OPTIONS_DATA_DIR", "/tmp/options_gamma_incremental"))
OUT = Path("research/results")
OUT.mkdir(parents=True, exist_ok=True)

SYMBOLS = ["SPY", "QQQ", "IWM"]
YEARS = [2020, 2021, 2022]
MIN_DTE = 1
MAX_DTE = 30
MONEYNESS = 0.05
IV_MIN = 0.05
IV_MAX = 2.00
NEAR_05 = 0.005
MIN_TRAIN_ROWS = 500
EPS = 1e-6

CONTROL_COLS = [
    "day_abs_oc", "day_range", "rv5", "rv20", "median20_range", "atr20", "range20_ratio"
]
GAMMA_COLS = ["near_gamma_share_0_5", "front_near_gamma_share", "weighted_abs_distance"]
TARGETS = ["next_rth_range", "next_max_excursion", "next_abs_oc"]
PRIMARY = ["next_rth_range", "next_max_excursion"]


def safe_spearman(x, y):
    d = pd.concat([pd.Series(x), pd.Series(y)], axis=1).replace([np.inf, -np.inf], np.nan).dropna()
    if len(d) < 5 or d.iloc[:, 0].nunique() < 2 or d.iloc[:, 1].nunique() < 2:
        return np.nan, np.nan, len(d)
    r, p = stats.spearmanr(d.iloc[:, 0], d.iloc[:, 1])
    return float(r), float(p), len(d)


def normal_pdf(z):
    return np.exp(-0.5 * z * z) / math.sqrt(2.0 * math.pi)


def load_prices(symbol: str) -> pd.DataFrame:
    p = yf.download(symbol, start="2019-11-01", end="2023-01-10", auto_adjust=False,
                    progress=False, actions=False, threads=False)
    if p.empty:
        raise RuntimeError(f"{symbol} price download returned no rows")
    if isinstance(p.columns, pd.MultiIndex):
        p.columns = [c[0] for c in p.columns]
    p = p[["Open", "High", "Low", "Close"]].copy().sort_index()
    p.index = pd.to_datetime(p.index).tz_localize(None).normalize()
    p["prev_close"] = p["Close"].shift(1)
    p["cc"] = p["Close"].pct_change()
    p["day_abs_oc"] = (p["Close"] / p["Open"] - 1).abs()
    p["day_range"] = (p["High"] - p["Low"]) / p["Open"]
    p["rv5"] = p["cc"].rolling(5).std(ddof=1)
    p["rv20"] = p["cc"].rolling(20).std(ddof=1)
    p["median20_range"] = p["day_range"].rolling(20).median()
    h_l = p["High"] - p["Low"]
    h_pc = (p["High"] - p["prev_close"]).abs()
    l_pc = (p["Low"] - p["prev_close"]).abs()
    p["norm_true_range"] = pd.concat([h_l, h_pc, l_pc], axis=1).max(axis=1) / p["prev_close"]
    p["atr20"] = p["norm_true_range"].rolling(20).mean()
    p["range20_ratio"] = p["day_range"] / p["median20_range"]
    p["next_date"] = pd.Series(p.index, index=p.index).shift(-1).values
    p["next_open"] = p["Open"].shift(-1)
    p["next_high"] = p["High"].shift(-1)
    p["next_low"] = p["Low"].shift(-1)
    p["next_close"] = p["Close"].shift(-1)
    return p


def actual_monthly_opex(d: pd.Timestamp, trading_days: pd.DatetimeIndex) -> pd.Timestamp:
    first = pd.Timestamp(year=d.year, month=d.month, day=1)
    fridays = pd.date_range(first, first + pd.offsets.MonthEnd(0), freq="W-FRI")
    expiry = fridays[2]
    if expiry in trading_days:
        return expiry
    prior = trading_days[(trading_days < expiry) & (trading_days.month == expiry.month)]
    return prior[-1] if len(prior) else expiry


def load_options_file(symbol: str, year: int) -> pd.DataFrame:
    fp = DATA_DIR / f"{symbol.lower()}_{year}.parquet"
    if not fp.exists():
        raise RuntimeError(f"Missing options parquet: {fp}")
    cols = ["date", "expiration", "strike", "open_interest", "implied_volatility", "type"]
    x = pd.read_parquet(fp, columns=cols)
    x["date"] = pd.to_datetime(x["date"], errors="coerce").dt.tz_localize(None).dt.normalize()
    x["expiration"] = pd.to_datetime(x["expiration"], errors="coerce").dt.tz_localize(None).dt.normalize()
    for c in ["strike", "open_interest", "implied_volatility"]:
        x[c] = pd.to_numeric(x[c], errors="coerce")
    x = x[x["date"].dt.year == year].copy()
    x["dte"] = (x["expiration"] - x["date"]).dt.days
    x = x[(x["dte"] >= MIN_DTE) & (x["dte"] <= MAX_DTE)]
    return x


def gamma_features(day_chain: pd.DataFrame, spot: float) -> dict:
    x = day_chain.copy()
    x = x[x["strike"].between(spot * (1 - MONEYNESS), spot * (1 + MONEYNESS))]
    x = x[(x["open_interest"].notna()) & (x["open_interest"] >= 0)]
    x = x[(x["implied_volatility"].notna()) &
          (x["implied_volatility"] >= IV_MIN) &
          (x["implied_volatility"] <= IV_MAX)]
    x = x[(x["strike"] > 0) & np.isfinite(x["strike"])]
    if x.empty:
        return {"eligible_contracts": 0}

    S = float(spot)
    K = x["strike"].to_numpy(float)
    sigma = x["implied_volatility"].to_numpy(float)
    T = x["dte"].to_numpy(float) / 365.0
    sqrtT = np.sqrt(T)
    d1 = (np.log(S / K) + 0.5 * sigma * sigma * T) / (sigma * sqrtT)
    gamma = normal_pdf(d1) / (S * sigma * sqrtT)
    oi = x["open_interest"].to_numpy(float)
    w = gamma * oi

    x["gamma_weight"] = w
    x["abs_dist"] = np.abs(x["strike"] / S - 1.0)
    x = x[np.isfinite(x["gamma_weight"]) & (x["gamma_weight"] >= 0)]
    total = float(x["gamma_weight"].sum())
    if total <= 0:
        return {"eligible_contracts": int(len(x)), "total_gamma_weight": 0.0}

    near = float(x.loc[x["abs_dist"] <= NEAR_05, "gamma_weight"].sum() / total)
    front_near = float(x.loc[(x["dte"] <= 7) & (x["abs_dist"] <= NEAR_05), "gamma_weight"].sum() / total)
    wad = float((x["gamma_weight"] * x["abs_dist"]).sum() / total)
    return {
        "eligible_contracts": int(len(x)),
        "total_gamma_weight": total,
        "near_gamma_share_0_5": near,
        "front_near_gamma_share": front_near,
        "weighted_abs_distance": wad,
    }


def build_panel():
    prices = {s: load_prices(s) for s in SYMBOLS}
    rows = []
    exclusions = {s: {"no_price": 0, "no_next_price": 0, "no_gamma": 0, "no_history": 0} for s in SYMBOLS}

    for symbol in SYMBOLS:
        p = prices[symbol]
        for year in YEARS:
            opt = load_options_file(symbol, year)
            for d, chain in opt.groupby("date", sort=True):
                d = pd.Timestamp(d).normalize()
                if d not in p.index:
                    exclusions[symbol]["no_price"] += 1
                    continue
                q = p.loc[d]
                if pd.isna(q["next_open"]) or pd.isna(q["next_close"]):
                    exclusions[symbol]["no_next_price"] += 1
                    continue
                if any(pd.isna(q[c]) or not np.isfinite(q[c]) for c in CONTROL_COLS):
                    exclusions[symbol]["no_history"] += 1
                    continue
                gf = gamma_features(chain, float(q["Close"]))
                if gf.get("eligible_contracts", 0) == 0 or gf.get("total_gamma_weight", 0) <= 0:
                    exclusions[symbol]["no_gamma"] += 1
                    continue

                o, h, l, c = map(float, [q["next_open"], q["next_high"], q["next_low"], q["next_close"]])
                next_range = (h - l) / o
                up_exc = max(h / o - 1, 0.0)
                down_exc = max(o / l - 1, 0.0)
                next_max_exc = max(up_exc, down_exc)
                next_abs_oc = abs(c / o - 1)
                opx = actual_monthly_opex(d, p.index)
                monthly_week = bool((d >= opx - pd.Timedelta(days=4)) and (d <= opx))

                rows.append({
                    "symbol": symbol,
                    "year": year,
                    "date": d,
                    "next_date": pd.Timestamp(q["next_date"]).normalize(),
                    **{c: float(q[c]) for c in CONTROL_COLS},
                    "next_rth_range": next_range,
                    "next_max_excursion": next_max_exc,
                    "next_abs_oc": next_abs_oc,
                    "monthly_opex_week": monthly_week,
                    **gf,
                })
            del opt

    panel = pd.DataFrame(rows).replace([np.inf, -np.inf], np.nan).dropna()
    panel = panel.sort_values(["date", "symbol"]).reset_index(drop=True)
    return panel, exclusions


def log_controls(df: pd.DataFrame) -> pd.DataFrame:
    z = pd.DataFrame(index=df.index)
    for c in CONTROL_COLS:
        z[f"log_{c}"] = np.log(df[c].astype(float).clip(lower=0) + EPS)
    return z


def design_matrix(df: pd.DataFrame, include_gamma: bool, include_symbol_fe: bool = True,
                  include_year_fe: bool = True) -> pd.DataFrame:
    parts = [log_controls(df)]
    if include_gamma:
        parts.append(df[["near_gamma_share_0_5"]].astype(float))
    if include_symbol_fe:
        parts.append(pd.get_dummies(df["symbol"], prefix="sym", drop_first=True, dtype=float))
    if include_year_fe:
        parts.append(pd.get_dummies(df["year"].astype(str), prefix="yr", drop_first=True, dtype=float))
    X = pd.concat(parts, axis=1)
    return sm.add_constant(X, has_constant="add")


def controlled_fit(df: pd.DataFrame, target: str, include_gamma: bool,
                   include_symbol_fe: bool = True, include_year_fe: bool = True):
    y = np.log(df[target].astype(float).clip(lower=0) + EPS)
    X = design_matrix(df, include_gamma, include_symbol_fe, include_year_fe)
    model = sm.OLS(y, X).fit(cov_type="HC3")
    return model


def controlled_table(panel: pd.DataFrame) -> pd.DataFrame:
    rows = []
    samples = {"POOLED": panel, "NON_OPEX": panel[~panel["monthly_opex_week"]]}
    for s in SYMBOLS:
        samples[f"SYMBOL_{s}"] = panel[panel["symbol"] == s]
    for y in YEARS:
        samples[f"YEAR_{y}"] = panel[panel["year"] == y]

    for sample, df in samples.items():
        if len(df) < 50:
            continue
        include_symbol = not sample.startswith("SYMBOL_")
        include_year = not sample.startswith("YEAR_")
        for target in PRIMARY:
            m = controlled_fit(df, target, True, include_symbol, include_year)
            coef = float(m.params.get("near_gamma_share_0_5", np.nan))
            p = float(m.pvalues.get("near_gamma_share_0_5", np.nan))
            rows.append({"sample": sample, "target": target, "n": int(m.nobs),
                         "gamma_coef": coef, "hc3_p_value": p, "r2": float(m.rsquared)})
    return pd.DataFrame(rows)


def residual_table(panel: pd.DataFrame) -> tuple[pd.DataFrame, pd.DataFrame]:
    residual_rows = []
    summary = []
    for sample, df in [("POOLED", panel), ("NON_OPEX", panel[~panel["monthly_opex_week"]])]:
        for target in PRIMARY:
            m = controlled_fit(df, target, False, True, True)
            resid = np.asarray(m.resid)
            rho, p, n = safe_spearman(df["near_gamma_share_0_5"].reset_index(drop=True), pd.Series(resid))
            summary.append({"sample": sample, "target": target, "n": n,
                            "residual_rho": rho, "residual_p_value": p})
            for i, (_, row) in enumerate(df.iterrows()):
                residual_rows.append({"sample": sample, "date": row["date"], "symbol": row["symbol"],
                                      "year": row["year"], "target": target,
                                      "near_gamma_share_0_5": row["near_gamma_share_0_5"],
                                      "vol_residual": float(resid[i])})
    return pd.DataFrame(residual_rows), pd.DataFrame(summary)


def wf_matrix(df: pd.DataFrame, cols: list[str], mu=None, sd=None):
    Xc = df[cols].to_numpy(float)
    if mu is None:
        mu = Xc.mean(axis=0)
        sd = Xc.std(axis=0)
        sd = np.where(sd == 0, 1, sd)
    Xs = (Xc - mu) / sd
    sym = pd.get_dummies(df["symbol"], dtype=float).reindex(columns=SYMBOLS, fill_value=0.0)
    # SPY is the baseline to avoid a redundant full dummy set with intercept.
    S = sym[["QQQ", "IWM"]].to_numpy(float)
    X = np.column_stack([np.ones(len(df)), Xs, S])
    return X, mu, sd


def walk_forward(panel: pd.DataFrame):
    base_cols = CONTROL_COLS
    ext_cols = CONTROL_COLS + GAMMA_COLS
    preds = []
    unique_dates = sorted(panel["date"].dropna().unique())

    for current_date in unique_dates:
        train = panel[panel["date"] < current_date]
        test = panel[panel["date"] == current_date]
        if len(train) < MIN_TRAIN_ROWS or test.empty:
            continue
        for target in TARGETS:
            for model_name, cols in [("baseline", base_cols), ("extended", ext_cols)]:
                tr = train[cols + [target, "symbol"]].dropna()
                te = test[cols + [target, "symbol"]].dropna()
                if len(tr) < MIN_TRAIN_ROWS or te.empty:
                    continue
                Xtr, mu, sd = wf_matrix(tr, cols)
                ytr = tr[target].to_numpy(float)
                beta = np.linalg.lstsq(Xtr, ytr, rcond=None)[0]
                Xte, _, _ = wf_matrix(te, cols, mu, sd)
                pred = Xte.dot(beta)
                for j, (_, row) in enumerate(te.iterrows()):
                    actual = float(row[target])
                    preds.append({"date": current_date, "symbol": row["symbol"], "target": target,
                                  "model": model_name, "pred": float(pred[j]), "actual": actual,
                                  "abs_error": abs(float(pred[j]) - actual)})

    p = pd.DataFrame(preds)
    rows = []
    for target in TARGETS:
        z = p[p["target"] == target]
        b = z[z["model"] == "baseline"]
        e = z[z["model"] == "extended"]
        if b.empty or e.empty:
            continue
        mb, me = float(b["abs_error"].mean()), float(e["abs_error"].mean())
        rows.append({"target": target, "n_test": len(b), "baseline_mae": mb,
                     "extended_mae": me,
                     "mae_improvement_pct": 100 * (mb - me) / mb if mb > 0 else np.nan})
    return p, pd.DataFrame(rows)


def fmt_pct(v):
    return "—" if pd.isna(v) else f"{100*v:.3f}%"


def main():
    panel, exclusions = build_panel()
    if len(panel) < 1500:
        raise RuntimeError(f"Too few observations for frozen holdout: {len(panel)}")

    ctl = controlled_table(panel)
    residual_rows, residual_summary = residual_table(panel)
    preds, wf = walk_forward(panel)

    panel.to_csv(OUT / "near_spot_gamma_incremental_value_v1_session_panel.csv", index=False)
    ctl.to_csv(OUT / "near_spot_gamma_incremental_value_v1_controlled_coefficients.csv", index=False)
    residual_rows.to_csv(OUT / "near_spot_gamma_incremental_value_v1_residuals.csv", index=False)
    residual_summary.to_csv(OUT / "near_spot_gamma_incremental_value_v1_residual_summary.csv", index=False)
    preds.to_csv(OUT / "near_spot_gamma_incremental_value_v1_walkforward_predictions.csv", index=False)
    wf.to_csv(OUT / "near_spot_gamma_incremental_value_v1_walkforward_summary.csv", index=False)

    def crow(sample, target):
        z = ctl[(ctl["sample"] == sample) & (ctl["target"] == target)]
        return None if z.empty else z.iloc[0]

    def rrow(sample, target):
        z = residual_summary[(residual_summary["sample"] == sample) &
                             (residual_summary["target"] == target)]
        return None if z.empty else z.iloc[0]

    pooled_range = crow("POOLED", "next_rth_range")
    gate1 = bool(pooled_range is not None and pooled_range.gamma_coef < 0 and pooled_range.hc3_p_value < 0.05)

    inst_neg = []
    for s in SYMBOLS:
        r = crow(f"SYMBOL_{s}", "next_rth_range")
        inst_neg.append(r is not None and r.gamma_coef < 0)
    year_neg = []
    for y in YEARS:
        r = crow(f"YEAR_{y}", "next_rth_range")
        year_neg.append(r is not None and r.gamma_coef < 0)
    gate2 = all(inst_neg) and sum(year_neg) >= 2

    pooled_exc = crow("POOLED", "next_max_excursion")
    rr = rrow("POOLED", "next_rth_range")
    re = rrow("POOLED", "next_max_excursion")
    gate3 = bool(
        pooled_exc is not None and pooled_exc.gamma_coef < 0 and
        rr is not None and rr.residual_rho < 0 and rr.residual_p_value < 0.05 and
        re is not None and re.residual_rho < 0 and re.residual_p_value < 0.05
    )

    non_r = crow("NON_OPEX", "next_rth_range")
    non_e = crow("NON_OPEX", "next_max_excursion")
    non_rr = rrow("NON_OPEX", "next_rth_range")
    non_re = rrow("NON_OPEX", "next_max_excursion")
    gate4 = bool(
        non_r is not None and non_e is not None and non_r.gamma_coef < 0 and non_e.gamma_coef < 0 and
        non_rr is not None and non_re is not None and non_rr.residual_rho < 0 and non_re.residual_rho < 0
    )

    wfmap = {r.target: r for _, r in wf.iterrows()}
    imp_range = float(wfmap["next_rth_range"].mae_improvement_pct) if "next_rth_range" in wfmap else -999
    imp_exc = float(wfmap["next_max_excursion"].mae_improvement_pct) if "next_max_excursion" in wfmap else -999
    gate5 = (imp_range >= 2.0 and imp_exc >= -1.0) or (imp_exc >= 2.0 and imp_range >= -1.0)

    if all([gate1, gate2, gate3, gate4, gate5]):
        verdict = "SUPPORTED ADDITIVE VALUE"
    elif all([gate1, gate2, gate3, gate4]):
        verdict = "CONDITIONAL ASSOCIATION / RESEARCH-ONLY"
    else:
        verdict = "MOSTLY VOLATILITY PROXY / NOT ADDITIVE"

    lines = []
    lines.append("# Near-Spot Unsigned Gamma Incremental Value v1.0 — Frozen Holdout Results\n")
    lines.append(f"Generated: {datetime.now(timezone.utc).isoformat(timespec='seconds')}\n")
    lines.append("## Coverage")
    lines.append(f"- Total matched Day-T observations: **{len(panel)}**")
    lines.append(f"- Instruments: **{', '.join(SYMBOLS)}**")
    lines.append(f"- Untouched holdout years: **{', '.join(map(str, YEARS))}**")
    lines.append(f"- Median eligible contracts/session: **{int(panel.eligible_contracts.median())}**")
    lines.append(f"- Monthly-OPEX-week observations: **{int(panel.monthly_opex_week.sum())}**")
    lines.append(f"- Exclusions: {exclusions}\n")

    lines.append("## Controlled HC3 gamma coefficients")
    lines.append(ctl.to_markdown(index=False, floatfmt=".5f"))

    lines.append("\n## Volatility-only residual associations")
    lines.append(residual_summary.to_markdown(index=False, floatfmt=".5f"))

    lines.append("\n## Walk-forward incremental prediction")
    w = wf.copy()
    for c in ["baseline_mae", "extended_mae"]:
        w[c] = w[c].map(fmt_pct)
    lines.append(w.to_markdown(index=False, floatfmt=".2f"))

    lines.append("\n## Frozen promotion gates")
    lines.append(f"- Controlled pooled range coefficient negative, HC3 p<0.05: **{'PASS' if gate1 else 'FAIL'}**")
    lines.append(f"- Controlled range sign stable across all 3 instruments and >=2/3 years: **{'PASS' if gate2 else 'FAIL'}**")
    lines.append(f"- Controlled max-excursion + both primary residual tests negative/significant: **{'PASS' if gate3 else 'FAIL'}**")
    lines.append(f"- Non-OPEX controlled/residual direction preserved: **{'PASS' if gate4 else 'FAIL'}**")
    lines.append(f"- Walk-forward >=2% primary MAE improvement without >1% degradation of other primary: **{'PASS' if gate5 else 'FAIL'}**")
    lines.append(f"- Overall frozen verdict: **{verdict}**")
    lines.append("\nNo result has directional authority or permission to alter STRENGTH, RUNWAY, R:R, action state, option selection, or overnight carry.")

    report = "\n".join(lines)
    (OUT / "near_spot_gamma_incremental_value_v1_results.md").write_text(report)
    print(report)


if __name__ == "__main__":
    main()
