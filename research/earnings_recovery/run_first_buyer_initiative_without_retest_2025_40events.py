#!/usr/bin/env python3
"""Frozen 40-announcement Jul–Aug 2025 earnings-shock buyer-initiative study.
No future candle used for signal. Unadjusted as-of previous completed RTH M5 close,
five-minute outcome path +1.5 before -1 over 3 entry-inclusive market sessions.
"""
import collections,datetime as dt,json,pathlib,statistics
from zoneinfo import ZoneInfo
R=pathlib.Path("research/earnings_recovery")
EVENTS=R/"frozen_2025_jul_aug_40_announcements_for_first_buyer_initiative_2026-10-10.json"
OUTPUT=R/"early_buyer_initiative_no_retest_2025_40events_actual_2026-10-10.json"
ET=ZoneInfo("America/New_York")
WEEKS=["2025-07-07","2025-07-14","2025-07-21","2025-07-28","2025-08-04","2025-08-11","2025-08-18","2025-08-25"]
EXPECTED=[(dt.datetime(2025,7,1,9,30)+dt.timedelta(minutes=5*k)).strftime("%H:%M") for k in range(78)]
def load():
 result={}
 for w in WEEKS:
  p=R/f"buyer_initiative_2025_frozen_raw_m5_week{w}_2026-10-10.json"
  if not p.exists():
   assert w=="2025-07-14"
   p=R/"buyer_initiative_2025_frozen_raw_m5_week2025-07-14_2026-10-10.json"
  d=json.loads(p.read_text())
  for item in d["stocks"]:
   t=item["ticker"];assert t not in result,t
   bars=[]
   for ar in item["bars"]:
    ts=dt.datetime.strptime(ar[0],"%Y-%m-%dT%H:%M:%S.%f%z").astimezone(ET)
    o,h,l,c,v=map(float,ar[1:])
    if o<=0 or h<max(o,c) or l>min(o,c) or v<0:
     raise ValueError(f"Invalid quote {t} {ar}")
    bars.append({"day":ts.strftime("%Y-%m-%d"),"clock":ts.strftime("%H:%M"),"et":ts.isoformat(),
                  "o":o,"h":h,"l":l,"c":c,"v":v})
   bars.sort(key=lambda x:x["et"])
   dct=collections.OrderedDict()
   for b in bars:dct.setdefault(b["day"],[]).append(b)
   invalid={day:len(bb) for day,bb in dct.items() if [b["clock"] for b in bb]!=EXPECTED}
   result[t]={"provider":d["source"],"days":dct,"invalid_days":invalid,"total_m5_bars":len(bars)}
 return result
def barrier(grouped,day,index):
 dates=list(grouped);offset=dates.index(day);en=grouped[day][index]["o"];target=en*1.015;stop=en*.99
 if offset+2>=len(dates):return {"status":"RIGHT_CENSORED"}
 for dd in dates[offset:offset+3]:
  if [b["clock"] for b in grouped[dd]]!=EXPECTED:
   return {"status":"MISSING_INTRADAY_EXIT_BARS","missing_day":dd}
 for j,dd in enumerate(dates[offset:offset+3]):
  bars=grouped[dd][index if j==0 else 0:]
  for i,b in enumerate(bars):
   label=None;out=None
   if j>0 and i==0 and b["o"]<=stop:label="STOP_GAP";out=b["o"]
   elif j>0 and i==0 and b["o"]>=target:label="TARGET_GAP";out=b["o"]
   elif b["l"]<=stop:label="STOP";out=stop
   elif b["h"]>=target:label="TARGET";out=target
   if label:return {"status":"RESOLVED","exit_type":label,"target_first":label.startswith("TARGET"),
                   "entry_day":day,"entry_clock":grouped[day][index]["clock"],"entry_open":en,
                   "exit_day":dd,"exit_clock":b["clock"],"exit_price":round(out,6),
                   "gross_return_pct":round(100*(out/en-1),5),"hold_days":j+1}
 last=grouped[dates[offset+2]][-1]
 return {"status":"RESOLVED","exit_type":"TIME","target_first":False,"entry_day":day,
    "entry_clock":grouped[day][index]["clock"],"entry_open":en,
    "exit_day":last["day"],"exit_clock":last["clock"],"exit_price":last["c"],
    "gross_return_pct":round(100*(last["c"]/en-1),5),"hold_days":3}
def rule(bar,i):
 if i+1>=78:return {"state":"FIRST_SHOCK_TOO_LATE_TO_BUY"}
 for k in range(i+2,min(i+9,77)):
  a=bar[k-1];b=bar[k]
  if a["c"]<=a["o"] or b["c"]<=b["o"]:continue
  if b["c"]<=a["c"] or b["l"]<a["l"] or b["c"]<=a["h"]:continue
  volumes=[bar[j]["v"] for j in range(k-3,k)]
  if len(volumes)!=3 or b["v"]<statistics.median(volumes):continue
  trough=min(x["l"] for x in bar[i:k+1])
  nxt=bar[k+1]
  desc={"first_shock_bar_index":i,"a_clock_ET":a["clock"],"b_clock_ET":b["clock"],
    "first_breakout_bar_volume":b["v"],"previous_three_bar_median_volume":statistics.median(volumes),
    "relative_buyer_bar_volume_to_recent_median":round(b["v"]/statistics.median(volumes),4) if statistics.median(volumes)>0 else None,
    "signal_close":b["c"],"observed_low_since_shock":trough,
    "entry_clock_ET":nxt["clock"],"entry_open":nxt["o"],
    "distance_above_observed_low_pct":round(100*(nxt["o"]/trough-1),5),"breakout_bar_index":k}
  if nxt["clock"]>"12:20" or nxt["o"]>trough*1.02:return {"state":"EXTENDED_OR_LATE_FIRST_SIGNAL","signal":desc}
  return {"state":"BUYER_INITIATIVE_ENTRY","signal":desc}
 return {"state":"NO_EARLY_TWO_CANDLE_BUYER_SIGNAL"}
def calc(rows,method,norm):
 valid=[x for x in rows if x.get("breach",{}).get("state")=="EARLY_5PCT_SHOCK"]
 trades=[x[method] for x in valid if x.get(method,{}).get("status")=="RESOLVED"]
 unresolved=[x for x in valid if x.get(method,{}).get("status") not in ("RESOLVED",None)]
 n=len(valid) if norm=="qualified_intraday_dislocation" else len(rows)
 wins=sum(x["target_first"] for x in trades)
 total=sum(x["gross_return_pct"] for x in trades)
 return {"denominator":n,"entries":len(trades),"target_first":wins,
  "stop_first":sum(x["exit_type"].startswith("STOP") for x in trades),
  "timeouts":sum(x["exit_type"]=="TIME" for x in trades),
  "unresolved_trade_paths":len(unresolved),
  "target_rate_pct_among_entries":round(100*wins/len(trades),3) if trades else None,
  "target_rate_pct_per_all_denominator_events":round(100*wins/n,3) if n else None,
  "mean_gross_pct_among_entries":round(total/len(trades),4) if trades else None,
  "mean_gross_pct_per_all_denominator_events_with_skips0":round(total/n,4) if n else None,
  "mean_net_sensitivity_minus20bps_trade_per_all_events_pct":round((total-.2*len(trades))/n,4) if n else None}
def main():
 events=json.loads(EVENTS.read_text())["events"]
 assert len(events)==40
 sources=load()
 data=[]
 for e in events:
  t=e["ticker"];reaction=e["reaction_day"];row={"ticker":t,"announcement":e["earnings_date"],"session":e["session"],
   "reaction_day":reaction,"source_ref":e["source"]}
  if t not in sources:
   row["coverage"]="MISSING_TICKER_SOURCE";data.append(row);continue
  source=sources[t];groups=source["days"];dates=list(groups);row["provider"]=source["provider"]
  row["source_total_5m_bars"]=source["total_m5_bars"]
  row["incomplete_RTH_sessions_in_source"]=source["invalid_days"]
  if reaction not in groups:
   row["coverage"]="MISSING_REACTION_DAY";data.append(row);continue
  idx=dates.index(reaction)
  if idx<1:
   row["coverage"]="MISSING_PRIOR_CLOSE";data.append(row);continue
  pred=dates[idx-1]
  if pred in source["invalid_days"] or reaction in source["invalid_days"]:
   row["coverage"]="INCOMPLETE_PREVIOUS_OR_REACTION_DAY";data.append(row);continue
  prev=groups[pred][-1]["c"]
  arr=groups[reaction]
  row["coverage"]="FULL_REACTION_DAY"
  row["pre_earnings_raw_5m_close_day"]=pred;row["raw_asof_pre_earnings_close"]=prev
  row["reaction_day_close_pct_vs_pre_close"]=round(100*(arr[-1]["c"]/prev-1),4)
  first=next((i for i,b in enumerate(arr) if b["l"]<=prev*.95),None)
  if first is None:
   row["breach"]={"state":"NO_INTRADAY_DOWN_5PCT"};data.append(row);continue
  bar=arr[first]
  if bar["clock"]>"11:30":
   row["breach"]={"state":"FIRST_SHOCK_AFTER_1130","time_ET":bar["clock"]};data.append(row);continue
  row["breach"]={"state":"EARLY_5PCT_SHOCK","bar_index":first,"time_ET":bar["clock"],
                 "first_bar_low":bar["l"],"first_bar_volume":bar["v"],
                 "event_close_no_longer_below_minus5":arr[-1]["c"]>prev*.95}
  row["bare_buy_next5m"]=barrier(groups,reaction,first+1)
  row["buyer_rule"]=rule(arr,first)
  if row["buyer_rule"]["state"]=="BUYER_INITIATIVE_ENTRY":
   row["buyer_entry"]=barrier(groups,reaction,row["buyer_rule"]["signal"]["breakout_bar_index"]+1)
  data.append(row)
 valid=[x for x in data if x["coverage"]=="FULL_REACTION_DAY"]
 quals=[x for x in valid if x["breach"]["state"]=="EARLY_5PCT_SHOCK"]
 a=calc(quals,"buyer_entry","qualified_intraday_dislocation")
 b=calc(quals,"bare_buy_next5m","qualified_intraday_dislocation")
 allres=calc(data,"buyer_entry","all_frozen_announcements")
 counters={"coverage":dict(collections.Counter(x["coverage"] for x in data)),
          "gate":dict(collections.Counter(x.get("breach",{}).get("state","NO_COVERAGE") for x in data)),
          "buyer_pattern":dict(collections.Counter(x.get("buyer_rule",{}).get("state","NOT_ELIGIBLE") for x in data))}
 gates={"at_least_10_buyer_signal_entries":a["entries"]>=10,
        "target_first_10pp_better_per_eligible_event_than_bare":a["target_rate_pct_per_all_denominator_events"] is not None and b["target_rate_pct_per_all_denominator_events"] is not None and a["target_rate_pct_per_all_denominator_events"]>=b["target_rate_pct_per_all_denominator_events"]+10,
        "at_least_three_more_target_wins":a["target_first"]>=b["target_first"]+3,
        "positive_cost_sensitivity_per_all_40_announcements":allres["mean_net_sensitivity_minus20bps_trade_per_all_events_pct"]>0}
 stats={"protocol":"frozen_2025_first_buyer_initiative_without_retest_protocol_2026-10-10.md",
  "cohort":"frozen_2025_jul_aug_40_announcements_for_first_buyer_initiative_2026-10-10.json",
  "source":"connected Webull M5 RTH as-traded and Massive unadjusted 5m backup for BK, all source bars archived",
  "research_time":"2026-10-10","events_frozen":len(data),"fully_evaluable_reaction_days":len(valid),
  "early_intraday_5pct_shocks":len(quals),
  "qualified_shocks_that_close_above_minus5pct":sum(x["breach"]["event_close_no_longer_below_minus5"] for x in quals),
  "counts":counters,"buyer":a,"bare":b,"buyer_per_all40":allres,"frozen_gates":gates,
  "all_gates_passed":all(gates.values()),
  "limitations":["Not a historically executable options P&L study: no contemporaneous contract bids asks IV delta or strike selection",
                 "Old historical roster stocks not randomly selected nor 2025 point-in-time financial quality validated",
                 "2025 year independent of July-Sep 2026 but prior general studies may have exposed outcome trends",
                 "5-min candles show total volume not signed buyer-initiated order flow",
                 "Stop first assumed for ambiguous same 5min bar, severe one-percent stock stop may truncate true recovery",
                 "Illustrative 20bp total transaction cost is NOT a real execution cost or options spread"],
  "rows":data}
 OUTPUT.write_text(json.dumps(stats,indent=2)+"\n")
 print("REPORT",json.dumps({k:v for k,v in stats.items() if k!="rows"},indent=2),flush=True)
 print("EVENTS",json.dumps([{"ticker":x["ticker"],"day":x["reaction_day"],"coverage":x["coverage"],
   "closePct":x.get("reaction_day_close_pct_vs_pre_close"),"gate":x.get("breach",{}).get("state"),
   "bare":x.get("bare_buy_next5m",{}).get("exit_type"),"bareRet":x.get("bare_buy_next5m",{}).get("gross_return_pct"),
   "pattern":x.get("buyer_rule",{}).get("state"),"entryDistance":x.get("buyer_rule",{}).get("signal",{}).get("distance_above_observed_low_pct"),
   "buyer":x.get("buyer_entry",{}).get("exit_type"),"buyerRet":x.get("buyer_entry",{}).get("gross_return_pct")} for x in data],indent=2),flush=True)
if __name__=="__main__":main()
