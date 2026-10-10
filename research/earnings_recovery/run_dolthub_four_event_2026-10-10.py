#!/usr/bin/env python3
"""Free DoltHub historical options quote retrieval for frozen 2025 earnings pilot.
No account, no key, no payment. Quotes are asynchronous EOD, not actual trade entry OPEN.
Preserve exact dates, unavailable dates and data validation.
"""
from __future__ import annotations
import datetime as dt, json, pathlib, time, urllib.parse, urllib.request, urllib.error
URL="https://www.dolthub.com/api/v1alpha1/post-no-preference/options/master"
OUT=pathlib.Path("research/earnings_recovery/dolthub_four_event_eod_chain_2026-10-10.json")
CASES=[
("DELL","day3","2025-03-06","2025-03-07",94.25),
("DELL","rising","2025-03-13","2025-03-17",93.95),
("QCOM","day3","2025-08-05","2025-08-13",148.52),
("QCOM","rising","2025-08-13","2025-09-05",153.97),
("PYPL","day3","2025-02-07","2025-02-21",79.00),
("PYPL","rising","2025-02-18","2025-02-24",78.20),
("AMAT","day3","2025-02-20","2025-02-25",175.14),
("AMAT","rising","2025-02-21","2025-02-25",176.13)
]
def sql_query(q):
    uri=URL+"?"+urllib.parse.urlencode({"q":q})
    req=urllib.request.Request(uri,headers={"Accept":"application/json","User-Agent":"Investing-OS-Research/1.0"})
    with urllib.request.urlopen(req,timeout=75) as resp:
        return json.loads(resp.read(2_000_000).decode("utf8"))
def fetch(ticker,date,spot):
    # Strictly date-scope, avoid market-wide scans.
    q=(f"SELECT date, expiration, strike, call_put, bid, ask, vol, delta, gamma, vega "
       f"FROM option_chain WHERE act_symbol = '{ticker}' AND date = '{date}' "
       f"AND call_put = 'Call' AND strike > {spot} AND strike <= {round(spot*1.25,2)} "
       f"ORDER BY expiration, strike LIMIT 1000")
    try:
        d=sql_query(q)
        status=d.get("query_execution_status")
        if status!="Success":return {"status":status or "API_ERROR", "message":str(d.get("query_execution_message"))[:600],"rows":[]}
        return {"status":"OK","rows":d.get("rows",[]),"n_rows":len(d.get("rows",[])),
                "has_more":len(d.get("rows",[]))>=1000}
    except urllib.error.HTTPError as e:return {"status":"HTTP_ERROR","code":e.code,"message":e.read(400).decode("utf8","replace"),"rows":[]}
    except Exception as e:return {"status":"ERROR","message":str(e)[:350],"rows":[]}
def main():
    out={"as_of":"2026-10-10","provider":URL,"data_type":"historical end-of-day option-chain bid/ask snapshots",
       "NO_EXECUTION":"EOD snapshot is not simultaneous with frozen next-open stock entry or intraday stock stop; cannot establish intraday option fills.",
       "fee_each_side_usd":0.65,"maximum_one_contract_entry_debit_usd":50,
       "all_8_cases":[], "unique_date_queries":[]}
    cache={}
    for ticker,method,entry,exit_,spot in CASES:
        for date in [entry,exit_]:
            key=(ticker,date,spot)
            if key not in cache:
                cache[key]=fetch(ticker,date,spot)
                x=cache[key]
                out["unique_date_queries"].append({"ticker":ticker,"date":date,"stock_reference_open":spot,"status":x.get("status"),"n_rows":x.get("n_rows"),"message":x.get("message","")})
                print(f"QUERY {ticker} {date} => {x.get('status')} n={x.get('n_rows')}",flush=True)
                time.sleep(.3)
        enter=cache[(ticker,entry,spot)]
        leave=cache[(ticker,exit_,spot)]
        def clean(rows):
            result=[]
            for r in rows:
                try:
                    x={k:r.get(k) for k in ["date","expiration","strike","call_put","bid","ask","vol","delta","gamma","vega"]}
                    x["strike"]=float(x["strike"]);x["bid"]=float(x["bid"]);x["ask"]=float(x["ask"])
                    x["entry_debit_usd"]=round(x["ask"]*100+0.65,2)
                    x["affordable_by_EOD_ask"]=0<x["ask"] and x["entry_debit_usd"]<=50 and x["bid"]>=0
                    x["valid_quote"]=x["ask"]>0 and x["ask"]>=x["bid"] and x["bid"]>=0
                    result.append(x)
                except Exception as e:
                    result.append({"unparsed":r,"error":str(e)[:200]})
            return result
        entry_rows=clean(enter.get("rows",[]))
        exit_rows=clean(leave.get("rows",[]))
        # Only EOD quote analysis, NOT selection according to frozen intraday first-TRADE and >=10 entry-volume rule.
        selections=[]
        for dte in (30,60):
            mind=(dt.date.fromisoformat(entry)+dt.timedelta(days=dte)).isoformat()
            maxd=(dt.date.fromisoformat(entry)+dt.timedelta(days=dte+7)).isoformat()
            candidates=[x for x in entry_rows if x.get("valid_quote") and x.get("affordable_by_EOD_ask") and mind<=str(x.get("expiration"))<=maxd]
            exp=min((str(x["expiration"]) for x in candidates),default=None)
            # Strike is nearest to spot among *affordable EOD asks*, not volume-qualified first-trade option strategy.
            found=min((x for x in candidates if str(x["expiration"])==exp),key=lambda r:r["strike"],default=None) if exp else None
            z={"nominal_dte":dte,"target_expiry_range":[mind,maxd],"eod_ask_affordable_candidates":len(candidates),"chosen_by_EOD_ask_only":found}
            if found:
                look=next((r for r in exit_rows if r.get("strike")==found["strike"] and str(r.get("expiration"))==str(found.get("expiration"))),None)
                z["exit_bid_quote"]=look
                if look and look.get("valid_quote"):
                    cost=found["entry_debit_usd"];proceeds=max(0,look["bid"]*100-.65)
                    z["eod_ask_to_eod_bid_return_pct"]=round(100*(proceeds-cost)/cost,3)
            selections.append(z)
        out["all_8_cases"].append({"ticker":ticker,"method":method,"entry":entry,"stock_exit":exit_,"spot_open":spot,
              "entry_status":enter.get("status"),"exit_status":leave.get("status"),
              "entry_quotes":entry_rows,"exit_quotes":exit_rows,"eod_ask_only_selections":selections})
    out["notes"]=["'vol' is annualized implied volatility, not option daily trade VOLUME. This dataset may not expose option volume and cannot prove the frozen >=10-contract volume floor.","Historical quote snapshot date may not have been collected every trading day; missing is not a $0 fill.","Strategy's predeclared entry was NEXT OPEN, not end-of-day. All computed bid/ask P&L are alternative EOD snapshots, NOT primary protocol executions."]
    OUT.parent.mkdir(exist_ok=True,parents=True)
    OUT.write_text(json.dumps(out,indent=2)+"\n")
    print(json.dumps({"saved":str(OUT),"n_cases":len(out["all_8_cases"]),"statuses":out["unique_date_queries"],
         "eod_example":[{"ticker":c["ticker"],"method":c["method"],"items":c["eod_ask_only_selections"]} for c in out["all_8_cases"] if any(q["chosen_by_EOD_ask_only"] for q in c["eod_ask_only_selections"])]},default=str)[:15000],flush=True)
if __name__=="__main__":main()
