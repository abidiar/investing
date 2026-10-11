#!/usr/bin/env python3
"""As-of previous day's 4pm prior-close call shortlist across ALL 55 2025 earnings events.
Historical data only. No call selected using its entry-day end-of-day quote.
"""
import concurrent.futures,collections,datetime as dt,json,math,pathlib,threading,time,urllib.parse,urllib.request,urllib.error
ROOT=pathlib.Path('research/earnings_recovery')
PRE=ROOT/'free_2025_eod_otm_55event_results_2026-10-10.json'
STOCK=ROOT/'actionable_bounce_event_price_windows_164_2026-10-10.json'
OUT=ROOT/'nonlookahead_priorclose_2025_55events_selections_2026-10-10.json'
RAW=ROOT/'nonlookahead_priorclose_2025_55events_rawchains_2026-10-10.json'
BASE='https://www.dolthub.com/api/v1alpha1/post-no-preference/options/master'
HEADER={'User-Agent':'Mozilla/5.0 HistoricalEarningsCallResearch/1.0','Accept':'application/json'}
limiter=threading.Semaphore(3)
def get(url,attempts=3):
 errors=[]
 for z in range(attempts):
  try:
   with limiter,urllib.request.urlopen(urllib.request.Request(url,headers=HEADER),timeout=40) as f:
    return json.loads(f.read(5_000_000)),None
  except Exception as e:
   errors.append(str(e)[:130]);time.sleep(0.4*(z+1))
 return None,errors[-1]
def yahoo(t):
 start=int(dt.datetime(2024,12,1,tzinfo=dt.timezone.utc).timestamp());end=int(dt.datetime(2026,10,12,tzinfo=dt.timezone.utc).timestamp())
 for host in ['query1.finance.yahoo.com','query2.finance.yahoo.com']:
  obj,err=get('https://'+host+'/v8/finance/chart/'+urllib.parse.quote(t)+'?period1='+str(start)+'&period2='+str(end)+'&interval=1d&events=split',2)
  if obj and obj.get('chart',{}).get('result'):break
 if not obj or not obj.get('chart',{}).get('result'):return {'status':'ERROR','error':err}
 a=obj['chart']['result'][0];splits=[]
 for q in a.get('events',{}).get('splits',{}).values():
  n=float(q.get('numerator',0));d=float(q.get('denominator',1))
  if d and n:
   when=q.get('date')
   date=dt.datetime.fromtimestamp(when,dt.timezone.utc).date().isoformat() if isinstance(when,(float,int)) else str(when)[:10]
   splits.append({'date':date,'ratio':n/d})
 dates=a.get('timestamp',[]);q=a.get('indicators',{}).get('quote',[{}])[0];closes={}
 for k,stamp in enumerate(dates):
  x=q.get('close',[None]*len(dates))[k]
  if x is None or not math.isfinite(float(x)):continue
  day=dt.datetime.fromtimestamp(stamp,dt.timezone.utc).date().isoformat()
  mult=math.prod(s['ratio'] for s in splits if s['date']>day)
  closes[day]=round(float(x)*mult,6)
 return {'status':'OK','closes':closes,'splits':splits}
def quote(t,date,spot):
 sql=(f"SELECT date, expiration, strike, bid, ask, vol, delta, call_put "
      f"FROM option_chain WHERE act_symbol = '{t}' AND date = '{date}' "
      f"AND call_put = 'Call' AND strike > {spot:.5f} AND strike <= {spot*1.25:.5f} "
      f"ORDER BY expiration, strike LIMIT 1000")
 result,err=get(BASE+'?'+urllib.parse.urlencode({'q':sql}),3)
 if err:return {'status':'ERROR','error':err,'rows':[]}
 if result.get('query_execution_status')!='Success':
  return {'status':'QUERY_ERROR','error':str(result.get('query_execution_message',''))[:160],'rows':[]}
 return {'status':'OK','rows':result.get('rows',[]),'truncated':len(result.get('rows',[]))>=1000}
def numeric(s):
 try:
  x=float(s)
  if math.isfinite(x):return x
 except (ValueError,TypeError):pass
 return None
def select(rows,entry,dte):
 start=dt.date.fromisoformat(entry)+dt.timedelta(days=dte)
 end=start+dt.timedelta(days=7)
 expiration=sorted(set(str(q['expiration'])[:10] for q in rows
                       if start<=dt.date.fromisoformat(str(q['expiration'])[:10])<=end))
 if not expiration:return {'status':'NO_PREVIOUS_DAY_EXPIRATION_OBSERVED','dte':dte}
 expiry=expiration[0]
 all_exp=[q for q in rows if str(q['expiration'])[:10]==expiry]
 eligible=[]
 for q in all_exp:
  bid=numeric(q.get('bid'));ask=numeric(q.get('ask'));strike=numeric(q.get('strike'))
  if None in (bid,ask,strike) or ask<=0 or bid<0 or ask<bid:continue
  if ask*100+.65>50 or (ask-bid)/ask>0.35:continue
  eligible.append((strike,q))
 if not eligible:return {'status':'NO_PREVIOUS_DAY_AFFORDABLE_TIGHT_SPREAD_CALL','dte':dte,'sampled_expiry':expiry,'strikes_in_expiry':len(all_exp)}
 eligible.sort(key=lambda x:x[0])
 q=eligible[0][1]
 return {'status':'PRESELECTED_PRIOR_CLOSE_ONLY','dte':dte,'sampled_expiry':expiry,
         'strike':numeric(q['strike']),'prior_bid':numeric(q['bid']),'prior_ask':numeric(q['ask']),
         'prior_total_ask_debit':round(numeric(q['ask'])*100+.65,2),
         'prior_quote_spread_pct':round(100*(numeric(q['ask'])-numeric(q['bid']))/numeric(q['ask']),3),
         'prior_iv':numeric(q.get('vol')),'prior_delta':numeric(q.get('delta')),
         'strikes_in_expiry':len(all_exp),'preselected_candidate_count':len(eligible),
         'volume_available_prev_day':False,'no_entry_day_price_lookahead':True}
def main():
 inputs=json.loads(PRE.read_text());saved=json.loads(STOCK.read_text())['series']
 lookup={(x['ticker'],x['date'],x['cohort']):x for x in saved}
 cases=[dict(c) for c in inputs['setups']]
 assert len(cases)==110
 pairs=[]
 for c in cases:
  if not c.get('entry'):continue
  ref=lookup[(c['ticker'],c['event'],c['cohort'])]
  i=next((i for i,b in enumerate(ref['bars']) if b[0]==c['entry']),None)
  c['_last_session_before_entry']=ref['bars'][i-1][0] if i is not None and i>0 else None
 symbols=sorted({c['ticker'] for c in cases})
 prices={}
 with concurrent.futures.ThreadPoolExecutor(max_workers=3) as pool:
  futs={pool.submit(yahoo,t):t for t in symbols}
  for f in concurrent.futures.as_completed(futs):
   t=futs[f]
   try:prices[t]=f.result()
   except Exception as e:prices[t]={'status':'ERROR','error':str(e)[:130]}
   print('CLOSE',len(prices),len(symbols),t,prices[t]['status'],flush=True)
 for c in cases:
  c['prior_close_date']=c.pop('_last_session_before_entry',None)
  if not c.get('entry'):
   c['priorclose_status']='NO_SIGNAL';continue
  day=c['prior_close_date']
  stock=prices[c['ticker']]
  value=stock.get('closes',{}).get(day)
  if value is None:
   c['priorclose_status']='MISSING_HISTORICAL_RAW_CLOSE';continue
  c['priorclose_status']='READY'
  c['prior_unadjusted_stock_close']=value
  pairs.append((c['ticker'],day,round(value,5)))
 unique=sorted(set(pairs))
 print('PRIOR_CHAINS',len(unique),flush=True)
 cache={}
 with concurrent.futures.ThreadPoolExecutor(max_workers=3) as pool:
  futs={pool.submit(quote,*z):z for z in unique}
  for i,f in enumerate(concurrent.futures.as_completed(futs),1):
   z=futs[f]
   try:cache[z]=f.result()
   except Exception as e:cache[z]={'status':'ERROR','error':str(e)[:170],'rows':[]}
   if i%15==0:print('CHAINS',i,len(unique),flush=True)
 for c in cases:
  if c['priorclose_status']!='READY':continue
  z=(c['ticker'],c['prior_close_date'],round(c['prior_unadjusted_stock_close'],5))
  q=cache[z];c['priorclose_source_status']=q['status'];c['priorclose_chain_rows']=len(q.get('rows',[]))
  if q['status']!='OK':
   c['priorclose_status']='PRIOR_CLOSE_CHAIN_SOURCE_MISSING';continue
  for dte in [30,60]:
   c[f'prior_dte_{dte}']=select(q['rows'],c['entry'],dte)
   sel=c[f'prior_dte_{dte}']
   if sel['status']=='PRESELECTED_PRIOR_CLOSE_ONLY':
    x=int(round(sel['strike']*1000))
    sel['occ']='O:'+c['ticker']+sel['sampled_expiry'][2:].replace('-','')+'C'+str(x).zfill(8)
 out={'frozen':'frozen_nonlookahead_prior_close_1000am_historical_option_protocol_2026-10-10.md',
      'provider':'DoltHub historical EOD option chains, previous trading day only; Yahoo underlying raw previous CLOSE',
      'caveat':'Candidate options selected ONLY using information dated before 2025 entry; actual entry 10am intraday option trade/volume and ask remain unverified; no options returns calculated. As-of 10am volume must use historical 9:30-9:55 bars, not end-of-day session volume.',
      'events':55,'cases':cases,'case_count':len(cases),'unique_provider_queries':len(unique),
      'query_statuses':dict(collections.Counter(x['status'] for x in cache.values())),
      'setup_statuses':dict(collections.Counter(x['priorclose_status'] for x in cases)),
      'selected_30':sum(c.get('prior_dte_30',{}).get('status')=='PRESELECTED_PRIOR_CLOSE_ONLY' for c in cases),
      'selected_60':sum(c.get('prior_dte_60',{}).get('status')=='PRESELECTED_PRIOR_CLOSE_ONLY' for c in cases),
      'selected_unique_events':len(set((c['ticker'],c['event']) for c in cases if any(c.get(f'prior_dte_{n}',{}).get('status')=='PRESELECTED_PRIOR_CLOSE_ONLY' for n in [30,60] )))}
 OUT.write_text(json.dumps(out,indent=2)+'\n')
 RAW.write_text(json.dumps({'snapshots':{str(k):v for k,v in cache.items()},'stock_close_metadata':{k:{'status':x['status'],'splits':x.get('splits')} for k,x in prices.items()}},indent=2)+'\n')
 print(json.dumps({k:v for k,v in out.items() if k not in ['cases']},indent=2),flush=True)
if __name__=='__main__':main()
