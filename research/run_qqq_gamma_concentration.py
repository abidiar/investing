#!/usr/bin/env python3
"""Frozen Investing OS experiment: QQQ gamma concentration / pinning v1.0.

Rules are frozen in research/qqq_gamma_concentration_v1.md. Do not alter
feature definitions or thresholds based on observed outcomes.
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

SRC = Path(os.environ.get("QQQ_OPTION_SRC", "/tmp/qqq-option/data/2026"))
OUT = Path("research/results")
OUT.mkdir(parents=True, exist_ok=True)

START = "2026-01-01"
END = "2026-09-20"  # yfinance end is exclusive
MIN_DTE = 1
MAX_DTE = 30
MONEYNESS = 0.05
IV_MIN = 0.05
IV_MAX = 2.00
NEAR_05 = 0.005
NEAR_10 = 0.010
MEANINGFUL_MOVE = 0.0025
MIN_TRAIN = 60


def safe_spearman(x: pd.Series, y: pd.Series):
    d = pd.concat([x, y], axis=1).replace([np.inf, -np.inf], np.nan).dropna()
    if len(d) < 5 or d.iloc[:, 0].nunique() < 2 or d.iloc[:, 1].nunique() < 2:
        return np.nan, np.nan, len(d)
    r, p = stats.spearmanr(d.iloc[:, 0], d.iloc[:, 1])
    return float(r), float(p), len(d)


def monthly_opex(d: pd.Timestamp) -> pd.Timestamp:
    first = pd.Timestamp(year=d.year, month=d.month, day=1)
    fridays = pd.date_range(first, first + pd.offsets.MonthEnd(0), freq="W-FRI")
    return fridays[2]


def load_prices() -> pd.DataFrame:
    p = yf.download("QQQ", start=START, end=END, auto_adjust=False,
                    progress=False, actions=False, threads=False)
    if p.empty:
        raise RuntimeError("QQQ price download returned no rows")
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
    p["next_close"] = p["Close"].shift(-1)
    p["next_open"] = p["Open"].shift(-1)
    p["next_high"] = p["High"].shift(-1)
    p["next_low"] = p["Low"].shift(-1)
    p["next_cc"] = p["next_close"] / p["Close"] - 1
    p["next_abs_cc"] = p["next_cc"].abs()
    p["next_gap"] = p["next_open"] / p["Close"] - 1
    p["next_oc"] = p["next_close"] / p["next_open"] - 1
    p["next_range"] = (p["next_high"] - p["next_low"]) / p["Close"]
    p["next_date"] = pd.Series(p.index, index=p.index).shift(-1).values
    return p


def snapshot_dates() -> list[pd.Timestamp]:
    if not SRC.exists():
        raise RuntimeError(f"Source path missing: {SRC}")
    out = []
    for m in sorted(SRC.iterdir()):
        if not m.is_dir():
            continue
        for d in sorted(m.iterdir()):
            if not d.is_dir() or not list(d.glob("*.csv")):
                continue
            try:
                out.append(pd.Timestamp(f"2026-{m.name}-{d.name}"))
            except Exception:
                pass
    return sorted(set(out))


def load_snapshot(d: pd.Timestamp) -> pd.DataFrame:
    daydir = SRC / f"{d.month:02d}" / f"{d.day:02d}"
    parts = []
    use = ["contractSymbol", "strike", "openInterest", "impliedVolatility", "type"]
    for fp in sorted(daydir.glob("*.csv")):
        try:
            exp = pd.Timestamp(fp.stem)
        except Exception:
            continue
        dte = (exp - d).days
        if not (MIN_DTE <= dte <= MAX_DTE):
            continue
        try:
            x = pd.read_csv(fp, usecols=use)
        except Exception:
            continue
        x["expiration"] = exp
        x["dte"] = dte
        parts.append(x)
    if not parts:
        return pd.DataFrame(columns=use + ["expiration", "dte"])
    x = pd.concat(parts, ignore_index=True)
    for c in ["strike", "openInterest", "impliedVolatility"]:
        x[c] = pd.to_numeric(x[c], errors="coerce")
    x["type"] = x["type"].astype(str).str.lower()
    return x.drop_duplicates("contractSymbol", keep="last")


def normal_pdf(z: np.ndarray) -> np.ndarray:
    return np.exp(-0.5 * z * z) / math.sqrt(2.0 * math.pi)


def gamma_features(chain: pd.DataFrame, spot: float) -> dict:
    x = chain.copy()
    x = x[x["strike"].between(spot * (1 - MONEYNESS), spot * (1 + MONEYNESS))]
    x = x[(x["openInterest"].notna()) & (x["openInterest"] >= 0)]
    x = x[(x["impliedVolatility"].notna()) &
          (x["impliedVolatility"] >= IV_MIN) &
          (x["impliedVolatility"] <= IV_MAX)]
    x = x[(x["dte"] >= MIN_DTE) & (x["dte"] <= MAX_DTE)]
    x = x[(x["strike"] > 0) & np.isfinite(x["strike"])]
    if x.empty:
        return {"eligible_contracts": 0}

    S = float(spot)
    K = x["strike"].to_numpy(dtype=float)
    sigma = x["impliedVolatility"].to_numpy(dtype=float)
    T = x["dte"].to_numpy(dtype=float) / 365.0
    sqrtT = np.sqrt(T)
    d1 = (np.log(S / K) + 0.5 * sigma * sigma * T) / (sigma * sqrtT)
    gamma = normal_pdf(d1) / (S * sigma * sqrtT)
    oi = x["openInterest"].to_numpy(dtype=float)
    w = gamma * oi

    x["gamma"] = gamma
    x["gamma_weight"] = w
    x["abs_dist"] = np.abs(x["strike"] / S - 1.0)
    x = x[np.isfinite(x["gamma_weight"]) & (x["gamma_weight"] >= 0)]
    total = float(x["gamma_weight"].sum())
    if total <= 0:
        return {"eligible_contracts": int(len(x)), "total_gamma_weight": 0.0}

    by_strike = x.groupby("strike", as_index=False)["gamma_weight"].sum()
    by_strike["share"] = by_strike["gamma_weight"] / total
    dom = by_strike.loc[by_strike["gamma_weight"].idxmax()]
    hhi = float(np.square(by_strike["share"]).sum())

    near05 = float(x.loc[x["abs_dist"] <= NEAR_05, "gamma_weight"].sum() / total)
    near10 = float(x.loc[x["abs_dist"] <= NEAR_10, "gamma_weight"].sum() / total)
    front = float(x.loc[x["dte"] <= 7, "gamma_weight"].sum() / total)
    front_near = float(x.loc[(x["dte"] <= 7) & (x["abs_dist"] <= NEAR_05), "gamma_weight"].sum() / total)
    wad = float((x["gamma_weight"] * x["abs_dist"]).sum() / total)

    return {
        "eligible_contracts": int(len(x)),
        "total_gamma_weight": total,
        "near_gamma_share_0_5": near05,
        "near_gamma_share_1_0": near10,
        "front_gamma_share": front,
        "front_near_gamma_share": front_near,
        "dominant_strike": float(dom["strike"]),
        "dominant_strike_share": float(dom["share"]),
        "dominant_strike_distance": abs(float(dom["strike"]) / S - 1.0),
        "weighted_abs_distance": wad,
        "strike_hhi": hhi,
        "effective_strikes": (1.0 / hhi) if hhi > 0 else np.nan,
    }


def build_panel(prices: pd.DataFrame):
    rows = []
    exclusions = {"no_price": 0, "no_next_price": 0, "empty_chain": 0,
                  "no_eligible_gamma": 0}
    for d in snapshot_dates():
        if d not in prices.index:
            exclusions["no_price"] += 1
            continue
        if pd.isna(prices.loc[d, "next_cc"]):
            exclusions["no_next_price"] += 1
            continue
        chain = load_snapshot(d)
        if chain.empty:
            exclusions["empty_chain"] += 1
            continue
        spot = float(prices.loc[d, "Close"])
        gf = gamma_features(chain, spot)
        if gf.get("eligible_contracts", 0) == 0 or gf.get("total_gamma_weight", 0) <= 0:
            exclusions["no_eligible_gamma"] += 1
            continue

        day_oc = float(prices.loc[d, "day_oc"])
        next_cc = float(prices.loc[d, "next_cc"])
        meaningful = abs(day_oc) >= MEANINGFUL_MOVE
        dom = gf["dominant_strike"]
        next_close = float(prices.loc[d, "next_close"])
        pin_before = abs(dom - spot) / spot
        pin_after = abs(dom - next_close) / spot
        opx = monthly_opex(d)

        row = {
            "date": d,
            "next_date": prices.loc[d, "next_date"],
            "qqq_open": float(prices.loc[d, "Open"]),
            "qqq_close": spot,
            "day_oc": day_oc,
            "day_abs_oc": float(prices.loc[d, "day_abs_oc"]),
            "day_range": float(prices.loc[d, "day_range"]) if pd.notna(prices.loc[d, "day_range"]) else np.nan,
            "rv5": float(prices.loc[d, "rv5"]) if pd.notna(prices.loc[d, "rv5"]) else np.nan,
            "meaningful_move": meaningful,
            "next_close": next_close,
            "next_cc": next_cc,
            "next_abs_cc": float(prices.loc[d, "next_abs_cc"]),
            "next_gap": float(prices.loc[d, "next_gap"]),
            "next_oc": float(prices.loc[d, "next_oc"]),
            "next_range": float(prices.loc[d, "next_range"]),
            "continuation_return": (np.sign(day_oc) * next_cc) if meaningful else np.nan,
            "continued": (float(np.sign(day_oc) == np.sign(next_cc)) if meaningful and next_cc != 0 else np.nan),
            "pin_improvement": pin_before - pin_after,
            "monthly_opex_week": bool((d >= opx - pd.Timedelta(days=4)) and (d <= opx)),
            "quarterly_opex_week": bool((d >= opx - pd.Timedelta(days=4)) and (d <= opx) and d.month in [3, 6, 9, 12]),
        }
        row.update(gf)
        rows.append(row)
    return pd.DataFrame(rows).sort_values("date").reset_index(drop=True), exclusions


PRIMARY_EXPECTED = {
    "near_gamma_share_0_5": -1,
    "front_near_gamma_share": -1,
    "strike_hhi": -1,
    "weighted_abs_distance": +1,
    "effective_strikes": +1,
}


def primary_tests(panel: pd.DataFrame) -> pd.DataFrame:
    rows = []
    midpoint = len(panel) // 2
    slices = {
        "FULL": panel,
        "FIRST_HALF": panel.iloc[:midpoint],
        "SECOND_HALF": panel.iloc[midpoint:],
    }
    for sample, d in slices.items():
        for feature, expected in PRIMARY_EXPECTED.items():
            for outcome in ["next_abs_cc", "next_range"]:
                r, p, n = safe_spearman(d[feature], d[outcome])
                rows.append({"sample": sample, "feature": feature, "expected_sign": expected,
                             "outcome": outcome, "n": n, "rho": r, "p_value": p})
    return pd.DataFrame(rows)


def secondary_tests(panel: pd.DataFrame) -> pd.DataFrame:
    rows = []
    near_dom = panel[panel["dominant_strike_distance"] <= 0.01]
    r, p, n = safe_spearman(near_dom["dominant_strike_share"], near_dom["pin_improvement"])
    rows.append({"test": "H3_near_dominant_pin", "feature": "dominant_strike_share",
                 "outcome": "pin_improvement", "n": n, "rho": r, "p_value": p})
    moved = panel[panel["meaningful_move"]]
    for feature in ["front_near_gamma_share", "strike_hhi"]:
        for outcome in ["continuation_return", "continued"]:
            r, p, n = safe_spearman(moved[feature], moved[outcome])
            rows.append({"test": "H4_continuation", "feature": feature,
                         "outcome": outcome, "n": n, "rho": r, "p_value": p})
    # Additional descriptive components named in the frozen spec.
    for feature in ["near_gamma_share_1_0", "front_gamma_share", "dominant_strike_share", "dominant_strike_distance"]:
        for outcome in ["next_abs_cc", "next_range"]:
            r, p, n = safe_spearman(panel[feature], panel[outcome])
            rows.append({"test": "SECONDARY_STRUCTURE", "feature": feature,
                         "outcome": outcome, "n": n, "rho": r, "p_value": p})
    return pd.DataFrame(rows)


def fit_predict(train: pd.DataFrame, test: pd.Series, features: list[str], target: str) -> float:
    X = train[features].astype(float)
    y = train[target].astype(float).to_numpy()
    mu = X.mean(axis=0)
    sd = X.std(axis=0, ddof=0).replace(0, 1.0)
    Xz = ((X - mu) / sd).to_numpy()
    tx = ((test[features].astype(float) - mu) / sd).to_numpy()
    Xd = np.column_stack([np.ones(len(Xz)), Xz])
    beta, *_ = np.linalg.lstsq(Xd, y, rcond=None)
    return float(np.r_[1.0, tx] @ beta)


def walk_forward(panel: pd.DataFrame):
    baseline = ["day_abs_oc", "day_range", "rv5"]
    extended = baseline + [
        "near_gamma_share_0_5", "front_gamma_share", "front_near_gamma_share",
        "strike_hhi", "weighted_abs_distance", "dominant_strike_share",
        "dominant_strike_distance",
    ]
    all_features = extended
    pred_rows = []
    summaries = []
    for target in ["next_abs_cc", "next_range"]:
        d = panel[["date", target] + all_features].replace([np.inf, -np.inf], np.nan).dropna().reset_index(drop=True)
        for i in range(MIN_TRAIN, len(d)):
            tr = d.iloc[:i]
            te = d.iloc[i]
            bp = fit_predict(tr, te, baseline, target)
            ep = fit_predict(tr, te, extended, target)
            pred_rows.append({"date": te["date"], "target": target, "actual": float(te[target]),
                              "baseline_pred": bp, "extended_pred": ep})
        pr = pd.DataFrame([r for r in pred_rows if r["target"] == target])
        if pr.empty:
            continue
        bmae = float(np.mean(np.abs(pr["actual"] - pr["baseline_pred"])))
        emae = float(np.mean(np.abs(pr["actual"] - pr["extended_pred"])))
        br, bpv, bn = safe_spearman(pr["baseline_pred"], pr["actual"])
        er, epv, en = safe_spearman(pr["extended_pred"], pr["actual"])
        summaries.append({
            "target": target,
            "n_test": len(pr),
            "baseline_mae": bmae,
            "extended_mae": emae,
            "mae_improvement_pct": (bmae - emae) / bmae if bmae > 0 else np.nan,
            "baseline_pred_rho": br,
            "baseline_pred_p": bpv,
            "extended_pred_rho": er,
            "extended_pred_p": epv,
        })
    return pd.DataFrame(summaries), pd.DataFrame(pred_rows)


def median_table(panel: pd.DataFrame, feature: str) -> pd.DataFrame:
    d = panel[[feature, "next_abs_cc", "next_range", "next_cc"]].dropna().copy()
    med = d[feature].median()
    d["bucket"] = np.where(d[feature] > med, "ABOVE_MEDIAN", "AT_OR_BELOW_MEDIAN")
    return d.groupby("bucket").agg(
        n=(feature, "size"),
        feature_mean=(feature, "mean"),
        avg_abs_next=("next_abs_cc", "mean"),
        avg_range=("next_range", "mean"),
        avg_signed_next=("next_cc", "mean"),
    ).reset_index()


def fmt_table(df: pd.DataFrame, pct_cols=None, digits=4) -> str:
    if df.empty:
        return "No eligible rows."
    pct_cols = set(pct_cols or [])
    x = df.copy()
    for c in x.columns:
        if c in pct_cols:
            x[c] = x[c].map(lambda v: "—" if pd.isna(v) else f"{100*v:.2f}%")
        elif pd.api.types.is_float_dtype(x[c]):
            x[c] = x[c].map(lambda v: "—" if pd.isna(v) else f"{v:.{digits}f}")
    return x.to_markdown(index=False)


def mechanical_verdict(primary: pd.DataFrame, secondary: pd.DataFrame, wf: pd.DataFrame):
    qualifying = []
    full = primary[primary["sample"] == "FULL"]
    for _, r in full.iterrows():
        f, out = r["feature"], r["outcome"]
        expected = int(r["expected_sign"])
        h1 = primary[(primary["sample"] == "FIRST_HALF") & (primary["feature"] == f) & (primary["outcome"] == out)]
        h2 = primary[(primary["sample"] == "SECOND_HALF") & (primary["feature"] == f) & (primary["outcome"] == out)]
        if h1.empty or h2.empty or pd.isna(r["rho"]):
            continue
        sign_ok = (expected * r["rho"] > 0 and expected * float(h1.iloc[0]["rho"]) > 0 and expected * float(h2.iloc[0]["rho"]) > 0)
        p_ok = r["p_value"] < 0.10
        if sign_ok and p_ok:
            qualifying.append((f, out, r["rho"], r["p_value"]))

    wf_map = {r["target"]: r["mae_improvement_pct"] for _, r in wf.iterrows()}
    a = wf_map.get("next_abs_cc", np.nan)
    b = wf_map.get("next_range", np.nan)
    wf_ok = ((pd.notna(a) and a >= 0.02 and pd.notna(b) and b >= -0.01) or
             (pd.notna(b) and b >= 0.02 and pd.notna(a) and a >= -0.01))

    pin = secondary[secondary["test"] == "H3_near_dominant_pin"]
    pin_ok = (not pin.empty and pd.notna(pin.iloc[0]["rho"]) and pin.iloc[0]["rho"] >= 0)
    cont = secondary[(secondary["test"] == "H4_continuation") & (secondary["outcome"] == "continuation_return")]
    cont_ok = bool((cont["rho"] <= 0).any()) if not cont.empty else False
    coherent = pin_ok and cont_ok

    promote = bool(qualifying and wf_ok and coherent)
    return promote, qualifying, wf_ok, coherent


def main():
    prices = load_prices()
    panel, exclusions = build_panel(prices)
    if panel.empty:
        raise RuntimeError("No eligible gamma sessions")

    primary = primary_tests(panel)
    secondary = secondary_tests(panel)
    wf, preds = walk_forward(panel)
    panel.to_csv(OUT / "qqq_gamma_concentration_v1_session_panel.csv", index=False)
    primary.to_csv(OUT / "qqq_gamma_concentration_v1_primary_tests.csv", index=False)
    secondary.to_csv(OUT / "qqq_gamma_concentration_v1_secondary_tests.csv", index=False)
    wf.to_csv(OUT / "qqq_gamma_concentration_v1_walk_forward.csv", index=False)
    preds.to_csv(OUT / "qqq_gamma_concentration_v1_predictions.csv", index=False)

    promote, qualifying, wf_ok, coherent = mechanical_verdict(primary, secondary, wf)
    first = panel["date"].min().date()
    last = panel["date"].max().date()
    med_contracts = float(panel["eligible_contracts"].median())

    near_split = median_table(panel, "near_gamma_share_0_5")
    hhi_split = median_table(panel, "strike_hhi")
    opx = panel.groupby("monthly_opex_week").agg(
        n=("date", "size"),
        near_share=("near_gamma_share_0_5", "mean"),
        front_near_share=("front_near_gamma_share", "mean"),
        strike_hhi=("strike_hhi", "mean"),
        avg_abs_next=("next_abs_cc", "mean"),
        avg_range=("next_range", "mean"),
    ).reset_index()

    lines = []
    lines += ["# QQQ Gamma Concentration / Pinning v1.0 — Frozen Backtest Results", "",
              f"Generated: {datetime.now(timezone.utc).isoformat(timespec='seconds')}", "",
              "## Frozen sample", f"- Eligible sessions: **{len(panel)}**",
              f"- First Day-T: **{first}**", f"- Last Day-T: **{last}**",
              f"- Median eligible contracts/session: **{med_contracts:.0f}**",
              "- DTE: **1–30 days**; moneyness: **±5%**; IV filter: **5%–200%**",
              "- Unsigned theoretical gamma only; this is **not dealer GEX**.", "",
              "### Exclusions", *[f"- {k}: {v}" for k, v in exclusions.items()], "",
              "## H1/H2 — Primary damping / expansion associations", "",
              fmt_table(primary, digits=4), "",
              "## Descriptive median split — near-spot gamma share", "",
              fmt_table(near_split, pct_cols=["avg_abs_next", "avg_range", "avg_signed_next"]), "",
              "## Descriptive median split — strike HHI", "",
              fmt_table(hhi_split, pct_cols=["avg_abs_next", "avg_range", "avg_signed_next"]), "",
              "## H3/H4 and secondary structure tests", "",
              fmt_table(secondary, digits=4), "",
              "## Walk-forward incremental test vs price-only baseline", "",
              fmt_table(wf, pct_cols=["baseline_mae", "extended_mae", "mae_improvement_pct"], digits=4), "",
              "## OPEX descriptive cut", "",
              fmt_table(opx, pct_cols=["avg_abs_next", "avg_range"], digits=4), "",
              "## Mechanical promotion screen", "",
              f"- Stable expected-sign primary associations with full-sample p<0.10: **{len(qualifying)}**",
              *[f"  - {f} -> {o}: rho={r:.4f}, p={p:.4f}" for f, o, r, p in qualifying],
              f"- Walk-forward MAE gate: **{'PASS' if wf_ok else 'FAIL'}**",
              f"- Pinning/continuation directional-coherence gate: **{'PASS' if coherent else 'FAIL'}**",
              f"- Overall v1.0 promotion verdict: **{'PROMOTE TO CONTEXT TAG' if promote else 'RESEARCH-ONLY'}**", "",
              "No result from this pass has independent directional authority or permission to alter STRENGTH, RUNWAY, R:R, or action state."]

    report = "\n".join(lines) + "\n"
    (OUT / "qqq_gamma_concentration_v1_results.md").write_text(report, encoding="utf-8")
    print(report)


if __name__ == "__main__":
    main()
