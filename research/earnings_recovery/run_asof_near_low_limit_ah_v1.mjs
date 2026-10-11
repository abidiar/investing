/**
 * Deterministic reproducible v1 exploratory study: post-earnings secondary-low
 * observed before D3 close → BUY LIMIT at 101% of the D1-D3 observed minimum.
 *
 * node research/earnings_recovery/run_asof_near_low_limit_ah_v1.mjs
 * Prints original per-event JSON to stdout. Source files must be present in
 * research/earnings_recovery/. Adjusted daily stock OHLC, not option quotes.
 */
import fs from 'node:fs';
import path from 'node:path';
const dir='research/earnings_recovery';
const read=n=>fs.readFileSync(path.join(dir,n),'utf8');
function parseCSV(txt) {
 const split=l=>{
  let rows=[],s='',inside=false;
  for(let i=0;i<l.length;i++) {
   const c=l[i];
   if(c==='"'&&inside&&l[i+1]==='"'){s+='"';i++}
   else if(c==='"')inside=!inside;
   else if(c===','&&!inside){rows.push(s);s=''}
   else s+=c;
  }
  rows.push(s);return rows;
 };
 const lines=txt.trim().split(/\r?\n/),h=split(lines.shift());
 return lines.map(l=>Object.fromEntries(split(l).map((v,i)=>[h[i],v])));
}
const roster=[
 ...JSON.parse(read('actionable_bounce_price_windows_92events_2026-10-10.json')).events,
 ...JSON.parse(read('actionable_bounce_price_windows_72events_2026-10-10.json')).events
];
const lookup=new Map([
 ...parseCSV(read('earnings_selloff_recovery_92events_2026-10-10.csv')),
 ...parseCSV(read('holdout_final_136events_2026-10-10.csv'))
].map(r=>[r.ticker+'|'+r.selloff_date,r]));
function manage(b,k,entry,atOpen,targetPct=3,stopPct=5,hold=20) {
 const upper=entry*(1+targetPct/100),lower=entry*(1-stopPct/100);
 for(let z=k;z<k+hold;z++) {
  const x=b[z];
  if(!x)return {type:'INCOMPLETE',entry,entryDate:b[k][0],atOpen};
  const [date,open,high,low,close]=x;
  let type=null,price=null;
  if(z>k&&open<=lower){type='STOP';price=open}
  else if(z>k&&open>=upper){type='TARGET';price=open}
  else if(low<=lower){type='STOP';price=lower}
  else if((z>k||atOpen)&&high>=upper){type='TARGET';price=upper}
  else if(z===k+hold-1){type='TIMEOUT';price=close}
  if(type)return {
   type,entry,entryDate:b[k][0],atOpen,exit:price,exitDate:date,
   gross:100*(price/entry-1),net:100*(price/entry-1)-.2,
   holding:z-k+1
  };
 }
}
const rows=[];
for(const e of roster) {
 const match=lookup.get(e.ticker+'|'+e.selloff_date);
 if(!match)throw Error('No metadata for '+e.ticker+' '+e.selloff_date);
 if(match.session!=='AH')continue;
 const b=e.bars,d=e.event_index,d0low=b[d][3];
 const knownLow=Math.min(...b.slice(d+1,d+4).map(x=>x[3]));
 const eligible=knownLow<d0low,limit=1.01*knownLow;
 let fill=null;
 if(eligible){
  for(let k=d+4;k<=d+6;k++){
   const bar=b[k];
   if(!bar)throw Error('Missing early window '+e.ticker);
   if(bar[1]<=limit){fill={index:k,price:bar[1],atOpen:true,mechanism:'opening_marketability'};break}
   if(bar[3]<limit){fill={index:k,price:limit,atOpen:false,mechanism:'intraday_low_touch'};break}
  }
 }
 rows.push({
  cohort:e.cohort,ticker:e.ticker,earningsDate:e.earnings_date,
  selloffDate:e.selloff_date,eventDrop:e.selloff_pct,eligible,
  previousD0low:d0low,knownD1toD3low:knownLow,
  limit:eligible?limit:null,
  fillDay:fill?b[fill.index][0]:null,fillDayNumber:fill?fill.index-d:null,
  fillMechanism:fill?fill.mechanism:null,
  limitTrade:fill?manage(b,fill.index,fill.price,fill.atOpen):null,
  d4:eligible?manage(b,d+4,b[d+4][1],true):null,
  d6:eligible?manage(b,d+6,b[d+6][1],true):null,
  allD6:manage(b,d+6,b[d+6][1],true)
 });
}
const avg=a=>a.length?a.reduce((s,x)=>s+x,0)/a.length:null;
const med=a=>{
 a=[...a].sort((u,v)=>u-v);
 return a.length?(a[Math.floor((a.length-1)/2)]+a[Math.floor(a.length/2)])/2:null;
};
function group(a){
 const n=a.length,eligible=a.filter(r=>r.eligible),fills=a.filter(r=>r.limitTrade),joined=fills.filter(r=>Number.isFinite(r.limitTrade?.gross)&&Number.isFinite(r.d6?.gross)&&Number.isFinite(r.d4?.gross));
 const stat=key=>{
  const list=a.map(key).filter(Boolean),ok=list.filter(t=>Number.isFinite(t.gross));
  return {
   n:list.length,complete:ok.length,
   targets:ok.filter(t=>t.type==='TARGET').length,
   stops:ok.filter(t=>t.type==='STOP').length,
   timeouts:ok.filter(t=>t.type==='TIMEOUT').length,
   meanGross:avg(ok.map(t=>t.gross)),
   meanNet:avg(ok.map(t=>t.net)),
   sumNet:ok.reduce((s,t)=>s+t.net,0),
   meanNetPerAll:ok.reduce((s,t)=>s+t.net,0)/n,
   meanNetPerEligible:ok.reduce((s,t)=>s+t.net,0)/eligible.length,
   medianHold:med(ok.map(t=>t.holding))
  };
 };
 return {
  allN:n,eligible:eligible.length,fill:fills.length,
  unfilled:eligible.length-fills.length,
  fillD4:fills.filter(r=>r.fillDayNumber===4).length,
  fillD5:fills.filter(r=>r.fillDayNumber===5).length,
  fillD6:fills.filter(r=>r.fillDayNumber===6).length,
  fillAtOpen:fills.filter(r=>r.fillMechanism==='opening_marketability').length,
  fillIntraday:fills.filter(r=>r.fillMechanism==='intraday_low_touch').length,
  limit:stat(r=>r.limitTrade),marketD4:stat(r=>r.d4),
  marketD6:stat(r=>r.d6),allD6:stat(r=>r.allD6),
  paired:{
   n:joined.length,
   meanLimit:avg(joined.map(r=>r.limitTrade.gross)),
   meanD6:avg(joined.map(r=>r.d6.gross)),
   meanD4:avg(joined.map(r=>r.d4.gross)),
   meanDiffVsD6:avg(joined.map(r=>r.limitTrade.gross-r.d6.gross)),
   meanDiffVsD4:avg(joined.map(r=>r.limitTrade.gross-r.d4.gross)),
   winsVsD6:joined.filter(r=>r.limitTrade.gross>r.d6.gross).length,
   limitTargets:joined.filter(r=>r.limitTrade.type==='TARGET').length,
   D6Targets:joined.filter(r=>r.d6.type==='TARGET').length,
   meanObservedPctOverKnownLowAtFill:avg(joined.map(r=>100*(r.limitTrade.entry/r.knownD1toD3low-1))),
   medianObservedPctOverKnownLowAtFill:med(joined.map(r=>100*(r.limitTrade.entry/r.knownD1toD3low-1)))
  }
 };
}
const out={
 name:'ah_near_low_asof_limit_retest_v1',date:'2026-10-11',
 status:'HISTORICAL_EXPLORATORY_OUTCOMES_PREVIOUSLY_KNOWN',
 method:'As-of observed D1..D3 low, buy at 101% of min D1..D3 low D4..D6, +3%/-5%, 20 bars, stop-first, 20bp stock cost',
 summary:{all:group(rows),original:group(rows.filter(x=>x.cohort==='original92')),separate:group(rows.filter(x=>x.cohort==='separate72'))},
 rows
};
process.stdout.write(JSON.stringify(out,null,2)+'\n');
