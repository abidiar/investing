#!/usr/bin/env python3
"""Frozen early intraday VWAP-reclaim test on the independent-2026 15-event list.
Webull five-minute data saved directly from connected API with UTC timestamps.
Important: stock-path proxy, not executable options or exact tick-VWAP.
"""
import collections, datetime as dt, json, math, pathlib, statistics
from zoneinfo import ZoneInfo
ROOT=pathlib.Path("research/earnings_recovery")
FROZEN=ROOT/"frozen_jul_sep2026_earnings_selloff_discovery_2026-10-10.json"
PROTOCOL=ROOT/"frozen_2026_intraday_early_rebound_vwap_test_2026-10-10.md"
DAILY=ROOT/"clean_jul_sep2026_stock_recovery_stock_bars_2026-10-10.json"
RESULT=ROOT/"early_2026_frozen_fivemin_vwap_rebound_actual_results_2026-10-10.json"
SOURCES=["jul17","jul21","jul23","jul28","jul29","jul31","aug05","aug13","sep02"]
ET=ZoneInfo("America/New_York")
def load_series():
    data={}
    for group in SOURCES:
        path=ROOT/f"early_reversal_2026_intraday_webull_{group}_2026-10-10.json"
        saved=json.loads(path.read_text())
        for item in saved["stocks"]:
            ticker=item["symbol"]
            assert ticker not in data,("duplicate stock",ticker)
            bars=[]
            for rec in item["bars"]:
                stamp=dt.datetime.strptime(rec[0],"%Y-%m-%dT%H:%M:%S.%f%z").astimezone(ET)
                if not dt.time(9,30)<=stamp.time()<=dt.time(15,55):continue
                o,h,l,c,v=map(float,rec[1:])
                if not (o>0 and h>=max(o,c) and l<=min(o,c) and v>=0):
                    # log as failed rather than impute
                    raise ValueError(f"malformed stock bar {ticker}: {rec}")
                bars.append({"date":stamp.date().isoformat(),"clock":stamp.strftime("%H:%M"),
                             "iso_ET":stamp.isoformat(),"open":o,"high":h,"low":l,"close":c,"volume":v})
            bars.sort(key=lambda x:x["iso_ET"])
            data[ticker]=bars
    return data
def day_groups(bars):
    grouped=collections.OrderedDict()
    for b in bars:grouped.setdefault(b["date"],[]).append(b)
    for day,series in grouped.items():
        cum_numerator=cum_volume=0.
        for x in series:
            typical=(x["high"]+x["low"]+x["close"])/3
            cum_numerator+=typical*x["volume"];cum_volume+=x["volume"]
            x["bar_based_running_vwap"]=cum_numerator/cum_volume if cum_volume>0 else None
        # mandatory exactly 78 RTH bars 09:30,...15:55: no silent sparse sample interpolation
        expected=[(dt.datetime.combine(dt.date(2026,1,1),dt.time(9,30))+dt.timedelta(minutes=5*i)).strftime("%H:%M") for i in range(78)]
        if [x["clock"] for x in series]!=expected:
            raise ValueError(f"Webull five-minute coverage not a full session: {day}, {len(series)}, firstlast {series[0]['clock']}/{series[-1]['clock']}")
    return grouped
def scan(grouped,event):
    dates=list(grouped)
    if event not in grouped:return {"status":"EVENT_DAY_MISSING"}
    start=dates.index(event)+1
    if len(dates)<start+7:return {"status":"TOO_FEW_FOLLOWUP_SESSIONS","sessions_after_event":len(dates)-start}
    # first 5 subsequent complete trading days; allow first qualified 5m close only
    for day in dates[start:start+5]:
        bars=grouped[day]
        for k in range(6,43): # 10:00 through 13:00 ET included: indices 6..42
            x=bars[k]
            prev=[bars[j] for j in [k-3,k-2,k-1]]
            if not all(y["bar_based_running_vwap"] is not None and y["close"]<y["bar_based_running_vwap"] for y in prev):continue
            if x["bar_based_running_vwap"] is None or not x["close"]>x["bar_based_running_vwap"]:continue
            if not x["close"]>bars[k-1]["high"]:continue
            if not bars[k-2]["low"]<=bars[k-1]["low"]<=x["low"]:continue
            trough=min(y["low"] for y in bars[:k+1])
            if not x["close"]<=trough*1.015:continue
            nxt=bars[k+1]
            if not nxt["clock"]<="13:05":raise AssertionError("late entry")
            entry_extension_pct=100*(nxt["open"]/trough-1)
            values={
                "signal_day":day,"signal_closed_bar_ET":x["clock"],"entry_ET":nxt["clock"],
                "session_low_known_by_signal":round(trough,6),
                "signal_close":x["close"],"asof_running_vwap":round(x["bar_based_running_vwap"],6),
                "entry_price":nxt["open"],"entry_distance_above_trough_pct":round(entry_extension_pct,5),
                "signal_close_distance_above_trough_pct":round(100*(x["close"]/trough-1),5),
                "post_selloff_session_number":dates.index(day)-dates.index(event),
                "first_signal_only":True
            }
            if nxt["open"]>trough*1.015:return {"status":"EXTENDED_AFTER_SIGNAL_SKIP",**values}
            return {"status":"SIGNAL",**values}
    return {"status":"NO_EARLY_SIGNAL"}
def trade(grouped,entry_day,entry_clock):
    days=list(grouped)
    if entry_day not in grouped:return {"status":"MISSING_ENTRY_DAY"}
    di=days.index(entry_day);ib=next((i for i,x in enumerate(grouped[entry_day]) if x["clock"]==entry_clock),None)
    if ib is None:return {"status":"MISSING_ENTRY_BAR"}
    entry=grouped[entry_day][ib]["open"]
    target=entry*1.015;stop=entry*.99
    exitdays=days[di:di+3]
    if len(exitdays)<3:return {"status":"RIGHT_CENSORED","entry_price":entry,"available_sessions":len(exitdays)}
    for dpos,day in enumerate(exitdays):
        candles=grouped[day][ib if dpos==0 else 0:]
        for i,b in enumerate(candles):
            which=None;exitprice=None
            if dpos>0 and i==0 and b["open"]<=stop:which="STOP_GAP";exitprice=b["open"]
            elif dpos>0 and i==0 and b["open"]>=target:which="TARGET_GAP";exitprice=b["open"]
            elif b["low"]<=stop:which="STOP";exitprice=stop
            elif b["high"]>=target:which="TARGET";exitprice=target
            if which:
                return {"status":"RESOLVED","result":which,"target_first":which.startswith("TARGET"),"entry_day":entry_day,"entry_time_ET":entry_clock,"entry_price":entry,
                        "exit_day":day,"exit_time_ET":b["clock"],"exit_price":round(exitprice,6),"elapsed_sessions":dpos+1,
                        "gross_return_pct":round(100*(exitprice/entry-1),5)}
    last=grouped[exitdays[-1]][-1]
    return {"status":"RESOLVED","result":"TIME","target_first":False,"entry_day":entry_day,"entry_time_ET":entry_clock,"entry_price":entry,
            "exit_day":last["date"],"exit_time_ET":last["clock"],"exit_price":last["close"],"elapsed_sessions":3,
            "gross_return_pct":round(100*(last["close"]/entry-1),5)}
def summary(rows,method):
    n=len(rows);arr=[x[method] for x in rows if x.get(method,{}).get("status")=="RESOLVED"]
    wins=sum(x["target_first"] for x in arr)
    return {"eligible_events":n,"entries":len(arr),"skips_or_data_unknown":n-len(arr),
            "targets":wins,"stops":sum(x["result"].startswith("STOP") for x in arr),"timeouts":sum(x["result"]=="TIME" for x in arr),
            "success_rate_per_all_events_pct":round(100*wins/n,2) if n else None,
            "success_rate_per_trade_pct":round(100*wins/len(arr),2) if arr else None,
            "gross_mean_per_traded_pct":round(statistics.mean(x["gross_return_pct"] for x in arr),4) if arr else None,
            "gross_mean_per_all_events_skip_zero_pct":round(sum(x["gross_return_pct"] for x in arr)/n,4) if n else None,
            "mean_per_all_events_less_20bps_roundtrip_cost_pct":round((sum(x["gross_return_pct"]-0.2 for x in arr))/n,4) if n else None}
def main():
    assert PROTOCOL.exists()
    frozen=json.loads(FROZEN.read_text())
    events=frozen["selected_events"];assert len(events)==15
    raw=load_series();expected=sorted(set(e["ticker"] for e in events))
    assert sorted(raw)==expected,(sorted(raw),expected)
    daily=json.loads(DAILY.read_text())["source_snapshots"]
    rows=[]
    for e in events:
        t=e["ticker"];event=e["selloff_day"]
        grouped=day_groups(raw[t])
        daybar=grouped.get(event)
        rawdaily=next((b for b in daily[t]["bars"] if b[0]==event),None)
        mark=daybar[-1]["close"] if daybar else None
        discrepancy=100*(mark/rawdaily[4]-1) if (mark is not None and rawdaily is not None) else None
        row={"ticker":t,"selloff_event_close_day":event,"earnings_announcement":e["earnings_announcement"],
             "frozen_close_reaction_pct":e["reaction_close_pct"],"webull_five_min_dayclose":mark,
             "yahoo_unadjusted_daily_dayclose":rawdaily[4] if rawdaily else None,
             "daily_source_close_discrepancy_pct":round(discrepancy,4) if discrepancy is not None else None,
             "daily5m_bars_by_date":{date:len(v) for date,v in grouped.items()}}
        if discrepancy is None or abs(discrepancy)>1.0:
            row["status"]="SOURCE_CLOSE_MISMATCH_OR_MISSING"
            rows.append(row);continue
        candidate=scan(grouped,event)
        row["early_signal"]=candidate
        row["status"]="EVENT_OK"
        if candidate["status"]=="SIGNAL":
            row["early_result"]=trade(grouped,candidate["signal_day"],candidate["entry_ET"])
        dates=list(grouped);ix=dates.index(event)
        for name,offset in [("day1_1000",1),("day3_1000",3)]:
            if ix+offset < len(dates):
                row[name]=trade(grouped,dates[ix+offset],"10:00")
            else:
                row[name]={"status":"MISSING_COMPARATOR_SESSION"}
        rows.append(row)
    valid=[x for x in rows if x["status"]=="EVENT_OK"]
    a=summary(valid,"early_result");b=summary(valid,"day1_1000");c=summary(valid,"day3_1000")
    ext=[x["early_signal"]["entry_distance_above_trough_pct"] for x in valid if x.get("early_signal",{}).get("status")=="SIGNAL"]
    # Note condition #4 applies to entered signals only.
    early_at_most_075=sum(v<=.75 for v in ext)
    gates={"at_least_10_early_entries":a["entries"]>=10,
           "early_win_advantage_at_least_10pp_vs_day1_all_events":a["success_rate_per_all_events_pct"]>=b["success_rate_per_all_events_pct"]+10 if valid else False,
           "early_net_20bps_per_all_events_positive":a["mean_per_all_events_less_20bps_roundtrip_cost_pct"]>0 if valid else False,
           "half_of_entries_within_075pct_of_known_intraday_low":early_at_most_075>=.5*len(ext) if ext else False}
    summary_obj={"protocol":str(PROTOCOL),"source":"Webull historical 5-minute US stock regular-session trade bars, 2026 Jul–Sep; approximate price*volume running VWAP, NOT exact tick-vwap",
                 "source_event_list_frozen_before_5m":True,"event_count":len(events),"valid_event_count":len(valid),
                 "missing_or_mismatched":len(events)-len(valid),"summary":{"early_reversal":a,"day1_1000":b,"day3_1000":c},
                 "early_entries_within_075pct_of_prior_session_low":early_at_most_075,
                 "early_entries_total":len(ext),
                 "earliness_median_distance_pct":round(statistics.median(ext),4) if ext else None,
                 "promotion_gates":gates,"all_gates_pass":all(gates.values()),
                 "limitation":["Only 15 2026 earnings events; no independently 2026-recertain quality; 6 earlier issuer source reaction gaps",
                               "Option contract bid/ask, fill timestamps, premium, IV, delta and theta not measured",
                               "Bar-based VWAP approximation and 5-minute bar same-bar stop-first ambiguity",
                               "Never infer that stock +1.5% gives positive call P&L",
                               "Event-day entry prohibited because source qualifies earnings reaction by that day's 4pm close"],
                 "events":rows}
    RESULT.write_text(json.dumps(summary_obj,indent=2)+"\n")
    print("RESULT",json.dumps({k:v for k,v in summary_obj.items() if k!="events"},indent=2),flush=True)
    print("PER_EVENT",json.dumps([{"ticker":x["ticker"],"status":x["status"],"event":x["selloff_event_close_day"],
             "signal":x.get("early_signal",{}).get("status"),"signal_time":x.get("early_signal",{}).get("signal_closed_bar_ET"),
             "entry":x.get("early_signal",{}).get("entry_day"),"extension_pct":x.get("early_signal",{}).get("entry_distance_above_trough_pct"),
             "reversal":x.get("early_result",{}).get("result"),"rev_pnl":x.get("early_result",{}).get("gross_return_pct"),
             "day1":x.get("day1_1000",{}).get("result"),"day1_pnl":x.get("day1_1000",{}).get("gross_return_pct")} for x in rows],indent=2),flush=True)
if __name__=="__main__":main()
