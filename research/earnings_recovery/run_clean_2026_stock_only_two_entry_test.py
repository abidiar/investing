#!/usr/bin/env python3
"""Stage 2: after Git committed stage-1 event list, reveal July-Sep 2026 stock outcomes.
Nothing about initial event qualification is recomputed from forward outcomes.
"""
import concurrent.futures,collections,datetime as dt,json,math,pathlib,time,urllib.parse,urllib.request
P=pathlib.Path("research/earnings_recovery")
COHORT=P/"frozen_jul_sep2026_earnings_selloff_discovery_2026-10-10.json"
OUT=P/"clean_jul_sep2026_stock_recovery_actual_outcomes_2026-10-10.json"
RAW=P/"clean_jul_sep2026_stock_recovery_stock_bars_2026-10-10.json"
def get(ticker):
 start=int(dt.datetime(2026,6,1,tzinfo=dt.timezone.utc).timestamp())
 end=int(dt.datetime(2026,10,10,tzinfo=dt.timezone.utc).timestamp())
 errors=[]
 for host in ("query1.finance.yahoo.com","query2.finance.yahoo.com"):
  url=f"https://{host}/v8/finance/chart/{urllib.parse.quote(ticker)}?period1={start}&period2={end}&interval=1d&events=split"
  try:
   req=urllib.request.Request(url,headers={"User-Agent":"Mozilla/5.0 AcademicHistoricalResearch/1.0"})
   with urllib.request.urlopen(req,timeout=35) as resp:jsondata=json.loads(resp.read(3000000))
   r=jsondata.get("chart",{}).get("result")
   if r:break
  except Exception as ex:
   errors.append(str(ex)[:140]);time.sleep(.35)
 else:return {"status":"HTTP_ERROR","ticker":ticker,"errors":errors,"bars":[]}
 data=r[0]
 raw=[]
 stamp=data.get("timestamp",[])
 quotes=data.get("indicators",{}).get("quote",[{}])[0]
 splits=[]
 for s in data.get("events",{}).get("splits",{}).values():
  denom=float(s.get("denominator") or 0)
  if not denom:continue
  ratio=float(s.get("numerator",0))/denom
  if ratio>0:
   when=s.get("date")
   date=dt.datetime.fromtimestamp(when,dt.timezone.utc).date().isoformat() if isinstance(when,(float,int)) else str(when)[:10]
   splits.append({"date":date,"ratio":ratio})
 for i,t in enumerate(stamp):
  try:
   vals=[float(quotes[k][i]) for k in ("open","high","low","close")]
   if not all(math.isfinite(x) for x in vals):continue
  except Exception:continue
  date=dt.datetime.fromtimestamp(t,dt.timezone.utc).date().isoformat()
  # Yahoo quote OHLC is split-adjusted to now, NOT dividend adjusted. Recover date-as-traded nominal units.
  mult=math.prod(s["ratio"] for s in splits if s["date"]>date)
  raw.append([date]+[round(x*mult,6) for x in vals])
 return {"status":"OK","ticker":ticker,"source":"Yahoo chart quote OHLC, not AdjClose, reverse future splits","splits":splits,"bars":raw}
def entry_idx(b,event,mode):
 s=next((i for i,x in enumerate(b) if x[0]==event),None)
 if s is None:return {"status":"EVENT_PRICE_MISSING"}
 if mode=="day3":
  if s+3>=len(b):return {"status":"NO_ENTRY_PRICE"}
  return {"status":"ENTRY","i":s+3,"signal_day":None,"event_idx":s}
 for k in range(s+3,min(s+20,len(b)-2)+1):
  if b[k-2][3]<=b[k-1][3]<=b[k][3] and b[k][4]>max(b[k-1][2],b[k-2][2]):
   i=k+1
   if b[i][1]>b[s][4]*1.08:
    return {"status":"SKIP_CHASE","signal_day":b[k][0],"next_entry_day":b[i][0],"chase_gap_pct":round(100*(b[i][1]/b[s][4]-1),4)}
   return {"status":"ENTRY","i":i,"signal_day":b[k][0],"event_idx":s}
 # If all possible signal days are not yet available, don't pretend no signal
 if len(b)-1 < s+21:return {"status":"NO_FULL_SIGNAL_WINDOW_YET","last_available_day":b[-1][0]}
 return {"status":"NO_SIGNAL_WITHIN_20"}
def outcome(b,split,info):
 if info["status"]!="ENTRY":return {"status":info["status"],**{k:v for k,v in info.items() if k!="status"}}
 i=info["i"];start=b[i];entry=start[1];target=entry*1.05;stop=entry*.95
 window=b[i:min(len(b),i+20)]
 if any(start[0]<s["date"]<=window[-1][0] for s in split):
  return {"status":"SPLIT_DURING_HOLD","entry":start[0],"entry_open":entry}
 for off,x in enumerate(window):
  d,o,h,l,c=x;result=None;exitprice=None
  if off>0 and o<=stop:result="STOP_GAP";exitprice=o
  elif off>0 and o>=target:result="TARGET_GAP";exitprice=o
  elif l<=stop:result="STOP";exitprice=stop
  elif h>=target:result="TARGET";exitprice=target
  if result:
   return {"status":"RESOLVED","result":result,"profit_target_before_stop":result.startswith("TARGET"),
           "entry":start[0],"entry_open":entry,"exit":d,"exit_price":round(exitprice,6),
           "gross_stock_return_pct":round(100*(exitprice/entry-1),4),"holding_sessions":off+1,
           "signal_day":info.get("signal_day"),"chase_gap_pct":None}
 if len(window)<20:
  return {"status":"RIGHT_CENSORED","entry":start[0],"entry_open":entry,"last_date":window[-1][0],
          "observed_sessions":len(window),"return_to_last_mark_pct":round(100*(window[-1][4]/entry-1),4)}
 last=window[-1]
 return {"status":"RESOLVED","result":"TIME","profit_target_before_stop":False,"entry":start[0],"entry_open":entry,
         "exit":last[0],"exit_price":last[4],"gross_stock_return_pct":round(100*(last[4]/entry-1),4),"holding_sessions":20,
         "signal_day":info.get("signal_day")}
def main():
 cohort=json.loads(COHORT.read_text())
 assert cohort.get("post_event_price_outcomes_in_this_file") is False
 events=cohort["selected_events"]
 tickers=sorted(set(e["ticker"] for e in events))
 print("FROZEN EVENTS",len(events),"TICKERS",tickers,flush=True)
 sources={}
 with concurrent.futures.ThreadPoolExecutor(max_workers=3) as pool:
  futs={pool.submit(get,t):t for t in tickers}
  for f in concurrent.futures.as_completed(futs):
   t=futs[f]
   try:sources[t]=f.result()
   except Exception as e:sources[t]={"status":"ERROR","error":str(e),"bars":[]}
   print("SOURCE",t,sources[t]["status"],len(sources[t].get("bars",[])),flush=True)
 cases=[]
 for e in events:
  t=e["ticker"];z=sources[t]
  result={**e,"source_status":z["status"],"qualifying_issuer_quality_is_historical_not_2026_recrosschecked":True}
  if z["status"]!="OK":result["test_status"]="MISSING_PRICE";cases.append(result);continue
  b=z["bars"];k=next((i for i,x in enumerate(b) if x[0]==e["selloff_day"]),None)
  if k is None or k==0:result["test_status"]="MISSING_REACTION_CLOSE";cases.append(result);continue
  exact_return=100*(b[k][4]/b[k-1][4]-1)
  result["raw_chart_reaction_return_pct"]=round(exact_return,4)
  result["source_reaction_discrepancy_pct_points"]=round(exact_return-e["reaction_close_pct"],4)
  # Corporate action/convention discrepancy >1.0% point: hold out rather than inflate.
  if abs(exact_return-e["reaction_close_pct"])>1.0:
   result["test_status"]="SOURCE_REACTION_MISMATCH";cases.append(result);continue
  result["test_status"]="QUALIFIED_TESTABLE"
  for mode in ["day3","rising_lows"]:
   result[mode]=outcome(b,z.get("splits",[]),entry_idx(b,e["selloff_day"],mode))
  cases.append(result)
 qualified=[x for x in cases if x["test_status"]=="QUALIFIED_TESTABLE"]
 summary={}
 for mode in ("day3","rising_lows"):
  rs=[x[mode] for x in qualified]
  status=dict(collections.Counter(x["status"] for x in rs))
  resolves=[x for x in rs if x["status"]=="RESOLVED"]
  wins=[x for x in resolves if x["profit_target_before_stop"]]
  losses=[x for x in resolves if x["result"].startswith("STOP")]
  timeouts=[x for x in resolves if x["result"]=="TIME"]
  uncens=[x for x in rs if x["status"]=="RIGHT_CENSORED"]
  skips=[x for x in rs if x["status"].startswith("NO_") or x["status"].startswith("SKIP")]
  n=len(rs)
  known_event_marks=sum(x["gross_stock_return_pct"] for x in resolves)/n if n else None
  # Bounds on target hit rate across ALL frozen eligible events, unresolved are unknown; no-signal counts as no trade.
  summary[mode]={"n_eligible_events":n,"status_counts":status,"resolved":len(resolves),"target_before_stop":len(wins),
     "stop_first":len(losses),"timeouts":len(timeouts),"right_censored":len(uncens),"no_trade_or_signal":len(skips),
     "observed_target_rate_ALL_events_pct_lower_bound":round(100*len(wins)/n,2) if n else None,
     "possible_target_rate_ALL_events_pct_upper_bound":round(100*(len(wins)+len(uncens))/n,2) if n else None,
     "target_rate_among_resolved_trades_pct":round(100*len(wins)/len(resolves),2) if resolves else None,
     "mean_return_resolved_trades_pct":round(sum(x["gross_stock_return_pct"] for x in resolves)/len(resolves),3) if resolves else None,
     "mean_gross_return_per_ALL_events_with_missing_as_unknown":None if uncens else round(known_event_marks,3) if n else None,
     "known_resolved_stock_return_contribution_pct_points_per_all_events":round(known_event_marks,3) if n else None,
     "median_sessions_to_target":sorted(x["holding_sessions"] for x in wins)[len(wins)//2] if wins else None}
 matched=[x for x in qualified if x.get("day3",{}).get("status")=="RESOLVED" and x.get("rising_lows",{}).get("status")=="RESOLVED"]
 deltas=[x["rising_lows"]["gross_stock_return_pct"]-x["day3"]["gross_stock_return_pct"] for x in matched]
 paired={"n_both_methods_resolved":len(matched),"mean_confirmation_minus_day3_return_pct_points":round(sum(deltas)/len(deltas),3) if deltas else None,
         "confirmation_better_count":sum(x>0 for x in deltas),"day3_better_count":sum(x<0 for x in deltas),"equal_count":sum(x==0 for x in deltas)}
 decision={
    "min_n_at_least_20":len(qualified)>=20,
    "signal_target_rate_at_least_60pct_lower_bound":summary["rising_lows"]["observed_target_rate_ALL_events_pct_lower_bound"]>=60 if qualified else False,
    "at_least_10pp_confirmed_target_advantage_lower_bound":summary["rising_lows"]["observed_target_rate_ALL_events_pct_lower_bound"]-summary["day3"]["possible_target_rate_ALL_events_pct_upper_bound"]>=10 if qualified else False,
    "positive_paired_mean_when_resolved":paired["mean_confirmation_minus_day3_return_pct_points"]>0 if deltas else False
 }
 out={"study_date":"2026-10-10","cohort_source":str(COHORT),"outcome_source":"Yahoo historical raw stock OHLC; split factor reversed; never adjclose, through 2026-10-09",
      "strategy":"Third-day opening baseline vs first three nondecreasing lows and previous-two-high break, following open; +5/-5 first, 20 entry-inclusive sessions",
      "candidate_universe_61":len(cohort["precommitted_61_issuers"]),
      "preselected_events":len(events),"usable_events":len(qualified),"excluded":len(events)-len(qualified),
      "event_status_counts":dict(collections.Counter(x["test_status"] for x in cases)),
      "summary":summary,"paired":paired,"decision_gates":decision,"all_decision_gates_passed":all(decision.values()),
      "caveats":["2026 issuers were qualified historically, but point-in-time 2026 statement quality was NOT rechecked",
       "Only FIRST earnings reaction <=-5% close qualified, earlier two-session rule narrowed before cohort discovery",
       "Contemporary Quant500 SEC filing session may lag true public press release","No options P&L, spreads, commissions or slippage",
       "Some late-Aug/early-Sep confirmation setups may be right-censored before a full 20-session exit"],
      "cases":cases}
 OUT.write_text(json.dumps(out,indent=2)+"\n")
 RAW.write_text(json.dumps({"source_snapshots":sources},indent=2)+"\n")
 print(json.dumps({k:v for k,v in out.items() if k not in ("cases",)},indent=2),flush=True)
 print("PER-EVENT",json.dumps([{"ticker":x["ticker"],"selloff":x["selloff_day"],"react":x["reaction_close_pct"],
   "day3":x.get("day3"),"confirmed":x.get("rising_lows"),"status":x["test_status"]} for x in cases],default=str)[:17000],flush=True)
if __name__=="__main__":main()
