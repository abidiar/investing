#!/usr/bin/env python3
"""Stage 1: freeze ALL Jul-Sep 2026 <= -5% first-session earnings reactions
from a pre-frozen issuer universe, WITHOUT fetching post-event OHLC returns.
"""
import concurrent.futures, datetime as dt, json, pathlib, re, time, urllib.request, urllib.error
from bs4 import BeautifulSoup
P=pathlib.Path("research/earnings_recovery")
OUT=P/"frozen_jul_sep2026_earnings_selloff_discovery_2026-10-10.json"
UNIVERSE="ABNB ADBE ADP AMAT AMD ANET CMCSA COIN COP CPRT CRM CRWD CSCO CVS DAL DELL DG DIS DLTR DOW EOG EW FDX FIS FSLR FTNT GE GILD GLW GOOG GPN HAL HON HPE HSY IBM ISRG JCI KDP KLAC KR LEN LOW MPWR NEM NFLX NOC NOW OKE PANW PYPL QCOM REGN SBUX TGT TMO TPR TXN UPS WAB ZBH".split()
assert len(UNIVERSE)==61
start,end="2026-07-01","2026-09-04"
def date(s):
 x=re.sub(r"\s+"," ",s.replace(".","")).strip()
 # Date may be e.g. "Aug 13, 2026" or full month
 for fmt in ["%b %d, %Y","%B %d, %Y","%Y-%m-%d"]:
  try:return dt.datetime.strptime(x,fmt).date().isoformat()
  except ValueError:pass
 return None
def get(ticker):
 url=f"https://quant500.com/earnings-date/{ticker}"
 detail={"ticker":ticker,"source":url,"fetch_status":"UNKNOWN","all_2026_window_announcements":[],"candidate_reactions":[]}
 for retry in range(3):
  try:
   request=urllib.request.Request(url,headers={"User-Agent":"Mozilla/5.0 (compatible; HistoricalResearch/1.0)","Accept":"text/html"})
   with urllib.request.urlopen(request,timeout=30) as r:html=r.read(900000).decode("utf8","replace")
   break
  except Exception as ex:
   detail["fetch_error"]=str(ex)[:150];time.sleep(.65*(retry+1))
 else:
  detail["fetch_status"]="HTTP_FAIL";return detail
 soup=BeautifulSoup(html,"html.parser")
 tables=soup.find_all("table")
 dates=[];reaction=[]
 for table in tables:
  rows=table.find_all("tr")
  if not rows:continue
  hdr=[x.get_text(" ",strip=True).lower() for x in rows[0].find_all(["th","td"])]
  if hdr and "quarter ended" in " ".join(hdr) and "announcement" in " ".join(hdr):
   for row in rows[1:]:
    c=[x.get_text(" ",strip=True) for x in row.find_all(["td","th"])]
    if len(c)<4:continue
    d=date(c[0]);session=c[3].lower()
    if d and start<=d<=end:dates.append({"announcement":d,"session":session,"label":c[0],"filing_sec_link_available":bool(row.find("a",href=re.compile("sec.gov")))})
  if hdr and "window" in " ".join(hdr) and "announcement" in " ".join(hdr):
   for row in rows[1:]:
    c=[x.get_text(" ",strip=True) for x in row.find_all(["td","th"])]
    if len(c)<4:continue
    d=date(c[0])
    if not d or not (start<=d<=end):continue
    sess=c[1].lower()
    match=re.search(r"([+\-−–]?\d+(?:\.\d+)?)\s*%",c[3])
    if not match:continue
    pct=float(match.group(1).replace("−","-").replace("–","-"))
    window=c[2].replace("–>","→")
    right=date(window.split("→")[-1].strip()) if "→" in window else None
    reaction.append({"announcement":d,"session":sess,"stock_reaction_close_pct":pct,"selloff_session":right,
                    "source_window":window,"quote_column":c[3]})
 detail["fetch_status"]="OK"
 detail["all_2026_window_announcements"]=dates
 detail["candidate_reactions"]=reaction
 if not reaction and dates:detail["fetch_status"]="MISSING_REACTION_PRICE_TABLE"
 return detail
def main():
 print("FROZEN UNIVERSE",len(UNIVERSE),flush=True)
 found=[]
 with concurrent.futures.ThreadPoolExecutor(max_workers=4) as pool:
  futs={pool.submit(get,t):t for t in UNIVERSE}
  for i,f in enumerate(concurrent.futures.as_completed(futs),1):
   t=futs[f]
   try:res=f.result()
   except Exception as e:res={"ticker":t,"source":f"https://quant500.com/earnings-date/{t}","fetch_status":"ERROR","fetch_error":str(e)[:140],"all_2026_window_announcements":[],"candidate_reactions":[]}
   found.append(res)
   if i%10==0:print("FETCHED",i,"/",len(UNIVERSE),flush=True)
 found.sort(key=lambda x:x["ticker"])
 valid=[]
 for x in found:
  for e in x["candidate_reactions"]:
   sess=e["session"].lower()
   okay=sess in ("after the close","before the open","bmo","ah","before open","after close")
   if not okay or not e["selloff_session"] or e["stock_reaction_close_pct"]> -5.0:continue
   source_announcement=next((z for z in x["all_2026_window_announcements"] if z["announcement"]==e["announcement"]),None)
   if not source_announcement or not source_announcement["filing_sec_link_available"]:continue
   valid.append({"ticker":x["ticker"],"earnings_announcement":e["announcement"],"selloff_day":e["selloff_session"],"session":e["session"],
                 "reaction_close_pct":e["stock_reaction_close_pct"],"window":e["source_window"],"source":x["source"]})
 valid.sort(key=lambda x:(x["selloff_day"],x["ticker"]))
 out={"freeze_date":"2026-10-10","source":"Quant500 SEC-linked earnings date/session and one-session closing reaction ONLY, no subsequent historical outcome prices consulted",
      "window":[start,end],"precommitted_61_issuers":UNIVERSE,"issuer_coverage":found,
      "selected_events":valid,"selected_count":len(valid),"unique_selected_tickers":len(set(z["ticker"] for z in valid)),
      "fetch_status_counts":{x:sum(z["fetch_status"]==x for z in found) for x in sorted(set(z["fetch_status"] for z in found))},
      "post_event_price_outcomes_in_this_file":False}
 OUT.write_text(json.dumps(out,indent=2)+"\n")
 print(json.dumps({"saved":str(OUT),"selected":valid,"fetch_status_counts":out["fetch_status_counts"],
                   "window_announcement_count":sum(len(z["all_2026_window_announcements"]) for z in found)},indent=2),flush=True)
if __name__=="__main__":main()
