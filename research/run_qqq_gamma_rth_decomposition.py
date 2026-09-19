#!/usr/bin/env python3
"""Frozen Investing OS experiment: QQQ gamma overnight vs RTH decomposition v1.0.

Rules are frozen in research/qqq_gamma_rth_decomposition_v1.md.
Do not change thresholds/features based on observed outcomes.
"""
from __future__ import annotations

from pathlib import Path
from datetime import datetime, timezone
import numpy as np
import pandas as pd
from scipy import stats

PANEL_PATH = Path("research/results/qqq_gamma_concentration_v1_session_panel.csv")
OUT_DIR = Path("research/results")
OUT_DIR.mkdir(parents=True, exist_ok=True)
MIN_TRAIN = 60
GAP_THRESHOLD = 0.0025

BASE_FEATURES = ["day_abs_oc", "day_range", "rv5"]
EXT_FEATURES = [
    "day_abs_oc", "day_range", "rv5",
    "near_gamma_share_0_5", "front_near_gamma_share", "weighted_abs_distance"
]
PRIMARY_FEATURES = ["near_gamma_share_0_5", "front_near_gamma_share", "weighted_abs_distance"]
TARGETS = ["abs_gap", "abs_rth_oc", "rth_range"]


def safe_spearman(x: pd.Series, y: pd.Series):
    d = pd.concat([x, y], axis=1).replace([np.inf, -np.inf], np.nan).dropna()
    if len(d) < 5 or d.iloc[:, 0].nunique() < 2 or d.iloc[:, 1].nunique() < 2:
        return np.nan, np.nan, len(d)
    r, p = stats.spearmanr(d.iloc[:, 0], d.iloc[:, 1])
    return float(r), float(p), len(d)


def ols_predict(train: pd.DataFrame, row: pd.Series, features: list[str], target: str) -> float:
    x = train[features].astype(float).to_numpy()
    y = train[target].astype(float).to_numpy()
    mu = np.nanmean(x, axis=0)
    sd = np.nanstd(x, axis=0, ddof=0)
    sd = np.where(sd == 0, 1.0, sd)
    xs = (x - mu) / sd
    xr = (row[features].astype(float).to_numpy() - mu) / sd
    X = np.column_stack([np.ones(len(xs)), xs])
    beta, *_ = np.linalg.lstsq(X, y, rcond=None)
    return float(np.r_[1.0, xr] @ beta)


def walk_forward(df: pd.DataFrame, target: str) -> pd.DataFrame:
    needed = list(dict.fromkeys(EXT_FEATURES + [target, "date"]))
    d = df[needed].replace([np.inf, -np.inf], np.nan).dropna().sort_values("date").reset_index(drop=True)
    rows = []
    for i in range(MIN_TRAIN, len(d)):
        train = d.iloc[:i]
        row = d.iloc[i]
        b = ols_predict(train, row, BASE_FEATURES, target)
        e = ols_predict(train, row, EXT_FEATURES, target)
        rows.append({"date": row["date"], "target": target, "actual": float(row[target]),
                     "baseline_pred": b, "extended_pred": e})
    return pd.DataFrame(rows)


def fmt_pct(x):
    return "—" if pd.isna(x) else f"{100*x:.2f}%"


def render_table(df: pd.DataFrame, pct_cols=None, digits=4):
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


def main():
    if not PANEL_PATH.exists():
        raise RuntimeError(f"Missing prerequisite panel: {PANEL_PATH}")
    df = pd.read_csv(PANEL_PATH, parse_dates=["date", "next_date"])
    df = df.sort_values("date").reset_index(drop=True)
    df["abs_gap"] = df["next_gap"].abs()
    df["abs_rth_oc"] = df["next_oc"].abs()
    df["rth_range"] = df["next_range"]
    df["abs_cc"] = df["next_cc"].abs()
    df["gap_followthrough"] = np.where(df["next_gap"] != 0, np.sign(df["next_gap"]) * df["next_oc"], np.nan)

    n = len(df)
    split = n // 2
    samples = {
        "FULL": df,
        "FIRST_HALF": df.iloc[:split],
        "SECOND_HALF": df.iloc[split:],
    }

    corr_rows = []
    for sname, sdf in samples.items():
        for feat in PRIMARY_FEATURES + ["strike_hhi"]:
            for outcome in ["abs_gap", "abs_rth_oc", "rth_range", "abs_cc"]:
                r, p, nn = safe_spearman(sdf[feat], sdf[outcome])
                corr_rows.append({"sample": sname, "feature": feat, "outcome": outcome,
                                  "n": nn, "rho": r, "p_value": p})
    corr = pd.DataFrame(corr_rows)
    corr.to_csv(OUT_DIR / "qqq_gamma_rth_decomposition_v1_correlations.csv", index=False)

    # Frozen differentials from FULL sample.
    full = corr[corr["sample"] == "FULL"].copy()
    diff_rows = []
    for feat in PRIMARY_FEATURES:
        vals = full[full["feature"] == feat].set_index("outcome")["rho"]
        if feat in ["near_gamma_share_0_5", "front_near_gamma_share"]:
            rth_diff = vals.get("abs_gap", np.nan) - vals.get("abs_rth_oc", np.nan)
            range_diff = vals.get("abs_gap", np.nan) - vals.get("rth_range", np.nan)
        else:
            rth_diff = vals.get("abs_rth_oc", np.nan) - vals.get("abs_gap", np.nan)
            range_diff = vals.get("rth_range", np.nan) - vals.get("abs_gap", np.nan)
        diff_rows.append({"feature": feat, "rth_oc_differential": rth_diff, "range_differential": range_diff})
    diffs = pd.DataFrame(diff_rows)
    diffs.to_csv(OUT_DIR / "qqq_gamma_rth_decomposition_v1_differentials.csv", index=False)

    # Secondary gap follow-through test at frozen 0.25% gap threshold.
    gd = df[df["abs_gap"] >= GAP_THRESHOLD].copy()
    gap_rows = []
    for feat in ["near_gamma_share_0_5", "front_near_gamma_share", "weighted_abs_distance"]:
        r, p, nn = safe_spearman(gd[feat], gd["gap_followthrough"])
        gap_rows.append({"feature": feat, "n": nn, "rho_vs_gap_followthrough": r, "p_value": p})
    gap_tests = pd.DataFrame(gap_rows)
    gap_tests.to_csv(OUT_DIR / "qqq_gamma_rth_decomposition_v1_gap_followthrough.csv", index=False)

    # Descriptive median split only.
    med = df["near_gamma_share_0_5"].median()
    ds = df.copy()
    ds["bucket"] = np.where(ds["near_gamma_share_0_5"] > med, "ABOVE_MEDIAN", "AT_OR_BELOW_MEDIAN")
    desc = ds.groupby("bucket").agg(
        n=("near_gamma_share_0_5", "size"),
        mean_near_share=("near_gamma_share_0_5", "mean"),
        avg_abs_gap=("abs_gap", "mean"),
        avg_abs_rth_oc=("abs_rth_oc", "mean"),
        avg_rth_range=("rth_range", "mean"),
        avg_abs_cc=("abs_cc", "mean"),
        avg_gap_followthrough=("gap_followthrough", "mean"),
    ).reset_index()

    # Walk-forward models.
    pred_parts = [walk_forward(df, t) for t in TARGETS]
    preds = pd.concat(pred_parts, ignore_index=True)
    preds.to_csv(OUT_DIR / "qqq_gamma_rth_decomposition_v1_walkforward_predictions.csv", index=False)
    wf_rows = []
    for target, td in preds.groupby("target"):
        b_mae = float(np.mean(np.abs(td["actual"] - td["baseline_pred"])))
        e_mae = float(np.mean(np.abs(td["actual"] - td["extended_pred"])))
        imp = (b_mae - e_mae) / b_mae if b_mae > 0 else np.nan
        br, bp, _ = safe_spearman(td["baseline_pred"], td["actual"])
        er, ep, _ = safe_spearman(td["extended_pred"], td["actual"])
        wf_rows.append({"target": target, "n_test": len(td), "baseline_mae": b_mae,
                        "extended_mae": e_mae, "mae_improvement_pct": imp,
                        "baseline_pred_rho": br, "baseline_pred_p": bp,
                        "extended_pred_rho": er, "extended_pred_p": ep})
    wf = pd.DataFrame(wf_rows)
    wf.to_csv(OUT_DIR / "qqq_gamma_rth_decomposition_v1_walkforward_summary.csv", index=False)

    # Mechanical promotion screen exactly per frozen spec.
    qualifies_assoc = []
    for feat in ["near_gamma_share_0_5", "front_near_gamma_share"]:
        for outcome in ["abs_rth_oc", "rth_range"]:
            sub = corr[(corr["feature"] == feat) & (corr["outcome"] == outcome)].set_index("sample")
            if set(["FULL", "FIRST_HALF", "SECOND_HALF"]).issubset(sub.index):
                signs_ok = all(sub.loc[s, "rho"] < 0 for s in ["FULL", "FIRST_HALF", "SECOND_HALF"])
                p_ok = sub.loc["FULL", "p_value"] < 0.10
                drow = diffs[diffs["feature"] == feat].iloc[0]
                diff = drow["rth_oc_differential"] if outcome == "abs_rth_oc" else drow["range_differential"]
                diff_ok = diff >= 0.10
                if signs_ok and p_ok and diff_ok:
                    qualifies_assoc.append((feat, outcome, float(diff)))

    wfmap = wf.set_index("target")["mae_improvement_pct"].to_dict()
    rth_a = wfmap.get("abs_rth_oc", np.nan)
    rth_b = wfmap.get("rth_range", np.nan)
    gap_i = wfmap.get("abs_gap", np.nan)
    walk_ok = ((rth_a >= 0.02 and rth_b >= -0.01) or (rth_b >= 0.02 and rth_a >= -0.01))
    best_rth = max(rth_a, rth_b) if not (pd.isna(rth_a) or pd.isna(rth_b)) else np.nan
    rth_specific_ok = (best_rth - gap_i) >= 0.01 if not (pd.isna(best_rth) or pd.isna(gap_i)) else False
    promote = bool(qualifies_assoc and walk_ok and rth_specific_ok)

    lines = []
    lines.append("# QQQ Gamma Overnight vs RTH Decomposition v1.0 — Frozen Results")
    lines.append("")
    lines.append(f"Generated: {datetime.now(timezone.utc).isoformat(timespec='seconds')}")
    lines.append("")
    lines.append("## Frozen sample")
    lines.append(f"- Sessions: **{len(df)}**")
    lines.append(f"- First Day-T: **{df['date'].min().date()}**")
    lines.append(f"- Last Day-T: **{df['date'].max().date()}**")
    lines.append("- Reuses the previously frozen gamma-concentration panel; this is a mechanism follow-up, not independent OOS proof.")
    lines.append("")
    lines.append("## Primary correlations")
    lines.append("")
    lines.append(render_table(corr[corr["feature"].isin(PRIMARY_FEATURES)], digits=4))
    lines.append("")
    lines.append("## Frozen RTH-vs-gap differentials")
    lines.append("")
    lines.append(render_table(diffs, digits=4))
    lines.append("")
    lines.append("Positive differential means stronger RTH-specific behavior in the predeclared expected direction.")
    lines.append("")
    lines.append("## Descriptive median split — near-spot gamma share")
    lines.append("")
    lines.append(render_table(desc, pct_cols=["avg_abs_gap", "avg_abs_rth_oc", "avg_rth_range", "avg_abs_cc", "avg_gap_followthrough"]))
    lines.append("")
    lines.append("## Secondary gap-followthrough test (|gap| >= 0.25%)")
    lines.append("")
    lines.append(render_table(gap_tests, digits=4))
    lines.append("")
    lines.append("## Walk-forward incremental test")
    lines.append("")
    wf_show = wf.copy()
    lines.append(render_table(wf_show, pct_cols=["baseline_mae", "extended_mae", "mae_improvement_pct"], digits=4))
    lines.append("")
    lines.append("## Mechanical promotion screen")
    lines.append("")
    lines.append(f"- Stable full/half association + p<0.10 + differential >=0.10: **{'PASS' if qualifies_assoc else 'FAIL'}**")
    if qualifies_assoc:
        for feat, outcome, diff in qualifies_assoc:
            lines.append(f"  - {feat} -> {outcome}, differential={diff:.4f}")
    lines.append(f"- Walk-forward RTH MAE gate: **{'PASS' if walk_ok else 'FAIL'}**")
    lines.append(f"- RTH-specific improvement vs ABS_GAP gate: **{'PASS' if rth_specific_ok else 'FAIL'}**")
    lines.append(f"- Overall v1.0 verdict: **{'PROMOTE CONTEXT TAG ONLY' if promote else 'RESEARCH-ONLY'}**")
    lines.append("")
    lines.append("No result from this pass has directional authority or permission to alter STRENGTH, RUNWAY, R:R, action state, or overnight-carry rules.")

    result_md = "\n".join(lines) + "\n"
    (OUT_DIR / "qqq_gamma_rth_decomposition_v1_results.md").write_text(result_md)
    print(result_md)


if __name__ == "__main__":
    main()
