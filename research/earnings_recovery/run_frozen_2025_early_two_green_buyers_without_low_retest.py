#!/usr/bin/env python3
"""No-retest earliest buyer-initiative historical Jul-Aug 2025, frozen 40 announcement universe.
Prices are connected Webull M5 historical as-traded OHLCV. Not a call premium backtest.
"""
import collections, datetime as dt, json, pathlib, statistics
from zoneinfo import ZoneInfo

BASE=pathlib.Path("research/earnings_recovery")
FROZEN=BASE/"frozen_2025_jul_aug_40_announcements_for_first_buyer_initiative_2026-10-10.json"
OUT=BASE/"first_buyer_initiative_no_retest_2025_40events_results_2026-10-10.json"
WEEKS=("2025-07-07","2025-07-14","2025-07-21","2025-07-28","2025-08-04","2025-08-11","2025-08-18","2025-08-25")
ET=ZoneInfo("America/New_York")
EXPECTED=[(dt.datetime(2025,1,1,9,30)+dt.timedelta(minutes=5*i)).strftime("%H:%M") for i in range(78)]

def sources():
  out={}
  for week in WEEKS:
    file=BASE/f"buyer_initiative_2025_frozen_raw_m5_week{week}_2026-10-10.json"
    d=json.loads(file.read_text())
    for item in d["stocks"]:
      t=item["ticker"]
      assert t not in out,t
      byday=collections.OrderedDict()
      for row in sorted(item["bars"],key=lambda z:z[0]):
        time=dt.datetime.strptime(row[0],"%Y-%m-%dT%H:%M:%S.%f%z").astimezone(ET)
        o,h,l,c,v=map(float,row[1:])
        assert o>0 and l<=min(o,c) and h>=max(o,c) and v>=0
        day=time.date().isoformat()
        byday.setdefault(day,[]).append({"day":day,"clock":time.strftime("%H:%M"),"o":o,"h":h,"l":l,"c":c,"v":v})
      bad={day:{"bar_count":len(rows),"missing_clocks":sorted(set(EXPECTED)-{x["clock"] for x in rows})} for day,rows in byday.items() if [x["clock"] for x in rows]!=EXPECTED}
      out[t]={"byday":byday,"bad_days":bad,"source_week":week}
  return out

def trade(byday,day,index):
  days=list(byday);position=days.index(day)
  future=days[position:position+3]
  if len(future)<3:return {"status":"RIGHT_CENSORED","available_days":len(future)}
  entry=byday[day][index]
  px=entry["o"];stop=px*.99;target=px*1.015
  for j,d in enumerate(future):
    for k,bar in enumerate(byday[d][index if j==0 else 0:]):
      result=None;exit_price=None
      if j>0 and k==0 and bar["o"]<=stop: result="STOP_GAP";exit_price=bar["o"]
      elif j>0 and k==0 and bar["o"]>=target: result="TARGET_GAP";exit_price=bar["o"]
      elif bar["l"]<=stop:result="STOP";exit_price=stop
      elif bar["h"]>=target:result="TARGET";exit_price=target
      if result:
        return {"status":"RESOLVED","result":result,"target_first":result.startswith("TARGET"),
         "entry_day":day,"entry_clock":entry["clock"],"entry_open":px,"exit_day":d,"exit_clock":bar["clock"],
         "exit_price":round(exit_price,6),"gross_pct":round(100*(exit_price/px-1),5),
         "exit_session":j+1}
  bar=byday[future[-1]][-1]
  return {"status":"RESOLVED","result":"TIME","target_first":False,"entry_day":day,"entry_clock":entry["clock"],
    "entry_open":px,"exit_day":future[-1],"exit_clock":bar["clock"],"exit_price":bar["c"],
    "gross_pct":round(100*(bar["c"]/px-1),5),"exit_session":3}

def decide(b,first_i):
  # FIRST complete as-of 5m bar whose low breached -5%. Scan next 8 5m bars.
  for k in range(first_i+2,min(first_i+9,len(b)-1)):
    a,bbar=b[k-1],b[k]
    if not (a["c"]>a["o"] and bbar["c"]>bbar["o"] and bbar["c"]>a["c"] and bbar["l"]>=a["l"] and bbar["c"]>a["h"]):continue
    vol_prior=statistics.median(x["v"] for x in b[k-3:k]) if k>=3 else None
    if vol_prior is None or bbar["v"]<vol_prior:continue
    nextbar=b[k+1]
    low=min(x["l"] for x in b[first_i:k+1])
    cand={"state":"FIRST_GREEN_PAIR","signal_clock":bbar["clock"],"signal_close":bbar["c"],
         "first_green_clock":a["clock"],"second_green_clock":bbar["clock"],"second_bar_volume":bbar["v"],
         "prior3_median_volume":vol_prior,"buyer_relative_vol":round(bbar["v"]/vol_prior,5) if vol_prior else None,
         "known_low":low,"entry_clock":nextbar["clock"],"entry_open":nextbar["o"],
         "entry_from_known_low_pct":round(100*(nextbar["o"]/low-1),5),
         "entry_bar_index":k+1}
    if nextbar["clock"]>"12:20" or nextbar["o"]>low*1.02:return {"state":"LATE_OR_OVEREXTENDED_SKIP","details":cand}
    return {"state":"BUYER_INITIATIVE_ENTRY","details":cand}
  return {"state":"NO_TWO_BAR_BUYER_INITIATIVE"}

def metrics(events,name,denom):
  traded=[x[name] for x in events if x.get(name,{}).get("status")=="RESOLVED"]
  uncertain=[x for x in events if x.get(name,{}).get("status")=="RIGHT_CENSORED"]
  wins=[x for x in traded if x["target_first"]]
  gross=sum(x["gross_pct"] for x in traded)
  return {"denominator":denom,"events":len(events),"trades":len(traded),"wins":len(wins),
    "stop_first":sum(x["result"].startswith("STOP") for x in traded),
    "timeouts":sum(x["result"]=="TIME" for x in traded),
    "right_censored":len(uncertain),
    "wins_per_trade_pct":round(100*len(wins)/len(traded),3) if traded else None,
    "wins_per_event_pct":round(100*len(wins)/len(events),3) if events else None,
    "mean_gross_pct_traded":round(gross/len(traded),4) if traded else None,
    "mean_gross_pct_per_event_skips_zero":round(gross/len(events),4) if events else None,
    "mean_after_20bp_cost_pct_per_event":round((gross-.2*len(traded))/len(events),4) if events else None}

def main():
  roster=json.loads(FROZEN.read_text());assert roster["count"]==40
  market=sources()
  assert sorted(market)==sorted(x["ticker"] for x in roster["events"]),sorted(set(x["ticker"] for x in roster["events"])-set(market))
  rows=[]
  for e in roster["events"]:
    t=e["ticker"];reaction=e["reaction_day"];info=market[t];byday=info["byday"];days=list(byday)
    item={"ticker":t,"earnings_announced":e["earnings_date"],"announcement_session":e["session"],
      "reaction_day":reaction,"source_week":info["source_week"],"missing5m_bar_days":info["bad_days"]}
    if reaction not in byday:
      item["status"]="MISSING_REACTION_DAY";rows.append(item);continue
    prior=[x for x in days if x<reaction]
    if not prior:
      item["status"]="MISSING_PRIOR_COMPLETED_RTH_CLOSE";rows.append(item);continue
    prev=prior[-1];item["prior_day"]=prev
    need=days.index(reaction)
    relevant=days[need:need+3]
    # Reject if a required RTH session has missing bars. A failure cannot be silently treated as full coverage.
    if prev in info["bad_days"] or reaction in info["bad_days"] or any(x in info["bad_days"] for x in relevant):
      item["status"]="INCOMPLETE_REQUIRED_RTH_5M_SESSION";item["required_days"]=relevant;rows.append(item);continue
    if len(relevant)<3:
      item["status"]="RIGHT_CENSORED_BEFORE_3_SESSIONS";rows.append(item);continue
    priorclose=byday[prev][-1]["c"];b=byday[reaction]
    item["as_traded_prior_close"]=priorclose
    item["reaction_day_closing_return_pct"]=round(100*(b[-1]["c"]/priorclose-1),4)
    ceiling=priorclose*.95
    touched=[(i,x) for i,x in enumerate(b) if x["l"]<=ceiling]
    if not touched:
      item["status"]="NO_MINUS_5_INTRADAY_TOUCH";rows.append(item);continue
    i,first=touched[0]
    item["first_touch_time_ET"]=first["clock"];item["first_touch_low"]=first["l"]
    if first["clock"]>"11:30":
      item["status"]="FIRST_MINUS5_TOO_LATE";rows.append(item);continue
    item["status"]="ELIGIBLE_MINUS5_EARLY"
    item["recovered_above_minus5_by_close"]=b[-1]["c"]>ceiling
    item["immediate_baseline"]=trade(byday,reaction,i+1)
    signal=decide(b,i);item["pattern"]=signal
    if signal["state"]=="BUYER_INITIATIVE_ENTRY":
      item["buyer_entry"]=trade(byday,reaction,signal["details"]["entry_bar_index"])
    rows.append(item)
  elig=[x for x in rows if x["status"]=="ELIGIBLE_MINUS5_EARLY"]
  good=[x for x in rows if x["status"] not in ["INCOMPLETE_REQUIRED_RTH_5M_SESSION","MISSING_REACTION_DAY",
          "MISSING_PRIOR_COMPLETED_RTH_CLOSE","RIGHT_CENSORED_BEFORE_3_SESSIONS"]]
  s=metrics(elig,"buyer_entry","asof_intraday_minus5_touch_by1130")
  base=metrics(elig,"immediate_baseline","asof_intraday_minus5_touch_by1130")
  alls=metrics(rows,"buyer_entry","all_40_timestamped_2025_earnings_announcements")
  gates={"at_least_10_buyer_entries":s["trades"]>=10,
        "at_least_plus10pp_wins_per_event_vs_immediate":s["wins_per_event_pct"]>=base["wins_per_event_pct"]+10 if elig else False,
        "at_least_three_more_wins":s["wins"]>=base["wins"]+3,
        "positive_after20bp_cost_across_all40":alls["mean_after_20bp_cost_pct_per_event"]>0}
  report={"design":"frozen_2025_first_buyer_initiative_without_retest_protocol_2026-10-10.md",
     "eligibility":"first finished five-minute LOW -5pct vs pre-earnings prior as-traded RTH close by 11:30 ET",
     "freeze":"2025 July-Aug roster + exact two-green buyer filter committed before Webull full 2025 historical bars",
     "source":"Connected Webull 5-minute RTH raw stock OHLCV; no signed-orderflow or actual option NBBO",
     "roster_n":len(rows),"usable_event_n":len(good),"eligible_early_dislocations":len(elig),
     "event_status_counts":dict(collections.Counter(x["status"] for x in rows)),
     "buyer_pattern_counts":dict(collections.Counter(x.get("pattern",{}).get("state","NO_ELIGIBLE_TOUCH") for x in elig)),
     "qualifying_intraday_breaches_that_recovered_above_minus5_by_close":sum(x["recovered_above_minus5_by_close"] for x in elig),
     "summary":{"first_buyer_no_retest":s,"immediate_minus5_breach":base,"buyer_per_all40_announcements":alls},
     "promotion_gates":gates,"all_gates_pass":all(gates.values()),"events":rows,
     "caveats":["Old historical outcomes on some 2025 issuer events previously inspected in unrelated studies; not prospectively untouched.",
      "Quality filter previously screened for different historical dates; not all 2025 events recertified by point-in-time fundamentals.",
      "All 5-minute candidate bars must be complete, missing vendor candles lead to exclusion from evaluable denominators not losses.",
      "Volume of a green candle is not signed market aggressor order flow.",
      "Stock simulated entry and barrier prices are NOT option quotes, spreads, Greeks, premiums, or historical executable contracts.",
      "Five-minute same candle stop target ambiguity is resolved conservatively stop first; gaps can exceed stock stop."]}
  OUT.write_text(json.dumps(report,indent=2)+"\n")
  print("SUMMARY",json.dumps({k:v for k,v in report.items() if k!="events"},indent=2),flush=True)
  print("PER_EVENT",json.dumps([{"t":r["ticker"],"status":r["status"],"reaction_pct":r.get("reaction_day_closing_return_pct"),
    "first_touch":r.get("first_touch_time_ET"),"pattern":r.get("pattern",{}).get("state"),
    "entry":r.get("pattern",{}).get("details",{}).get("entry_clock"),
    "buyer_result":r.get("buyer_entry",{}).get("result"),"base":r.get("immediate_baseline",{}).get("result")} for r in rows],indent=2),flush=True)

if __name__=="__main__":main()
