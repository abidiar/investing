/**
 * Reproduce AH delayed-secondary-low one-day stabilization v0.1.
 * Node 18+; run from repository root:
 * node research/earnings_recovery/run_ah_delayed_secondary_dip_oneday_stabilization_v0_1.mjs
 * Archived price files must be present in same directory. Price OHLC is adjusted
 * historical daily data, no volume or options premium. This is exploratory only.
 */
import fs from "node:fs";
import path from "node:path";
const dir="research/earnings_recovery";
const file=n=>fs.readFileSync(path.join(dir,n),"utf8");
const main=[...JSON.parse(file("actionable_bounce_price_windows_92events_2026-10-10.json")).events,
...JSON.parse(file("actionable_bounce_price_windows_72events_2026-10-10.json")).events];
function parseCsv(text){
 const c=s=>{let out=[],v="",quoted=false;for(let i=0;i<s.length;i++){
  const x=s[i];if(x==='"'&&quoted&&s[i+1]==='"'){v+='"';i++}
  else if(x==='"'){quoted=!quoted}
  else if(x===","&&!quoted){out.push(v);v=""}else{v+=x}
 }out.push(v);return out};
 const lines=text.trim().split(/\r?\n/),headers=c(lines.shift());
 return lines.map(x=>Object.fromEntries(c(x).map((v,i)=>[headers[i],v])));
}
const lookup=new Map([
...parseCsv(file("earnings_selloff_recovery_92events_2026-10-10.csv")),
...parseCsv(file("holdout_final_136events_2026-10-10.csv"))
].map(r=>[r.ticker+"|"+r.selloff_date,r]));
function runTrade(b,i,stopPct=5,hold=20){
 if(!b[i])return {state:"INCOMPLETE_ENTRY"};
 const entry=b[i][1],target=entry*1.05,stop=entry*(1-stopPct/100);
 for(let k=i;k<i+hold;k++){
  if(!b[k])return {state:"INCOMPLETE_EXIT",entry,entryDay:b[i][0]};
  const [date,o,h,l,c]=b[k];
  let state,exit,reason;
  if(k>i && o<=stop){state="STOP";exit=o;reason="GAP_STOP"}
  else if(k>i && o>=target){state="TARGET";exit=o;reason="GAP_TARGET"}
  else if(l<=stop){state="STOP";exit=stop;reason=h>=target?"SAME_BAR_STOP_FIRST":"STOP_TOUCH"}
  else if(h>=target){state="TARGET";exit=target;reason="TARGET_TOUCH"}
  else if(k===i+hold-1){state="TIMEOUT";exit=c;reason="TIMEOUT_CLOSE"}
  if(state){const pct=100*(exit/entry-1);return {state,entry,entryDay:b[i][0],exit,exitDay:date,reason,pct,netPct:pct-0.2,days:k-i+1}}
 }
}
const rows=[];
for(const e of main){
 const join=lookup.get(e.ticker+"|"+e.selloff_date);
 if(!join)throw Error("no release time "+e.ticker+" "+e.selloff_date);
 if(join.session!=="AH")continue;
 const b=e.bars,d=e.event_index,hadDip=(k)=>Array.from({length:k},(_,u)=>b[d+1+u][3]).some(l=>l<b[d][3]);
 const earlyDip=hadDip(5);let signalDay=null,signalState="NO_TRIGGER",entryIndex=null,extensionPct=null;
 for(let t=2;t<=10;t++){
  if(!hadDip(Math.min(t-1,5)))continue;
  const cur=b[d+t],prev=b[d+t-1];
  if(!cur||!prev)continue;
  if(cur[3]>=prev[3]&&cur[4]>cur[1]&&cur[4]>prev[4]){
   signalDay=t;entryIndex=d+t+1;
   const knownTrough=Math.min(...b.slice(d,d+t+1).map(x=>x[3]));
   extensionPct=100*(b[entryIndex][1]/knownTrough-1);
   signalState=b[entryIndex][1]<=knownTrough*1.04?"TRADE":"SKIP_EXTENDED";
   break;
  }
 }
 rows.push({
  ticker:e.ticker,cohort:e.cohort,earningsDate:e.earnings_date,selloffDate:e.selloff_date,
  initialSelloffPct:e.selloff_pct,earlyDip,signalState,signalDay,
  entryDistanceFromObservedTroughPct:extensionPct,
  entryDay:signalState==="TRADE"?b[entryIndex][0]:null,
  trigger:signalState==="TRADE"?runTrade(b,entryIndex):null,
  D3:runTrade(b,d+3),D6:runTrade(b,d+6),D6_afterDip:earlyDip?runTrade(b,d+6):null,
  secondary:{
   signalStop3:signalState==="TRADE"?runTrade(b,entryIndex,3,20):null,
   signalHold40:signalState==="TRADE"?runTrade(b,entryIndex,5,40):null
  }
 });
}
const avg=a=>a.length?a.reduce((s,x)=>s+x,0)/a.length:null;
function summarize(a){
 const n=a.length,earlyDip=a.filter(x=>x.earlyDip).length, count=state=>a.filter(x=>x.signalState===state).length;
 const detail=key=>{
  const items=a.map(x=>x[key]).filter(x=>x&&Number.isFinite(x.pct));
  return {n:items.length,target:items.filter(x=>x.state==="TARGET").length,
   stop:items.filter(x=>x.state==="STOP").length,
   timeout:items.filter(x=>x.state==="TIMEOUT").length,
   grossMean:avg(items.map(x=>x.pct)),netMean:avg(items.map(x=>x.netPct)),
   grossPerEvent:items.reduce((s,x)=>s+x.pct,0)/n,
   netPerEvent:items.reduce((s,x)=>s+x.netPct,0)/n}
 };
 const pair=a.filter(x=>Number.isFinite(x.trigger?.pct)&&Number.isFinite(x.D6?.pct));
 const extra=field=>{
  const items=a.map(x=>x.secondary[field]).filter(Boolean);
  return {n:items.length,target:items.filter(x=>x.state==="TARGET").length,netMean:avg(items.map(x=>x.netPct))}
 };
 return {n,earlyDip,tradeSignals:count("TRADE"),noTrigger:count("NO_TRIGGER"),extendedSkip:count("SKIP_EXTENDED"),
  signalDays:Object.fromEntries(Array.from({length:9},(_,i)=>i+2).map(d=>[d,a.filter(x=>x.signalDay===d).length])),
  triggered:detail("trigger"),D3:detail("D3"),D6:detail("D6"),D6Dip:detail("D6_afterDip"),
  pairedD6:{n:pair.length,signalMean:avg(pair.map(x=>x.trigger.pct)),
   d6Mean:avg(pair.map(x=>x.D6.pct)),avgDiff:avg(pair.map(x=>x.trigger.pct-x.D6.pct)),
   signalTargets:pair.filter(x=>x.trigger.state==="TARGET").length,
   D6Targets:pair.filter(x=>x.D6.state==="TARGET").length},
  stop3:extra("signalStop3"),hold40:extra("signalHold40")};
}
const obj={id:"ah_delayed_secondary_dip_oneday_stabilization_v0_1_2026-10-11",
 protocol:"frozen_ah_delayed_secondary_dip_oneday_stabilization_v0_1_2026-10-11.md",
 status:"RETROSPECTIVE_EXPLORATORY_NOT_UNSEEN",
 summary:{allAH:summarize(rows),original65:summarize(rows.filter(x=>x.cohort==="original92")),
 companyDisjoint26:summarize(rows.filter(x=>x.cohort==="separate72"))},rows};
process.stdout.write(JSON.stringify(obj,null,2)+"\n");
