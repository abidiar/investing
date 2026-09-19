#!/usr/bin/env python3
"""Frozen Investing OS experiment: QQQ gap-conditioned gamma continuation v1.0."""
from __future__ import annotations

from pathlib import Path
from datetime import datetime, timezone

import numpy as np
import pandas as pd
from scipy import stats
import yfinance as yf

PANEL_PATH = Path("research/results/qqq_gamma_concentration_v1_session_panel.csv")
OUT = Path("research/results")
OUT.mkdir(parents=True, exist_ok=True)
GAP_MIN = 0.0025
MIN_TRAIN = 60


def safe_spearman(x, y):
    d = pd.concat([pd.Series(x), pd.Series(y)], axis=1).replace([np.inf, -np.inf], np.nan).dropna()
    if len(d) < 5 or d.iloc[:,0].nunique() < 2 or d.iloc[:,1].nunique() < 2:
        return np.nan, np.nan, len(d)
    r,p = stats.spearmanr(d.iloc[:,0], d.iloc[:,1])
    return float(r), float(p), len(d)


def monthly_opex(d: pd.Timestamp) -> pd.Timestamp:
    first = pd.Timestamp(year=d.year, month=d.month, day=1)
    fridays = pd.date_range(first, first + pd.offsets.MonthEnd(0), freq="W-FRI")
    return fridays[2]


def load_daily():
    d = yf.download("QQQ", start="2026-01-01", end="2026-09-20", auto_adjust=False,
                    progress=False, actions=False, threads=False)
    if d.empty:
        raise RuntimeError("QQQ daily download returned no rows")
    if isinstance(d.columns, pd.MultiIndex):
        d.columns = [c[0] for c in d.columns]
    d = d[["Open","High","Low","Close"]].copy()
    d.index = pd.to_datetime(d.index).tz_localize(None).normalize()
    d["prev_close"] = d["Close"].shift(1)
    d["gap"] = d["Open"] / d["prev_close"] - 1
    d["abs_gap"] = d["gap"].abs()
    return d


def build_panel():
    g = pd.read_csv(PANEL_PATH, parse_dates=["date","next_date"])
    d = load_daily()
    rows = []
    for _, r in g.iterrows():
        nd = pd.Timestamp(r["next_date"]).normalize()
        if nd not in d.index:
            continue
        q = d.loc[nd]
        gap = float(q["gap"])
        if not np.isfinite(gap) or abs(gap) < GAP_MIN or gap == 0:
            continue
        sign = 1.0 if gap > 0 else -1.0
        o,h,l,c,pc = map(float, [q["Open"],q["High"],q["Low"],q["Close"],q["prev_close"]])
        follow = sign * (c/o - 1)
        if sign > 0:
            mfe = max(h/o - 1, 0.0)
            mae = max(o/l - 1, 0.0)
            gap_fill = float(l <= pc)
        else:
            mfe = max(o/l - 1, 0.0)
            mae = max(h/o - 1, 0.0)
            gap_fill = float(h >= pc)
        eff = mfe/(mfe+mae) if (mfe+mae) > 0 else np.nan
        retention = sign * (c/pc - 1)
        dt = pd.Timestamp(r["date"])
        opx = monthly_opex(dt)
        monthly_week = bool((dt >= opx-pd.Timedelta(days=4)) and (dt <= opx))
        rows.append({
            "date":dt, "next_date":nd,
            "gap":gap,"abs_gap":abs(gap),"gap_sign":sign,
            "gap_followthrough":follow,
            "gap_direction_success":float(follow>0),
            "mfe_from_open":mfe,"mae_from_open":mae,
            "excursion_efficiency":eff,"gap_fill":gap_fill,
            "gap_retention_close":retention,
            "day_abs_oc":float(r["day_abs_oc"]),
            "day_range":float(r["day_range"]),"rv5":float(r["rv5"]),
            "near_gamma_share_0_5":float(r["near_gamma_share_0_5"]),
            "front_near_gamma_share":float(r["front_near_gamma_share"]),
            "weighted_abs_distance":float(r["weighted_abs_distance"]),
            "monthly_opex_week":monthly_week,
            "quarterly_opex_week":bool(monthly_week and dt.month in [3,6,9,12]),
        })
    return pd.DataFrame(rows).sort_values("date").reset_index(drop=True)


def correlation_table(panel):
    expected = {
        "near_gamma_share_0_5": {
            "gap_followthrough":1,"excursion_efficiency":1,"mfe_from_open":1,
            "gap_retention_close":1,"mae_from_open":-1,"gap_fill":-1},
        "front_near_gamma_share": {
            "gap_followthrough":1,"excursion_efficiency":1,"mfe_from_open":1,
            "gap_retention_close":1,"mae_from_open":-1,"gap_fill":-1},
        "weighted_abs_distance": {
            "gap_followthrough":-1,"excursion_efficiency":-1,"mfe_from_open":-1,
            "gap_retention_close":-1,"mae_from_open":1,"gap_fill":1},
    }
    halves = {
        "FULL":panel,
        "FIRST_HALF":panel.iloc[:len(panel)//2],
        "SECOND_HALF":panel.iloc[len(panel)//2:],
        "NON_OPEX":panel[~panel["monthly_opex_week"]],
    }
    rows=[]
    for sample, df in halves.items():
        for f, outcomes in expected.items():
            for o, es in outcomes.items():
                rho,p,n = safe_spearman(df[f],df[o])
                rows.append({"sample":sample,"feature":f,"outcome":o,"expected_sign":es,
                             "n":n,"rho":rho,"p_value":p})
    return pd.DataFrame(rows)


def median_split(panel):
    med = panel["near_gamma_share_0_5"].median()
    x=panel.copy()
    x["bucket"]=np.where(x["near_gamma_share_0_5"]>med,"ABOVE_MEDIAN","AT_OR_BELOW_MEDIAN")
    return x.groupby("bucket").agg(
        n=("date","size"),
        mean_near_share=("near_gamma_share_0_5","mean"),
        continuation_rate=("gap_direction_success","mean"),
        avg_followthrough=("gap_followthrough","mean"),
        avg_mfe=("mfe_from_open","mean"),
        avg_mae=("mae_from_open","mean"),
        avg_efficiency=("excursion_efficiency","mean"),
        gap_fill_rate=("gap_fill","mean"),
        avg_retention=("gap_retention_close","mean"),
    ).reset_index()


def walk_forward(panel):
    base_cols=["abs_gap","day_abs_oc","day_range","rv5"]
    ext_cols=base_cols+["near_gamma_share_0_5","front_near_gamma_share","weighted_abs_distance"]
    targets=["gap_followthrough","excursion_efficiency","mae_from_open"]
    preds=[]
    for i in range(MIN_TRAIN,len(panel)):
        train=panel.iloc[:i]
        test=panel.iloc[i:i+1]
        for target in targets:
            for name,cols in [("baseline",base_cols),("extended",ext_cols)]:
                tr=train[cols+[target]].replace([np.inf,-np.inf],np.nan).dropna()
                te=test[cols+[target]].replace([np.inf,-np.inf],np.nan).dropna()
                if len(tr)<MIN_TRAIN or te.empty:
                    continue
                X=tr[cols].to_numpy(float); y=tr[target].to_numpy(float)
                # Standardize using training data only, add intercept, OLS without tuning.
                mu=X.mean(axis=0); sd=X.std(axis=0); sd=np.where(sd==0,1,sd)
                Xs=(X-mu)/sd
                Xa=np.column_stack([np.ones(len(Xs)),Xs])
                beta=np.linalg.lstsq(Xa,y,rcond=None)[0]
                xt=(te[cols].to_numpy(float)-mu)/sd
                pred=float(np.r_[1.0,xt[0]].dot(beta))
                actual=float(te[target].iloc[0])
                preds.append({"date":test["date"].iloc[0],"target":target,"model":name,
                              "pred":pred,"actual":actual,"abs_error":abs(pred-actual)})
    p=pd.DataFrame(preds)
    rows=[]
    for target in targets:
        z=p[p["target"]==target]
        b=z[z["model"]=="baseline"]; e=z[z["model"]=="extended"]
        if b.empty or e.empty:
            continue
        mb=float(b["abs_error"].mean()); me=float(e["abs_error"].mean())
        rows.append({"target":target,"n_test":len(b),"baseline_mae":mb,"extended_mae":me,
                     "mae_improvement_pct":100*(mb-me)/mb if mb>0 else np.nan})
    return p,pd.DataFrame(rows)


def format_pct(v):
    return "—" if pd.isna(v) else f"{100*v:.2f}%"


def main():
    panel=build_panel()
    if len(panel)<80:
        raise RuntimeError(f"Too few qualifying gap sessions: {len(panel)}")
    corr=correlation_table(panel)
    split=median_split(panel)
    preds,wf=walk_forward(panel)

    panel.to_csv(OUT/"qqq_gap_gamma_continuation_v1_session_panel.csv",index=False)
    corr.to_csv(OUT/"qqq_gap_gamma_continuation_v1_correlations.csv",index=False)
    preds.to_csv(OUT/"qqq_gap_gamma_continuation_v1_walkforward_predictions.csv",index=False)
    wf.to_csv(OUT/"qqq_gap_gamma_continuation_v1_walkforward_summary.csv",index=False)

    # Mechanical frozen promotion screen.
    near_features=["near_gamma_share_0_5","front_near_gamma_share"]
    primary_outcomes=["gap_followthrough","excursion_efficiency"]
    stable_candidates=[]
    for f in near_features:
        for o in primary_outcomes:
            sub=corr[(corr.feature==f)&(corr.outcome==o)]
            vals={r["sample"]:r for _,r in sub.iterrows()}
            if all(k in vals for k in ["FULL","FIRST_HALF","SECOND_HALF","NON_OPEX"]):
                if (vals["FULL"]["rho"]>0 and vals["FIRST_HALF"]["rho"]>0 and
                    vals["SECOND_HALF"]["rho"]>0 and vals["NON_OPEX"]["rho"]>0 and
                    vals["FULL"]["p_value"]<0.10):
                    stable_candidates.append((f,o,float(vals["FULL"]["rho"]),float(vals["FULL"]["p_value"])))
    gate1=bool(stable_candidates)

    failure_coherent=False
    for f in near_features:
        for o in ["mae_from_open","gap_fill"]:
            r=corr[(corr["sample"]=="FULL")&(corr.feature==f)&(corr.outcome==o)]
            if not r.empty and float(r.iloc[0]["rho"])<0:
                failure_coherent=True
    gate2=failure_coherent

    wfmap={r.target:r for _,r in wf.iterrows()}
    core_imp=max([float(wfmap[t].mae_improvement_pct) for t in ["gap_followthrough","excursion_efficiency"] if t in wfmap],default=-999)
    mae_imp=float(wfmap["mae_from_open"].mae_improvement_pct) if "mae_from_open" in wfmap else -999
    gate3=core_imp>=2.0 and mae_imp>=-1.0
    gate4=gate1  # gate1 explicitly requires same sign outside OPEX.
    verdict="PROMOTE_CONTEXT_TAG" if all([gate1,gate2,gate3,gate4]) else "RESEARCH-ONLY"

    lines=[]
    lines.append("# QQQ Gap-Conditioned Gamma Continuation v1.0 — Frozen Results\n")
    lines.append(f"Generated: {datetime.now(timezone.utc).isoformat(timespec='seconds')}\n")
    lines.append("## Coverage")
    lines.append(f"- Qualifying abs(gap) >= 0.25% sessions: **{len(panel)}**")
    lines.append(f"- First Day-T: **{panel.date.min().date()}**; last Day-T: **{panel.date.max().date()}**")
    lines.append(f"- Monthly-OPEX-week qualifying sessions: **{int(panel.monthly_opex_week.sum())}**")
    lines.append("- Day-T gamma predicts only Day-T+1; gap direction comes from Day-T+1 open.\n")

    lines.append("## Primary correlations")
    lines.append(corr.to_markdown(index=False,floatfmt=".4f"))

    lines.append("\n## Near-gamma median split — descriptive only")
    s=split.copy()
    for c in ["continuation_rate","avg_followthrough","avg_mfe","avg_mae","avg_efficiency","gap_fill_rate","avg_retention"]:
        s[c]=s[c].map(format_pct)
    lines.append(s.to_markdown(index=False,floatfmt=".4f"))

    lines.append("\n## Walk-forward incremental test")
    w=wf.copy()
    for c in ["baseline_mae","extended_mae"]:
        w[c]=w[c].map(format_pct)
    lines.append(w.to_markdown(index=False,floatfmt=".2f"))

    lines.append("\n## Mechanical promotion screen")
    lines.append(f"- Stable full/half/non-OPEX primary relationship gate: **{'PASS' if gate1 else 'FAIL'}**")
    if stable_candidates:
        for f,o,r,p in stable_candidates:
            lines.append(f"  - {f} -> {o}: rho={r:.4f}, p={p:.4f}")
    lines.append(f"- Failure-control directional-coherence gate: **{'PASS' if gate2 else 'FAIL'}**")
    lines.append(f"- Walk-forward >=2% core MAE and <=1% MAE-adverse degradation gate: **{'PASS' if gate3 else 'FAIL'}**")
    lines.append(f"- Non-OPEX persistence gate: **{'PASS' if gate4 else 'FAIL'}**")
    lines.append(f"- Overall verdict: **{verdict}**")
    lines.append("\nNo result may alter STRENGTH, RUNWAY, R:R or action state unless the frozen promotion standard passes.")

    report="\n".join(lines)
    (OUT/"qqq_gap_gamma_continuation_v1_results.md").write_text(report)
    print(report)

if __name__ == "__main__":
    main()
