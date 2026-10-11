#!/usr/bin/env python3
"""Frozen 45-announcement intraday selling-exhaustion + buyer-initiation study.
Only as-of completed historical Webull 5m bars used for signal; all 45 included.
"""
import collections,datetime as dt,json,math,pathlib,statistics
from zoneinfo import ZoneInfo
R=pathlib.Path("research/earnings_recovery"); ET=ZoneInfo("America/New_York")
EV=R/"frozen_all45_jul_sep2026_earnings_announcements_pre_5min.json"
OUT=R/"first_failed_low_volume_buyer_takeover_45events_results_2026-10-10.json"
WEEKS=["2026-07-06","2026-07-13","2026-07-20","2026-07-27","2026-08-03","2026-08-10","2026-08-17","2026-08-24","2026-08-31"]
def collect():
 intraday={}; daily={}
 for week in WEEKS:
  path=R/f"first_failed_low_2026_all45_intraday_week{week}_2026-10-10.json"
  data=json.loads(path.read_text())
  for s in data["stocks"]:
   t=s["ticker"]
   if t in intraday:raise ValueError("ticker collision "+t)
   b=[]
   for z in s["bars"]:
    stamp=dt.datetime.strptime(z[0],"%Y-%m-%dT%H:%M:%S.%f%z").astimezone(ET)
    o,h,l,c,v=map(float,z[1:])
    assert o>0 and h>=max(o,c) and l<=min(o,c) and v>=0,(t,z)
    b.append({"day":stamp.strftime("%Y-%m-%d"),"clock":stamp.strftime("%H:%M"),"time_ET":stamp.isoformat(),
              "o":o,"h":h,"l":l,"c":c,"v":v})
   b.sort(key=lambda x:x["time_ET"]);intraday[t]=b
 for k in range(1,4):
  data=json.loads((R/f"first_failed_low_2026_all45_daily_priorclose_part{k}_2026-10-10.json").read_text())
  for s in data["stocks"]:
   t=s["ticker"]
   if t in daily:raise ValueError("daily ticker collision "+t)
   daily[t]=sorted([[z[0][:10]]+[float(v) for v in z[1:]] for z in s["bars"]],key=lambda z:z[0])
 return intraday,daily
def grouped(b):
 d=collections.OrderedDict()
 for z in b:d.setdefault(z["day"],[]).append(z)
 expected=[(dt.datetime(2026,1,1,9,30)+dt.timedelta(minutes=5*i)).strftime("%H:%M") for i in range(78)]
 issues={}
 for day,items in d.items():
  if [x["clock"] for x in items]!=expected:issues[day]={"size":len(items),"first":items[0]["clock"],"last":items[-1]["clock"]}
 return d,issues
def selloff_gate(eventBars,oldClose):
 cutoff=oldClose*.95
 qualifying=[(i,b) for i,b in enumerate(eventBars) if b["l"]<=cutoff]
 if not qualifying:return {"state":"NO_INTRADAY_5PCT_DISLOCATION","threshold":round(cutoff,6)}
 i,b=qualifying[0]
 if b["clock"]>"11:30":
  return {"state":"FIRST_5PCT_TOUCH_TOO_LATE","first_time":b["clock"],"first_low":b["l"],"threshold":round(cutoff,6)}
 return {"state":"ELIGIBLE_GATE","initial_bar_index":i,"initial_time":b["clock"],"initial_low":b["l"],"initial_volume":b["v"],
         "threshold":round(cutoff,6),"first_event_day_close_above_minus5":eventBars[-1]["c"]>cutoff}
def pattern(b,gate):
 if gate["state"]!="ELIGIBLE_GATE":return {"state":"NO_ENTRY", "reason":gate["state"]}
 i=gate["initial_bar_index"];l0=gate["initial_low"];v0=gate["initial_volume"];early=b[:]
 retest=None
 for j in range(i+1,min(i+13,len(b))):
  x=b[j]
  if x["l"]<l0*.998:
   return {"state":"BROKEN_FIRST_LOW","time_ET":x["clock"],"low":x["l"],"initial_low":l0}
  if j<i+2:continue
  if x["clock"]>"12:30":break
  if x["l"]<=l0*1.003 and x["v"]<=v0*.8:
   retest=j;break
 if retest is None:return {"state":"NO_WEAKER_SELL_VOLUME_RETEST","initial_time":gate["initial_time"]}
 j=retest
 for k in range(j+1,min(j+4,len(b)-1)):
  x=b[k];preceding=b[k-3:k];avg=sum(y["v"] for y in preceding)/3
  if x["c"]>x["o"] and x["c"]>max(b[j]["h"],b[j-1]["h"]) and x["v"]>=1.2*avg:
   nxt=b[k+1]
   detail={"first_low":l0,"first_low_time":gate["initial_time"],
           "first_low_volume":v0,"retest_time":b[j]["clock"],"retest_low":b[j]["l"],
           "retest_volume":b[j]["v"],"retest_relative_volume":round(b[j]["v"]/v0,5) if v0 else None,
           "buyer_time":x["clock"],"buyer_green":True,"buyer_close":x["c"],"buyer_volume":x["v"],
           "buyer_volume_relative_to_prev3":round(x["v"]/avg,5) if avg else None,
           "entry_time":nxt["clock"],"entry_price":nxt["o"],
           "entry_distance_from_initial_low_pct":round(100*(nxt["o"]/l0-1),5),
           "buyer_close_distance_from_initial_low_pct":round(100*(x["c"]/l0-1),5),
           "k_bar":k,"retest_j":j}
   if nxt["clock"]>"13:05" or nxt["o"]>l0*1.015:return {"state":"EXTENDED_OR_LATE_AFTER_BUYERS","details":detail}
   return {"state":"BUYER_TAKEOVER_SIGNAL","details":detail}
 return {"state":"NO_BUYER_BREAKOUT_AFTER_FIRST_RETEST","retest_time":b[j]["clock"],"retest_low":b[j]["l"],"retest_volume":b[j]["v"]}
def exit_path(grouped,entryday,idx):
 dates=list(grouped);p=dates.index(entryday);start=grouped[entryday][idx];en=start["o"];target=en*1.015;stop=en*.99
 future=dates[p:p+3]
 if len(future)<3:return {"status":"RIGHT_CENSORED"}
 for di,day in enumerate(future):
  candles=grouped[day][idx if di==0 else 0:]
  for ii,z in enumerate(candles):
   result=None;out=None
   if di>0 and ii==0 and z["o"]<=stop:result="STOP_GAP";out=z["o"]
   elif di>0 and ii==0 and z["o"]>=target:result="TARGET_GAP";out=z["o"]
   elif z["l"]<=stop:result="STOP";out=stop
   elif z["h"]>=target:result="TARGET";out=target
   if result:return {"status":"RESOLVED","result":result,"winner":result.startswith("TARGET"),
     "entry_day":entryday,"entry_time_ET":start["clock"],"entry_open":en,"exit_day":day,"exit_time_ET":z["clock"],
     "exit_price":round(out,6),"gross_return_pct":round(100*(out/en-1),5),"sessions":di+1}
 last=grouped[future[-1]][-1]
 return {"status":"RESOLVED","result":"TIME","winner":False,"entry_day":entryday,"entry_time_ET":start["clock"],
  "entry_open":en,"exit_day":future[-1],"exit_time_ET":last["clock"],"exit_price":last["c"],
  "gross_return_pct":round(100*(last["c"]/en-1),5),"sessions":3}
def aggregate(events,key,denom):
 trades=[x[key] for x in events if x.get(key,{}).get("status")=="RESOLVED"]
 unknown=sum(x.get(key,{}).get("status")=="RIGHT_CENSORED" for x in events)
 n=len(trades)
 returns=[x["gross_return_pct"] for x in trades]
 winners=sum(x["winner"] for x in trades)
 stops=sum(x["result"].startswith("STOP") for x in trades)
 return {"full_denominator_events":len(events),"denominator_type":denom,"entries":n,"target_wins":winners,
   "stop_first":stops,"timeouts":sum(x["result"]=="TIME" for x in trades),"unresolved_trades":unknown,
   "target_pct_per_all_events":round(100*winners/len(events),3) if events else None,
   "target_pct_per_trades":round(100*winners/n,3) if n else None,
   "mean_gross_stock_return_pct_per_traded":round(statistics.mean(returns),4) if n else None,
   "mean_gross_return_pct_per_all_events_zero_for_no_trades":round(sum(returns)/len(events),4) if events else None,
   "mean_after_20bps_cost_per_event_pct":round((sum(returns)-.2*n)/len(events),4) if events else None}
def run():
 cohort=json.loads(EV.read_text());assert cohort["event_count"]==45
 intraday,daily=collect()
 assert sorted(intraday)==sorted(x["ticker"] for x in cohort["events"])
 assert sorted(daily)==sorted(intraday)
 out=[]
 for e in cohort["events"]:
  t=e["ticker"];day=e["reaction_day"];g,issues=grouped(intraday[t]);prior=[x for x in daily[t] if x[0]<day]
  case={"ticker":t,"earnings_announcement":e["announcement"],"session":e["session"],"reaction_day":day,
    "source_closing_reaction_pct":e["source_close_reaction_pct"],
    "source_bar_count":len(intraday[t]),"incomplete_session_days":issues}
  if day not in g or not prior:
   case["state"]="NO_REACTION_DAY_OR_PRIOR_CLOSE";out.append(case);continue
  # Avoid hindsight corporate-action adjustment in Webull DAILY history.
  # As-of reaction-session start, the last observed FULL 5m RTH previous-day CLOSE is known.
  before=prior[-1]
  prior_days=[d for d in g if d<day and d not in issues]
  if not prior_days:
   case["state"]="MISSING_PRIOR_COMPLETE_5MIN_CLOSE";out.append(case);continue
  lastprior=prior_days[-1]
  rawprior=g[lastprior][-1]["c"]
  close=rawprior
  case["pre_earnings_previous_close_day"]=lastprior
  case["pre_earnings_previous_close"]=close
  case["source_daily_adjusted_prior_close"]=before[4]
  case["five_min_reaction_day_closing_price"]=g[day][-1]["c"]
  case["daily_reaction_day_close"]=next((r[4] for r in daily[t] if r[0]==day),None)
  if day in issues or any(d in issues for d in list(g)[list(g).index(day):list(g).index(day)+3]):
   case["state"]="INCOMPLETE_RTH_BARS";out.append(case);continue
  if case["daily_reaction_day_close"] is None:
   case["state"]="NO_DAILY_CROSSCHECK";out.append(case);continue
  ratio_pre=before[4]/rawprior
  ratio_day=case["daily_reaction_day_close"]/g[day][-1]["c"]
  case["historical_daily_corporate_action_adjustment_pct"]=round((ratio_pre-1)*100,4)
  case["adjustment_basis_ratio_diff_ppt"]=round(abs(ratio_pre-ratio_day)*100,5)
  if abs(ratio_pre-ratio_day)>.005:
   case["state"]="INCONSISTENT_CORPORATE_ACTION_ADJUSTMENT";out.append(case);continue
  base=100*(g[day][-1]["c"]/close-1);case["actual_session_close_reaction_pct"]=round(base,4)
  if e.get("source_close_reaction_pct") is not None and abs(base-e["source_close_reaction_pct"])>1.0:
   case["state"]="SOURCE_REACTION_CLOSE_MISMATCH";out.append(case);continue
  gate=selloff_gate(g[day],close);case["gate"]=gate;case["state"]=gate["state"]
  if gate["state"]!="ELIGIBLE_GATE":out.append(case);continue
  i=gate["initial_bar_index"]
  if i+1>=len(g[day]):case["state"]="NO_BASE_ENTRY_BAR";out.append(case);continue
  case["immediate_breach_entry"]=exit_path(g,day,i+1)
  find=pattern(g[day],gate);case["first_failed_low_pattern"]=find
  if find["state"]=="BUYER_TAKEOVER_SIGNAL":
   k=find["details"]["k_bar"]+1
   case["takeover_entry"]=exit_path(g,day,k)
  out.append(case)
 eligible=[x for x in out if x["state"]=="ELIGIBLE_GATE"]
 a=aggregate(eligible,"takeover_entry","asof_first_5pct_intraday_dislocations")
 b=aggregate(eligible,"immediate_breach_entry","asof_first_5pct_intraday_dislocations")
 av_all=aggregate(out,"takeover_entry","all_45_unambiguously_timed_earnings")
 first_touch_that_closed_above=sum(x["gate"].get("first_event_day_close_above_minus5",False) for x in eligible)
 bystatus=dict(collections.Counter(x["state"] for x in out))
 status_pattern=dict(collections.Counter(x.get("first_failed_low_pattern",{}).get("state","NO_DISLOCATION") for x in eligible))
 ext=[x["first_failed_low_pattern"]["details"]["entry_distance_from_initial_low_pct"] for x in eligible
      if x.get("first_failed_low_pattern",{}).get("state")=="BUYER_TAKEOVER_SIGNAL"]
 gates={"at_least_12_takeover_entries":a["entries"]>=12,
        "at_least_plus10pp_target_rate_per_dislocation":a["target_pct_per_all_events"]>=b["target_pct_per_all_events"]+10 if eligible else False,
        "at_least_five_more_target_winners":a["target_wins"]>=b["target_wins"]+5,
        "positive_after_cost_mean_per_all_45_earnings":av_all["mean_after_20bps_cost_per_event_pct"]>0}
 meta={"study":"First failed attempt to make low, contraction of 5m traded volume on retest, expansion on green buyer breakout",
  "protocol":"frozen_intraday_first_failed_low_volume_takeover_45events_2026-10-10.md",
  "event_roster":"frozen_all45_jul_sep2026_earnings_announcements_pre_5min.json",
  "asof_threshold":"first finished 5m candle LOW <=95% of last completed pre-earnings daily close by 11:30",
  "source":"Webull connected 5m RTH stock OHLCV and Webull prior daily completed market close",
  "announcements_frozen":len(out),"reliable_asof_dislocations":len(eligible),
  "event_state_counts":bystatus,"pattern_state_counts":status_pattern,
  "intraday_dislocations_that_did_not_close_down_5pct":first_touch_that_closed_above,
  "summary":{"first_failed_low_buyer_takeover":a,"immediate_5pct_breach_reference":b,"takeover_per_all45_announcements":av_all},
  "entry_distance_pct_from_first_breach_low":ext,
  "entry_distance_median":round(statistics.median(ext),4) if ext else None,
  "go_nogo_gates":gates,"all_gates_met":all(gates.values()),
  "caveats":["A 5m green bar is not measured actual aggressive buying or selling, only directional candle and relative TOTAL volume",
  "Fixed *first* low can be legitimately breached again: this first-try strategy then skips; no rescan or hindsight anchor",
  "Five-minute OHLC cannot prove within-bar stop/target order; stop-first adverse sequence",
  "Historical nonrandom 61-name universe, partial outcome exposure for 15 old names, contemporary survivorship",
  "Historical CALL ask/bid and option Greeks at exact entry unavailable; do not infer user's META call return","2026 issuer fundamentals not freshly point-in-time qualified"],
  "events":out}
 OUT.write_text(json.dumps(meta,indent=2)+"\n")
 print("RESULT",json.dumps({k:v for k,v in meta.items() if k!="events"},indent=2),flush=True)
 print("CASES",json.dumps([{"ticker":x["ticker"],"event":x["reaction_day"],"close_change":x.get("actual_session_close_reaction_pct"),
  "gate":x.get("gate",{}).get("state"),"breach_time":x.get("gate",{}).get("initial_time"),
  "pattern":x.get("first_failed_low_pattern",{}).get("state"),"signal":x.get("first_failed_low_pattern",{}).get("details"),
  "baseline":x.get("immediate_breach_entry",{}).get("result"),"strategy":x.get("takeover_entry",{}).get("result")}
 for x in out],indent=2),flush=True)
if __name__=="__main__":run()
