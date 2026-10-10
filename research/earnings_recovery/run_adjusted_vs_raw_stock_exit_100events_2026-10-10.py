#!/usr/bin/env python3
"""Audit dividend-adjusted saved stocks vs raw tradable underlying stock barriers in 100-event option study."""
from __future__ import annotations
import concurrent.futures,collections,datetime as dt,json,math,pathlib,time,urllib.parse,urllib.request,urllib.error
P=pathlib.Path("research/earnings_recovery")
OUT=P/"raw_stock_price_dividend_exit_audit_100events_2026-10-10.json"
FILES=[P/"free_2024_eod_otm_45event_results_2026-10-10.json",P/"free_2025_eod_otm_55event_results_2026-10-10.json"]
EVENTS=P/"actionable_bounce_event_price_windows_164_2026-10-10.json"
HEADERS={"User-Agent":"Mozilla/5.0 InvestingOSHistoricalResearch/1.0"}
def grab(ticker):
 start=int(dt.datetime(2023,12,1,tzinfo=dt.timezone.utc).timestamp())
 end=int(dt.datetime(2026,10,12,tzinfo=dt.timezone.utc).timestamp())
 for host in ["query1.finance.yahoo.com","query2.finance.yahoo.com"]:
  url=f"https://{host}/v8/finance/chart/{urllib.parse.quote(ticker)}?period1={start}&period2={end}&interval=1d&events=div%2Csplits"
  try:
   req=urllib.request.Request(url,headers=HEADERS)
   with urllib.request.urlopen(req,timeout=35) as res:
    j=json.loads(res.read(4_000_000))
   result=j.get("chart",{}).get("result")
   if not result:continue
   z=result[0]
   splits=[]
   for a in z.get("events",{}).get("splits",{}).values():
    ratio=float(a.get("numerator",0))/float(a.get("denominator",1)) if a.get("denominator") else 0
    if ratio>0:
     st=a.get("date")
     d=dt.datetime.fromtimestamp(st,dt.timezone.utc).date().isoformat() if isinstance(st,(float,int)) else str(st)[:10]
     splits.append({"date":d,"ratio":ratio})
   dividends=[]
   for a in z.get("events",{}).get("dividends",{}).values():
    st=a.get("date")
    try:d=dt.datetime.fromtimestamp(st,dt.timezone.utc).date().isoformat() if isinstance(st,(float,int)) else str(st)[:10]
    except:d=str(st)
    dividends.append({"date":d,"amount":a.get("amount")})
   stamps=z.get("timestamp",[])
   quote=z.get("indicators",{}).get("quote",[{}])[0]
   bars={}
   for i,ts in enumerate(stamps):
    day=dt.datetime.fromtimestamp(ts,dt.timezone.utc).date().isoformat()
    try:
     x=[float(quote[k][i]) for k in ("open","high","low","close")]
     if not all(math.isfinite(v) for v in x):continue
     future=math.prod(s["ratio"] for s in splits if s["date"]>day)
     bars[day]=[round(v*future,6) for v in x]
    except (TypeError,ValueError,IndexError,KeyError):continue
   return {"status":"OK","bars":bars,"dividends":dividends,"splits":splits,"n":len(bars)}
  except Exception as e:
   last=type(e).__name__+": "+str(e)[:180]
 return {"status":"ERROR","error":last}

def raw_outcome(saved_ohlc,bars,entry_i):
 entry_date=saved_ohlc[entry_i][0]
 entry=bars.get(entry_date)
 if not entry:return {"status":"MISSING_ENTRY_RAW_OHLC"}
 buy=entry[0];tp=1.05*buy;stop=.95*buy
 for j in range(entry_i,min(entry_i+20,len(saved_ohlc))):
  day=saved_ohlc[j][0];q=bars.get(day)
  if not q:return {"status":"MISSING_HISTORICAL_DAY","missing_date":day}
  op,hi,lo,cl=q
  if j>entry_i and op<=stop:return {"status":"OK","exit":day,"reason":"stop_gap","entry_open":buy,"stop":stop,"target":tp,"exit_price":op}
  if j>entry_i and op>=tp:return {"status":"OK","exit":day,"reason":"target_gap","entry_open":buy,"stop":stop,"target":tp,"exit_price":op}
  if lo<=stop:return {"status":"OK","exit":day,"reason":"stop","entry_open":buy,"stop":stop,"target":tp,"exit_price":stop}
  if hi>=tp:return {"status":"OK","exit":day,"reason":"target","entry_open":buy,"stop":stop,"target":tp,"exit_price":tp}
 end=saved_ohlc[min(entry_i+19,len(saved_ohlc)-1)][0]
 return {"status":"OK","exit":end,"reason":"time","entry_open":buy,"stop":stop,"target":tp,"exit_price":bars[end][3]}

def main():
 ds=[json.loads(x.read_text()) for x in FILES]
 raw_events=json.loads(EVENTS.read_text())["series"]
 lookup={(z["ticker"],z["date"],z["cohort"]):z for z in raw_events}
 setups=[c for doc in ds for c in doc["setups"]]
 tickers=sorted({c["ticker"] for c in setups})
 print(f"START {len(setups)} setups {len(tickers)} unique tickers",flush=True)
 prices={}
 with concurrent.futures.ThreadPoolExecutor(max_workers=6) as pool:
  fut={pool.submit(grab,t):t for t in tickers}
  for f in concurrent.futures.as_completed(fut):
   t=fut[f]
   try:prices[t]=f.result()
   except Exception as e:prices[t]={"status":"ERROR","error":str(e)[:200]}
   if len(prices)%12==0:print("PRICE",len(prices),len(tickers),flush=True)
 rows=[]
 for c in setups:
  r={"year":c["event"][:4],"ticker":c["ticker"],"cohort":c["cohort"],"event":c["event"],
     "method":c["method"],"saved_setup_status":c["status"],"saved_exit":c.get("stock_exit"),
     "saved_exit_reason":c.get("exit_reason"),"entry":c.get("entry"),"raw_data_status":prices[c["ticker"]]["status"]}
  if not c.get("entry"):
   r["audit_status"]="NO_ENTRY";rows.append(r);continue
  saved=lookup.get((c["ticker"],c["event"],c["cohort"]))
  if not saved:
   r["audit_status"]="EVENT_NOT_IN_ARCHIVE";rows.append(r);continue
  o=prices[c["ticker"]]
  if o["status"]!="OK":
   r["audit_status"]="UNAVAILABLE_RAW_PRICES";rows.append(r);continue
  idx=next((i for i,b in enumerate(saved["bars"]) if b[0]==c["entry"]),None)
  if idx is None:
   r["audit_status"]="ENTRY_NOT_IN_SAVED_BARS";rows.append(r);continue
  x=raw_outcome(saved["bars"],o["bars"],idx)
  if x["status"]!="OK":
   r["audit_status"]=x["status"];r["audit_error"]=x;rows.append(r);continue
  ratio=x["entry_open"]/saved["bars"][idx][1]
  r["entry_dividend_adjustment_factor_vs_saved"]=round(ratio,6)
  r["raw_entry_open"]=x["entry_open"];r["raw_target"]=round(x["target"],5);r["raw_stop"]=round(x["stop"],5)
  r["raw_exit"]=x["exit"];r["raw_exit_reason"]=x["reason"];r["audit_status"]="OK"
  r["original_exit_matches_raw"]=(c.get("stock_exit")==x["exit"])
  last=max(x["exit"],c.get("stock_exit",x["exit"]))
  r["dividend_events_during_entry_to_later_exit"]=[z for z in o["dividends"] if c["entry"]<z["date"]<=last]
  r["any_dividend_during"]=len(r["dividend_events_during_entry_to_later_exit"])>0
  r["splits_during_entry_to_later_exit"]=[z for z in o["splits"] if c["entry"]<z["date"]<=last]
  r["quote_matches"]=[{"dte":days,"expiry":c[f"eod_{days}"].get("expiry"),
                      "strike":c[f"eod_{days}"].get("strike"),
                      "eod_return_pct":c[f"eod_{days}"].get("eod_ask_to_bid_return_pct")} for days in [30,60]
     if "eod_ask_to_bid_return_pct" in c.get(f"eod_{days}",{})]
  rows.append(r)
 audited=[x for x in rows if x["audit_status"]=="OK"]
 matched=[x for x in audited if x["quote_matches"]]
 result={
  "asof":"2026-10-10",
  "description":"Recompute original frozen +5/-5 stock exits from historic actual as-of-event OHLC instead of dividend-adjusted saved OHLC; no fitted rules, note sources differ.",
  "caveat":"Option bid/ask at first raw intraday target still unavailable. Raw Yahoo daily bars may differ slightly from Massive; do not replace missing exact contract quotes with synthetic.",
  "total_setups":len(rows),"audited":len(audited),
  "source_statuses":dict(collections.Counter(z["status"] for z in prices.values())),
  "audit_statuses":dict(collections.Counter(x["audit_status"] for x in rows)),
  "match_count":sum(x["original_exit_matches_raw"] for x in audited),
  "mismatch_count":sum(not x["original_exit_matches_raw"] for x in audited),
  "any_dividend_count":sum(x["any_dividend_during"] for x in audited),
  "matched_quote_setups":len(matched),
  "matched_quote_setups_with_exit_day_mismatch":sum(not x["original_exit_matches_raw"] for x in matched),
  "matched_quote_setup_details":matched,
  "all_setups":rows}
 OUT.write_text(json.dumps(result,indent=2)+"\n")
 print(json.dumps({k:v for k,v in result.items() if k not in ("all_setups","matched_quote_setup_details")},default=str),flush=True)
 print("MISMATCHED_QUOTE_CASES",json.dumps([x for x in matched if not x["original_exit_matches_raw"]])[:14000],flush=True)
if __name__=="__main__":main()
