/** Frozen v2 source-quality check ONLY; does NOT access post-signal bars or trade returns.
 * Run at repo root: node research/swing_two_session/run_106_prior20_rth_volume_source_audit_2026_10_11.mjs
 */
import fs from 'node:fs';
const base="research/swing_two_session/data/";
const read=(p)=>JSON.parse(fs.readFileSync(base+p,'utf8'));
const manifest=read("frozen106_event_day_m5_source_audit_manifest_2026_10_11.json");
const one=[],two=[];
for(let i=1;i<=9;i++){
 const id=String(i).padStart(2,"0");
 one.push(...read("frozen106_source_m5_signalday_chunk"+id+"_2026_10_11.json").data);
 two.push(...read("frozen106_source_m5_prior20_extension_chunk"+id+"_2026_10_11.json").data);
}
if(manifest.signals.length!==106||one.length!==106||two.length!==106)throw new Error('frozen input count mismatch');
const key=x=>x.symbol+"|"+x.date,main=new Map(one.map(x=>[key(x),x])),prior=new Map(two.map(x=>[key(x),x]));
const perEvent=manifest.signals.map(x=>{
 const m=main.get(key(x)),p=prior.get(key(x));
 if(!m||!p)throw Error("missing source "+key(x));
 const dates=new Map();
 for(const v of m.days)dates.set(v.date,{n:v.n,v:v.v,source:"current"});
 for(const v of p.extraDays){
  const old=dates.get(v.date);
  if(!old||v.n>old.n)dates.set(v.date,{n:v.n,v:v.v,source:"extension"});
 }
 const historical=x.priorDate20.map(date=>({date,...(dates.get(date)||{n:null,v:null})}));
 const nPresent=historical.filter(v=>v.v!==null).length;
 const historicalMean=nPresent===20?historical.reduce((s,v)=>s+v.v,0)/20:null;
 const rthRelativeVolume=historicalMean&&m.event?.v?m.event.v/historicalMean:null;
 const daily=x.dailyVolRel20;
 return {symbol:x.symbol,date:x.date,prior20Present:nPresent,prior20M5Incomplete:historical.filter(z=>z.n!==78).map(z=>({date:z.date,n:z.n})),
  eventM5Count:m.event?.n??null,dailyVolRel20:daily,rthVolRel20:rthRelativeVolume,
  originalDailyPass:daily>=1.2,rthM5Pass:rthRelativeVolume!==null?rthRelativeVolume>=1.2:null,
  disagreement:rthRelativeVolume!==null?(daily>=1.2)!==(rthRelativeVolume>=1.2):null,
  dailySignalVolume:x.Dvolume,rthSignalVolume:m.event?.v??null,ratioDToRth:x.Dvolume/(m.event?.v??NaN)};
});
const stats={n:perEvent.length,withPrior20:perEvent.filter(x=>x.prior20Present===20).length,withCompleteM5SignalDay:perEvent.filter(x=>x.eventM5Count===78).length,
 dailyVolumePass:perEvent.filter(x=>x.originalDailyPass).length,rthVolumePass:perEvent.filter(x=>x.rthM5Pass).length,
 disagreement:perEvent.filter(x=>x.disagreement).length,
 disagreementEvents:perEvent.filter(x=>x.disagreement).map(x=>({symbol:x.symbol,date:x.date,dailyVolRel20:x.dailyVolRel20,rthVolRel20:x.rthVolRel20})),
 fully78Prior20:perEvent.filter(x=>!x.prior20M5Incomplete.length).length};
process.stdout.write(JSON.stringify({status:"SOURCE_AUDIT_ONLY_NO_TRADES",stats,perEvent},null,2)+"\n");