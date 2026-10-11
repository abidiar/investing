/**
 * FROZEN EVENT-LEVEL DIAGNOSTIC: 49 issuer-disjoint range-break VWAP reclaim, Oct 11 2026
 * Protocol: research/swing_two_session/frozen_issuer_disjoint_range_vwap_replication_v2_2026_10_11.md
 * Execution memo committed BEFORE downloading the 106 two-session M5 paths:
 * research/swing_two_session/source_gate_106_pre_outcome_memo_2026_10_11.md
 * Run from repository root: node research/swing_two_session/run_disjoint49_m5_vwap_outcome_diagnostic_v2_2026_10_11.mjs
 * Writes JSON to STDOUT; redirect to research/swing_two_session/data/...
 * THE SOURCE-CERTIFICATION GATE HAS NOT BEEN COMPLETED: diagnostic, NOT production validation.
 */
import fs from "node:fs";
import path from "node:path";
const dir="research/swing_two_session/data";
const read=(name)=>JSON.parse(fs.readFileSync(path.join(dir,name),"utf8"));
const universe=read("disjoint49_daily_screen_preliminary_2026_10_11.json").candidates;
const qa=Array.from({length:6},(_,i)=>read("qa_106_signal_day_m5_batch"+String(i+1).padStart(2,"0")+"_2026_10_11.json").records).flat();
const raw=Array.from({length:6},(_,i)=>read("forward_two_session_m5_diagnostic_batch"+String(i+1).padStart(2,"0")+"_2026_10_11.json").results).flat();
if(universe.length!==106||qa.length!==106||raw.length!==106)throw Error("FROZEN 106 denominator altered");
const k=v=>v.symbol+"|"+(v.signalDate||v.date),byQA=new Map(qa.map(v=>[k(v),v])),byRaw=new Map(raw.map(v=>[k(v),v]));
if(byQA.size!==106||byRaw.size!==106)throw Error("Duplicate or missing event keys");
const etf=new Intl.DateTimeFormat("en-US",{timeZone:"America/New_York",hour:"2-digit",minute:"2-digit",hour12:false});
function minutesNY(b){const z=etf.formatToParts(new Date(b[0].replace("+0000","Z")));return 60*Number(z.find(x=>x.type==="hour").value)+Number(z.find(x=>x.type==="minute").value)}
function exitAt(candles,j,buy){
 const stop=buy*0.98,target=buy*1.02;
 for(let i=j;i<candles.length;i++){
  const b=candles[i],op=b[1],hi=b[2],lo=b[3],close=b[4];
  if(![op,hi,lo,close].every(x=>Number.isFinite(x)&&x>0))return {status:"UNKNOWN_BAD_CANDLE",grossPct:null};
  if(op<=stop)return {status:"STOP_GAP",exit:i,exitPrice:op,grossPct:100*(op/buy-1)};
  if(op>=target)return {status:"TARGET_GAP",exit:i,exitPrice:op,grossPct:100*(op/buy-1)};
  const hitS=lo<=stop,hitT=hi>=target;
  if(hitS)return {status:hitT?"STOP_FIRST_SAME_BAR":"STOP",exit:i,exitPrice:stop,grossPct:-2};
  if(hitT)return {status:"TARGET",exit:i,exitPrice:target,grossPct:2};
 }
 return {status:"TIMEOUT",exit:candles.length-1,exitPrice:candles.at(-1)[4],grossPct:100*(candles.at(-1)[4]/buy-1)};
}
function getEntry(day){
 let sumVP=0,sumVol=0,seenBelow=false,above=0;
 for(let i=0;i<day.length;i++){
  const b=day[i],vol=b[5];
  if(vol<0||!Number.isFinite(vol))return {type:"UNKNOWN_BAD_VOLUME"};
  sumVP+=((b[2]+b[3]+b[4])/3)*vol;sumVol+=vol;
  if(!sumVol)continue;
  const vwap=sumVP/sumVol;
  if(b[4]<vwap){seenBelow=true;above=0;continue}
  if(!seenBelow)continue;
  if(b[4]>vwap){above++;} else {above=0;}
  if(above>=2){const next=day[i+1];if(!next||minutesNY(next)>720)return {type:"SKIP_AFTER_NOON"};
   return {type:"ENTRY",barIndex:i+1,entryTimeNY:minutesNY(next),entryTimestamp:next[0],price:next[1],confirmationBarEndNY:minutesNY(b)+5};
  }
 }
 return {type:"SKIP_NO_TRIGGER"};
}
const records=universe.map(e=>{
 const id=k(e),q=byQA.get(id),x=byRaw.get(id);
 if(!q||!x)throw Error("missing "+id);
 const base={symbol:e.symbol,date:e.date,year:e.date.slice(0,4),countByDay:x.countByDay,sessionDates:x.sessionDates,dailySourceEventVolumeRatio:q.ratioDToM5};
 const incomplete=q.barCount!==78||x.countByDay.length!==2||x.countByDay.some(n=>n!==78);
 if(incomplete)return {...base,status:"UNKNOWN_INCOMPLETE_RTH",vwEntry:null,openBenchmark:null};
 const day1=x.bars.slice(0,78),day2=x.bars.slice(78),candles=[...day1,...day2];
 if(candles.length!==156)return {...base,status:"UNKNOWN_LENGTH",vwEntry:null,openBenchmark:null};
 for(let i=1;i<candles.length;i++)if(!(candles[i][0]>candles[i-1][0]))throw Error("Bar time not increasing "+id);
 const overnight=day2[0][1]/day1.at(-1)[4];
 if(overnight<0.5||overnight>2)return {...base,status:"UNKNOWN_POSSIBLE_SPLIT",overnightRatio:overnight,vwEntry:null,openBenchmark:null};
 const opening=exitAt(candles,0,day1[0][1]);
 const gate=getEntry(day1);
 const vw=gate.type==="ENTRY"?exitAt(candles,gate.barIndex,gate.price):null;
 return {...base,status:"EVALUABLE",openBenchmark:{entryPrice:day1[0][1],...opening},vwEntry:{...gate,...(vw||{})},openingGrossPct:opening.grossPct,vwGrossPct:vw?vw.grossPct:0,entered:!!vw,targetFirst:!!vw&&vw.status.startsWith("TARGET"),stopFirst:!!vw&&vw.status.startsWith("STOP"),timeOut:!!vw&&vw.status==="TIMEOUT"};
});
const evaluated=records.filter(x=>x.status==="EVALUABLE");
const missing=records.filter(x=>x.status!=="EVALUABLE");
const mean=x=>x.length?x.reduce((s,v)=>s+v,0)/x.length:null;
function stat(xs,cost){
 const trades=xs.filter(x=>x.entered),costVW=xs.map(x=>x.entered?x.vwGrossPct-cost:0),costOpen=xs.map(x=>x.openingGrossPct-cost),paired=costVW.map((v,i)=>v-costOpen[i]);
 return {allSignals:xs.length,entries:trades.length,skips:xs.length-trades.length,
  targets:trades.filter(x=>x.targetFirst).length,stops:trades.filter(x=>x.stopFirst).length,timeouts:trades.filter(x=>x.timeOut).length,
  meanVwPerOriginalSignalPct:mean(costVW),meanVwPerEnteredPct:mean(trades.map(x=>x.vwGrossPct-cost)),
  meanOpeningPerOriginalPct:mean(costOpen),meanPairedVWminusOpeningPp:mean(paired)};
}
function rng(seed){let state=seed>>>0;return ()=>{state^=state<<13;state^=state>>>17;state^=state<<5;return ((state>>>0)/4294967296)}}
function pctile(a,p){a.sort((x,y)=>x-y);return a[Math.floor(p*(a.length-1))]}
function bootstrap(xs,cost=0.5,n=10000,seed=20261011){
 const map=new Map();for(const x of xs){if(!map.has(x.symbol))map.set(x.symbol,[]);map.get(x.symbol).push(x)}
 const symbols=[...map.keys()].sort(),random=rng(seed),v=[],diff=[];
 for(let i=0;i<n;i++){let nSum=0,aSum=0,dSum=0;for(let j=0;j<symbols.length;j++){
  const sym=symbols[Math.floor(random()*symbols.length)];for(const x of map.get(sym)){
    const va=x.entered?x.vwGrossPct-cost:0;const op=x.openingGrossPct-cost;
    nSum++;aSum+=va;dSum+=va-op
   }}
  v.push(aSum/nSum);diff.push(dSum/nSum)
 }
 return {replicates:n,tickerClusters:symbols.length,seed,CI95MeanNetVWPerOriginalPct:[pctile(v,.025),pctile(v,.975)],CI95PairedVWMinusOpenPp:[pctile(diff,.025),pctile(diff,.975)]};
}
const costs=Object.fromEntries([0,0.2,0.5,1].map(c=>[String(c),stat(evaluated,c)]));
const byYear=Object.fromEntries(["2024","2025","2026"].map(y=>[y,stat(evaluated.filter(x=>x.year===y),.5)]));
const byTicker=Object.fromEntries([...new Set(evaluated.map(x=>x.symbol))].sort().map(t=>[t,stat(evaluated.filter(x=>x.symbol===t),.5)]));
const contributions=Object.entries(byTicker).map(([ticker,v])=>({ticker,netSumPct:v.meanVwPerOriginalSignalPct*v.allSignals,events:v.allSignals,entries:v.entries})).sort((x,y)=>y.netSumPct-x.netSumPct);
const pos=contributions.filter(x=>x.netSumPct>0),sumPos=pos.reduce((s,x)=>s+x.netSumPct,0);
const share=sumPos?100*pos.slice(0,3).reduce((s,x)=>s+x.netSumPct,0)/sumPos:null;
const bs=bootstrap(evaluated,.5);
const promo={noOutcomeSelection:true,eventsAtLeast40:evaluated.length>=40,issuersAtLeast12:bs.tickerClusters>=12,entriesAtLeast25:costs["0.5"].entries>=25,positive50bpNetLowerBound:bs.CI95MeanNetVWPerOriginalPct[0]>0,pairedNetImprovement50bpLowerBound:bs.CI95PairedVWMinusOpenPp[0]>0,top3PositiveContributionAtMost50Pct:share!==null&&share<=50,
 FULL_49_sourceBasisVerified:false,ALL_sourceComplete:missing.length===0,overallDecision:"RESEARCH_ONLY_FULL_V2_SOURCE_GATE_NOT_CERTIFIED_REGARDLESS_OF_NUMERIC_RESULT"};
const output={id:"v2_49_issuer_disjoint_vwap_raw_m5_two_session_outcome_diagnostic_2026_10_11",status:"DIAGNOSTIC_ONLY_NOT_V2_PRODUCTION_CERTIFIED",reproScript:"research/swing_two_session/run_disjoint49_m5_vwap_outcome_diagnostic_v2_2026_10_11.mjs",sourceArchives:Array.from({length:6},(_,i)=>"research/swing_two_session/data/forward_two_session_m5_diagnostic_batch"+String(i+1).padStart(2,"0")+"_2026_10_11.json"),sample:{totalFrozenDailyCandidates:records.length,evaluable:evaluated.length,dataUnknown:missing.map(x=>({s:x.symbol,date:x.date,reason:x.status,days:x.countByDay}))},costs,byYear,byTicker,top3ShareOfPositiveTickerNetPct:share,topContributors:contributions.slice(0,12),bootstrap50bps:bs,promotionChecks:promo,records};
process.stdout.write(JSON.stringify(output,null,2)+"\n");
