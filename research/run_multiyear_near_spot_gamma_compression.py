#!/usr/bin/env python3
"""Frozen Investing OS experiment: multi-year near-spot unsigned gamma compression v1.0.

Rules are frozen in research/multiyear_near_spot_gamma_compression_v1.md.
Do not change thresholds or promotion gates after observing results.
"""
from __future__ import annotations

import math
import os
from pathlib import Path
from datetime import datetime, timezone

import numpy as np
import pandas as pd
from scipy import stats
import yfinance as yf

DATA_DIR = Path(os.environ.get("OPTIONS_DATA_DIR", "/tmp/options_gamma_multi"))
OUT = Path("research/results")
OUT.mkdir(parents=True, exist_ok=True)

SYMBOLS = ["SPY", "QQQ", "IWM"]
YEARS = [2023, 2024, 2025]
MIN_DTE = 1
MAX_DTE = 30
MONEYNESS = 0.05
IV_MIN = 0.05
IV_MAX = 2.00
NEAR_05 = 0.005
MIN_TRAIN_ROWS = 500


def safe_spearman(x, y):
    d = pd.concat([pd.Series(x), pd.Series(y)], axis=1).replace([np.inf, -np.inf], np.nan).dropna()
    if len(d) < 5 or d.iloc[:, 0].nunique() < 2 or d.iloc[:, 1].nunique() < 2:
        return np.nan, np.nan, len(d)
    r, p = stats.spearmanr(d.iloc[:, 0], d.iloc[:, 1])
    return float(r), float(p), len(d)


def normal_pdf(z):
    return np.exp(-0.5 * z * z) / math.sqrt(2.0 * math.pi)


def load_prices(symbol: str) -> pd.DataFrame:
    p = yf.download(symbol, start="2022-11-01", end="2026-01-10", auto_adjust=False,
                    progress=False, actions=False, threads=False)
    if p.empty:
        raise RuntimeError(f"{symbol} price download returned no rows")
    if isinstance(p.columns, pd.MultiIndex):
        p.columns = [c[0] for c in p.columns]
    p = p[["Open", "High", "Low", "Close"]].copy().sort_index()
    p.index = pd.to_datetime(p.index).tz_localize(None).normalize()
    p["cc"] = p["Close"].pct_change()
    p["day_abs_oc"] = (p["Close"] / p["Open"] - 1).abs()
    p["day_range"] = (p["High"] - p["Low"]) / p["Open"]
    p["rv5"] = p["cc"].rolling(5).std(ddof=1)
    p["median20_range"] = p["day_range"].rolling(20).median()
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
                if pd.isna(q["rv5"]) or pd.isna(q["median20_range"]):
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
                next_range_vs20 = next_range / float(q["median20_range"]) if q["median20_range"] > 0 else np.nan
                opx = actual_monthly_opex(d, p.index)
                monthly_week = bool((d >= opx - pd.Timedelta(days=4)) and (d <= opx))

                rows.append({
                    "symbol": symbol,
                    "year": year,
                    "date": d,
                    "next_date": pd.Timestamp(q["next_date"]).normalize(),
                    "day_abs_oc": float(q["day_abs_oc"]),
                    "day_range": float(q["day_range"]),
                    "rv5": float(q["rv5"]),
                    "median20_range": float(q["median20_range"]),
                    "next_rth_range": next_range,
                    "next_max_excursion": next_max_exc,
                    "next_abs_oc": next_abs_oc,
                    "next_range_vs_20d": next_range_vs20,
                    "monthly_opex_week": monthly_week,
                    **gf,
                })
            del opt

    panel = pd.DataFrame(rows).sort_values(["date", "symbol"]).reset_index(drop=True)
    return panel, exclusions


def correlation_table(panel):
    expected = {
        "near_gamma_share_0_5": -1,
        "front_near_gamma_share": -1,
        "weighted_abs_distance": 1,
    }
    outcomes = ["next_rth_range", "next_max_excursion", "next_abs_oc", "next_range_vs_20d"]
    samples = {"POOLED": panel, "NON_OPEX": panel[~panel["monthly_opex_week"]]}
    for s in SYMBOLS:
        samples[f"SYMBOL_{s}"] = panel[panel["symbol"] == s]
    for y in YEARS:
        samples[f"YEAR_{y}"] = panel[panel["year"] == y]

    rows = []
    for sample, df in samples.items():
        for f, es in expected.items():
            for o in outcomes:
                rho, p, n = safe_spearman(df[f], df[o])
                rows.append({"sample": sample, "feature": f, "outcome": o,
                             "expected_sign": es, "n": n, "rho": rho, "p_value": p})
    return pd.DataFrame(rows)


def median_split(panel):
    x = panel.copy()
    med = x.groupby(["symbol", "year"])["near_gamma_share_0_5"].transform("median")
    x["gamma_bucket"] = np.where(x["near_gamma_share_0_5"] > med, "HIGH", "LOW")
    pooled = x.groupby("gamma_bucket").agg(
        n=("date", "size"),
        mean_near_share=("near_gamma_share_0_5", "mean"),
        mean_next_range=("next_rth_range", "mean"),
        median_next_range=("next_rth_range", "median"),
        mean_max_excursion=("next_max_excursion", "mean"),
        mean_abs_oc=("next_abs_oc", "mean"),
        mean_range_vs20=("next_range_vs_20d", "mean"),
    ).reset_index()
    by_group = x.groupby(["symbol", "year", "gamma_bucket"]).agg(
        n=("date", "size"),
        mean_next_range=("next_rth_range", "mean"),
        mean_max_excursion=("next_max_excursion", "mean"),
        mean_abs_oc=("next_abs_oc", "mean"),
    ).reset_index()
    return pooled, by_group


def walk_forward(panel):
    base_cols = ["day_abs_oc", "day_range", "rv5", "median20_range"]
    ext_cols = base_cols + ["near_gamma_share_0_5", "front_near_gamma_share", "weighted_abs_distance"]
    targets = ["next_rth_range", "next_max_excursion", "next_abs_oc"]
    preds = []
    unique_dates = sorted(panel["date"].dropna().unique())

    for current_date in unique_dates:
        train = panel[panel["date"] < current_date]
        test = panel[panel["date"] == current_date]
        if len(train) < MIN_TRAIN_ROWS or test.empty:
            continue
        for target in targets:
            for name, cols in [("baseline", base_cols), ("extended", ext_cols)]:
                tr = train[cols + [target]].replace([np.inf, -np.inf], np.nan).dropna()
                te = test[cols + [target]].replace([np.inf, -np.inf], np.nan).dropna()
                if len(tr) < MIN_TRAIN_ROWS or te.empty:
                    continue
                X = tr[cols].to_numpy(float)
                y = tr[target].to_numpy(float)
                mu = X.mean(axis=0)
                sd = X.std(axis=0)
                sd = np.where(sd == 0, 1, sd)
                Xs = (X - mu) / sd
                Xa = np.column_stack([np.ones(len(Xs)), Xs])
                beta = np.linalg.lstsq(Xa, y, rcond=None)[0]
                xt = (te[cols].to_numpy(float) - mu) / sd
                Xta = np.column_stack([np.ones(len(xt)), xt])
                pred = Xta.dot(beta)
                for j, (_, row) in enumerate(te.iterrows()):
                    actual = float(row[target])
                    preds.append({"date": current_date, "symbol": test.loc[row.name, "symbol"],
                                  "target": target, "model": name, "pred": float(pred[j]),
                                  "actual": actual, "abs_error": abs(float(pred[j]) - actual)})
    p = pd.DataFrame(preds)
    rows = []
    for target in targets:
        z = p[p["target"] == target]
        b = z[z["model"] == "baseline"]
        e = z[z["model"] == "extended"]
        if b.empty or e.empty:
            continue
        mb, me = float(b["abs_error"].mean()), float(e["abs_error"].mean())
        rows.append({"target": target, "n_test": len(b), "baseline_mae": mb, "extended_mae": me,
                     "mae_improvement_pct": 100 * (mb - me) / mb if mb > 0 else np.nan})
    return p, pd.DataFrame(rows)


def fmt_pct(v):
    return "—" if pd.isna(v) else f"{100*v:.3f}%"


def main():
    panel, exclusions = build_panel()
    if len(panel) < 1500:
        raise RuntimeError(f"Too few observations for frozen multi-year test: {len(panel)}")
    corr = correlation_table(panel)
    split, split_group = median_split(panel)
    preds, wf = walk_forward(panel)

    panel.to_csv(OUT / "multiyear_near_spot_gamma_compression_v1_session_panel.csv", index=False)
    corr.to_csv(OUT / "multiyear_near_spot_gamma_compression_v1_correlations.csv", index=False)
    split_group.to_csv(OUT / "multiyear_near_spot_gamma_compression_v1_group_splits.csv", index=False)
    preds.to_csv(OUT / "multiyear_near_spot_gamma_compression_v1_walkforward_predictions.csv", index=False)
    wf.to_csv(OUT / "multiyear_near_spot_gamma_compression_v1_walkforward_summary.csv", index=False)

    def rho(sample, outcome):
        z = corr[(corr["sample"] == sample) &
                 (corr["feature"] == "near_gamma_share_0_5") &
                 (corr["outcome"] == outcome)]
        return None if z.empty else z.iloc[0]

    pooled_range = rho("POOLED", "next_rth_range")
    gate1 = bool(pooled_range is not None and float(pooled_range["rho"]) < 0 and float(pooled_range["p_value"]) < 0.05)

    inst_signs = []
    for s in SYMBOLS:
        r = rho(f"SYMBOL_{s}", "next_rth_range")
        inst_signs.append(r is not None and float(r["rho"]) < 0)
    year_signs = []
    for y in YEARS:
        r = rho(f"YEAR_{y}", "next_rth_range")
        year_signs.append(r is not None and float(r["rho"]) < 0)
    gate2 = all(inst_signs) and sum(year_signs) >= 2

    pooled_exc = rho("POOLED", "next_max_excursion")
    exc_inst = []
    for s in SYMBOLS:
        r = rho(f"SYMBOL_{s}", "next_max_excursion")
        exc_inst.append(r is not None and float(r["rho"]) < 0)
    gate3 = bool(pooled_exc is not None and float(pooled_exc["rho"]) < 0 and sum(exc_inst) >= 2)

    non_r = rho("NON_OPEX", "next_rth_range")
    non_e = rho("NON_OPEX", "next_max_excursion")
    gate4 = bool(non_r is not None and non_e is not None and float(non_r["rho"]) < 0 and float(non_e["rho"]) < 0)

    wfmap = {r.target: r for _, r in wf.iterrows()}
    imp_range = float(wfmap["next_rth_range"].mae_improvement_pct) if "next_rth_range" in wfmap else -999
    imp_exc = float(wfmap["next_max_excursion"].mae_improvement_pct) if "next_max_excursion" in wfmap else -999
    gate5 = (imp_range >= 2.0 and imp_exc >= -1.0) or (imp_exc >= 2.0 and imp_range >= -1.0)

    if all([gate1, gate2, gate3, gate4, gate5]):
        verdict = "SUPPORTED"
    elif all([gate1, gate2, gate3, gate4]):
        verdict = "REPLICATED ASSOCIATION / RESEARCH-ONLY"
    else:
        verdict = "FAILED GENERAL COMPRESSION HYPOTHESIS"

    lines = []
    lines.append("# Multi-Year Near-Spot Unsigned Gamma Compression v1.0 — Frozen Results\n")
    lines.append(f"Generated: {datetime.now(timezone.utc).isoformat(timespec='seconds')}\n")
    lines.append("## Coverage")
    lines.append(f"- Total matched Day-T observations: **{len(panel)}**")
    lines.append(f"- Instruments: **{', '.join(SYMBOLS)}**")
    lines.append(f"- Years: **{', '.join(map(str, YEARS))}**")
    lines.append(f"- Median eligible contracts/session: **{int(panel.eligible_contracts.median())}**")
    lines.append(f"- Monthly-OPEX-week observations: **{int(panel.monthly_opex_week.sum())}**")
    lines.append(f"- Exclusions: {exclusions}\n")

    lines.append("## Correlations")
    lines.append(corr.to_markdown(index=False, floatfmt=".4f"))

    lines.append("\n## Instrument-year median split — pooled descriptive summary")
    s = split.copy()
    for c in ["mean_next_range", "median_next_range", "mean_max_excursion", "mean_abs_oc"]:
        s[c] = s[c].map(fmt_pct)
    lines.append(s.to_markdown(index=False, floatfmt=".4f"))

    lines.append("\n## Walk-forward incremental test")
    w = wf.copy()
    for c in ["baseline_mae", "extended_mae"]:
        w[c] = w[c].map(fmt_pct)
    lines.append(w.to_markdown(index=False, floatfmt=".2f"))

    lines.append("\n## Frozen promotion gates")
    lines.append(f"- Pooled negative range relationship p<0.05: **{'PASS' if gate1 else 'FAIL'}**")
    lines.append(f"- Negative range relationship across all 3 instruments and >=2/3 years: **{'PASS' if gate2 else 'FAIL'}**")
    lines.append(f"- Negative max-excursion relationship pooled and >=2/3 instruments: **{'PASS' if gate3 else 'FAIL'}**")
    lines.append(f"- Non-OPEX persistence for both primary outcomes: **{'PASS' if gate4 else 'FAIL'}**")
    lines.append(f"- Walk-forward >=2% primary MAE improvement without >1% degradation of the other: **{'PASS' if gate5 else 'FAIL'}**")
    lines.append(f"- Overall frozen verdict: **{verdict}**")
    lines.append("\nNo result has directional authority or permission to alter STRENGTH, RUNWAY, R:R, action state, option selection, or overnight carry.")

    report = "\n".join(lines)
    (OUT / "multiyear_near_spot_gamma_compression_v1_results.md").write_text(report)
    print(report)


if __name__ == "__main__":
    main()
