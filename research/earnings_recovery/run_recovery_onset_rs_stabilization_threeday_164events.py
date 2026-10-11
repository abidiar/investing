#!/usr/bin/env python3
"""Frozen stock-only two-factor recovery-onset test: original92 vs disjoint holdout72.
RS vs SPY and stabilized lows from signal CLOSE, realized stock risk path after NEXT OPEN.
No historical option trade / NBBO assumptions, and no price data beyond entry signal used for features.
"""
import concurrent.futures, collections, datetime as dt, json, math, pathlib, random, statistics, time, urllib.parse, urllib.request
BASE=pathlib.Path("research/earnings_recovery")
INPUT=BASE/"actionable_bounce_event_price_windows_164_2026-10-10.json"
OUTPUT=BASE/"recovery_onset_rs_stabilization_164events_actual_2026-10-10.json"
PRICE_SNAPSHOT=BASE/"recovery_onset_rs_stabilization_164events_market_price_sources_2026-10-10.json"
START=int(dt.datetime(2023,1,1,tzinfo=dt.timezone.utc).timestamp())
END=int(dt.datetime(2026,10,10,tzinfo=dt.timezone.utc).timestamp())
def price(ticker):
    errs=[]
    for host in ["query1.finance.yahoo.com","query2.finance.yahoo.com"]:
        url=f"https://{host}/v8/finance/chart/{urllib.parse.quote(ticker)}?period1={START}&period2={END}&interval=1d&events=split"
        try:
            req=urllib.request.Request(url,headers={"User-Agent":"Mozilla/5.0 (compatible; HistoricStockRecoveryResearch/1.0)"})
            with urllib.request.urlopen(req,timeout=40) as resp:data=json.loads(resp.read(12000000))
            res=data.get("chart",{}).get("result") or []
            if res:break
        except Exception as e:
            errs.append(str(e)[:130]);time.sleep(.5)
    else:return {"status":"SOURCE_UNAVAILABLE","errors":errs,"ticker":ticker,"bars":[]}
    dat=res[0]
    splits=[]
    for s in (dat.get("events",{}).get("splits",{}) or {}).values():
        try:
            frac=float(s.get("numerator"))/float(s.get("denominator"))
            if frac<=0:continue
            when=s.get("date")
            day=dt.datetime.fromtimestamp(when,dt.timezone.utc).date().isoformat() if isinstance(when,(int,float)) else str(when)[:10]
            splits.append({"day":day,"ratio":frac})
        except (ValueError,TypeError,ZeroDivisionError):continue
    timestamps=dat.get("timestamp",[])
    q=(dat.get("indicators",{}).get("quote") or [{}])[0]
    bars=[]
    for i,ts in enumerate(timestamps):
        try:
            vals=[float(q[key][i]) for key in ("open","high","low","close")]
            if not all(math.isfinite(x) and x>0 for x in vals):continue
        except Exception:continue
        day=dt.datetime.fromtimestamp(ts,dt.timezone.utc).date().isoformat()
        factor=math.prod(s["ratio"] for s in splits if s["day"]>day)
        bars.append([day]+[round(factor*x,6) for x in vals])
    return {"status":"OK","ticker":ticker,"bars":bars,"splits":splits,"source":"Yahoo quote OHLC unadjusted for dividends, reverse post-date split ratio"}
def first_price_repair(b,event_day):
    ix=next((i for i,x in enumerate(b) if x[0]==event_day),None)
    if ix is None:return {"status":"MISSING_EVENT_BAR"}
    for k in range(ix+5,min(ix+20,len(b)-2)+1):
        c=b[k][4];sma=sum(x[4] for x in b[k-4:k+1])/5
        pc=b[k-1][4];psma=sum(x[4] for x in b[k-5:k])/5
        if c>sma and pc<=psma and c>b[k-1][2]:
            entrybar=b[k+1]
            if entrybar[1] > b[ix][4]*1.08:
                return {"status":"SKIP_CHASE","signal_date":b[k][0],"entry_date":entrybar[0],
                        "chase_open_pct":round(100*(entrybar[1]/b[ix][4]-1),4)}
            return {"status":"READY","event_idx":ix,"signal_idx":k,"entry_idx":k+1,
                    "signal_date":b[k][0],"entry_date":entrybar[0],"signal_lag":k-ix,
                    "signal_close":round(c,6),"entry_open":entrybar[1]}
    return {"status":"NO_REPAIR_SIGNAL"}
def day_three(b,event_day):
    ix=next((i for i,x in enumerate(b) if x[0]==event_day),None)
    if ix is None:return {"status":"MISSING_EVENT_BAR"}
    if ix+3>=len(b):return {"status":"MISSING_ENTRY_BAR"}
    return {"status":"READY","entry_idx":ix+3,"entry_date":b[ix+3][0],"entry_open":b[ix+3][1]}
def barriers(b,i,splits):
    e=b[i][1];profit=e*1.015;stop=e*.99
    bars=b[i:min(i+3,len(b))]
    if len(bars)<3:return {"status":"RIGHT_CENSORED"}
    if any(b[i][0]<s["day"]<=bars[-1][0] for s in splits):
        return {"status":"SPLIT_DURING_TRADE"}
    for j,bar in enumerate(bars):
        day,o,h,l,c=bar;which=None;px=None
        if j>0 and o<=stop:which="STOP_GAP";px=o
        elif j>0 and o>=profit:which="TARGET_GAP";px=o
        elif l<=stop:which="STOP";px=stop
        elif h>=profit:which="TARGET";px=profit
        if which is not None:
            return {"status":"RESOLVED","result":which,"win":which.startswith("TARGET"),"entry":bars[0][0],
                    "exit":day,"sessions":j+1,"entry_price":e,"exit_price":round(px,6),
                    "gross_ret_pct":round(100*(px/e-1),4)}
    return {"status":"RESOLVED","result":"TIME","win":False,"entry":bars[0][0],"exit":bars[-1][0],
            "sessions":3,"entry_price":e,"exit_price":bars[-1][4],
            "gross_ret_pct":round(100*(bars[-1][4]/e-1),4)}
def grouped(rows,filterfn):
    eligible=[x for x in rows if x["status"]=="EVENT_OK"]
    selected=[x for x in eligible if filterfn(x)]
    resolved=[x["repair_outcome"] for x in selected if x.get("repair_outcome",{}).get("status")=="RESOLVED"]
    wins=sum(o["win"] for o in resolved)
    signals=len([x for x in eligible if x.get("repair",{}).get("status")=="READY"])
    n=len(eligible)
    return {"eligible_events":n,"entry_signals_total":signals,"filter_entry_count":len(selected),
       "complete_trades":len(resolved),"target_wins":wins,
       "stop_first":sum(o["result"].startswith("STOP") for o in resolved),
       "three_session_timeouts":sum(o["result"]=="TIME" for o in resolved),
       "target_rate_selected_pct":round(100*wins/len(resolved),2) if resolved else None,
       "target_rate_per_ALL_events_pct":round(100*wins/n,2) if n else None,
       "mean_gross_stock_return_selected_pct":round(statistics.mean(o["gross_ret_pct"] for o in resolved),4) if resolved else None,
       "mean_gross_stock_return_per_ALL_events_skip0_pct":round(sum(o["gross_ret_pct"] for o in resolved)/n,4) if n else None,
       "distinct_signal_tickers":len(set(x["ticker"] for x in selected))}
def cluster_ci(eligible, predicate, B=1800):
    """Ticker-level bootstrap probability difference for conditional target wins. Not option profits."""
    groups={}
    for x in eligible:groups.setdefault(x["ticker"],[]).append(x)
    tickers=sorted(groups);rng=random.Random(20261010)
    diffs=[]
    for _ in range(B):
        sample=[v for t in (rng.choice(tickers) for _ in tickers) for v in groups[t]]
        b=[z for z in sample if z.get("repair",{}).get("status")=="READY" and z.get("repair_outcome",{}).get("status")=="RESOLVED"]
        chosen=[z for z in b if predicate(z)]
        if len(chosen)<5 or len(b)<5:continue
        diffs.append(100*(sum(z["repair_outcome"]["win"] for z in chosen)/len(chosen)-
                          sum(z["repair_outcome"]["win"] for z in b)/len(b)))
    if len(diffs)<200:return None
    diffs.sort()
    return [round(diffs[int(.025*len(diffs))],2),round(diffs[int(.975*len(diffs))],2)]
def main():
    frozen=json.loads(INPUT.read_text())["series"]
    tickers=sorted({e["ticker"] for e in frozen}|{"SPY"})
    historical={}
    with concurrent.futures.ThreadPoolExecutor(max_workers=4) as pool:
        futures={pool.submit(price,t):t for t in tickers}
        for n,f in enumerate(concurrent.futures.as_completed(futures),1):
            t=futures[f]
            try:historical[t]=f.result()
            except Exception as ex:historical[t]={"ticker":t,"status":"ERROR","errors":[str(ex)[:150]],"bars":[]}
            if n%10==0:print("HISTORICAL_PRICE_FETCH",n,len(tickers),flush=True)
    print("STOCK_SOURCES",collections.Counter(v["status"] for v in historical.values()),flush=True)
    spymap={x[0]:x for x in historical["SPY"].get("bars",[])}
    results=[]
    for e in frozen:
        t=e["ticker"];raw=historical[t];row={"ticker":t,"cohort":e["cohort"],"earnings_selloff_day":e["date"],
                                              "pre_existing_selloff_size_pct":e.get("drop"),"price_status":raw["status"]}
        if raw["status"]!="OK" or not spymap:
            row["status"]="MISSING_MARKET_SOURCE";results.append(row);continue
        bars=raw["bars"];repair=first_price_repair(bars,e["date"]);day3=day_three(bars,e["date"])
        row["repair"]=repair;row["day3"]=day3
        row["status"]="EVENT_OK" if repair["status"] not in ("MISSING_EVENT_BAR",) and day3["status"]=="READY" else "MISSING_EVENT_BAR"
        if day3["status"]=="READY":row["day3_outcome"]=barriers(bars,day3["entry_idx"],raw.get("splits",[]))
        if repair["status"]=="READY":
            k=repair["signal_idx"];spy0=spymap.get(bars[k-3][0]);spy1=spymap.get(bars[k][0])
            if not spy0 or not spy1:
                row["status"]="MISSING_SPY_COMPARATOR"
            else:
                rs=100*((bars[k][4]/bars[k-3][4]-1)-(spy1[4]/spy0[4]-1))
                stabilized=bars[k-2][3]<=bars[k-1][3]<=bars[k][3]
                row["factors"]={"three_day_relative_strength_vs_SPY_pct_points":round(rs,4),
                                "relative_strength_at_least_plus_1pp":rs>=1.0,
                                "three_non_decreasing_session_lows":stabilized,
                                "both_filters":rs>=1.0 and stabilized,
                                "last_3_stock_close_return_pct":round(100*(bars[k][4]/bars[k-3][4]-1),4),
                                "last_3_spy_close_return_pct":round(100*(spy1[4]/spy0[4]-1),4),
                                "signal_lag_sessions":repair["signal_lag"],
                                "remaining_pct_to_pre_event_close":round(100*(bars[repair["event_idx"]-1][4]/bars[k][4]-1),4)}
                row["repair_outcome"]=barriers(bars,repair["entry_idx"],raw.get("splits",[]))
        results.append(row)
    summary={}
    for cohort in ["original92","holdout72","all164"]:
        rr=[x for x in results if x["cohort"]==cohort] if cohort!="all164" else results
        good=[x for x in rr if x["status"]=="EVENT_OK"]
        full=[x for x in good if x.get("repair",{}).get("status")=="READY"]
        status_counts=dict(collections.Counter(x["repair"]["status"] for x in good))
        screens={
            "first_sma5_price_repair":lambda x:x.get("repair",{}).get("status")=="READY",
            "repair_AND_relstrength_1pp":lambda x:x.get("repair",{}).get("status")=="READY" and x.get("factors",{}).get("relative_strength_at_least_plus_1pp") is True,
            "repair_AND_stabilized_lows":lambda x:x.get("repair",{}).get("status")=="READY" and x.get("factors",{}).get("three_non_decreasing_session_lows") is True,
            "repair_AND_both":lambda x:x.get("repair",{}).get("status")=="READY" and x.get("factors",{}).get("both_filters") is True}
        st={name:grouped(good,fn) for name,fn in screens.items()}
        baseline=[x["day3_outcome"] for x in good if x.get("day3_outcome",{}).get("status")=="RESOLVED"]
        paired=[x for x in full if x.get("day3_outcome",{}).get("status")=="RESOLVED" and x.get("repair_outcome",{}).get("status")=="RESOLVED"]
        deltas=[x["repair_outcome"]["gross_ret_pct"]-x["day3_outcome"]["gross_ret_pct"] for x in paired]
        summary[cohort]={
            "n_cases":len(rr),"n_valid_market":len(good),"repair_event_states":status_counts,
            "screens":st,
            "day3_same_1p5_minus1_three_session":{"trades":len(baseline),"target_wins":sum(x["win"] for x in baseline),
                "win_pct":round(100*sum(x["win"] for x in baseline)/len(baseline),2) if baseline else None,
                "mean_ret_pct":round(statistics.mean(x["gross_ret_pct"] for x in baseline),4) if baseline else None},
            "paired_repair_vs_day3":{"n":len(paired),"mean_diff_repair_minus_day3_pct_points":round(statistics.mean(deltas),4) if deltas else None},
            "cluster_CI_rel_strength_selected_win_rate_advantage_pp":cluster_ci(good,screens["repair_AND_relstrength_1pp"]),
            "cluster_CI_both_filters_selected_win_rate_advantage_pp":cluster_ci(good,screens["repair_AND_both"])}
    s=summary["holdout72"]["screens"]
    a=s["first_sma5_price_repair"];combo=s["repair_AND_both"]
    gates={"holdout_combination_at_least_20_entries":combo["filter_entry_count"]>=20,
           "holdout_combination_win_rate_at_least_plus10pp":combo["target_rate_selected_pct"] is not None and a["target_rate_selected_pct"] is not None and combo["target_rate_selected_pct"]>=a["target_rate_selected_pct"]+10,
           "holdout_combination_no_loss_in_absolute_event_successes":combo["target_wins"]>=a["target_wins"]}
    payload={"protocol":"frozen_recovery_onset_rs_stabilization_threeday_protocol_2026-10-10.md",
             "data_last_session":"2026-10-09","cohort_preexisting_outcome_exposure":True,
             "barrier_stock_target_plus_pct":1.5,"barrier_stock_stop_minus_pct":1.0,"max_entry_inclusive_sessions":3,
             "source_status":dict(collections.Counter(v["status"] for v in historical.values())),
             "important":"As-of preceding signal close daily STOCK proxy, not contemporaneous option bid/ask or META-style 0DTE execution; tested known-at-entry first signal and all skipped events.",
             "summary":summary,"gate_checks_holdout":gates,"all_holdout_gate_checks_pass":all(gates.values()),"events":results}
    OUTPUT.write_text(json.dumps(payload,indent=2)+"\n")
    PRICE_SNAPSHOT.write_text(json.dumps({"sources":historical},separators=(",",":"))+"\n")
    print("SUMMARY",json.dumps({k:v for k,v in payload.items() if k not in ("events",)},indent=2),flush=True)
if __name__=="__main__":main()
