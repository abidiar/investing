#!/usr/bin/env python3
"""Check exactly the free historical option quote and volume sources needed for our fixed 100-event study.
No subscriptions or credentials. Preserve negative access results, never impute absent trades.
"""
import json, pathlib, urllib.request, urllib.parse, urllib.error, time, concurrent.futures
ROOT=pathlib.Path("research/earnings_recovery")
FILES=[ROOT/"free_2024_eod_otm_45event_results_2026-10-10.json",ROOT/"free_2025_eod_otm_55event_results_2026-10-10.json"]
OUT=ROOT/"historical_options_missing_contract_source_probe_2026-10-10.json"
URL="https://www.dolthub.com/api/v1alpha1/post-no-preference/options/master"
def req(url, method="GET"):
    r=urllib.request.Request(url,headers={"User-Agent":"InvestingOS-historical-data-feasibility/1.0","Accept":"application/json,*/*","Range":"bytes=0-31"},method=method)
    try:
        with urllib.request.urlopen(r,timeout=20) as response:
            b=response.read(100000)
            return {"ok":True,"code":response.status,"content_type":response.headers.get("Content-Type"),"content_length":response.headers.get("Content-Length"),
                    "content_range":response.headers.get("Content-Range"),"head_bytes_hex":b[:20].hex(),
                    "body":b.decode("utf8","replace")[:600] if "json" in (response.headers.get("Content-Type","")) else None}
    except urllib.error.HTTPError as e:
        return {"ok":False,"code":e.code,"response":e.read(180).decode("utf8","replace")}
    except Exception as e:
        return {"ok":False,"error":type(e).__name__+": "+str(e)[:200]}
def get_json(q):
    u=URL+"?"+urllib.parse.urlencode({"q":q})
    r=urllib.request.Request(u,headers={"Accept":"application/json","User-Agent":"InvestingOS-Research/1.0"})
    try:
        with urllib.request.urlopen(r,timeout=30) as response:return json.loads(response.read(100000))
    except Exception as e:return {"query_execution_status":"ERROR","query_execution_message":str(e)[:200]}
data=[json.loads(p.read_text()) for p in FILES]
unmatched=[]
for d in data:
 for c in d["setups"]:
  for horizon in [30,60]:
   q=c.get("eod_"+str(horizon)) or {}
   if q.get("selection_status")!="NO_MATCHED_EXIT_EOD_QUOTE":continue
   unmatched.append({"year":c["event"][:4],"ticker":c["ticker"],"event":c["event"],"method":c["method"],
                     "entry":c["entry"],"exit":c["stock_exit"],"expiry":q["expiry"],"strike":q["strike"],
                     "entry_bid":q["entry_bid"],"entry_ask":q["entry_ask"],"delta":q.get("delta"),"iv":q.get("entry_iv"),"horizon":horizon})
def check_exact(x):
 q=("SELECT date, act_symbol, expiration, strike, call_put, bid, ask, vol, delta "
    "FROM option_chain WHERE act_symbol='"+x["ticker"]+"' AND date='"+x["exit"]+
    "' AND expiration='"+x["expiry"]+"' AND strike="+str(x["strike"])+
    " AND call_put='Call' LIMIT 5")
 obj=get_json(q)
 return {"ticker":x["ticker"],"method":x["method"],"exit":x["exit"],"expiry":x["expiry"],"strike":x["strike"],
         "year":x["year"],"status":obj.get("query_execution_status"),"rows":obj.get("rows",[]),
         "error":obj.get("query_execution_message")}
def collect():
 out={"as_of":"2026-10-10","purpose":"Resolve missing exact contract exit-day quote and missing historical daily option volume; no change to frozen criteria",
      "source_note":"The 104-ticker CDN described by a now-404 Github repo is NOT presumed accessible; this probes actual HTTP availability",
      "candidate_unmatched_exit":len(unmatched),"candidate_unmatched":unmatched,
      "cdn_checks":[],"dolt_exact_exit":[]}
 urls=[
  "https://static.philippdubach.com/data/options/qcom/options.parquet",
  "https://static.philippdubach.com/data/options/pypl/options.parquet",
  "https://static.philippdubach.com/data/options/tgt/options.parquet",
  "https://static.philippdubach.com/data/options/txn/options.parquet",
  "https://static.philippdubach.com/data/options/adbe/options.parquet",
  "https://static.philippdubach.com/data/options/spy/options.parquet",
  "https://github.com/SaidBahaDev/options-data"
 ]
 with concurrent.futures.ThreadPoolExecutor(max_workers=4) as pool:
  futs={pool.submit(req,u,"HEAD"):u for u in urls}
  for f in concurrent.futures.as_completed(futs):
   o={"url":futs[f],"method":"HEAD","result":f.result()};out["cdn_checks"].append(o);print("CDN",o["url"],o["result"].get("code"),flush=True)
 # If HEAD errors only for specific URL, perform small-range GET for 2 to avoid HEAD-specific incompatibility
 for u in urls[:2]:
  v=req(u,method="GET");out["cdn_checks"].append({"url":u,"method":"Range GET bytes 0-31","result":v});print("RANGE",u,v.get("code"),v.get("content_length"),flush=True)
 with concurrent.futures.ThreadPoolExecutor(max_workers=4) as pool:
  futs={pool.submit(check_exact,x):x for x in unmatched}
  for i,f in enumerate(concurrent.futures.as_completed(futs),1):
   y=f.result();out["dolt_exact_exit"].append(y)
   if i%10==0:print("EXACT",i,len(unmatched), "recovered",sum(bool(z["rows"]) for z in out["dolt_exact_exit"]),flush=True)
 out["dolt_exact_exit"].sort(key=lambda x:(x["year"],x["ticker"],x["exit"],x["strike"]))
 OUT.write_text(json.dumps(out,indent=2)+"\n")
 print(json.dumps({"saved":str(OUT),"cdn":out["cdn_checks"],"dolt_n":len(out["dolt_exact_exit"]),
   "recovered":sum(bool(z["rows"]) for z in out["dolt_exact_exit"]),"other_statuses":sorted(set(z["status"] for z in out["dolt_exact_exit"]))},default=str)[:7000],flush=True)
if __name__=="__main__":collect()
