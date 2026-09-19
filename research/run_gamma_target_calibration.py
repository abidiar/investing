#!/usr/bin/env python3
"""Frozen Investing OS experiment: gamma target calibration v1.0.

Rules are frozen in research/gamma_target_calibration_v1.md.
Do not change sample, target ladder, features, model, threshold, utility metric, or gates after results.
"""
from __future__ import annotations

import math
import os
from pathlib import Path
from datetime import datetime, timezone

import numpy as np
import pandas as pd
import yfinance as yf
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import brier_score_loss

DATA_DIR = Path(os.environ.get("OPTIONS_DATA_DIR", "/tmp/options_gamma_target"))
OUT = Path("research/results")
OUT.mkdir(parents=True, exist_ok=True)

SYMBOLS = ["SPY", "QQQ", "IWM"]
TRAIN_YEARS = [2011]
TEST_YEARS = [2012, 2013]
ALL_YEARS = TRAIN_YEARS + TEST_YEARS
MIN_DTE = 1
MAX_DTE = 30
MONEYNESS = 0.05
IV_MIN = 0.05
IV_MAX = 2.00
NEAR_05 = 0.005
GAP_MIN = 0.0025
TARGET_MULTS = [0.50, 0.75, 1.00]
DECISION_P = 0.60
BOOT_N = 10_000
BOOT_SEED = 0

BASE_COLS = [
    "abs_gap", "gap_atr20", "gap_up", "day_abs_oc", "day_range",
    "rv5", "rv20", "median20_range", "atr20", "range20_ratio",
]
GAMMA_COLS = ["near_gamma_share_0_5", "front_near_gamma_share", "weighted_abs_distance"]
TARGET_HIT_COLS = {0.50: "hit_t1", 0.75: "hit_t2", 1.00: "hit_t3"}


def normal_pdf(z):
    return np.exp(-0.5 * z * z) / math.sqrt(2.0 * math.pi)


def load_prices(symbol: str) -> pd.DataFrame:
    p = yf.download(symbol, start="2010-10-01", end="2014-01-10", auto_adjust=False,
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
    exclusions = {s: {"no_price": 0, "no_next_price": 0, "no_history": 0, "no_gamma": 0, "small_gap": 0} for s in SYMBOLS}

    for symbol in SYMBOLS:
        p = prices[symbol]
        for year in ALL_YEARS:
            opt = load_options_file(symbol, year)
            for d, chain in opt.groupby("date", sort=True):
                d = pd.Timestamp(d).normalize()
                if d not in p.index:
                    exclusions[symbol]["no_price"] += 1
                    continue
                q = p.loc[d]
                if pd.isna(q["next_open"]) or pd.isna(q["next_high"]) or pd.isna(q["next_low"]):
                    exclusions[symbol]["no_next_price"] += 1
                    continue
                needed = ["day_abs_oc", "day_range", "rv5", "rv20", "median20_range", "atr20", "range20_ratio"]
                if any(pd.isna(q[c]) or not np.isfinite(q[c]) for c in needed):
                    exclusions[symbol]["no_history"] += 1
                    continue
                if any(float(q[c]) <= 0 for c in ["day_range", "rv5", "rv20", "median20_range", "atr20", "range20_ratio"]):
                    exclusions[symbol]["no_history"] += 1
                    continue

                spot = float(q["Close"])
                gf = gamma_features(chain, spot)
                if gf.get("eligible_contracts", 0) == 0 or gf.get("total_gamma_weight", 0) <= 0:
                    exclusions[symbol]["no_gamma"] += 1
                    continue

                o = float(q["next_open"])
                h = float(q["next_high"])
                l = float(q["next_low"])
                gap = o / spot - 1.0
                if not np.isfinite(gap) or abs(gap) < GAP_MIN or gap == 0:
                    exclusions[symbol]["small_gap"] += 1
                    continue

                same_mfe = max(h / o - 1.0, 0.0) if gap > 0 else max(o / l - 1.0, 0.0)
                med = float(q["median20_range"])
                row = {
                    "symbol": symbol,
                    "year": int(d.year),
                    "date": d,
                    "next_date": pd.Timestamp(q["next_date"]).normalize(),
                    "gap": gap,
                    "abs_gap": abs(gap),
                    "gap_atr20": abs(gap) / float(q["atr20"]),
                    "gap_up": 1.0 if gap > 0 else 0.0,
                    "day_abs_oc": float(q["day_abs_oc"]),
                    "day_range": float(q["day_range"]),
                    "rv5": float(q["rv5"]),
                    "rv20": float(q["rv20"]),
                    "median20_range": med,
                    "atr20": float(q["atr20"]),
                    "range20_ratio": float(q["range20_ratio"]),
                    "same_dir_mfe": same_mfe,
                    "t1_distance": 0.50 * med,
                    "t2_distance": 0.75 * med,
                    "t3_distance": 1.00 * med,
                    "hit_t1": float(same_mfe >= 0.50 * med),
                    "hit_t2": float(same_mfe >= 0.75 * med),
                    "hit_t3": float(same_mfe >= 1.00 * med),
                    **gf,
                }
                rows.append(row)
            del opt

    panel = pd.DataFrame(rows).replace([np.inf, -np.inf], np.nan).dropna()
    panel = panel.sort_values(["date", "symbol"]).reset_index(drop=True)
    return panel, exclusions


def make_matrix(df: pd.DataFrame, cols: list[str], means=None, sds=None):
    X = df[cols].to_numpy(float)
    if means is None:
        means = X.mean(axis=0)
        sds = X.std(axis=0)
        sds = np.where(sds == 0, 1.0, sds)
    Xs = (X - means) / sds
    dummies = pd.get_dummies(df["symbol"], dtype=float).reindex(columns=SYMBOLS, fill_value=0.0)
    Xf = np.column_stack([Xs, dummies[["QQQ", "IWM"]].to_numpy(float)])
    return Xf, means, sds


def fit_predict(train: pd.DataFrame, test: pd.DataFrame, cols: list[str], ycol: str):
    Xtr, mu, sd = make_matrix(train, cols)
    Xte, _, _ = make_matrix(test, cols, mu, sd)
    y = train[ycol].astype(int).to_numpy()
    if len(np.unique(y)) < 2:
        raise RuntimeError(f"Training sample has only one class for {ycol}")
    m = LogisticRegression(C=1.0, solver="lbfgs", class_weight=None, max_iter=2000, random_state=0)
    m.fit(Xtr, y)
    return m.predict_proba(Xte)[:, 1]


def choose_target(probs: dict[float, float]) -> float:
    eligible = [m for m in TARGET_MULTS if probs[m] >= DECISION_P]
    return max(eligible) if eligible else 0.50


def walk_forward(panel: pd.DataFrame) -> pd.DataFrame:
    seed = panel[panel["year"].isin(TRAIN_YEARS)].copy()
    test_all = panel[panel["year"].isin(TEST_YEARS)].copy()
    if len(seed) < 150:
        raise RuntimeError(f"Too few 2011 seed candidates: {len(seed)}")

    preds = []
    for current_date in sorted(test_all["date"].unique()):
        train = panel[panel["date"] < current_date]
        test = test_all[test_all["date"] == current_date]
        if test.empty:
            continue

        pa = {}
        pb = {}
        for mult, ycol in TARGET_HIT_COLS.items():
            pa[mult] = fit_predict(train, test, BASE_COLS, ycol)
            pb[mult] = fit_predict(train, test, BASE_COLS + GAMMA_COLS, ycol)

        for j, (_, r) in enumerate(test.iterrows()):
            p_a = {m: float(pa[m][j]) for m in TARGET_MULTS}
            p_b = {m: float(pb[m][j]) for m in TARGET_MULTS}
            mult_a = choose_target(p_a)
            mult_b = choose_target(p_b)
            med = float(r["median20_range"])
            target_a = mult_a * med
            target_b = mult_b * med
            mfe = float(r["same_dir_mfe"])
            hit_a = float(mfe >= target_a)
            hit_b = float(mfe >= target_b)
            cap_a = target_a * hit_a
            cap_b = target_b * hit_b
            ratio_a = min(max(cap_a / max(mfe, 1e-9), 0.0), 1.0)
            ratio_b = min(max(cap_b / max(mfe, 1e-9), 0.0), 1.0)
            preds.append({
                **r.to_dict(),
                "pA_t1": p_a[0.50], "pA_t2": p_a[0.75], "pA_t3": p_a[1.00],
                "pB_t1": p_b[0.50], "pB_t2": p_b[0.75], "pB_t3": p_b[1.00],
                "target_mult_a": mult_a, "target_mult_b": mult_b,
                "target_a": target_a, "target_b": target_b,
                "target_hit_a": hit_a, "target_hit_b": hit_b,
                "capture_a": cap_a, "capture_b": cap_b,
                "capture_mfe_ratio_a": ratio_a, "capture_mfe_ratio_b": ratio_b,
                "target_change": "UPGRADE" if mult_b > mult_a else ("DOWNGRADE" if mult_b < mult_a else "UNCHANGED"),
            })
    return pd.DataFrame(preds).sort_values(["date", "symbol"]).reset_index(drop=True)


def group_metrics(df: pd.DataFrame, label: str) -> dict:
    mean_a = float(df["capture_a"].mean()) if len(df) else np.nan
    mean_b = float(df["capture_b"].mean()) if len(df) else np.nan
    rel = (mean_b / mean_a - 1.0) if mean_a and np.isfinite(mean_a) else np.nan
    counts = df["target_change"].value_counts()
    return {
        "sample": label,
        "n": int(len(df)),
        "mean_capture_a": mean_a,
        "mean_capture_b": mean_b,
        "capture_improvement_rel": rel,
        "hit_rate_a": float(df["target_hit_a"].mean()) if len(df) else np.nan,
        "hit_rate_b": float(df["target_hit_b"].mean()) if len(df) else np.nan,
        "hit_rate_diff_pp": 100.0 * (float(df["target_hit_b"].mean()) - float(df["target_hit_a"].mean())) if len(df) else np.nan,
        "mean_target_mult_a": float(df["target_mult_a"].mean()) if len(df) else np.nan,
        "mean_target_mult_b": float(df["target_mult_b"].mean()) if len(df) else np.nan,
        "target_mult_ratio_b_to_a": float(df["target_mult_b"].mean() / df["target_mult_a"].mean()) if len(df) and df["target_mult_a"].mean() else np.nan,
        "capture_mfe_ratio_a": float(df["capture_mfe_ratio_a"].mean()) if len(df) else np.nan,
        "capture_mfe_ratio_b": float(df["capture_mfe_ratio_b"].mean()) if len(df) else np.nan,
        "upgrade_count": int(counts.get("UPGRADE", 0)),
        "downgrade_count": int(counts.get("DOWNGRADE", 0)),
        "unchanged_count": int(counts.get("UNCHANGED", 0)),
        "a_t1_share": float((df["target_mult_a"] == 0.50).mean()) if len(df) else np.nan,
        "a_t2_share": float((df["target_mult_a"] == 0.75).mean()) if len(df) else np.nan,
        "a_t3_share": float((df["target_mult_a"] == 1.00).mean()) if len(df) else np.nan,
        "b_t1_share": float((df["target_mult_b"] == 0.50).mean()) if len(df) else np.nan,
        "b_t2_share": float((df["target_mult_b"] == 0.75).mean()) if len(df) else np.nan,
        "b_t3_share": float((df["target_mult_b"] == 1.00).mean()) if len(df) else np.nan,
    }


def paired_bootstrap(pred: pd.DataFrame):
    d = (pred["capture_b"] - pred["capture_a"]).to_numpy(float)
    rng = np.random.default_rng(BOOT_SEED)
    means = np.empty(BOOT_N, dtype=float)
    n = len(d)
    for i in range(BOOT_N):
        idx = rng.integers(0, n, size=n)
        means[i] = d[idx].mean()
    lo, hi = np.quantile(means, [0.025, 0.975])
    return float(d.mean()), float(lo), float(hi)


def brier_table(pred: pd.DataFrame) -> pd.DataFrame:
    rows = []
    for mult, ycol in TARGET_HIT_COLS.items():
        a = brier_score_loss(pred[ycol].astype(int), pred[{0.50:"pA_t1",0.75:"pA_t2",1.00:"pA_t3"}[mult]])
        b = brier_score_loss(pred[ycol].astype(int), pred[{0.50:"pB_t1",0.75:"pB_t2",1.00:"pB_t3"}[mult]])
        rows.append({"target_mult": mult, "brier_a": a, "brier_b": b, "improvement_rel": (a-b)/a if a else np.nan})
    return pd.DataFrame(rows)


def subgroup_mfe(pred: pd.DataFrame) -> pd.DataFrame:
    rows = []
    for g in ["UPGRADE", "DOWNGRADE", "UNCHANGED"]:
        x = pred[pred["target_change"] == g]
        rows.append({"group": g, "n": len(x), "mean_same_dir_mfe": float(x["same_dir_mfe"].mean()) if len(x) else np.nan})
    return pd.DataFrame(rows)


def main():
    panel, exclusions = build_panel()
    pred = walk_forward(panel)
    if pred.empty:
        raise RuntimeError("No holdout predictions")

    metrics = [group_metrics(pred, "FULL")]
    for s in SYMBOLS:
        metrics.append(group_metrics(pred[pred["symbol"] == s], f"SYMBOL_{s}"))
    for y in TEST_YEARS:
        metrics.append(group_metrics(pred[pred["year"] == y], f"YEAR_{y}"))
    metrics = pd.DataFrame(metrics)
    brier = brier_table(pred)
    change_mfe = subgroup_mfe(pred)
    boot_mean, boot_lo, boot_hi = paired_bootstrap(pred)

    full = metrics[metrics["sample"] == "FULL"].iloc[0]
    inst = metrics[metrics["sample"].str.startswith("SYMBOL_")]
    years = metrics[metrics["sample"].str.startswith("YEAR_")]

    gate1 = bool(full["capture_improvement_rel"] >= 0.03)
    gate2 = bool(boot_lo > 0)
    gate3 = bool(full["hit_rate_diff_pp"] >= -2.0)
    gate4 = bool(full["target_mult_ratio_b_to_a"] >= 0.95)
    gate5 = bool((inst["capture_improvement_rel"] > 0).sum() >= 2 and (years["capture_improvement_rel"] > 0).all())

    if all([gate1, gate2, gate3, gate4, gate5]):
        verdict = "SUPPORTED FOR SHADOW TARGET CONTEXT TESTING"
    elif all([gate1, gate3, gate4, gate5]) and not gate2:
        verdict = "DECISION UTILITY SIGNAL / RESEARCH-ONLY"
    else:
        verdict = "FAILED DECISION-LEVEL TARGET OVERLAY"

    pred.to_csv(OUT / "gamma_target_calibration_v1_predictions.csv", index=False)
    metrics.to_csv(OUT / "gamma_target_calibration_v1_metrics.csv", index=False)
    brier.to_csv(OUT / "gamma_target_calibration_v1_brier.csv", index=False)
    change_mfe.to_csv(OUT / "gamma_target_calibration_v1_change_mfe.csv", index=False)

    avg_brier_improvement = float(brier["improvement_rel"].mean())
    med_contracts = float(panel["eligible_contracts"].median())

    def pct(x):
        return "—" if pd.isna(x) else f"{100*x:.2f}%"

    def pp(x):
        return "—" if pd.isna(x) else f"{x:.2f} pp"

    lines = []
    lines.append("# Gamma Target Calibration v1.0 — Frozen Results")
    lines.append("")
    lines.append(f"Generated: {datetime.now(timezone.utc).isoformat(timespec='seconds')}")
    lines.append("")
    lines.append("## Coverage")
    lines.append(f"- Total panel rows (2011–2013): **{len(panel)}**")
    lines.append(f"- Training seed candidates (2011): **{len(panel[panel['year']==2011])}**")
    lines.append(f"- Untouched holdout candidates (2012–2013): **{len(pred)}**")
    lines.append(f"- Median eligible option contracts/candidate: **{med_contracts:.0f}**")
    lines.append(f"- Exclusions: `{exclusions}`")
    lines.append("")
    lines.append("## Full-sample decision utility")
    lines.append(f"- Mean capture A (price-only target): **{pct(full['mean_capture_a'])}**")
    lines.append(f"- Mean capture B (price+gamma target): **{pct(full['mean_capture_b'])}**")
    lines.append(f"- Relative capture improvement: **{pct(full['capture_improvement_rel'])}**")
    lines.append(f"- Paired mean capture difference: **{pct(boot_mean)}**")
    lines.append(f"- Paired bootstrap 95% CI: **[{pct(boot_lo)}, {pct(boot_hi)}]**")
    lines.append(f"- Target hit rate A: **{pct(full['hit_rate_a'])}**")
    lines.append(f"- Target hit rate B: **{pct(full['hit_rate_b'])}**")
    lines.append(f"- Hit-rate change: **{pp(full['hit_rate_diff_pp'])}**")
    lines.append(f"- Mean target multiple A: **{full['mean_target_mult_a']:.3f}× median20 range**")
    lines.append(f"- Mean target multiple B: **{full['mean_target_mult_b']:.3f}× median20 range**")
    lines.append(f"- B/A target-multiple ratio: **{full['target_mult_ratio_b_to_a']:.3f}**")
    lines.append(f"- Mean captured-MFE ratio A: **{pct(full['capture_mfe_ratio_a'])}**")
    lines.append(f"- Mean captured-MFE ratio B: **{pct(full['capture_mfe_ratio_b'])}**")
    lines.append(f"- Target changes: **{int(full['upgrade_count'])} upgrades / {int(full['downgrade_count'])} downgrades / {int(full['unchanged_count'])} unchanged**")
    lines.append("")
    lines.append("## Target selection shares")
    lines.append(f"- A: T1 {pct(full['a_t1_share'])}, T2 {pct(full['a_t2_share'])}, T3 {pct(full['a_t3_share'])}")
    lines.append(f"- B: T1 {pct(full['b_t1_share'])}, T2 {pct(full['b_t2_share'])}, T3 {pct(full['b_t3_share'])}")
    lines.append("")
    lines.append("## Instrument / year robustness")
    show = metrics[["sample","n","capture_improvement_rel","hit_rate_diff_pp","mean_target_mult_a","mean_target_mult_b"]].copy()
    show["capture_improvement_rel"] = show["capture_improvement_rel"].map(lambda x: f"{100*x:.2f}%" if pd.notna(x) else "—")
    show["hit_rate_diff_pp"] = show["hit_rate_diff_pp"].map(lambda x: f"{x:.2f}" if pd.notna(x) else "—")
    lines.append(show.to_markdown(index=False))
    lines.append("")
    lines.append("## Probability diagnostic")
    lines.append(brier.to_markdown(index=False, floatfmt=".6f"))
    lines.append(f"- Average relative Brier improvement across T1/T2/T3: **{pct(avg_brier_improvement)}**")
    lines.append("")
    lines.append("## Target-change MFE diagnostic")
    lines.append(change_mfe.to_markdown(index=False, floatfmt=".6f"))
    lines.append("")
    lines.append("## Frozen decision gates")
    lines.append(f"- Mean capture improvement >=3%: **{'PASS' if gate1 else 'FAIL'}**")
    lines.append(f"- Paired bootstrap lower bound >0: **{'PASS' if gate2 else 'FAIL'}**")
    lines.append(f"- Hit rate worsens by <=2pp: **{'PASS' if gate3 else 'FAIL'}**")
    lines.append(f"- Mean target multiple B >=95% of A: **{'PASS' if gate4 else 'FAIL'}**")
    lines.append(f"- Positive capture improvement in >=2/3 instruments and both years: **{'PASS' if gate5 else 'FAIL'}**")
    lines.append(f"- Overall frozen verdict: **{verdict}**")
    lines.append("")
    lines.append("## Interpretation constraint")
    lines.append("This is a target-feasibility proxy on opening-gap continuation candidates. All entries are retained in both models. Daily OHLC cannot determine target-before-stop ordering. No result changes production direction, STRENGTH, RUNWAY, R:R, option selection, BUY/WAIT, or overnight logic automatically.")

    result_text = "\n".join(lines) + "\n"
    (OUT / "gamma_target_calibration_v1_results.md").write_text(result_text)
    print(result_text)


if __name__ == "__main__":
    main()
