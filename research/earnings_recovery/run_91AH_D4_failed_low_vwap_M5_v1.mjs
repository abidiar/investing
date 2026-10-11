/**
 * Reproduce 91-AH intraday selloff D4 first failed low + VWAP participation study.
 * node research/earnings_recovery/run_91AH_D4_failed_low_vwap_M5_v1.mjs
 * Files previously saved via Webull M5. No network, no options prices.
 * Time stop and data completeness are frozen in protocol.
 */
import fs from 'node:fs';
import path from 'node:path';
const dir='research/earnings_recovery';
const rd=f=>JSON.parse(fs.readFileSync(path.join(dir,f),'utf8'));
const roster=rd('roster_91AH_exact_D4_D6_M5_v1_2026-10-11.json').roster;
const source=[
 ...rd('raw_12AH_3d_webull_M5_OHLCV_2026-10-11.json').records.map(x=>({
 ticker:x.symbol,d4:x.d4,d5:x.d5,d6:x.d6,bars:x.bars,oldPilot:true
 })),
 ...Array.from({length:8},(_,i)=>rd('raw_79AH_M5_expansion_part'+i+'_2026-10-11.json').records)
];
const median=a=>{if(!a.length)return null;a=[...a].sort((a,b)=>a-b);return(a[Math.floor((a.length-1)/2)]+a[Math.floor(a.length/2)])/2};
const mean=a=>a.length?a.reduce((s,x)=>s+x,0)/a.length:null;
function trade(b,index){
 if(index===null)return{state:'SKIP',net:0,gross:0};
 const entry=b[index][1],stop=entry*.99,target=entry*1.02;
 for(let i=index;i<b.length;i++){
  const z=b[i];let type='',exit=0,why='';
  if(i>index&&z[1]<=stop){type='STOP';exit=z[1];why='GAP_STOP';}
  else if(i>index&&z[1]>=target){type='TARGET';exit=z[1];why='GAP_TARGET';}
  else if(z[3]<=stop){type='STOP';exit=stop;why=z[2]>=target?'BOTH_SAME_CANDLE_STOP_FIRST':'STOP_TOUCH';}
  else if(z[2]>=target){type='TARGET';exit=target;why='TARGET_TOUCH';}
  else if(i===b.length-1){type='TIMEOUT';exit=z[4];why='THIRD_DAY_CLOSE';}
  if(type){const gross=100*(exit/entry-1);return{state:type,entryIndex:index,entryTime:b[index][0],entry,
   exitTime:z[0],exit,why,gross,net:gross-.2,barsHeld:i-index+1};}
 }
 throw Error('No timeout');
}
function scan(all){
 const b=all.slice(0,78),vw=[];let v=0,pv=0;
 b.forEach((z,i)=>{v+=z[5];pv+=(z[2]+z[3]+z[4])/3*z[5];vw.push(pv/v);});
 const volok=i=>i>=4&&b[i][5]>=median(b.slice(i-Math.min(6,i),i).map(z=>z[5]));
 const cross=i=>b[i-1][4]<=vw[i-1]&&b[i][4]>vw[i]&&b[i][4]>b[i][1];
 let kfail=null;
 for(let k=3;k<=21;k++){
  const earlier=Math.min(...b.slice(0,k).map(z=>z[3]));
  if(b[k][3]<earlier&&b[k][4]>earlier&&b[k][4]>(b[k][2]+b[k][3])/2){kfail=k;break;}
 }
 let confirm=null,crossCount=0,qualifiedCount=0,chaseRejections=0;
 if(kfail!==null){
  for(let j=kfail+1;j<=Math.min(kfail+6,26);j++){
   if(!cross(j))continue;
   crossCount++;
   if(!volok(j))continue;
   qualifiedCount++;
   const entry=b[j+1][1];
   if(j+1<=30&&entry<=b[0][1]*1.015&&entry<=b[kfail][3]*1.02){confirm=j;break;}
   chaseRejections++;
  }
 }
 let vwapEntry=null;
 for(let j=4;j<=27;j++){
  if(!cross(j)||!volok(j))continue;
  const low=Math.min(...b.slice(0,j+1).map(z=>z[3])),entry=b[j+1][1];
  if(j+1<=30&&entry<=b[0][1]*1.015&&entry<=low*1.02){vwapEntry=j+1;break;}
 }
 const pidx=confirm===null?null:confirm+1,primary=trade(all,pidx);
 return{
  failedLowCandidateIndex:kfail,failedLowCandidateTime:kfail===null?null:b[kfail][0],
  confirmIndex:confirm,confirmTime:confirm===null?null:b[confirm][0],
  reclaimCrossesAfterCandidate:crossCount,volumeQualified:qualifiedCount,chaseRejections,
  entryMoveVsD4OpenPct:pidx===null?null:100*(primary.entry/b[0][1]-1),
  entryAdvanceVsKnownLowPct:pidx===null?null:100*(primary.entry/Math.min(...b.slice(0,pidx).map(z=>z[3]))-1),
  primary,vwapOnly:trade(all,vwapEntry),baseline0950:trade(all,4)
 };
}
function minute(t){const x=t.slice(11,16).split(':').map(Number);return x[0]*60+x[1];}
const bySource=new Map(source.map(x=>[x.ticker+'|'+x.d4,x]));
if(bySource.size!==91||roster.length!==91)throw Error('Coverage uniqueness discrepancy '+bySource.size);
const events=roster.map(m=>{
 const r=bySource.get(m.ticker+'|'+m.d4);
 if(!r)return{...m,status:'NO_SOURCE'};
 const dates=[m.d4,m.d5,m.d6],sessions=dates.map(d=>r.bars.filter(b=>b[0].slice(0,10)===d));
 const counts=sessions.map(a=>a.length);
 const startsEnds=sessions.map(a=>a.length?{start:a[0][0],end:a.at(-1)[0]}:null);
 const dayQuality=sessions.every(a=>a.length>=75&&
   [810,870].includes(minute(a[0][0])) && [1195,1255].includes(minute(a.at(-1)[0])));
 const morningComplete=sessions[0].length>=31&&
  sessions[0].slice(0,31).every((b,i)=>minute(b[0])===minute(sessions[0][0][0])+5*i);
 if(!dayQuality||!morningComplete)return{...m,status:'DATA_INVALID',counts,startsEnds,morningComplete};
 return{...m,status:'VALID',counts,startsEnds,morningComplete,...scan(sessions.flat())};
});
const valid=events.filter(x=>x.status==='VALID');
function stats(arr,key){
 const trades=arr.map(x=>x[key]),entered=trades.filter(x=>x.state!=='SKIP');
 return{eligible:arr.length,entered:entered.length,skipped:trades.length-entered.length,
  targets:entered.filter(x=>x.state==='TARGET').length,stops:entered.filter(x=>x.state==='STOP').length,
  timeouts:entered.filter(x=>x.state==='TIMEOUT').length,
  targetRatePerEntryPct:entered.length?100*entered.filter(x=>x.state==='TARGET').length/entered.length:null,
  meanNetPerEntryPct:mean(entered.map(x=>x.net)),medianNetPerEntryPct:median(entered.map(x=>x.net)),
  meanNetPerEligibleEventSkippingZeroPct:mean(trades.map(x=>x.net))};
}
function group(arr){
 const signals=arr.filter(e=>e.primary.state!=='SKIP');
 return{eligible:arr.length,signals:signals.length,failedLowFound:arr.filter(e=>e.failedLowCandidateIndex!==null).length,
 reclaimAfterFailed:arr.filter(e=>e.reclaimCrossesAfterCandidate>0).length,
 volumeQualifiedAfterFailed:arr.filter(e=>e.volumeQualified>0).length,
 chaseRejectedEvents:arr.filter(e=>e.chaseRejections>0).length,
 medianSignalAdvanceFromKnownLowPct:median(signals.map(e=>e.entryAdvanceVsKnownLowPct)),
 medianSignalMoveFromOpeningPct:median(signals.map(e=>e.entryMoveVsD4OpenPct)),
 primary:stats(arr,'primary'),vwapOnly:stats(arr,'vwapOnly'),baseline0950:stats(arr,'baseline0950'),
 avgPrimaryMinusBaselinePct:mean(arr.map(e=>e.primary.net-e.baseline0950.net)),
 avgVWAPMinusBaselinePct:mean(arr.map(e=>e.vwapOnly.net-e.baseline0950.net)),
 };
}
const result={id:'D4_failedLow_vwapVolume_91AH_M5_2026-10-11',
 frozen:'frozen_91AH_D4_failed_low_vwap_volume_M5_expansion_2026-10-11.md',
 source:'raw_12AH_3d_webull_M5_OHLCV_2026-10-11.json and raw_79AH_M5_expansion_part0..7_2026-10-11.json',
 status:'RETROSPECTIVE_OUTCOME_EXPOSED_NOT_VALIDATED_OPTIONS',
 coverage:{all:91,valid:valid.length,invalid:events.filter(x=>x.status!=='VALID').map(x=>({ticker:x.ticker,day:x.d4,reason:x.status,counts:x.counts,startsEnds:x.startsEnds,morningComplete:x.morningComplete}))},
 groups:{allValid:group(valid),priorPilot:group(valid.filter(x=>x.oldPilot)),
 new79:group(valid.filter(x=>!x.oldPilot)),
 originalCohort:group(valid.filter(x=>x.cohort==='original92')),
 separateCohort:group(valid.filter(x=>x.cohort==='separate72')),
 priorD4StockWinners:group(valid.filter(x=>x.oldD4Win)),
 priorD4StockNonWinners:group(valid.filter(x=>!x.oldD4Win)),
 byYear:Object.fromEntries([2023,2024,2025,2026].map(y=>[y,group(valid.filter(x=>x.d4.startsWith(String(y))))]))},
 events};
process.stdout.write(JSON.stringify(result,null,2)+'\n');
