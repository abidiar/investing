/**
 * Read-only reproducible summary of the 49-name frozen v2 data QA:
 * node research/swing_two_session/run_range_vwap_basis_audit_summary_v2.mjs
 * Does not calculate trade outcomes / cannot constitute independent replication.
 */
import fs from 'node:fs';
import path from 'node:path';
const root='research/swing_two_session/data';
const load=n=>JSON.parse(fs.readFileSync(path.join(root,n),'utf8'));
const corporate=load('disjoint49_preliminary106_corporate_action_flagged_2026_10_11.json');
const parts=Array.from({length:6},(_,i)=>load('frozen18_m5_daily_audit_part'+String(i+1).padStart(2,'0')+'_2026_10_11.json'));
const cases=parts.flatMap((p,i)=>p.cases.map(c=>({sourcePart:i+1,...c})));
if(cases.length!==18||corporate.n!==106)throw Error('Frozen input count drift');
const rows=cases.map(c=>{
 const ticker=c.symbol||c.sym,raw=c.rawSig||c.rawSignal||c.rawTest||c.raw;
 const passed=raw?.qualifies??raw?.qualified??raw?.passes;
 if(typeof passed!=='boolean')throw Error('No explicit original criteria comparison for '+ticker+' '+c.date);
 const flags=raw?.flags||raw?.checks||{},dividend=corporate.candidates.find(x=>x.symbol===ticker&&x.date===c.date);
 if(!dividend)throw Error('Frozen audit case missing in preliminary universe');
 const absences=c.missing||c.miss||c.absent||[];
 const last=c.rows?.at(-1),d=last?.D||last?.adjusted||last?.dailyOriginal||last?.sourceD;
 const m=last?.M5||last?.raw||last?.fromM5;
 return {ticker,date:c.date,year:c.date.slice(0,4),rawPass:passed,
  failedConditions:Object.entries(flags).filter(([,v])=>!v).map(([name])=>name),
  exDates:dividend.exDateActions||[],anyExDate:dividend.hasExDate,
  priceFactorDriftPct:c.ratioDriftPct??c.ratioVariationPct??c.adjustmentRatioDriftPct??null,
  full41SourceDays:absences.length===0,
  incompleteRTH5mLookbackCount:(c.short||c.partial||c.non78||[]).length,
  reportedDToM5RTHVolumeRatio:d?.volume&&m?.volume?d.volume/m.volume:null,
  sourcePart:c.sourcePart};
});
const byYear=Object.fromEntries(['2024','2025','2026'].map(y=>[y,{reviewed:rows.filter(x=>x.year===y).length,pass:rows.filter(x=>x.year===y&&x.rawPass).length}]));
const summary={version:'2026-10-11',status:'PRE_OUTCOME_SOURCE_QA_NO_FULL_49_INDEPENDENT_TRADE_TEST',
 frozen:{universe:corporate.universeN,preliminaryDailyAdjustedCandidates:corporate.n,
  preliminaryDividendWindowExposed:corporate.withDividend,preliminaryNoObservedExDate:corporate.withoutKnownExDate,
  byYear:corporate.byYear},
 sourceAudit:{reviewed:rows.length,pass:rows.filter(x=>x.rawPass).length,fail:rows.filter(x=>!x.rawPass).length,
  passByYear:byYear,fullPrior40AndEventDays:rows.filter(x=>x.full41SourceDays).length,
  dividendInPrior40:rows.filter(x=>x.anyExDate).length,
  dividendAndFailed:rows.filter(x=>x.anyExDate&&!x.rawPass).length,
  dividendAndPassed:rows.filter(x=>x.anyExDate&&x.rawPass).length,
  noObservedDividendAndPassed:rows.filter(x=>!x.anyExDate&&x.rawPass).length},
 limitations:['selected only from Webull adjusted-DAY positives; as-traded candidate false negatives not identified',
 'M5 regular-hours and D aggregate volume differ and must not be silently merged',
 'some prior40 minute days are incomplete (77) or valid holiday short sessions (41-42)',
 'no future entry/exit bars read and no v2 profitability inferred'],cases:rows};
process.stdout.write(JSON.stringify(summary,null,2)+'\n');
