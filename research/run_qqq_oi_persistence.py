#!/usr/bin/env python3
"""Frozen Investing OS experiment: QQQ settled OI persistence v1.0.

Rules are documented in research/qqq_oi_persistence_v1.md and must not be
changed in this script based on observed outcomes.
"""
from __future__ import annotations

import math
import os
from pathlib import Path
from datetime import date, datetime, timedelta

import numpy as np
import pandas as pd
from scipy import stats
import yfinance as yf

SRC = Path(os.environ.get("QQQ_OPTION_SRC", "/tmp/qqq-option/data/2026"))
OUT_DIR = Path("research/results")
OUT_DIR.mkdir(parents=True, exist_ok=True)

START = "2026-01-01"
END = "2026-09-20"  # yfinance end is exclusive; current sample ends 9/18.
MONEYNESS = 0.03
MIN_DTE = 1
MAX_DTE = 30
MEANINGFUL_MOVE = 0.0025


def pct(x: float) -> str:
    return "—" if pd.isna(x) else f"{100*x:.3f}%"


def fnum(x: float, digits: int = 3) -> str:
    return "—" if pd.isna(x) else f"{x:.{digits}f}"


def safe_spearman(x: pd.Series, y: pd.Series):
    d = pd.concat([x, y], axis=1).replace([np.inf, -np.inf], np.nan).dropna()
    if len(d) < 5 or d.iloc[:, 0].nunique() < 2 or d.iloc[:, 1].nunique() < 2:
        return (np.nan, np.nan, len(d))
    r, p = stats.spearmanr(d.iloc[:, 0], d.iloc[:, 1])
    return (float(r), float(p), len(d))


def monthly_opex(d: pd.Timestamp) -> pd.Timestamp:
    first = pd.Timestamp(year=d.year, month=d.month, day=1)
    fridays = pd.date_range(first, first + pd.offsets.MonthEnd(0), freq="W-FRI")
    return fridays[2]


def load_prices() -> pd.DataFrame:
    df = yf.download("QQQ", start=START, end=END, auto_adjust=False,
                     progress=False, actions=False, threads=False)
    if df.empty:
        raise RuntimeError("QQQ price download returned no rows")
    if isinstance(df.columns, pd.MultiIndex):
        df.columns = [c[0] for c in df.columns]
    df = df[["Open", "High", "Low", "Close"]].copy()
    df.index = pd.to_datetime(df.index).tz_localize(None).normalize()
    df = df.sort_index()
    df["day_oc"] = df["Close"] / df["Open"] - 1
    df["next_cc"] = df["Close"].shift(-1) / df["Close"] - 1
    df["next_abs_cc"] = df["next_cc"].abs()
    df["next_gap"] = df["Open"].shift(-1) / df["Close"] - 1
    df["next_oc"] = df["Close"].shift(-1) / df["Open"].shift(-1) - 1
    df["next_range"] = (df["High"].shift(-1) - df["Low"].shift(-1)) / df["Close"]
    df["next_date"] = pd.Series(df.index, index=df.index).shift(-1).values
    return df


def snapshot_dates() -> list[pd.Timestamp]:
    dates = []
    if not SRC.exists():
        raise RuntimeError(f"Source path does not exist: {SRC}")
    for month_dir in sorted(SRC.iterdir()):
        if not month_dir.is_dir():
            continue
        for day_dir in sorted(month_dir.iterdir()):
            if not day_dir.is_dir():
                continue
            try:
                d = pd.Timestamp(f"2026-{month_dir.name}-{day_dir.name}")
            except Exception:
                continue
            if list(day_dir.glob("*.csv")):
                dates.append(d)
    return sorted(set(dates))


def load_snapshot(d: pd.Timestamp) -> pd.DataFrame:
    daydir = SRC / f"{d.month:02d}" / f"{d.day:02d}"
    pieces = []
    for fp in sorted(daydir.glob("*.csv")):
        try:
            exp = pd.Timestamp(fp.stem)
        except Exception:
            continue
        dte = (exp - d).days
        if dte < MIN_DTE or dte > MAX_DTE:
            continue
        try:
            x = pd.read_csv(fp, usecols=["contractSymbol", "strike", "volume", "openInterest", "type"])
        except Exception:
            continue
        x["expiration"] = exp
        x["dte"] = dte
        pieces.append(x)
    if not pieces:
        return pd.DataFrame(columns=["contractSymbol", "strike", "volume", "openInterest", "type", "expiration", "dte"])
    x = pd.concat(pieces, ignore_index=True)
    x["strike"] = pd.to_numeric(x["strike"], errors="coerce")
    x["volume"] = pd.to_numeric(x["volume"], errors="coerce")
    x["openInterest"] = pd.to_numeric(x["openInterest"], errors="coerce")
    x["type"] = x["type"].astype(str).str.lower()
    x = x.drop_duplicates("contractSymbol", keep="last")
    return x


def summarize_bucket(cur: pd.DataFrame, prev_oi: pd.Series, spot: float,
                     dte_lo: int, dte_hi: int, prefix: str) -> dict:
    x = cur[(cur["dte"] >= dte_lo) & (cur["dte"] <= dte_hi)].copy()
    x = x[x["strike"].between(spot * (1 - MONEYNESS), spot * (1 + MONEYNESS))]
    x = x.dropna(subset=["openInterest"])
    x["prev_oi"] = x["contractSymbol"].map(prev_oi)
    x = x.dropna(subset=["prev_oi"])
    x["delta_oi"] = x["openInterest"] - x["prev_oi"]
    x["build"] = x["delta_oi"].clip(lower=0)
    x["unwind"] = (-x["delta_oi"]).clip(lower=0)
    x["vol0"] = x["volume"].fillna(0).clip(lower=0)

    out = {f"{prefix}_matched_contracts": int(len(x))}
    for side in ["call", "put"]:
        s = x[x["type"] == side]
        build = float(s["build"].sum())
        unwind = float(s["unwind"].sum())
        vol = float(s["vol0"].sum())
        out[f"{prefix}_{side}_build"] = build
        out[f"{prefix}_{side}_unwind"] = unwind
        out[f"{prefix}_{side}_volume"] = vol
        out[f"{prefix}_{side}_persistence"] = build / vol if vol > 0 else np.nan

    cb = out[f"{prefix}_call_build"]
    pb = out[f"{prefix}_put_build"]
    tv = out[f"{prefix}_call_volume"] + out[f"{prefix}_put_volume"]
    tb = cb + pb
    out[f"{prefix}_total_build"] = tb
    out[f"{prefix}_total_unwind"] = out[f"{prefix}_call_unwind"] + out[f"{prefix}_put_unwind"]
    out[f"{prefix}_total_volume"] = tv
    out[f"{prefix}_total_persistence"] = tb / tv if tv > 0 else np.nan
    out[f"{prefix}_build_imbalance"] = (cb - pb) / tb if tb > 0 else np.nan
    return out


def build_panel(prices: pd.DataFrame) -> tuple[pd.DataFrame, dict]:
    sdates = snapshot_dates()
    cache: dict[pd.Timestamp, pd.DataFrame] = {}
    rows = []
    exclusions = {"no_price": 0, "no_next_price": 0, "missing_prior_snapshot": 0,
                  "nonconsecutive_snapshot": 0, "empty_chain": 0}

    trading_dates = list(prices.index)
    prev_trading = {trading_dates[i]: trading_dates[i-1] for i in range(1, len(trading_dates))}
    sset = set(sdates)

    for d in sdates:
        if d not in prices.index:
            exclusions["no_price"] += 1
            continue
        if pd.isna(prices.loc[d, "next_cc"]):
            exclusions["no_next_price"] += 1
            continue
        ptd = prev_trading.get(d)
        if ptd is None or ptd not in sset:
            exclusions["missing_prior_snapshot"] += 1
            continue
        # This enforces the immediate prior trading-session snapshot rule.
        prevd = ptd
        if prevd not in cache:
            cache[prevd] = load_snapshot(prevd)
        if d not in cache:
            cache[d] = load_snapshot(d)
        prev = cache[prevd]
        cur = cache[d]
        if prev.empty or cur.empty:
            exclusions["empty_chain"] += 1
            continue
        prev_oi = prev.set_index("contractSymbol")["openInterest"]
        spot = float(prices.loc[d, "Close"])

        row = {
            "date": d,
            "prev_snapshot": prevd,
            "next_date": prices.loc[d, "next_date"],
            "qqq_open": float(prices.loc[d, "Open"]),
            "qqq_close": spot,
            "day_oc": float(prices.loc[d, "day_oc"]),
            "meaningful_move": abs(float(prices.loc[d, "day_oc"])) >= MEANINGFUL_MOVE,
            "next_cc": float(prices.loc[d, "next_cc"]),
            "next_abs_cc": float(prices.loc[d, "next_abs_cc"]),
            "next_gap": float(prices.loc[d, "next_gap"]),
            "next_oc": float(prices.loc[d, "next_oc"]),
            "next_range": float(prices.loc[d, "next_range"]),
        }
        row["continued"] = bool(np.sign(row["day_oc"]) == np.sign(row["next_cc"])) if row["meaningful_move"] and row["next_cc"] != 0 else np.nan
        opx = monthly_opex(d)
        row["monthly_opex_week"] = bool((d >= opx - pd.Timedelta(days=4)) and (d <= opx))
        row["quarterly_opex_week"] = bool(row["monthly_opex_week"] and d.month in [3, 6, 9, 12])

        row.update(summarize_bucket(cur, prev_oi, spot, 1, 30, "dte1_30"))
        row.update(summarize_bucket(cur, prev_oi, spot, 1, 7, "dte1_7"))
        row.update(summarize_bucket(cur, prev_oi, spot, 8, 30, "dte8_30"))
        rows.append(row)

    panel = pd.DataFrame(rows).sort_values("date").reset_index(drop=True)
    return panel, exclusions


def describe_split(panel: pd.DataFrame, col: str) -> pd.DataFrame:
    d = panel[[col, "next_abs_cc", "next_range", "next_cc"]].dropna()
    if d.empty:
        return pd.DataFrame()
    med = d[col].median()
    d["bucket"] = np.where(d[col] > med, "ABOVE_MEDIAN", "AT_OR_BELOW_MEDIAN")
    return d.groupby("bucket").agg(
        n=(col, "size"),
        mean_persistence=(col, "mean"),
        avg_abs_next=("next_abs_cc", "mean"),
        avg_range=("next_range", "mean"),
        avg_signed_next=("next_cc", "mean"),
    ).reset_index()


def continuation_table(panel: pd.DataFrame, col: str) -> pd.DataFrame:
    d = panel[panel["meaningful_move"]][[col, "continued", "next_abs_cc", "next_cc", "day_oc"]].dropna()
    if d.empty:
        return pd.DataFrame()
    med = d[col].median()
    d["bucket"] = np.where(d[col] > med, "ABOVE_MEDIAN", "AT_OR_BELOW_MEDIAN")
    return d.groupby("bucket").agg(
        n=(col, "size"),
        mean_persistence=(col, "mean"),
        continuation_rate=("continued", "mean"),
        avg_abs_next=("next_abs_cc", "mean"),
    ).reset_index()


def render_table(df: pd.DataFrame, percent_cols=None, digits=3) -> str:
    if df.empty:
        return "No eligible rows."
    percent_cols = set(percent_cols or [])
    x = df.copy()
    for c in x.columns:
        if c in percent_cols:
            x[c] = x[c].map(lambda v: "—" if pd.isna(v) else f"{100*v:.2f}%")
        elif pd.api.types.is_float_dtype(x[c]):
            x[c] = x[c].map(lambda v: "—" if pd.isna(v) else f"{v:.{digits}f}")
    return x.to_markdown(index=False)


def main():
    prices = load_prices()
    panel, exclusions = build_panel(prices)
    if panel.empty:
        raise RuntimeError("No eligible sequential-snapshot sessions were produced")

    panel.to_csv(OUT_DIR / "qqq_oi_persistence_v1_session_panel.csv", index=False)

    tests = []
    for bucket in ["dte1_30", "dte1_7", "dte8_30"]:
        pers = panel[f"{bucket}_total_persistence"]
        for outcome in ["next_abs_cc", "next_range"]:
            r, p, n = safe_spearman(pers, panel[outcome])
            tests.append({"bucket": bucket, "feature": "total_persistence", "outcome": outcome,
                          "n": n, "spearman_rho": r, "p_value": p})
        r, p, n = safe_spearman(panel[f"{bucket}_build_imbalance"], panel["next_cc"])
        tests.append({"bucket": bucket, "feature": "build_imbalance", "outcome": "next_cc",
                      "n": n, "spearman_rho": r, "p_value": p})
    tests_df = pd.DataFrame(tests)
    tests_df.to_csv(OUT_DIR / "qqq_oi_persistence_v1_tests.csv", index=False)

    full_col = "dte1_30_total_persistence"
    split = describe_split(panel, full_col)
    cont = continuation_table(panel, full_col)

    # Additional robustness: call and put persistence separately vs movement.
    side_tests = []
    for side in ["call", "put"]:
        c = f"dte1_30_{side}_persistence"
        for outcome in ["next_abs_cc", "next_range"]:
            r, p, n = safe_spearman(panel[c], panel[outcome])
            side_tests.append({"side": side, "outcome": outcome, "n": n, "rho": r, "p": p})
    side_df = pd.DataFrame(side_tests)

    # OPEX descriptive cut only.
    opx = panel.dropna(subset=[full_col]).groupby("monthly_opex_week").agg(
        n=(full_col, "size"),
        mean_persistence=(full_col, "mean"),
        avg_abs_next=("next_abs_cc", "mean"),
        avg_range=("next_range", "mean")
    ).reset_index()

    # Basic data-quality diagnostics, deliberately not repaired after seeing outcomes.
    finite = panel[full_col].replace([np.inf, -np.inf], np.nan).dropna()
    ratio_gt1 = int((finite > 1).sum())
    ratio_gt2 = int((finite > 2).sum())
    matched_median = float(panel["dte1_30_matched_contracts"].median())

    h1_abs = tests_df[(tests_df.bucket == "dte1_30") & (tests_df.outcome == "next_abs_cc")].iloc[0]
    h1_rng = tests_df[(tests_df.bucket == "dte1_30") & (tests_df.outcome == "next_range")].iloc[0]
    h2 = tests_df[(tests_df.bucket == "dte1_30") & (tests_df.feature == "build_imbalance")].iloc[0]

    lines = []
    lines.append("# QQQ OI Persistence v1.0 — Frozen Backtest Results")
    lines.append("")
    lines.append(f"Generated: {datetime.utcnow().isoformat(timespec='seconds')}Z")
    lines.append("")
    lines.append("## Frozen sample construction")
    lines.append(f"- Eligible sequential snapshot sessions: **{len(panel)}**")
    lines.append(f"- First eligible T date: **{panel.date.min().date()}**")
    lines.append(f"- Last eligible T date: **{panel.date.max().date()}**")
    lines.append(f"- Median matched 1–30DTE near-spot contracts/session: **{matched_median:.0f}**")
    lines.append(f"- Current-moneyness window: **±{MONEYNESS*100:.1f}%** of QQQ Day-T close")
    lines.append(f"- DTE universe: **{MIN_DTE}–{MAX_DTE} calendar days**")
    lines.append("- Day-T snapshot predicts **T+1 only**; no same-day use of settled OI.")
    lines.append("")
    lines.append("### Exclusions / source coverage")
    for k, v in exclusions.items():
        lines.append(f"- {k}: {v}")
    lines.append(f"- TOTAL_PERSISTENCE > 1.0: {ratio_gt1} sessions; > 2.0: {ratio_gt2}. These were **reported, not clipped** per frozen rule.")
    lines.append("")
    lines.append("## Primary tests")
    lines.append("")
    lines.append("### H1 — Does total OI persistence predict next-session movement magnitude?")
    lines.append(f"- 1–30DTE persistence vs next |close-to-close|: **rho={fnum(h1_abs.spearman_rho)}**, p={fnum(h1_abs.p_value)}, n={int(h1_abs.n)}")
    lines.append(f"- 1–30DTE persistence vs next high-low range: **rho={fnum(h1_rng.spearman_rho)}**, p={fnum(h1_rng.p_value)}, n={int(h1_rng.n)}")
    lines.append("")
    lines.append("All frozen bucket tests:")
    lines.append(render_table(tests_df, digits=4))
    lines.append("")
    lines.append("### Descriptive above/below-median persistence cut")
    lines.append("This median split is **exploratory/readability only**, not a scanner threshold.")
    lines.append(render_table(split, percent_cols=["avg_abs_next", "avg_range", "avg_signed_next"], digits=3))
    lines.append("")
    lines.append("### H2 — Is call-vs-put OI buildup imbalance directionally predictive?")
    lines.append(f"- BUILD_IMBALANCE vs next signed close-to-close return: **rho={fnum(h2.spearman_rho)}**, p={fnum(h2.p_value)}, n={int(h2.n)}")
    lines.append("- Per frozen rules, this is not promoted unless stable; long/short identity remains unobserved.")
    lines.append("")
    lines.append("### H3 — Does persistence improve continuation after price has already moved >=0.25%?")
    lines.append(render_table(cont, percent_cols=["continuation_rate", "avg_abs_next"], digits=3))
    lines.append("")
    lines.append("### Call vs put persistence robustness")
    lines.append(render_table(side_df, digits=4))
    lines.append("")
    lines.append("### Monthly-OPEX-week descriptive cut")
    lines.append(render_table(opx, percent_cols=["avg_abs_next", "avg_range"], digits=3))
    lines.append("")
    lines.append("## Automatic interpretation guardrails")
    lines.append("- A positive/negative call-vs-put buildup imbalance is **not** buyer/seller direction.")
    lines.append("- Persistence is treated as a possible *positioning intensity / stickiness* measure only.")
    lines.append("- No result from this pass adds STRENGTH, RUNWAY, R:R, or creates a trade.")
    lines.append("- If the relationship is weak/unstable across DTE buckets, the feature is rejected or kept research-only.")
    lines.append("")

    # Conservative mechanical verdict; human review can be stricter, never looser without a new frozen test.
    strong_h1 = (pd.notna(h1_abs.spearman_rho) and pd.notna(h1_rng.spearman_rho)
                 and h1_abs.spearman_rho > 0.20 and h1_rng.spearman_rho > 0.20
                 and (h1_abs.p_value < 0.10 or h1_rng.p_value < 0.10))
    if strong_h1:
        verdict = "PROMISING: persistence shows a consistent positive movement-magnitude relationship; requires untouched replication before scanner promotion."
    else:
        verdict = "NOT YET SUPPORTED: persistence does not meet the predeclared conservative movement-magnitude screen; keep research-only."
    lines.append("## Mechanical Pass-2A verdict")
    lines.append(verdict)
    lines.append("")
    lines.append("The mechanical screen is deliberately conservative and is not an optimization target.")

    (OUT_DIR / "qqq_oi_persistence_v1_results.md").write_text("\n".join(lines), encoding="utf-8")
    print("\n".join(lines))


if __name__ == "__main__":
    main()
