/**
 * Reproduce the 2026-10-11 quality-164 pre-D4 sector/macro factor audit.
 * From a clone of abidiar/investing: node research/earnings_recovery/run_quality164_asofD3_sector_market_v1.mjs > /tmp/result.json
 * Requires only already committed local JSON and OHLC archives. No network.
 */
import fs from 'node:fs';
import path from 'node:path';
const dir='research/earnings_recovery',read=f=>JSON.parse(fs.readFileSync(path.join(dir,f),'utf8'));
const prior=read('matched_quality164_fundamentals_v1_all_events_pairs_2026-10-11.json');
const events=[...read('actionable_bounce_price_windows_92events_2026-10-10.json').events,
 ...read('actionable_bounce_price_windows_72events_2026-10-10.json').events];
const quotes=read('frozen_source_spdr_sector_etf_daily_1200_2026-10-11.json').quotes;
const sectorMap={
 XLK:['ADBE','AMAT','AMD','ANET','CRM','CRWD','CSCO','DELL','FSLR','FTNT','GLW','HPE','IBM','KLAC','MPWR','NOW','PANW','QCOM','TXN'],
 XLC:['CMCSA','DIS','GOOG','NFLX'],XLY:['ABNB','LEN','LOW','SBUX','TPR'],
 XLP:['DG','DLTR','HSY','KDP','KR','TGT'],XLE:['COP','EOG','HAL','OKE'],
 XLF:['COIN','FIS','GPN','PYPL'],XLV:['CVS','EW','GILD','ISRG','REGN','TMO','ZBH'],
 XLI:['ADP','CPRT','DAL','FDX','GE','HON','JCI','NOC','UPS','WAB'],XLB:['DOW','NEM']
};
const sect=new Map();for(const [s,names] of Object.entries(sectorMap))for(const n of names){if(sect.has(n))throw Error('Dup ETF');sect.set(n,s)}
if(sect.size!==61)throw Error('missing sector');
const q=Object.fromEntries(Object.entries(quotes).map(([s,arr])=>[s,{list:arr,byDate:new Map(arr),index:new Map(arr.map((x,i)=>[x[0],i]))}]));
const base=new Map(prior.events.map(x=>[x.ticker+'|'+x.selloffDate,x]));
function gain(o,start,end){const a=o.byDate.get(start),b=o.byDate.get(end);if(a===undefined||b===undefined)throw Error('Missing ETF date '+start+' -> '+end);return 100*(b/a-1)}
const cases=[];
for(const e of events){
 const b=e.bars,d=e.event_index,ref=base.get(e.ticker+'|'+e.selloff_date);
 if(!ref||!b[d+60])throw Error('Incomplete event '+e.ticker);
 const sec=sect.get(e.ticker),s=q[sec],market=q.SPY;
 const initial=ref.session==='AH'?b.find(x=>x[0]===e.earnings_date):b[b.findIndex(x=>x[0]===e.earnings_date)-1];
 if(!initial)throw Error('Missing actual pre-release close');
 const D0=b[d],D3=b[d+3],D60=b[d+60],si=s.index.get(D0[0]),mi=market.index.get(D0[0]);
 if(si===undefined||mi===undefined||si<21||mi<21)throw Error('Insufficient ETF lookback '+D0[0]);
 const shock=100*(D0[4]/initial[4]-1),sector03=gain(s,D0[0],D3[0]),market03=gain(market,D0[0],D3[0]);
 cases.push({ticker:e.ticker,cohort:e.cohort,sector:sec,year:ref.year,
 session:ref.session,earningsDate:e.earnings_date,selloffDate:e.selloff_date,
 initialStockShockPct:shock,fullRecovery60d:ref.fullRecovery60d,
 d4TradeWin:ref.tradeWin,d4HypNetPct:ref.trade.hypNetPct,
 earlyLowerLowByD3:ref.earlyLowerLowByD3,features:{
 preSector20Pct:100*(s.list[si-1][1]/s.list[si-21][1]-1),
 preSPY20Pct:100*(market.list[mi-1][1]/market.list[mi-21][1]-1),
 sectorD0ToD3Pct:sector03,spyD0ToD3Pct:market03,
 sectorMinusSPYD0D3Pp:sector03-market03,
 stockMinusSectorD0D3Pp:100*(D3[4]/D0[4]-1)-sector03,
 shockMinusSectorD0Pp:shock-gain(s,initial[0],D0[0]),
 sectorD0ToD60Pct:gain(s,D0[0],D60[0]),
 spyD0ToD60Pct:gain(market,D0[0],D60[0])
 }});
}
if(cases.length!==164||cases.filter(x=>x.session==='AH').length!==91)throw Error('Wrong cohort');
const median=x=>{if(!x.length)return null;x=[...x].sort((a,b)=>a-b);return(x[Math.floor((x.length-1)/2)]+x[Math.floor(x.length/2)])/2};
const mean=x=>x.length?x.reduce((a,b)=>a+b,0)/x.length:null;
const fields=Object.keys(cases[0].features);
const pval=(a,b)=>{let n=a+b;if(!n)return null;let p=0;for(let k=0;k<=Math.min(a,b);k++){let c=1;for(let i=1;i<=k;i++)c*=(n-i+1)/i;p+=c/2**n}return Math.min(1,p*2)};
function summary(rows,win){
 const a=rows.filter(win),b=rows.filter(x=>!win(x));
 return {n:rows.length,winner:a.length,nonwinner:b.length,
 features:Object.fromEntries(fields.map(k=>[k,{
 winnerMedian:median(a.map(x=>x.features[k])),loserMedian:median(b.map(x=>x.features[k])),
 winnerMean:mean(a.map(x=>x.features[k])),loserMean:mean(b.map(x=>x.features[k]))}]))};
}
function match(rows,isWinner){
 const positive=rows.filter(isWinner).sort((a,b)=>Math.abs(a.initialStockShockPct)-Math.abs(b.initialStockShockPct)||a.ticker.localeCompare(b.ticker)||a.selloffDate.localeCompare(b.selloffDate));
 const negative=rows.filter(x=>!isWinner(x)),used=new Set(),pairs=[],unmatched=[];
 for(const a of positive){
  const eligible=negative.filter(b=>b.year===a.year&&b.session===a.session&&b.sector===a.sector&&b.ticker!==a.ticker
  &&!used.has(b.ticker+'|'+b.selloffDate)&&Math.abs(Math.abs(b.initialStockShockPct)-Math.abs(a.initialStockShockPct))<=5)
  .sort((b,c)=>Math.abs(Math.abs(b.initialStockShockPct)-Math.abs(a.initialStockShockPct))-Math.abs(Math.abs(c.initialStockShockPct)-Math.abs(a.initialStockShockPct))||b.ticker.localeCompare(c.ticker)||b.selloffDate.localeCompare(c.selloffDate));
  if(!eligible.length){unmatched.push(a.ticker+'|'+a.selloffDate);continue}
  const b=eligible[0];used.add(b.ticker+'|'+b.selloffDate);
  pairs.push({case:a.ticker+'|'+a.selloffDate,control:b.ticker+'|'+b.selloffDate,
  year:a.year,session:a.session,sector:a.sector,initialShockGapPp:Math.abs(a.initialStockShockPct-b.initialStockShockPct),
  deltas:Object.fromEntries(fields.map(k=>[k,a.features[k]-b.features[k]]))});
 }
 return{cases:positive.length,controls:negative.length,n:pairs.length,unmatched:unmatched.length,
 bySession:{AH:pairs.filter(x=>x.session==='AH').length,BMO:pairs.filter(x=>x.session==='BMO').length},
 features:Object.fromEntries(fields.map(k=>{let x=pairs.map(p=>p.deltas[k]),up=x.filter(z=>z>0).length,down=x.filter(z=>z<0).length;
 return[k,{pairs:x.length,medianWinMinusLoser:median(x),meanWinMinusLoser:mean(x),winnerHigher:up,winnerLower:down,signTwoSidedP:pval(up,down)}]})),
 pairs,unmatchedCases:unmatched};
}
const both=r=>({recovery60:summary(r,x=>x.fullRecovery60d),d4:summary(r,x=>x.d4TradeWin)});
const groups={all164:both(cases),AH91:both(cases.filter(x=>x.session==='AH')),
 AH54Early:both(cases.filter(x=>x.session==='AH'&&x.earlyLowerLowByD3)),
 original92:both(cases.filter(x=>x.cohort==='original92')),
 disjoint72:both(cases.filter(x=>x.cohort==='separate72')),
 yearSplit:Object.fromEntries([2023,2024,2025,2026].map(y=>[y,both(cases.filter(x=>x.year===y))]))};
const result={experiment:'quality164_asof_D3_sector_risk_factors_v1_2026-10-11',
 status:'EXPLORATORY_PRECOMMITTED_CONTRAST_KNOWN_OUTCOMES_NOT_CAUSAL',
 source:'frozen_source_spdr_sector_etf_daily_1200_2026-10-11.json',
 protocol:'frozen_quality164_sector_market_preD4_recovery_factors_2026-10-11.md',
 coverage:{cases:164,missing:0,AH:91,BMO:73},
 mapping:Object.fromEntries([...sect].map(([ticker,s])=>[ticker,s])),
 groups,matched:{fullRecovery60:match(cases,x=>x.fullRecovery60d),d4StockFirstHit:match(cases,x=>x.d4TradeWin)},events:cases};
process.stdout.write(JSON.stringify(result,null,2)+'\n');
