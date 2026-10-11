/**
 * Recompute frozen 18-case support-reclaim data-quality audit WITHOUT looking at trades.
 * Run: node research/swing_two_session/run_frozen18_price_volume_reconciliation_2026_10_11.mjs
 * Inputs are the 6 committed 40-session as-traded M5-derived OHLC audit files.
 * IMPORTANT: daily close / same-day M5 close rescales price BASIS for quality assessment,
 * it is NOT an independent ex-date schedule nor a valid source of trading profits.
 */
import fs from 'node:fs';
import path from 'node:path';
const dir="research/swing_two_session/data";
const cases=Array.from({length:6},(_,i)=>JSON.parse(fs.readFileSync(
 path.join(dir,"frozen18_m5_daily_audit_part"+String(i+1).padStart(2,"0")+"_2026_10_11.json"),"utf8")).cases).flat();
if(cases.length!==18)throw Error('sample changed');
function test(series,entry){
 const lo=Math.min(...series.map(v=>v.low)),hi=Math.max(...series.map(v=>v.high));
 const touch=series.flatMap((v,i)=>v.low<=lo*1.012?[i]:[]);
 const avg20=series.slice(-20).reduce((s,v)=>s+v.volume,0)/20;
 const flags={range:hi/lo>=1.06,
 touches:touch.some((i,k)=>touch.some((j,h)=>h>k&&j-i>=5)),
 reclaim:entry.low<lo&&entry.close>lo,
 near:entry.close>=lo*.995&&entry.close<=lo*1.025,
 volume:entry.volume>=1.2*avg20};
 return {qualifies:Object.values(flags).every(Boolean),flags,volRatio:entry.volume/avg20,support:lo};
}
const rows=cases.map(rec=>{
 const symbol=rec.symbol??rec.sym;
 const arr=rec.rows.map(x=>{
  const daily=x.D??x.dailyOriginal??x.adjusted??x.sourceD;
  const raw=x.M5??x.fromM5??x.raw??x.m5;
  if(!daily||!raw)throw Error('missing source '+symbol+' '+x.date);
  const factor=daily.close/raw.close;
  return {date:x.date,daily,raw,adjustedFromM5:{
   open:raw.open*factor,high:raw.high*factor,low:raw.low*factor,
   close:raw.close*factor,volume:raw.volume}};
 });
 if(arr.length!==41)throw Error('missing original 40 sessions '+symbol);
 const D=test(arr.slice(0,40).map(x=>x.daily),arr[40].daily);
 const R=test(arr.slice(0,40).map(x=>x.adjustedFromM5),arr[40].adjustedFromM5);
 const drifts=arr.map(x=>x.daily.close/x.raw.close);
 return {symbol,date:rec.date,originalDailyPass:D.qualifies,
  rescaledRthM5Pass:R.qualifies,
  dailyRelativeVolume:D.volRatio,rtH5minRelativeVolume:R.volRatio,
  dailyDivRthVol:arr[40].daily.volume/arr[40].raw.volume,
  dailyToRawCloseAdjustmentDriftPct:100*(Math.max(...drifts)/Math.min(...drifts)-1),
  originalChecks:D.flags,reconstructedChecks:R.flags,
  eventM5Count:arr[40].raw.bars??arr[40].raw.n??arr[40].raw.count??arr[40].raw.m5Count};
});
const totals={n:rows.length,originalDaily:rows.filter(x=>x.originalDailyPass).length,
 normalizedRth:rows.filter(x=>x.rescaledRthM5Pass).length,
 volumeSpecificDisagreements:rows.filter(x=>x.originalDailyPass&&!x.rescaledRthM5Pass&&!x.reconstructedChecks.volume).length};
process.stdout.write(JSON.stringify({status:"DATA_QUALITY_ONLY_NO_PNL",totals,rows},null,2)+"\n");
