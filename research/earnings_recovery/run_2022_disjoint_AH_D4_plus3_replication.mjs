/**
 * Reproduce 2022 AH disjoint-company historical rebound replication from
 * already archived Webull daily-price windows. This script only reads the
 * FROZEN price windows and does not query providers.
 *
 * node research/earnings_recovery/run_2022_disjoint_AH_D4_plus3_replication.mjs
 *
 * Protocol was committed before the historical trade outcomes were read.
 * This is gross/illustrative-net STOCK price analysis; not option returns.
 */
import fs from 'node:fs';
import path from 'node:path';
const dir='research/earnings_recovery';
const input=JSON.parse(fs.readFileSync(path.join(dir,'disjoint_2022_14issuer_ah_earnings_rth_source_windows_2026-10-11.json'),'utf8'));
function trade(b,k){
 const buy=b[k]?.[1];if(!Number.isFinite(buy))return {state:'MISSING_ENTRY'};
 const t=buy*1.03,s=buy*.95;
 for(let x=k;x<k+20;x++){
  if(!b[x])return {state:'MISSING_FOLLOWUP'};
  const [date,op,hi,lo,cl]=b[x];let state,px,reason;
  if(x>k&&op<=s){state='STOP';px=op;reason='GAP_STOP'}
  else if(x>k&&op>=t){state='TARGET';px=op;reason='GAP_TARGET'}
  else if(lo<=s){state='STOP';px=s;reason=hi>=t?'STOP_FIRST_BOTH_HIT':'STOP_TOUCH'}
  else if(hi>=t){state='TARGET';px=t;reason='TARGET_TOUCH'}
  else if(x===k+19){state='TIMEOUT';px=cl;reason='TIMEOUT'}
  if(state)return{state,entryPrice:buy,entryDate:b[k][0],exitDate:date,exitPrice:px,grossPct:(px/buy-1)*100,netPct:(px/buy-1)*100-.2,heldSessions:x-k+1,fillReason:reason};
 }
}
const events=[];
for(const v of input.events){
 const b=v.bars;let j=b.findIndex(x=>x[0]===v.announcementDate);
 if(j<0)throw Error('Missing earnings day '+v.ticker+' '+v.announcementDate);
 const p=b[j][4];let k=null;
 if(b[j+1][4]<=.95*p)k=j+1;
 else if(b[j+2][4]<=.95*p)k=j+2;
 const qualified=k!==null;
 const dip=qualified&&Math.min(...b.slice(k+1,k+4).map(x=>x[3]))<b[k][3];
 let firstLow=null;
 if(qualified)for(let d=1;d<=10;d++)if(b[k+d][3]<b[k][3]){firstLow=d;break}
 let w=null;
 if(qualified){let min=Math.min(...b.slice(k+1,k+6).map(x=>x[3]));w=b.slice(k+1,k+6).findIndex(x=>x[3]===min)+1;}
 events.push({ticker:v.ticker,announcementDate:v.announcementDate,qualified,earlyDipByD3:dip,d0:qualified?b[k][0]:null,
 firstAdditionalLowDay:firstLow,lowD1toD5Day:w,D4:qualified?trade(b,k+4):null,D6:qualified?trade(b,k+6):null});
}
function stats(x,k){
 const a=x.map(y=>y[k]).filter(y=>y&&Number.isFinite(y.grossPct));
 return {entries:a.length,targets:a.filter(y=>y.state==='TARGET').length,stops:a.filter(y=>y.state==='STOP').length,timeouts:a.filter(y=>y.state==='TIMEOUT').length,meanGrossPct:a.reduce((s,y)=>s+y.grossPct,0)/a.length,meanNetPct:a.reduce((s,y)=>s+y.netPct,0)/a.length};
}
let q=events.filter(x=>x.qualified),d=q.filter(x=>x.earlyDipByD3),no=q.filter(x=>!x.earlyDipByD3);
const report={announcements:events.length,qualified:q.length,earlyDipByD3:d.length,
 earlyDipD4:stats(d,'D4'),earlyDipD6:stats(d,'D6'),noDipD4:stats(no,'D4'),
 allQualifiedD4:stats(q,'D4'),rows:events};
process.stdout.write(JSON.stringify(report,null,2)+'\n');
