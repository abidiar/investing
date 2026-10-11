/**
 * Research-only point-in-time disclosure coverage join and exploratory stratification.
 * Running: node research/earnings_recovery/run_quality164_asof_expectations_sector_coverage_v1.mjs
 * Pre-existing frozen design: frozen_catalyst_mechanism_matched_study_v1_2026-10-11.md
 * Does not pretend to have acquired 164 event releases or FY1 Street consensus snapshots.
 */
import fs from "node:fs";
import path from "node:path";
const dir="research/earnings_recovery";
const j=n=>JSON.parse(fs.readFileSync(path.join(dir,n),"utf8"));
function csv(src){
 const lines=src.trim().split(/\r?\n/);const parse=line=>{
  const result=[];let v="",quoted=false;
  for(let i=0;i<line.length;i++){const c=line[i];if(c==='"'&&quoted&&line[i+1]==='"'){v+='"';i++}
   else if(c==='"')quoted=!quoted;
   else if(c===','&&!quoted){result.push(v);v=""}else v+=c}
  result.push(v);return result};
 const hdr=parse(lines.shift());
 return lines.map(line=>Object.fromEntries(parse(line).map((value,i)=>[hdr[i],value])));
}
const events=j("matched_quality164_fundamentals_v1_all_events_pairs_2026-10-11.json").events;
const sector=j("quality164_asofD3_sector_market_factors_fullmatched_results_2026-10-11.json").events;
const release=j("ah_6matched_pairs_12_original_release_news_coding_v1_2026-10-11.json").events;
const dell=j("dell_asof_forward_expectation_results_2026-10-11.json").results;
const qtr=j("ah_12_original_release_quant_management_surprises_inputs_2026-10-11.json").codedRows;
const annual=csv(fs.readFileSync(path.join(dir,"forward_guidance_proxy_audit_72events_2026-10-10.csv"),"utf8"));
if(events.length!==164||sector.length!==164||release.length!==12||dell.length!==3||annual.length!==72||qtr.length!==6)throw Error("Frozen input counts changed.");
const map=(xs,k)=>new Map(xs.map(x=>[k(x),x]));
const bySector=map(sector,x=>x.ticker+"|"+x.earningsDate);
const byRelease=map(release,x=>x.ticker+"|"+x.earningsDate);
const byDell=map(dell,x=>x.ticker+"|"+x.earningsDate);
const byQtr=map(qtr,x=>x.key);
const byAnnual=map(annual,x=>x.ticker+"|"+x.earnings_date);
const rows=events.map(o=>{
 const key=o.ticker+"|"+o.earningsDate,s=bySector.get(key),r=byRelease.get(key),
  d=byDell.get(key),q=byQtr.get(key),g=byAnnual.get(key);
 if(!s)throw Error("No sector pair "+key);
 const eps=d?.priorVsCurrentManagementGuidance.FYAdjustedEPS.changePct ??
  (q?.futureFYGuidance?100*(q.futureFYGuidance.currentMidpoint/q.futureFYGuidance.previousMidpoint-1):null);
 const marginStreet=d?.priorVsCurrentManagementGuidance.GrossMarginStreetSurprisePp??null;
 return {
  ticker:o.ticker,earningsDate:o.earningsDate,selloffDate:o.selloffDate,
  year:o.year,cohort:o.cohort,session:o.session,sector:s.sector,initialSelloffPct:o.selloffPct,
  fullRecovery60d:o.fullRecovery60d,d4StockTarget:o.tradeWin,
  d4StockNetPct:o.trade.hypNetPct,earlyLowerLowByD3:o.earlyLowerLowByD3,
  asOfD3Sector:{shockMinusSectorPp:s.features.shockMinusSectorD0Pp,
   stockMinusSectorD0D3Pp:s.features.stockMinusSectorD0D3Pp,
   sectorD0D3Pct:s.features.sectorD0ToD3Pct,spyD0D3Pct:s.features.spyD0ToD3Pct},
  futureSectorMovement_EXPLANATORY_ONLY:{sectorD0D60Pct:s.features.sectorD0ToD60Pct},
  historicalCompanyFYGuidanceDirection:g&&g.guidance_direction!=="UNKNOWN"?
   {label:g.guidance_direction,epsDirection:g.eps_direction,source:g.guidance_source,
    observation:"PRIOR_72_STUDY_ALREADY_RESULT_EXPOSED"}:null,
  original12Release:r?{source:r.sourceUrl,revenueYoYPct:r.revenueYoYPct,grossMarginYoYPp:r.grossMarginYoYPp,
   outlookDirection:r.outlookDirection,explicitDemandConcerns:r.explicitDemandConcerns,
   priorGuidanceExecution:r.priorSameQuarterGuidanceExecution?.status}:null,
  observedNumericPriorQuarterGuideSurprises:q?
   {sourcePrior:q.priorSource,sourceActual:q.currentSource,metrics:q.metrics}:null,
  observedSameFYCompanyEPSForecastChangePct:eps,
  observedSameFYCompanyEPSForecastSource:d?.originalSources||(q?.futureFYGuidance?[q.priorSource,q.currentSource]:null),
  grossMarginStreetSurprisePp:marginStreet,
  dellSpecific:d?{originalSources:d.originalSources,otherFYChanges:d.priorVsCurrentManagementGuidance,
   firstClosingRecoveryDate:d.afterD3Outcomes_NOT_early_signal.firstFullClosingRecoveryDate}:null,
  coverage:{numericManagementQtrSurprise:!!q,sameFYCompanyEPSChange:eps!==null,
   originalReleaseNarrative:!!r||!!d,previousFYManagementProxyClassified:!!g&&g.guidance_direction!=="UNKNOWN",
   trueHistoricalAnalystFY1Revision:false,unexpectedMarginVersusStreet:marginStreet!==null}
 };
});
const median=a=>{if(!a.length)return null;a.sort((x,y)=>x-y);return a.length%2?a[Math.floor(a.length/2)]:
 (a[a.length/2-1]+a[a.length/2])/2};
const sum=a=>a.reduce((s,x)=>s+x,0);
const stat=xs=>({n:xs.length,d4Target:xs.filter(x=>x.d4StockTarget).length,
 d4MeanNetPct:xs.length?sum(xs.map(x=>x.d4StockNetPct))/xs.length:null,
 fullRec60:xs.filter(x=>x.fullRecovery60d).length,
 medInitialShockSector:median(xs.map(x=>x.asOfD3Sector.shockMinusSectorPp)),
 medStockSectorD3:median(xs.map(x=>x.asOfD3Sector.stockMinusSectorD0D3Pp)),
 medSectorD0D3:median(xs.map(x=>x.asOfD3Sector.sectorD0D3Pct)),
 medSectorFuture60_RETRO:median(xs.map(x=>x.futureSectorMovement_EXPLANATORY_ONLY.sectorD0D60Pct))});
const guid=rows.filter(x=>x.coverage.previousFYManagementProxyClassified);
const releases=rows.filter(x=>x.original12Release),numeric=rows.filter(x=>x.coverage.numericManagementQtrSurprise);
const origs=rows.filter(x=>x.coverage.originalReleaseNarrative);
const fy=rows.filter(x=>x.coverage.sameFYCompanyEPSChange);
const strat=(column,values)=>Object.fromEntries(values.map(v=>[v,stat(guid.filter(x=>x.historicalCompanyFYGuidanceDirection[column]===v))]));
const result={
 id:"quality164_asof_expectations_sector_source_coverage_audit_2026-10-11",
 status:"REUSE_EXISTING_FROZEN_FULL_POPULATION_PLUS_12_ORIGINAL_RELEASES_3_DELL_6_NEW_PRIOR_QUARTER_GUIDE_CHECKS_DESCRIPTIVE_ONLY",
 method:"All outcomes were previously exposed; not independent validation; no invented FY1 analyst forecasts.",
 counts:{full164:rows.length,sectorCoverage:rows.length,historicalFYGuidanceSourceCohort:annual.length,
  historicalClassifiedFYGuidance:guid.length,original12ReleaseNarrative:releases.length,
  dellPriorVsCurrent:origs.length-releases.length,uniqueOriginalIssuerReleaseNarratives:origs.length,
  sameQuarterNumericActualVsPriorMgmtGuidance:numeric.length,
  sameFYQuantEPSForecastComparables:fy.length,
  overlapAnnualProxyAndOriginalRelease:rows.filter(x=>x.coverage.previousFYManagementProxyClassified&&x.coverage.originalReleaseNarrative).length,
  trueHistoricalFY1AnalystEPSRevisions:0,
  grossMarginAgainstStreet:rows.filter(x=>x.coverage.unexpectedMarginVersusStreet).length},
 whole164:{d4Target:stat(rows.filter(x=>x.d4StockTarget)),d4NonTarget:stat(rows.filter(x=>!x.d4StockTarget)),
  fullRecovery:stat(rows.filter(x=>x.fullRecovery60d)),noFullRecovery:stat(rows.filter(x=>!x.fullRecovery60d))},
 priorFYguidanceAsOfProxy:{label:"PREVIOUS_72_EVENT_TEST_ALREADY_KNOWN_NOT_NEW_INDEPENDENT_TEST",
  byGuidance:strat("label",["STABLE_OR_UP","DOWN","MIXED"]),byEPS:strat("epsDirection",["UP","STABLE","DOWN"])},
 original12AHsixPairedNarrative:{d4Targets:stat(releases.filter(x=>x.d4StockTarget)),
  d4NonTargets:stat(releases.filter(x=>!x.d4StockTarget)),nNumericGuide:numeric.length,
  positiveQuarterRevenueOrOrdersGuide:numeric.map(x=>({ticker:x.ticker,date:x.earningsDate,
   d4Win:x.d4StockTarget,metrics:x.observedNumericPriorQuarterGuideSurprises.metrics
    .filter(v=>v.unit!=="pct"&&/revenue|orders|billings/i.test(v.metric))
    .map(v=>({metric:v.metric,surprisePct:v.deltaPct}))}))},
 quantEPSForecastEvents:fy.map(x=>({ticker:x.ticker,date:x.earningsDate,
  epsChangePct:x.observedSameFYCompanyEPSForecastChangePct,d4Target:x.d4StockTarget,
  fullRec:x.fullRecovery60d,shockMinusSectorPp:x.asOfD3Sector.shockMinusSectorPp,
  stockMinusSectorD0D3Pp:x.asOfD3Sector.stockMinusSectorD0D3Pp})),
 rows
};
process.stdout.write(JSON.stringify(result,null,2)+"\n");
