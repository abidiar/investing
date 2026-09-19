#!/usr/bin/env python3
"""Frozen Investing OS experiment: gamma compression chase decision v1.0.

Rules are frozen in research/gamma_chase_decision_v1.md.
Do not change sample, target, features, model, threshold, or gates after results.
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

DATA_DIR = Path(os.environ.get("OPTIONS_DATA_DIR", "/tmp/options_gamma_chase"))
OUT = Path("research/results")
OUT.mkdir(parents=True, exist_ok=True)

SYMBOLS = ["SPY", "QQQ", "IWM"]
TRAIN_YEARS = [2014, 2015, 2016]
TEST_YEARS = [2017, 2018, 2019]
ALL_YEARS = TRAIN_YEARS + TEST_YEARS
MIN_DTE = 1
MAX_DTE = 30
MONEYNESS = 0.05
IV_MIN = 0.05
IV_MAX = 2.00
NEAR_05 = 0.005
GAP_MIN = 0.0025
T1_MULT = 0.50
T2_MULT = 0.75
DECISION_P = 0.60

BASE_COLS = [
    "abs_gap", "gap_atr20", "gap_up", "day_abs_oc", "day_range",
    "rv5", "rv20", "median20_range", "atr20", "range20_ratio",
]
GAMMA_COLS = ["near_gamma_share_0_5", "front_near_gamma_share", "weighted_abs_distance"]


def normal_pdf(z):
    return np.exp(-0.5 * z * z) / math.sqrt(2.0 * math.pi)


def load_prices(symbol: str) -> pd.DataFrame:
    p = yf.download(symbol, start="2013-10-01", end="2020-01-10", auto_adjust=False,
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
                if any(pd.isna(q[c]) or not np.isfinite(q[c]) or float(q[c]) <= 0 for c in needed[1:]):
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

                gap_up = 1.0 if gap > 0 else 0.0
                same_mfe = max(h / o - 1.0, 0.0) if gap > 0 else max(o / l - 1.0, 0.0)
                t1 = T1_MULT * float(q["median20_range"])
                t2 = T2_MULT * float(q["median20_range"])
                row = {
                    "symbol": symbol,
                    "year": int(d.year),
                    "date": d,
                    "next_date": pd.Timestamp(q["next_date"]).normalize(),
                    "gap": gap,
                    "abs_gap": abs(gap),
                    "gap_atr20": abs(gap) / float(q["atr20"]),
                    "gap_up": gap_up,
                    "day_abs_oc": float(q["day_abs_oc"]),
                    "day_range": float(q["day_range"]),
                    "rv5": float(q["rv5"]),
                    "rv20": float(q["rv20"]),
                    "median20_range": float(q["median20_range"]),
                    "atr20": float(q["atr20"]),
                    "range20_ratio": float(q["range20_ratio"]),
                    "same_dir_mfe": same_mfe,
                    "t1_distance": t1,
                    "t2_distance": t2,
                    "t1_hit": float(same_mfe >= t1),
                    "t2_hit": float(same_mfe >= t2),
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
    # SPY baseline, append QQQ/IWM.
    Xf = np.column_stack([Xs, dummies[["QQQ", "IWM"]].to_numpy(float)])
    return Xf, means, sds


def fit_predict(train: pd.DataFrame, test: pd.DataFrame, cols: list[str]):
    Xtr, mu, sd = make_matrix(train, cols)
    Xte, _, _ = make_matrix(test, cols, mu, sd)
    y = train["t1_hit"].astype(int).to_numpy()
    if len(np.unique(y)) < 2:
        raise RuntimeError("Training sample has only one T1 class")
    m = LogisticRegression(C=1.0, solver="lbfgs", class_weight=None, max_iter=2000, random_state=0)
    m.fit(Xtr, y)
    return m.predict_proba(Xte)[:, 1]


def walk_forward(panel: pd.DataFrame) -> pd.DataFrame:
    seed = panel[panel["year"].isin(TRAIN_YEARS)].copy()
    test_all = panel[panel["year"].isin(TEST_YEARS)].copy()
    if len(seed) < 200:
        raise RuntimeError(f"Too few seed candidates: {len(seed)}")
    preds = []
    for current_date in sorted(test_all["date"].unique()):
        train = panel[panel["date"] < current_date]
        test = test_all[test_all["date"] == current_date]
        if test.empty:
            continue
        p_a = fit_predict(train, test, BASE_COLS)
        p_b = fit_predict(train, test, BASE_COLS + GAMMA_COLS)
        for j, (_, r) in enumerate(test.iterrows()):
            pa = float(p_a[j]); pb = float(p_b[j])
            chase_a = pa >= DECISION_P
            chase_b = chase_a and (pb >= DECISION_P)
            preds.append({
                **r.to_dict(),
                "p_price": pa,
                "p_gamma": pb,
                "chase_a": float(chase_a),
                "chase_b": float(chase_b),
                "gamma_veto": float(chase_a and not chase_b),
            })
    return pd.DataFrame(preds).sort_values(["date", "symbol"]).reset_index(drop=True)


def safe_rate(df, col):
    return float(df[col].mean()) if len(df) else np.nan


def decision_metrics(df: pd.DataFrame, label: str) -> dict:
    base = df[df["chase_a"] == 1]
    over = df[df["chase_b"] == 1]
    veto = df[df["gamma_veto"] == 1]
    base_hits = float(base["t1_hit"].sum()) if len(base) else 0.0
    over_hits = float(over["t1_hit"].sum()) if len(over) else 0.0
    return {
        "sample": label,
        "n_candidates": len(df),
        "baseline_chases": len(base),
        "overlay_chases": len(over),
        "vetoes": len(veto),
        "baseline_t1_precision": safe_rate(base, "t1_hit"),
        "overlay_t1_precision": safe_rate(over, "t1_hit"),
        "precision_improvement_pp": 100.0 * (safe_rate(over, "t1_hit") - safe_rate(base, "t1_hit")) if len(base) and len(over) else np.nan,
        "baseline_miss_rate": 1.0 - safe_rate(base, "t1_hit") if len(base) else np.nan,
        "veto_miss_rate": 1.0 - safe_rate(veto, "t1_hit") if len(veto) else np.nan,
        "veto_miss_minus_baseline_pp": 100.0 * ((1.0 - safe_rate(veto, "t1_hit")) - (1.0 - safe_rate(base, "t1_hit"))) if len(veto) and len(base) else np.nan,
        "retained_baseline_winners": over_hits / base_hits if base_hits > 0 else np.nan,
        "baseline_t2_hit_rate": safe_rate(base, "t2_hit"),
        "overlay_t2_hit_rate": safe_rate(over, "t2_hit"),
        "veto_t2_hit_rate": safe_rate(veto, "t2_hit"),
        "baseline_mean_mfe": float(base["same_dir_mfe"].mean()) if len(base) else np.nan,
        "overlay_mean_mfe": float(over["same_dir_mfe"].mean()) if len(over) else np.nan,
        "veto_mean_mfe": float(veto["same_dir_mfe"].mean()) if len(veto) else np.nan,
    }


def main():
    panel, exclusions = build_panel()
    if len(panel) < 700:
        raise RuntimeError(f"Too few total candidates: {len(panel)}")
    pred = walk_forward(panel)
    if len(pred) < 250:
        raise RuntimeError(f"Too few holdout candidates: {len(pred)}")

    # Overall predictive calibration.
    y = pred["t1_hit"].astype(float).to_numpy()
    brier_a = float(brier_score_loss(y, pred["p_price"].to_numpy(float)))
    brier_b = float(brier_score_loss(y, pred["p_gamma"].to_numpy(float)))
    brier_imp = 100.0 * (brier_a - brier_b) / brier_a if brier_a > 0 else np.nan

    rows = [decision_metrics(pred, "FULL")]
    for s in SYMBOLS:
        rows.append(decision_metrics(pred[pred["symbol"] == s], f"SYMBOL_{s}"))
    for yv in TEST_YEARS:
        rows.append(decision_metrics(pred[pred["year"] == yv], f"YEAR_{yv}"))
    metrics = pd.DataFrame(rows)

    full = metrics[metrics["sample"] == "FULL"].iloc[0]
    gate1 = bool(np.isfinite(full["precision_improvement_pp"]) and full["precision_improvement_pp"] >= 3.0)
    gate2 = bool(np.isfinite(full["veto_miss_minus_baseline_pp"]) and full["veto_miss_minus_baseline_pp"] >= 10.0)
    gate3 = bool(np.isfinite(full["retained_baseline_winners"]) and full["retained_baseline_winners"] >= 0.85)
    gate4 = bool(np.isfinite(brier_imp) and brier_imp >= 2.0)

    inst_pos = 0
    for s in SYMBOLS:
        r = metrics[metrics["sample"] == f"SYMBOL_{s}"].iloc[0]
        if np.isfinite(r["precision_improvement_pp"]) and r["precision_improvement_pp"] > 0:
            inst_pos += 1
    year_pos = 0
    for yv in TEST_YEARS:
        r = metrics[metrics["sample"] == f"YEAR_{yv}"].iloc[0]
        if np.isfinite(r["precision_improvement_pp"]) and r["precision_improvement_pp"] > 0:
            year_pos += 1
    gate5 = inst_pos >= 2 and year_pos >= 2

    if all([gate1, gate2, gate3, gate4, gate5]):
        verdict = "SUPPORTED FOR SHADOW CONTEXT TESTING"
    elif gate1 and gate2 and gate3 and gate5:
        verdict = "DECISION UTILITY SIGNAL / RESEARCH-ONLY"
    else:
        verdict = "FAILED DECISION-LEVEL OVERLAY"

    panel.to_csv(OUT / "gamma_chase_decision_v1_panel.csv", index=False)
    pred.to_csv(OUT / "gamma_chase_decision_v1_predictions.csv", index=False)
    metrics.to_csv(OUT / "gamma_chase_decision_v1_metrics.csv", index=False)

    def pct(v):
        return "—" if pd.isna(v) else f"{100*v:.2f}%"

    disp = metrics.copy()
    for c in ["baseline_t1_precision", "overlay_t1_precision", "baseline_miss_rate", "veto_miss_rate",
              "retained_baseline_winners", "baseline_t2_hit_rate", "overlay_t2_hit_rate", "veto_t2_hit_rate",
              "baseline_mean_mfe", "overlay_mean_mfe", "veto_mean_mfe"]:
        disp[c] = disp[c].map(pct)

    lines = []
    lines.append("# Gamma Compression Chase Decision v1.0 — Frozen Results\n")
    lines.append(f"Generated: {datetime.now(timezone.utc).isoformat(timespec='seconds')}\n")
    lines.append("## Coverage")
    lines.append(f"- Total candidate panel rows (2014–2019): **{len(panel)}**")
    lines.append(f"- Untouched holdout candidate rows (2017–2019): **{len(pred)}**")
    lines.append(f"- Training seed candidates (2014–2016): **{int(panel['year'].isin(TRAIN_YEARS).sum())}**")
    lines.append(f"- Holdout T1 base hit rate: **{100*pred['t1_hit'].mean():.2f}%**")
    lines.append(f"- Median eligible option contracts/candidate: **{int(panel['eligible_contracts'].median())}**")
    lines.append(f"- Exclusions: {exclusions}\n")

    lines.append("## Decision metrics")
    lines.append(disp.to_markdown(index=False, floatfmt=".2f"))

    lines.append("\n## Probability calibration")
    lines.append(f"- Price-only Brier score: **{brier_a:.5f}**")
    lines.append(f"- Price+gamma Brier score: **{brier_b:.5f}**")
    lines.append(f"- Brier improvement: **{brier_imp:.2f}%**")

    lines.append("\n## Frozen decision gates")
    lines.append(f"- Overlay precision improvement >=3.0pp: **{'PASS' if gate1 else 'FAIL'}**")
    lines.append(f"- Veto miss-rate lift >=10.0pp vs baseline miss rate: **{'PASS' if gate2 else 'FAIL'}**")
    lines.append(f"- Retain >=85% of baseline T1 winners: **{'PASS' if gate3 else 'FAIL'}**")
    lines.append(f"- Brier improvement >=2%: **{'PASS' if gate4 else 'FAIL'}**")
    lines.append(f"- Positive precision improvement in >=2/3 instruments and >=2/3 years: **{'PASS' if gate5 else 'FAIL'}**")
    lines.append(f"- Overall frozen verdict: **{verdict}**")

    lines.append("\n## Interpretation constraint")
    lines.append("This is a proxy opening-gap chase/target-feasibility study, not a backtest of the full Investing OS scanner. Daily OHLC cannot determine target-before-stop ordering. No result changes production STRENGTH, RUNWAY, direction, R:R, option selection, or BUY/WAIT logic automatically.")

    report = "\n".join(lines)
    (OUT / "gamma_chase_decision_v1_results.md").write_text(report)
    print(report)


if __name__ == "__main__":
    main()
