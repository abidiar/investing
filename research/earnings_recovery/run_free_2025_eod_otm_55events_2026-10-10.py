#!/usr/bin/env python3
"""Frozen 55-event 2025 earnings rebound audit, using free EOD option quotes.
Reuses previously frozen 164-event price windows and signal/stock-exit rules.
Outputs EOD quote proxy only; cannot verify first-option-trade volume or true fills.
NO PAID API KEY, NO FUTURE SHADOW TEST.
"""
from __future__ import annotations
import collections, concurrent.futures, datetime as dt, gzip, json, math, pathlib, random, threading, time, urllib.error, urllib.parse, urllib.request
BASE="https://www.dolthub.com/api/v1alpha1/post-no-preference/options/master"
ROOT=pathlib.Path("research/earnings_recovery")
INPUT=ROOT/"actionable_bounce_event_price_windows_164_2026-10-10.json"
OUTPUT=ROOT/"free_2025_eod_otm_55event_results_2026-10-10.json"
RAW=ROOT/"free_2025_eod_otm_55event_raw_quotes_2026-10-10.json.gz"
INDEX=7
HEADERS={"User-Agent":"InvestingOS-historical-frozen-research/1.0","Accept":"application/json"}
throttle=threading.Semaphore(3)

def iso_day(n):return dt.date.fromordinal(n).isoformat()
def asdate(s):return dt.date.fromisoformat(s)
def req(url, max_retries=2):
    errs=[]
    for retry in range(max_retries+1):
        try:
            with throttle:
                with urllib.request.urlopen(urllib.request.Request(url,headers=HEADERS),timeout=35) as r:
                    return json.loads(r.read(5_000_000).decode("utf8")), None
        except Exception as ex:
            e=type(ex).__name__+": "+str(ex)[:120]
            errs.append(e)
            if retry<max_retries:time.sleep((retry+1)*1.3)
    return None,errs[-1]

def yahoo(symbol):
    # Yahoo quote fields are split-adjusted, but not dividend-adjusted.
    start=int(dt.datetime(2024,12,20,tzinfo=dt.timezone.utc).timestamp())
    end=int(dt.datetime(2026,10,12,tzinfo=dt.timezone.utc).timestamp())
    result=None;errors=[]
    for host in ["query1.finance.yahoo.com","query2.finance.yahoo.com"]:
        url=f"https://{host}/v8/finance/chart/{urllib.parse.quote(symbol)}?period1={start}&period2={end}&interval=1d&events=split"
        result,err=req(url,max_retries=1)
        if result and result.get("chart",{}).get("result"):break
        errors.append(err)
    if not result or not result.get("chart",{}).get("result"):
        return {"ok":False,"error":str(errors)[:300]}
    z=result["chart"]["result"][0]
    stamps=z.get("timestamp",[])
    opens=z.get("indicators",{}).get("quote",[{}])[0].get("open",[])
    splitlist=z.get("events",{}).get("splits",{})
    splits=[]
    for spl in splitlist.values():
        r=float(spl.get("numerator",0))/float(spl.get("denominator",1)) if spl.get("denominator") else 0
        if r>0:
            sd=spl.get("date")
            try:
                date=dt.datetime.fromtimestamp(int(sd),dt.timezone.utc).date().isoformat() if isinstance(sd,(int,float)) or str(sd).isdigit() else str(sd)[:10]
            except (ValueError,TypeError,OverflowError):date=str(sd)[:10]
            splits.append({"date":date,"ratio":r})
    quotes={}
    for t,p in zip(stamps,opens):
        if p is None or not math.isfinite(float(p)):continue
        date=dt.datetime.fromtimestamp(t,dt.timezone.utc).date().isoformat()
        # Reverse only FUTURE splits relative to a 2025 historical entry.
        mult=math.prod(a["ratio"] for a in splits if a["date"]>date)
        quotes[date]=round(float(p)*mult,7)
    return {"ok":True,"quotes":quotes,"splits":splits,"source":"Yahoo chart raw (split-reversed)"}

def parse_cash(x):
    try:
        n=float(x)
        return n if math.isfinite(n) else None
    except (TypeError,ValueError):return None

def signal(e):
    b=e["bars"];event=INDEX; n=len(b)
    ans={"day3":event+3,"rising_lows":None}
    for t in range(event+3,min(event+21,n-1)):
        if b[t-2][3]<=b[t-1][3] and b[t-1][3]<=b[t][3] and b[t][4]>max(b[t-2][2],b[t-1][2]):
            ans["rising_lows"]=t+1 if b[t+1][1]<=1.08*b[event][4] else None
            break
    return ans

def stock_exit(b,i):
    entry=b[i][1]
    target=entry*1.05;stop=entry*.95
    for j in range(i,min(i+20,len(b))):
        date,op,hi,lo,cl=b[j][:5]
        if j>i and op<=stop:return {"date":date,"reason":"stop_gap","spot_proxy":op,"entry":entry,"i":i,"j":j}
        if j>i and op>=target:return {"date":date,"reason":"target_gap","spot_proxy":op,"entry":entry,"i":i,"j":j}
        if lo<=stop:return {"date":date,"reason":"stop","spot_proxy":stop,"entry":entry,"i":i,"j":j}
        if hi>=target:return {"date":date,"reason":"target","spot_proxy":target,"entry":entry,"i":i,"j":j}
    j=min(i+19,len(b)-1)
    return {"date":b[j][0],"reason":"time","spot_proxy":b[j][4],"entry":entry,"i":i,"j":j}

def chain(ticker,date,spot):
    # Freeze both upper strike bound and exact date; strips any providers not needed.
    q=(f"SELECT date, expiration, strike, call_put, bid, ask, vol, delta "
       f"FROM option_chain WHERE act_symbol = '{ticker}' AND date = '{date}' "
       f"AND call_put = 'Call' AND strike > {spot:.5f} "
       f"AND strike <= {spot*1.25:.5f} ORDER BY expiration,strike LIMIT 1000")
    url=BASE+"?"+urllib.parse.urlencode({"q":q})
    resp,err=req(url)
    if err:return {"status":"ERROR","error":err,"rows":[]}
    if resp.get("query_execution_status")!="Success":
        return {"status":"QUERY_ERROR","error":str(resp.get("query_execution_message","unknown"))[:300],"rows":[]}
    return {"status":"OK","rows":resp.get("rows",[]),"truncated":len(resp.get("rows",[]))>=1000}

def quote_valid(x):
    bid,ask=parse_cash(x.get("bid")),parse_cash(x.get("ask"))
    return bid is not None and ask is not None and ask>0 and 0<=bid<=ask

def choose(entr,leave,entryDate,expiryDays):
    d=asdate(entryDate);minExp=d+dt.timedelta(days=expiryDays);maxExp=minExp+dt.timedelta(days=7)
    e=[x for x in entr if minExp<=asdate(str(x["expiration"])[:10])<=maxExp]
    all_exp=sorted(set(str(x["expiration"])[:10] for x in e))
    chosen_exp=all_exp[0] if all_exp else None
    opts=[x for x in e if str(x["expiration"])[:10]==chosen_exp and quote_valid(x)]
    afford=sorted([x for x in opts if float(x["ask"])*100+.65<=50 and parse_cash(x.get("strike"))],key=lambda x:float(x["strike"]))
    selected=afford[0] if afford else None
    info={"dte":expiryDays,"observed_expiry_count":len(all_exp),"sampled_first_expiry":chosen_exp,"sampled_quoted_strikes":len(opts),
          "affordable_EOD_asks_in_first_expiry":len(afford),
          "selection_status":"NO_QUOTED_EXPIRY" if not chosen_exp else "NO_AFFORDABLE_EOD_ASK" if not selected else "SELECTED_EOD_PROXY",
          "NO_VOLUME_DATA":True}
    if not selected:return info
    exp=str(selected["expiration"])[:10];strike=float(selected["strike"]);ask=float(selected["ask"]);bid=float(selected["bid"])
    info.update({"expiry":exp,"strike":strike,"delta":parse_cash(selected.get("delta")),"entry_iv":parse_cash(selected.get("vol")),
       "entry_bid":bid,"entry_ask":ask,"entry_ask_cost":round(ask*100+.65,2),"entry_spread_pct_of_ask":round((ask-bid)/ask*100,2)})
    found=next((x for x in leave if str(x["expiration"])[:10]==exp and float(x["strike"])==strike and quote_valid(x)),None)
    if found:
        exitbid=float(found["bid"]);revenue=max(0,100*exitbid-.65);cost=100*ask+.65
        info.update({"exit_quote_present":True,"exit_bid":exitbid,"exit_ask":float(found["ask"]),"exit_iv":parse_cash(found.get("vol")),
                    "eod_ask_to_bid_return_pct":round(100*(revenue-cost)/cost,3),
                    "exit_after_premium_pct":round(100*revenue/cost,3)})
    else:info["exit_quote_present"]=False;info["selection_status"]="NO_MATCHED_EXIT_EOD_QUOTE"
    return info

def go():
    allobj=json.loads(INPUT.read_text())
    events=sorted([x for x in allobj["series"] if x["date"].startswith("2025-")],
       key=lambda x:(x["date"],x["ticker"],x["cohort"]))
    assert len(events)==55 and collections.Counter(x["cohort"] for x in events)=={"original92":29,"holdout72":26}
    symbols=sorted({x["ticker"] for x in events})
    print(f"START {len(events)} events, {len(symbols)} unique tickers",flush=True)
    # Fetch independent unadjusted historical spot once per ticker.
    prices={}
    with concurrent.futures.ThreadPoolExecutor(max_workers=3) as pool:
        futures={pool.submit(yahoo,t):t for t in symbols}
        for fut in concurrent.futures.as_completed(futures):
            ticker=futures[fut]
            try:prices[ticker]=fut.result()
            except Exception as e:prices[ticker]={"ok":False,"error":str(e)[:120]}
            print(f"SPOT {ticker} {prices[ticker].get('ok')} count={len(prices[ticker].get('quotes',{}))}",flush=True)
    cases=[];requests=[]
    for e in events:
        for method,i in signal(e).items():
            c={"ticker":e["ticker"],"cohort":e["cohort"],"event":e["date"],"method":method}
            if i is None or i>=len(e["bars"]):
                c["status"]="NO_SIGNAL";cases.append(c);continue
            when=e["bars"][i][0];x=stock_exit(e["bars"],i)
            c.update({"entry":when,"stock_entry_adjusted_open":e["bars"][i][1],"stock_exit":x["date"],
              "exit_reason":x["reason"],"underlying_entry_to_exit_pct":round(100*(x["spot_proxy"]/x["entry"]-1),4)})
            y=prices[e["ticker"]]
            spot=y.get("quotes",{}).get(when) if y.get("ok") else None
            c["stock_spot_method"]=y.get("source") if y.get("ok") else "MISSING"
            c["stock_splits"]=y.get("splits",[])
            if not spot or spot<=0:
                c["status"]="MISSING_UNADJUSTED_SPOT";cases.append(c);continue
            c["underlying_unadjusted_open"]=spot
            c["underlying_saved_adjusted_ratio"]=round(spot/e["bars"][i][1],6)
            # A massive mismatch usually signifies split/OCC adjustment. Exclude rather than construct wrong strike.
            ratio=spot/e["bars"][i][1]
            expected_factor=math.prod(z["ratio"] for z in y.get("splits",[]) if z["date"]>when)
            c["reversed_future_split_factor"]=round(expected_factor,5)
            if ratio/max(0.000001,expected_factor)<.67 or ratio/max(0.000001,expected_factor)>1.5:
                c["status"]="SOURCE_PRICE_SCALE_CONFLICT";cases.append(c);continue
            if any(when<s["date"]<=x["date"] for s in y.get("splits",[])):
                c["status"]="SPLIT_DURING_HOLD";cases.append(c);continue
            c["status"]="READY_FOR_EOD_QUOTE_CHECK";cases.append(c)
            requests.append((e["ticker"],when,round(spot,5)))
            requests.append((e["ticker"],x["date"],round(spot,5)))
    request_keys=sorted(set(requests))
    print(f"SETUPS {len(cases)} cache queries {len(request_keys)}",flush=True)
    cache={}
    with concurrent.futures.ThreadPoolExecutor(max_workers=3) as pool:
        futs={pool.submit(chain,*key):key for key in request_keys}
        for n,fut in enumerate(concurrent.futures.as_completed(futs),1):
            key=futs[fut]
            try:cache[key]=fut.result()
            except Exception as e:cache[key]={"status":"ERROR","error":str(e)[:100],"rows":[]}
            if n%20==0:print(f"QUOTES {n}/{len(request_keys)} successes={sum(z['status']=='OK' for z in cache.values())}",flush=True)
    for c in cases:
        if c["status"]!="READY_FOR_EOD_QUOTE_CHECK":continue
        ticker=c["ticker"];spot=round(c["underlying_unadjusted_open"],5)
        ent=cache[(ticker,c["entry"],spot)];exit_=cache[(ticker,c["stock_exit"],spot)]
        c["quote_entry_status"]=ent["status"];c["quote_exit_status"]=exit_["status"]
        c["entry_quote_rows"]=len(ent.get("rows",[]));c["exit_quote_rows"]=len(exit_.get("rows",[]))
        if ent["status"]!="OK" or exit_["status"]!="OK":
            c["status"]="QUOTE_SOURCE_INCOMPLETE";continue
        c["status"]="EOD_QUOTE_READ"
        for days in [30,60]:
            c[f"eod_{days}"]=choose(ent["rows"],exit_["rows"],c["entry"],days)
    out={"asof":"2026-10-10","frozenSource":str(INPUT),"cohorts":{"original92":29,"holdout72":26},
      "scope":"55 preexisting 2025 historical events; two fixed entry methods, 30/60 sampled EOD expiry buckets. Research only, outcome previously inspected.",
      "CAVEAT":"EOD bid/ask source lacks volume, and is not contemporaneous with next OPEN entry or intraday stock trigger. This is NOT the original first-option-trade, >=10-volume, actionable options backtest.",
      "quotesProvider":BASE,"quote_queries":len(request_keys),
      "quote_status_counts":dict(collections.Counter(x["status"] for x in cache.values())),
      "price_source_status":{x:{"ok":v.get("ok"),"error":v.get("error"),"splits":v.get("splits")} for x,v in prices.items()},
      "setups":cases}
    for cohort in ["original92","holdout72"]:
        for method in ["day3","rising_lows"]:
            ev=[x for x in cases if x["cohort"]==cohort and x["method"]==method]
            st=dict(collections.Counter(x["status"] for x in ev))
            data={"cohort":cohort,"method":method,"n_events":len(ev),"setup_status":st,"dtes":{}}
            for dte in [30,60]:
                col=[x.get(f"eod_{dte}",{}) for x in ev]
                ret=[x["eod_ask_to_bid_return_pct"] for x in col if "eod_ask_to_bid_return_pct" in x]
                data["dtes"][str(dte)]={
                   "n_with_entry_and_exit_EOD_bidask":len(ret),
                   "n_with_affordable_entry_ask":sum(x.get("entry_ask_cost") is not None for x in col),
                   "no_quote_match":sum(x.get("selection_status")=="NO_MATCHED_EXIT_EOD_QUOTE" for x in col),
                   "no_expiry":sum(x.get("selection_status")=="NO_QUOTED_EXPIRY" for x in col),
                   "no_affordable_ask":sum(x.get("selection_status")=="NO_AFFORDABLE_EOD_ASK" for x in col),
                   "mean_return_pct":round(sum(ret)/len(ret),3) if ret else None,
                   "median_return_pct":sorted(ret)[len(ret)//2] if len(ret)%2 else (round((sorted(ret)[len(ret)//2-1]+sorted(ret)[len(ret)//2])/2,3) if ret else None),
                   "positive_count":sum(v>0 for v in ret)}
            out.setdefault("grouped",[]).append(data)
    OUTPUT.write_text(json.dumps(out,indent=2)+"\n")
    with gzip.open(RAW,"wt") as g:
        json.dump({"source":BASE,"date":"2026-10-10","cache":{str(k):v for k,v in cache.items()},
          "raw_unadjusted_price_sources":prices},g)
    print(json.dumps({"cases":len(cases),"query_count":len(request_keys),"quote_statuses":out["quote_status_counts"],
       "setup_states":dict(collections.Counter(c["status"] for c in cases)),"grouped":out.get("grouped")},default=str)[:15000],flush=True)

if __name__=="__main__":go()
