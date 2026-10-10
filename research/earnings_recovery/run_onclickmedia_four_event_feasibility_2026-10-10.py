#!/usr/bin/env python3
"""Public, free-source FEASIBILITY probe for frozen 2025 earnings recovery option events.

Historical provider: https://backtest.onclickmedia.com/
This is NOT a direct quote fetch and its historical EOD simulation does not match
the frozen intraday stock target/stop. We strictly test whether it exposes dated
option bid/ask, strike, expiration, and affordable integer-contract selection.
No credentials, no paid data; public tickers/dates only.
"""
import json, os, sys, time, urllib.request, urllib.parse, urllib.error
from datetime import datetime, timezone
from pathlib import Path

BASE = "https://backtest.onclickmedia.com/"
RESULT_PATH = Path("research/earnings_recovery/onclickmedia_four_event_feasibility_2026-10-10.json")
CASES = [
    ("DELL","day3","2025-03-06","2025-03-07"),
    ("DELL","rising_lows","2025-03-13","2025-03-17"),
    ("QCOM","day3","2025-08-05","2025-08-13"),
    ("QCOM","rising_lows","2025-08-13","2025-09-05"),
    ("PYPL","day3","2025-02-07","2025-02-21"),
    ("PYPL","rising_lows","2025-02-18","2025-02-24"),
    ("AMAT","day3","2025-02-20","2025-02-25"),
    ("AMAT","rising_lows","2025-02-21","2025-02-25"),
]
DTES=[30,60]
MONEYNESS=[-0.05,-0.10,-0.15,-0.20]
HEADERS={"User-Agent":"InvestingOS-HistoricalResearch/1.0", "Accept":"application/json"}

def get(url):
    request=urllib.request.Request(url,headers=HEADERS)
    with urllib.request.urlopen(request,timeout=20) as resp:
        return json.loads(resp.read(10_000_000).decode())

def post(data):
    request=urllib.request.Request(
        BASE+"?data=all&output=json",
        data=json.dumps(data).encode(),
        headers={**HEADERS,"Content-Type":"application/json"},
        method="POST")
    with urllib.request.urlopen(request,timeout=25) as resp:
        return json.loads(resp.read(10_000_000).decode())

def describe_error(err):
    if isinstance(err,urllib.error.HTTPError):
        try: body=err.read(1200).decode("utf-8","replace")
        except Exception:body=""
        return "HTTP %s: %s"%(err.code,body[:400])
    return type(err).__name__+": "+str(err)[:450]

def payload(ticker,entry,exitdate,dte,moneyness):
    return {
       "ticker":ticker,"portfolio_start":50,
       "start_date":entry,"end_date":exitdate,
       "real":True,"percent_per_trade":1,"max_invested":1,
       "distribution":"equal_contracts",
       "legs":[{"ticker":ticker,"type":"call","direction":"long",
         "percent_itm":moneyness,"days_till_expiration":dte,
         "rebalance_period":None,"fee_per_trade":0,
         "fee_per_contract":0.65,"prime":True,
         "stop_loss":None,"stop_profit":None,"stop_at_midpoint":False}],
       "stock":None
    }

def main():
    result={"as_of":"2026-10-10","provider":BASE,
            "meaning":"EOD bid/ask driven provider backtest; NOT an executable opening-price quote or an intraday stock-trigger fill",
            "events":CASES,"dte_targets":DTES,"fixed_moneyness":MONEYNESS,
            "budget_USD":50,"availability":{},"probes":[]}
    for ticker in ["DELL","QCOM","PYPL","AMAT"]:
        try:
            a=get(BASE+"?"+urllib.parse.urlencode({"ticker":ticker,"list":"date"}))
            s=json.dumps(a)
            dates=[(v if isinstance(v,str) else "") for v in (a if isinstance(a,list) else (a.get("dates") if isinstance(a,dict) and isinstance(a.get("dates"),list) else []))]
            result["availability"][ticker]={"ok":True,"dates_count":len(dates),
              "pilot_dates_present":{e:e in dates for t,m,e,x in CASES if t==ticker},
              "response_shape":type(a).__name__,
              "snippet":s[:250]}
        except Exception as err:
            result["availability"][ticker]={"ok":False,"error":describe_error(err)}
        time.sleep(0.3)
    # If ALL date lookups return errors, avoid pounding a nonworking provider.
    if not any(x.get("ok") for x in result["availability"].values()):
        result["status"]="UNREACHABLE: all availability checks failed, no POST requests attempted"
    else:
        for ticker,method,entry,exitdate in CASES:
            for dte in DTES:
                for m in MONEYNESS:
                    info={"ticker":ticker,"method":method,"entry":entry,"stock_exit":exitdate,"dte":dte,"percent_itm":m}
                    try:
                        a=post(payload(ticker,entry,exitdate,dte,m))
                        rows=a if isinstance(a,list) else a.get("data",[]) if isinstance(a,dict) else []
                        info.update({"ok":True,"rows":len(rows),"response_shape":type(a).__name__,
                           "first":rows[0] if rows else (a if isinstance(a,dict) else None),
                           "last":rows[-1] if rows else None,
                           "reported_errors":sorted(set(str(x.get("error")) for x in rows if isinstance(x,dict) and x.get("error"))),
                           "field_names":list(rows[0]) if rows and isinstance(rows[0],dict) else []})
                    except Exception as err:
                        info.update({"ok":False,"error":describe_error(err)})
                    result["probes"].append(info)
                    time.sleep(0.3)
        result["status"]="DONE: %d successful POST scenario responses; not yet validated actual historical bid/ask values"%sum(p.get("ok",False) for p in result["probes"])
    RESULT_PATH.parent.mkdir(parents=True,exist_ok=True)
    RESULT_PATH.write_text(json.dumps(result,indent=2,default=str)+"\n")
    print(json.dumps({"status":result["status"],"availability":result["availability"],
       "n_probes":len(result["probes"]),"successes":sum(x.get("ok",False) for x in result["probes"]),
       "sample":result["probes"][:1]},default=str)[:5000])

if __name__=="__main__":main()
