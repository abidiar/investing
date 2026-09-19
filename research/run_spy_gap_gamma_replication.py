#!/usr/bin/env python3
"""Frozen Investing OS experiment: SPY gap-conditioned gamma independent replication v1.0.

Rules are frozen in research/spy_gap_gamma_replication_v1.md and must not be
changed after observing results.
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

SRC = Path(os.environ.get("SPY_OPTIONS_PARQUET", "/tmp/options_2025.parquet"))
OUT = Path("research/results")
OUT.mkdir(parents=True, exist_ok=True)

YEAR = 2025
START = "2024-12-01"
END = "2026-01-10"
MIN_DTE = 1
MAX_DTE = 30
MONEYNESS = 0.05
IV_MIN = 0.05
IV_MAX = 2.00
NEAR_05 = 0.005
GAP_MIN = 0.0025
MIN_TRAIN = 60


def safe_spearman(x, y):
    d = pd.concat([pd.Series(x), pd.Series(y)], axis=1).replace([np.inf, -np.inf], np.nan).dropna()
    if len(d) < 5 or d.iloc[:, 0].nunique() < 2 or d.iloc[:, 1].nunique() < 2:
        return np.nan, np.nan, len(d)
    r, p = stats.spearmanr(d.iloc[:, 0], d.iloc[:, 1])
    return float(r), float(p), len(d)


def monthly_opex(d: pd.Timestamp) -> pd.Timestamp:
    first = pd.Timestamp(year=d.year, month=d.month, day=1)
    fridays = pd.date_range(first, first + pd.offsets.MonthEnd(0), freq="W-FRI")
    return fridays[2]


def normal_pdf(z: np.ndarray) -> np.ndarray:
    return np.exp(-0.5 * z * z) / math.sqrt(2.0 * math.pi)


def load_prices() -> pd.DataFrame:
    p = yf.download("SPY", start=START, end=END, auto_adjust=False,
                    progress=False, actions=False, threads=False)
    if p.empty:
        raise RuntimeError("SPY price download returned no rows")
    if isinstance(p.columns, pd.MultiIndex):
        p.columns = [c[0] for c in p.columns]
    p = p[["Open", "High", "Low", "Close"]].copy().sort_index()
    p.index = pd.to_datetime(p.index).tz_localize(None).normalize()
    p["prev_close"] = p["Close"].shift(1)
    p["cc"] = p["Close"].pct_change()
    p["day_oc"] = p["Close"] / p["Open"] - 1
    p["day_abs_oc"] = p["day_oc"].abs()
    p["day_range"] = (p["High"] - p["Low"]) / p["prev_close"]
    p["rv5"] = p["cc"].rolling(5).std(ddof=1)
    p["next_date"] = pd.Series(p.index, index=p.index).shift(-1).values
    p["next_open"] = p["Open"].shift(-1)
    p["next_high"] = p["High"].shift(-1)
    p["next_low"] = p["Low"].shift(-1)
    p["next_close"] = p["Close"].shift(-1)
    return p


def load_options() -> pd.DataFrame:
    if not SRC.exists():
        raise RuntimeError(f"Missing options parquet: {SRC}")
    wanted = ["date", "expiration", "strike", "open_interest", "implied_volatility", "type"]
    x = pd.read_parquet(SRC, columns=wanted)
    x["date"] = pd.to_datetime(x["date"], errors="coerce").dt.tz_localize(None).dt.normalize()
    x["expiration"] = pd.to_datetime(x["expiration"], errors="coerce").dt.tz_localize(None).dt.normalize()
    for c in ["strike", "open_interest", "implied_volatility"]:
        x[c] = pd.to_numeric(x[c], errors="coerce")
    x["type"] = x["type"].astype(str).str.lower()
    x = x[x["date"].dt.year == YEAR].copy()
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


def build_panel() -> tuple[pd.DataFrame, dict]:
    prices = load_prices()
    opt = load_options()
    rows = []
    exclusions = {"no_price": 0, "no_next_price": 0, "no_gamma": 0, "gap_below_threshold": 0}

    for d, day_chain in opt.groupby("date", sort=True):
        d = pd.Timestamp(d).normalize()
        if d not in prices.index:
            exclusions["no_price"] += 1
            continue
        q = prices.loc[d]
        if pd.isna(q["next_open"]) or pd.isna(q["next_close"]):
            exclusions["no_next_price"] += 1
            continue
        spot = float(q["Close"])
        gf = gamma_features(day_chain, spot)
        if gf.get("eligible_contracts", 0) == 0 or gf.get("total_gamma_weight", 0) <= 0:
            exclusions["no_gamma"] += 1
            continue

        nd = pd.Timestamp(q["next_date"]).normalize()
        o, h, l, c = map(float, [q["next_open"], q["next_high"], q["next_low"], q["next_close"]])
        gap = o / spot - 1
        if not np.isfinite(gap) or abs(gap) < GAP_MIN or gap == 0:
            exclusions["gap_below_threshold"] += 1
            continue
        sign = 1.0 if gap > 0 else -1.0
        follow = sign * (c / o - 1)
        if sign > 0:
            mfe = max(h / o - 1, 0.0)
            mae = max(o / l - 1, 0.0)
            gap_fill = float(l <= spot)
        else:
            mfe = max(o / l - 1, 0.0)
            mae = max(h / o - 1, 0.0)
            gap_fill = float(h >= spot)
        eff = mfe / (mfe + mae) if (mfe + mae) > 0 else np.nan
        retention = sign * (c / spot - 1)
        opx = monthly_opex(d)
        monthly_week = bool((d >= opx - pd.Timedelta(days=4)) and (d <= opx))

        rows.append({
            "date": d,
            "next_date": nd,
            "spy_close": spot,
            "gap": gap,
            "abs_gap": abs(gap),
            "gap_sign": sign,
            "gap_followthrough": follow,
            "gap_direction_success": float(follow > 0),
            "mfe_from_open": mfe,
            "mae_from_open": mae,
            "excursion_efficiency": eff,
            "gap_fill": gap_fill,
            "gap_retention_close": retention,
            "day_abs_oc": float(q["day_abs_oc"]),
            "day_range": float(q["day_range"]),
            "rv5": float(q["rv5"]),
            "monthly_opex_week": monthly_week,
            "quarterly_opex_week": bool(monthly_week and d.month in [3, 6, 9, 12]),
            **gf,
        })

    panel = pd.DataFrame(rows).sort_values("date").reset_index(drop=True)
    return panel, exclusions


def correlation_table(panel: pd.DataFrame) -> pd.DataFrame:
    expected = {
        "near_gamma_share_0_5": {
            "gap_followthrough": 1, "excursion_efficiency": 1, "mfe_from_open": 1,
            "gap_retention_close": 1, "mae_from_open": -1, "gap_fill": -1},
        "front_near_gamma_share": {
            "gap_followthrough": 1, "excursion_efficiency": 1, "mfe_from_open": 1,
            "gap_retention_close": 1, "mae_from_open": -1, "gap_fill": -1},
        "weighted_abs_distance": {
            "gap_followthrough": -1, "excursion_efficiency": -1, "mfe_from_open": -1,
            "gap_retention_close": -1, "mae_from_open": 1, "gap_fill": 1},
    }
    samples = {
        "FULL": panel,
        "FIRST_HALF": panel.iloc[:len(panel)//2],
        "SECOND_HALF": panel.iloc[len(panel)//2:],
        "NON_OPEX": panel[~panel["monthly_opex_week"]],
    }
    rows = []
    for sample, df in samples.items():
        for f, outcomes in expected.items():
            for o, es in outcomes.items():
                rho, p, n = safe_spearman(df[f], df[o])
                rows.append({"sample": sample, "feature": f, "outcome": o,
                             "expected_sign": es, "n": n, "rho": rho, "p_value": p})
    return pd.DataFrame(rows)


def median_split(panel: pd.DataFrame) -> pd.DataFrame:
    med = panel["near_gamma_share_0_5"].median()
    x = panel.copy()
    x["bucket"] = np.where(x["near_gamma_share_0_5"] > med, "ABOVE_MEDIAN", "AT_OR_BELOW_MEDIAN")
    return x.groupby("bucket").agg(
        n=("date", "size"),
        mean_near_share=("near_gamma_share_0_5", "mean"),
        continuation_rate=("gap_direction_success", "mean"),
        avg_followthrough=("gap_followthrough", "mean"),
        avg_mfe=("mfe_from_open", "mean"),
        avg_mae=("mae_from_open", "mean"),
        avg_efficiency=("excursion_efficiency", "mean"),
        gap_fill_rate=("gap_fill", "mean"),
        avg_retention=("gap_retention_close", "mean"),
    ).reset_index()


def walk_forward(panel: pd.DataFrame) -> tuple[pd.DataFrame, pd.DataFrame]:
    base_cols = ["abs_gap", "day_abs_oc", "day_range", "rv5"]
    ext_cols = base_cols + ["near_gamma_share_0_5", "front_near_gamma_share", "weighted_abs_distance"]
    targets = ["gap_followthrough", "excursion_efficiency", "mae_from_open"]
    preds = []
    for i in range(MIN_TRAIN, len(panel)):
        train = panel.iloc[:i]
        test = panel.iloc[i:i+1]
        for target in targets:
            for name, cols in [("baseline", base_cols), ("extended", ext_cols)]:
                tr = train[cols + [target]].replace([np.inf, -np.inf], np.nan).dropna()
                te = test[cols + [target]].replace([np.inf, -np.inf], np.nan).dropna()
                if len(tr) < MIN_TRAIN or te.empty:
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
                pred = float(np.r_[1.0, xt[0]].dot(beta))
                actual = float(te[target].iloc[0])
                preds.append({"date": test["date"].iloc[0], "target": target, "model": name,
                              "pred": pred, "actual": actual, "abs_error": abs(pred - actual)})
    p = pd.DataFrame(preds)
    rows = []
    for target in targets:
        z = p[p["target"] == target]
        b = z[z["model"] == "baseline"]
        e = z[z["model"] == "extended"]
        if b.empty or e.empty:
            continue
        mb = float(b["abs_error"].mean())
        me = float(e["abs_error"].mean())
        rows.append({"target": target, "n_test": len(b), "baseline_mae": mb,
                     "extended_mae": me,
                     "mae_improvement_pct": 100 * (mb - me) / mb if mb > 0 else np.nan})
    return p, pd.DataFrame(rows)


def format_pct(v):
    return "—" if pd.isna(v) else f"{100*v:.2f}%"


def main():
    panel, exclusions = build_panel()
    if len(panel) < 70:
        raise RuntimeError(f"Too few qualifying SPY gap sessions for frozen replication: {len(panel)}")

    corr = correlation_table(panel)
    split = median_split(panel)
    preds, wf = walk_forward(panel)

    panel.to_csv(OUT / "spy_gap_gamma_replication_v1_session_panel.csv", index=False)
    corr.to_csv(OUT / "spy_gap_gamma_replication_v1_correlations.csv", index=False)
    preds.to_csv(OUT / "spy_gap_gamma_replication_v1_walkforward_predictions.csv", index=False)
    wf.to_csv(OUT / "spy_gap_gamma_replication_v1_walkforward_summary.csv", index=False)

    # Frozen replication gates.
    def getrow(sample, outcome):
        z = corr[(corr["sample"] == sample) &
                 (corr["feature"] == "near_gamma_share_0_5") &
                 (corr["outcome"] == outcome)]
        return None if z.empty else z.iloc[0]

    primary_outcomes = ["gap_followthrough", "excursion_efficiency"]
    expected_positive_all = True
    full_ps = []
    for o in primary_outcomes:
        for sample in ["FULL", "FIRST_HALF", "SECOND_HALF", "NON_OPEX"]:
            r = getrow(sample, o)
            if r is None or not np.isfinite(r["rho"]) or float(r["rho"]) <= 0:
                expected_positive_all = False
        fr = getrow("FULL", o)
        if fr is not None:
            full_ps.append(float(fr["p_value"]))
    gate1 = expected_positive_all and any(p < 0.10 for p in full_ps)

    mae_row = getrow("FULL", "mae_from_open")
    gate2 = bool(mae_row is not None and np.isfinite(mae_row["rho"]) and float(mae_row["rho"]) < 0)

    nonopex_ok = True
    for o in primary_outcomes:
        r = getrow("NON_OPEX", o)
        if r is None or not np.isfinite(r["rho"]) or float(r["rho"]) <= 0:
            nonopex_ok = False
    gate3 = nonopex_ok

    wfmap = {r.target: r for _, r in wf.iterrows()}
    core_imps = [float(wfmap[t].mae_improvement_pct) for t in primary_outcomes if t in wfmap]
    best_core = max(core_imps) if core_imps else -999
    adverse_imp = float(wfmap["mae_from_open"].mae_improvement_pct) if "mae_from_open" in wfmap else -999
    gate4 = best_core >= 2.0 and adverse_imp >= -1.0

    if all([gate1, gate2, gate3, gate4]):
        verdict = "SUPPORTED"
    elif gate1 and gate2 and gate3:
        verdict = "REPLICATED ASSOCIATION / RESEARCH-ONLY"
    else:
        verdict = "FAILED REPLICATION"

    lines = []
    lines.append("# SPY Gap-Conditioned Gamma Independent Replication v1.0 — Frozen Results\n")
    lines.append(f"Generated: {datetime.now(timezone.utc).isoformat(timespec='seconds')}\n")
    lines.append("## Coverage")
    lines.append(f"- Qualifying abs(gap) >= 0.25% sessions: **{len(panel)}**")
    lines.append(f"- First Day-T: **{panel.date.min().date()}**; last Day-T: **{panel.date.max().date()}**")
    lines.append(f"- Monthly-OPEX-week qualifying sessions: **{int(panel.monthly_opex_week.sum())}**")
    lines.append(f"- Median eligible contracts/session: **{int(panel.eligible_contracts.median())}**")
    lines.append("- Instrument/time independence: SPY calendar 2025; no 2026 QQQ observations used.")
    lines.append(f"- Exclusions: {exclusions}\n")

    lines.append("## Primary correlations")
    lines.append(corr.to_markdown(index=False, floatfmt=".4f"))

    lines.append("\n## Near-gamma median split — descriptive only")
    s = split.copy()
    for c in ["continuation_rate", "avg_followthrough", "avg_mfe", "avg_mae",
              "avg_efficiency", "gap_fill_rate", "avg_retention"]:
        s[c] = s[c].map(format_pct)
    lines.append(s.to_markdown(index=False, floatfmt=".4f"))

    lines.append("\n## Walk-forward incremental test")
    w = wf.copy()
    for c in ["baseline_mae", "extended_mae"]:
        w[c] = w[c].map(format_pct)
    lines.append(w.to_markdown(index=False, floatfmt=".2f"))

    lines.append("\n## Frozen replication gates")
    lines.append(f"- Expected-sign full/half/non-OPEX primary gate: **{'PASS' if gate1 else 'FAIL'}**")
    lines.append(f"- Adverse-excursion coherence gate: **{'PASS' if gate2 else 'FAIL'}**")
    lines.append(f"- Non-OPEX persistence gate: **{'PASS' if gate3 else 'FAIL'}**")
    lines.append(f"- Walk-forward incremental-usefulness gate: **{'PASS' if gate4 else 'FAIL'}**")
    lines.append(f"- Overall frozen verdict: **{verdict}**")
    lines.append("\nNo result from this replication independently creates BUY/SELL/CALL/PUT authority or changes STRENGTH, RUNWAY, R:R, action state, or overnight-carry rules.")

    report = "\n".join(lines)
    (OUT / "spy_gap_gamma_replication_v1_results.md").write_text(report)
    print(report)


if __name__ == "__main__":
    main()
