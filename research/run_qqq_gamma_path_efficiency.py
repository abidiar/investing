#!/usr/bin/env python3
"""Frozen Investing OS experiment: QQQ gamma path efficiency v1.0.

Rules are frozen in research/qqq_gamma_path_efficiency_v1.md.
Do not change thresholds/features after viewing outcomes.
"""
from __future__ import annotations

from pathlib import Path
from datetime import datetime, timezone
import numpy as np
import pandas as pd
from scipy import stats
import yfinance as yf

PANEL_PATH = Path("research/results/qqq_gamma_concentration_v1_session_panel.csv")
OUT_DIR = Path("research/results")
OUT_DIR.mkdir(parents=True, exist_ok=True)
MEANINGFUL = 0.0025
MIN_TRAIN = 60
BASE = ["day_abs_oc", "day_range", "rv5"]
GAMMA = ["near_gamma_share_0_5", "front_near_gamma_share", "weighted_abs_distance"]


def safe_spearman(x, y):
    d = pd.concat([pd.Series(x), pd.Series(y)], axis=1).replace([np.inf, -np.inf], np.nan).dropna()
    if len(d) < 5 or d.iloc[:, 0].nunique() < 2 or d.iloc[:, 1].nunique() < 2:
        return np.nan, np.nan, len(d)
    r, p = stats.spearmanr(d.iloc[:, 0], d.iloc[:, 1])
    return float(r), float(p), len(d)


def fetch_intraday(interval: str, start: str, end: str) -> pd.DataFrame:
    x = yf.download("QQQ", start=start, end=end, interval=interval, auto_adjust=False,
                    prepost=False, progress=False, actions=False, threads=False)
    if x.empty:
        return x
    if isinstance(x.columns, pd.MultiIndex):
        x.columns = [c[0] for c in x.columns]
    x = x[["Open", "High", "Low", "Close"]].copy()
    idx = pd.to_datetime(x.index)
    if idx.tz is None:
        idx = idx.tz_localize("UTC").tz_convert("America/New_York")
    else:
        idx = idx.tz_convert("America/New_York")
    x.index = idx
    # yfinance regular-session download should already exclude extended hours;
    # enforce RTH boundaries explicitly anyway.
    x = x.between_time("09:30", "15:59")
    x["session_date"] = x.index.tz_localize(None).normalize()
    return x


def session_metrics(x: pd.DataFrame) -> dict | None:
    x = x.sort_index().dropna(subset=["Open", "High", "Low", "Close"])
    if len(x) < 2:
        return None
    o = float(x.iloc[0]["Open"])
    c = float(x.iloc[-1]["Close"])
    hi = float(x["High"].max())
    lo = float(x["Low"].min())
    closes = x["Close"].astype(float).to_numpy()
    first_leg = abs(closes[0] - o)
    gross = first_leg + float(np.abs(np.diff(closes)).sum())
    eff = abs(c - o) / gross if gross > 0 else np.nan
    whip = 1.0 - eff if np.isfinite(eff) else np.nan
    bar_moves = (x["Close"].astype(float) - x["Open"].astype(float)).to_numpy()
    signs = np.sign(bar_moves)
    signs = signs[signs != 0]
    sess_sign = np.sign(c - o)
    persist = np.mean(signs == sess_sign) if len(signs) and sess_sign != 0 else np.nan
    reversals = int(np.sum(signs[1:] != signs[:-1])) if len(signs) >= 2 else 0
    rth_oc = c / o - 1.0
    adverse = np.nan
    adverse_to_net = np.nan
    if abs(rth_oc) >= MEANINGFUL:
        if rth_oc > 0:
            adverse = max(0.0, (o - lo) / o)
        else:
            adverse = max(0.0, (hi - o) / o)
        adverse_to_net = adverse / abs(rth_oc) if abs(rth_oc) > 0 else np.nan
    return {
        "bars": int(len(x)), "rth_open": o, "rth_close": c, "rth_high": hi, "rth_low": lo,
        "rth_oc": rth_oc, "path_efficiency": eff, "whipsaw_ratio": whip,
        "bar_direction_persistence": persist, "reversal_count": reversals,
        "adverse_excursion": adverse, "adverse_to_net": adverse_to_net,
    }


def build_metrics(bars: pd.DataFrame, label: str) -> pd.DataFrame:
    rows = []
    if bars.empty:
        return pd.DataFrame()
    for d, g in bars.groupby("session_date"):
        m = session_metrics(g)
        if m:
            m["next_date"] = pd.Timestamp(d)
            m["resolution"] = label
            rows.append(m)
    return pd.DataFrame(rows)


def correlation_table(d: pd.DataFrame, sample_name: str) -> pd.DataFrame:
    outcomes = ["path_efficiency", "whipsaw_ratio", "bar_direction_persistence", "reversal_count", "adverse_to_net", "gap_aligned_efficiency"]
    expected = {
        "near_gamma_share_0_5": {"path_efficiency":1,"whipsaw_ratio":-1,"bar_direction_persistence":1,"reversal_count":-1,"adverse_to_net":-1,"gap_aligned_efficiency":1},
        "front_near_gamma_share": {"path_efficiency":1,"whipsaw_ratio":-1,"bar_direction_persistence":1,"reversal_count":-1,"adverse_to_net":-1,"gap_aligned_efficiency":1},
        "weighted_abs_distance": {"path_efficiency":-1,"whipsaw_ratio":1,"bar_direction_persistence":-1,"reversal_count":1,"adverse_to_net":1,"gap_aligned_efficiency":-1},
    }
    rows = []
    for feat in GAMMA:
        for out in outcomes:
            r,p,n = safe_spearman(d[feat], d[out])
            rows.append({"sample":sample_name,"feature":feat,"outcome":out,"expected_sign":expected[feat][out],"n":n,"rho":r,"p_value":p})
    return pd.DataFrame(rows)


def median_split(d: pd.DataFrame, resolution: str) -> pd.DataFrame:
    x = d.dropna(subset=["near_gamma_share_0_5"]).copy()
    if x.empty: return pd.DataFrame()
    med = x["near_gamma_share_0_5"].median()
    x["bucket"] = np.where(x["near_gamma_share_0_5"] > med, "ABOVE_MEDIAN", "AT_OR_BELOW_MEDIAN")
    return x.groupby("bucket").agg(
        n=("near_gamma_share_0_5","size"),
        mean_near_share=("near_gamma_share_0_5","mean"),
        mean_efficiency=("path_efficiency","mean"),
        mean_whipsaw=("whipsaw_ratio","mean"),
        mean_bar_persistence=("bar_direction_persistence","mean"),
        mean_reversals=("reversal_count","mean"),
        mean_adverse_to_net=("adverse_to_net","mean"),
    ).reset_index().assign(resolution=resolution)


def fit_predict(train: pd.DataFrame, test: pd.Series, features: list[str], target: str):
    tr = train[features + [target]].replace([np.inf,-np.inf],np.nan).dropna()
    if len(tr) < MIN_TRAIN or test[features].isna().any(): return np.nan
    X = np.column_stack([np.ones(len(tr)), tr[features].to_numpy(float)])
    y = tr[target].to_numpy(float)
    beta, *_ = np.linalg.lstsq(X, y, rcond=None)
    xt = np.r_[1.0, test[features].to_numpy(float)]
    return float(xt @ beta)


def walk_forward(d: pd.DataFrame) -> tuple[pd.DataFrame,pd.DataFrame]:
    x = d.sort_values("next_date").reset_index(drop=True).copy()
    preds=[]
    for i in range(MIN_TRAIN, len(x)):
        train=x.iloc[:i]
        row=x.iloc[i]
        for target in ["path_efficiency","whipsaw_ratio"]:
            b=fit_predict(train,row,BASE,target)
            e=fit_predict(train,row,BASE+GAMMA,target)
            preds.append({"next_date":row["next_date"],"target":target,"actual":row[target],"baseline_pred":b,"extended_pred":e})
    p=pd.DataFrame(preds).dropna()
    rows=[]
    for target,g in p.groupby("target"):
        bmae=float(np.mean(np.abs(g.actual-g.baseline_pred)))
        emae=float(np.mean(np.abs(g.actual-g.extended_pred)))
        rows.append({"target":target,"n_test":len(g),"baseline_mae":bmae,"extended_mae":emae,"mae_improvement_pct":100*(bmae-emae)/bmae if bmae>0 else np.nan})
    return p,pd.DataFrame(rows)


def fmt_pct(v):
    return "—" if pd.isna(v) else f"{100*v:.2f}%"


def main():
    panel=pd.read_csv(PANEL_PATH, parse_dates=["date","next_date"])
    start=panel["next_date"].min().strftime("%Y-%m-%d")
    end=(panel["next_date"].max()+pd.Timedelta(days=2)).strftime("%Y-%m-%d")
    bars60=fetch_intraday("60m",start,end)
    m60=build_metrics(bars60,"60m")

    recent_start=max(panel["next_date"].min(), panel["next_date"].max()-pd.Timedelta(days=58)).strftime("%Y-%m-%d")
    try:
        bars5=fetch_intraday("5m",recent_start,end)
        m5=build_metrics(bars5,"5m")
    except Exception as exc:
        print(f"5m download unavailable: {exc}")
        m5=pd.DataFrame()

    def merge(m):
        if m.empty: return pd.DataFrame()
        x=panel.merge(m,on="next_date",how="inner")
        x["gap_aligned_efficiency"]=np.nan
        ok=x["next_gap"].abs()>=MEANINGFUL
        aligned=np.sign(x.loc[ok,"rth_oc"])==np.sign(x.loc[ok,"next_gap"])
        x.loc[ok,"gap_aligned_efficiency"]=np.where(aligned,x.loc[ok,"path_efficiency"],-x.loc[ok,"path_efficiency"])
        return x
    d60=merge(m60); d5=merge(m5)
    if d60.empty: raise RuntimeError("No 60m sessions matched frozen panel")

    # Full + chronological halves for primary coverage.
    mid=len(d60)//2
    tests=[correlation_table(d60,"60M_FULL"), correlation_table(d60.iloc[:mid],"60M_FIRST_HALF"), correlation_table(d60.iloc[mid:],"60M_SECOND_HALF")]
    if not d5.empty: tests.append(correlation_table(d5,"5M_RECENT"))
    tests=pd.concat(tests,ignore_index=True)

    splits=[median_split(d60,"60m")]
    if not d5.empty: splits.append(median_split(d5,"5m"))
    splits=pd.concat(splits,ignore_index=True)

    preds,wf=walk_forward(d60)
    d60.to_csv(OUT_DIR/"qqq_gamma_path_efficiency_v1_60m_panel.csv",index=False)
    if not d5.empty: d5.to_csv(OUT_DIR/"qqq_gamma_path_efficiency_v1_5m_panel.csv",index=False)
    tests.to_csv(OUT_DIR/"qqq_gamma_path_efficiency_v1_tests.csv",index=False)
    splits.to_csv(OUT_DIR/"qqq_gamma_path_efficiency_v1_splits.csv",index=False)
    preds.to_csv(OUT_DIR/"qqq_gamma_path_efficiency_v1_walkforward_predictions.csv",index=False)
    wf.to_csv(OUT_DIR/"qqq_gamma_path_efficiency_v1_walkforward_summary.csv",index=False)

    # Mechanical promotion gates.
    prim=tests[tests.outcome.isin(["path_efficiency","whipsaw_ratio"])]
    stable=[]
    for feat in ["near_gamma_share_0_5","front_near_gamma_share"]:
        for out,sgn in [("path_efficiency",1),("whipsaw_ratio",-1)]:
            sub=prim[(prim.feature==feat)&(prim.outcome==out)].set_index("sample")
            needed=["60M_FULL","60M_FIRST_HALF","60M_SECOND_HALF"]
            if all(k in sub.index for k in needed):
                good=all(np.sign(sub.loc[k,"rho"])==sgn for k in needed) and sub.loc["60M_FULL","p_value"]<0.10
                if good: stable.append((feat,out))
    robust=False
    if not d5.empty and stable:
        for feat,out in stable:
            row=tests[(tests["sample"]=="5M_RECENT")&(tests.feature==feat)&(tests.outcome==out)]
            if not row.empty:
                exp=1 if out=="path_efficiency" else -1
                if np.sign(row.iloc[0].rho)==exp: robust=True
    s60=splits[splits.resolution=="60m"].set_index("bucket")
    effect_gate=False
    if {"ABOVE_MEDIAN","AT_OR_BELOW_MEDIAN"}.issubset(s60.index):
        low_eff=s60.loc["AT_OR_BELOW_MEDIAN","mean_efficiency"]
        high_eff=s60.loc["ABOVE_MEDIAN","mean_efficiency"]
        low_wh=s60.loc["AT_OR_BELOW_MEDIAN","mean_whipsaw"]
        high_wh=s60.loc["ABOVE_MEDIAN","mean_whipsaw"]
        eff_imp=(high_eff-low_eff)/abs(low_eff) if low_eff!=0 else np.nan
        whip_red=(low_wh-high_wh)/abs(low_wh) if low_wh!=0 else np.nan
        effect_gate=bool((pd.notna(eff_imp) and eff_imp>=0.10) or (pd.notna(whip_red) and whip_red>=0.10))
    wfd=wf.set_index("target") if not wf.empty else pd.DataFrame()
    wf_gate=False
    if not wf.empty and {"path_efficiency","whipsaw_ratio"}.issubset(wfd.index):
        a=wfd.loc["path_efficiency","mae_improvement_pct"]
        b=wfd.loc["whipsaw_ratio","mae_improvement_pct"]
        wf_gate=bool(((a>=2 and b>=-1) or (b>=2 and a>=-1)))
    overall=bool(stable and robust and effect_gate and wf_gate)

    lines=[]
    lines += ["# QQQ Gamma Path Efficiency v1.0 — Frozen Results","",f"Generated: {datetime.now(timezone.utc).isoformat(timespec='seconds')}",""]
    lines += ["## Coverage",f"- 60m matched sessions: **{len(d60)}** ({d60.next_date.min().date()} to {d60.next_date.max().date()})",f"- 5m robustness sessions: **{len(d5)}**" if not d5.empty else "- 5m robustness sessions: **0 / unavailable**","- Day-T gamma predicts only Day T+1 RTH path.",""]
    lines += ["## Primary/secondary correlations","",tests.to_markdown(index=False,floatfmt=".4f"),""]
    lines += ["## Near-gamma median split","",splits.to_markdown(index=False,floatfmt=".4f"),""]
    lines += ["## Walk-forward incremental test","",wf.to_markdown(index=False,floatfmt=".4f"),""]
    lines += ["## Mechanical promotion screen",f"- Stable full/half primary relationship gate: **{'PASS' if stable else 'FAIL'}**" + (f" — {stable}" if stable else ""),f"- Same-sign 5m robustness gate: **{'PASS' if robust else 'FAIL'}**",f"- >=10% descriptive effect-size gate: **{'PASS' if effect_gate else 'FAIL'}**",f"- Walk-forward >=2% MAE gate: **{'PASS' if wf_gate else 'FAIL'}**",f"- Overall verdict: **{'PROMOTION-CANDIDATE' if overall else 'RESEARCH-ONLY'}**","","No result has directional authority or permission to alter STRENGTH, RUNWAY, R:R, action state, or overnight carry."]
    report="\n".join(lines)
    (OUT_DIR/"qqq_gamma_path_efficiency_v1_results.md").write_text(report)
    print(report)

if __name__=="__main__":
    main()
