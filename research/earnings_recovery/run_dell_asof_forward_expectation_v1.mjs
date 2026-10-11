/**
* Reproducer for source-audited THREE DELL outcome-exposed descriptive as-of earnings expectation changes.
* node research/earnings_recovery/run_dell_asof_forward_expectation_v1.mjs
* Does NOT run frozen 164-case hypothesis test; remaining 161 event releases not newly coded.
* Uses archived existing adjusted stock price and ETF-relative results; no future fundamentals at D3.
*/
import fs from 'node:fs';
import path from 'node:path';
const dir='research/earnings_recovery';
const read=(n)=>JSON.parse(fs.readFileSync(path.join(dir,n),'utf8'));
const input=read('dell_asof_forward_expectation_source_inputs_2026-10-11.json');
const bars=read('actionable_bounce_price_windows_92events_2026-10-10.json').events;
const sector=read('quality164_asofD3_sector_market_factors_fullmatched_results_2026-10-11.json').events;
const outcomes=read('matched_quality164_fundamentals_v1_all_events_pairs_2026-10-11.json').events;
const round=(v,d=3)=>v===null||v===undefined?null:Number(v.toFixed(d));
const delta=(oldval,newval)=>oldval===null||oldval===undefined||newval===null||newval===undefined||oldval===0?null:round((newval/oldval-1)*100);
const pp=(a,b)=>a===null||a===undefined||b===null||b===undefined?null:round(b-a);
const results=input.records.map(x=>{
 const e=bars.find(y=>y.ticker===x.ticker&&y.earnings_date===x.earningsDate);
 const s=sector.find(y=>y.ticker===x.ticker&&y.earningsDate===x.earningsDate);
 const o=outcomes.find(y=>y.ticker===x.ticker&&y.earningsDate===x.earningsDate);
 if(!e||!s||!o)throw Error('Missing existing archive event '+x.earningsDate);
 const d=e.event_index,prevEarnings=e.bars.find(q=>q[0]===e.earnings_date);
 if(!prevEarnings||!e.bars[d+3]||!e.bars[d+4])throw Error('Missing price windows '+x.earningsDate);
 const preClose=prevEarnings[4],d0=e.bars[d],d3=e.bars[d+3],d4=e.bars[d+4];
 const oldEPS=x.priorAdjustedEPS,newEPS=x.updatedAdjustedEPS;
 const fromPrePriceRatio=oldEPS===null?null:preClose/oldEPS;
 const fromD3PriceRatio=newEPS===null?null:d3[4]/newEPS;
 const firstFullRec=e.bars.slice(d,d+61).find(q=>q[4]>=preClose);
 return {
  ticker:x.ticker,earningsDate:x.earningsDate,outcomeKnown:true,
  sourcePublicByD3:true,minuteLevelReleaseTimestampVerified:false,
  knowledgeCutoff:d3[0]+' 16:00 America/New_York',
  originalSources:x.primaryUrls,
  period:x.guidancePeriod,
  priorVsCurrentManagementGuidance:{
   FYAdjustedEPS:{old:oldEPS,new:newEPS,changePct:delta(oldEPS,newEPS)},
   FYRevenueBillion:{old:x.priorRevenueBillion??null,new:x.updatedRevenueBillion??null,changePct:delta(x.priorRevenueBillion,x.updatedRevenueBillion)},
   FYRevenueGrowthPct:{old:x.priorRevenueGrowthPct??null,new:x.updatedRevenueGrowthPct??null,changePp:pp(x.priorRevenueGrowthPct,x.updatedRevenueGrowthPct)},
   AnnualAIShipmentsBillion:{old:x.priorAIServerShipmentsAnnualBillion??null,new:x.updatedAIServerShipmentsAnnualBillion??null,changePct:delta(x.priorAIServerShipmentsAnnualBillion,x.updatedAIServerShipmentsAnnualBillion)},
   QuarterAIOrdersBillion:{old:x.priorAIServerOrdersBillion??null,new:x.updatedAIServerOrdersBillion??null,changePct:delta(x.priorAIServerOrdersBillion,x.updatedAIServerOrdersBillion)},
   AIBacklogBillion:{old:x.priorAIBacklogBillion??null,new:x.updatedAIBacklogBillion??null,changePct:delta(x.priorAIBacklogBillion,x.updatedAIBacklogBillion),note:x.priorAIBacklogAsOf?'UNLIKE_SNAPSHOT_TIMES':null},
   ISGOperatingMarginPct:{old:x.priorISGRevenueBillion?round(100*x.priorISGOperatingIncomeBillion/x.priorISGRevenueBillion):null,new:x.updatedISGRevenueBillion?round(100*x.updatedISGOperatingIncomeBillion/x.updatedISGRevenueBillion):null,changePp:x.priorISGRevenueBillion&&x.updatedISGRevenueBillion?round(100*(x.updatedISGOperatingIncomeBillion/x.updatedISGRevenueBillion-x.priorISGOperatingIncomeBillion/x.priorISGRevenueBillion)):null},
   NextQtrAdjustedEPSStreetSurprisePct:delta(x.reportedNextQuarterStreetEPS??null,x.reportedNextQuarterAdjustedEPS??null),
   GrossMarginStreetSurprisePp:pp(x.reportedStreetGrossMarginPct??null,x.reportedGrossMarginPct??null),
   NewlyIntroducedFYAdjustedEPSGrowthVsPriorActualPct:delta(x.latestCompletedFYAdjustedEPS??null,newEPS)
  },
  tradingInfoAsOfD3:{
    priorEarningsDateCloseAdjusted:round(preClose,4),
    d0SelloffDate:d0[0],d0ReturnFromEarningsClosePct:delta(preClose,d0[4]),
    d3Date:d3[0],d3CloseAdjusted:round(d3[4],4),
    d3ReturnFromEarningsClosePct:delta(preClose,d3[4]),
    d4Date:d4[0],d4OpeningAdjusted:round(d4[1],4),
    originalShockMinusXLKPp:round(s.features.shockMinusSectorD0Pp),
    stockRelativeXLKD0toD3Pp:round(s.features.stockMinusSectorD0D3Pp),
    sectorXLKD0toD3Pct:round(s.features.sectorD0ToD3Pct),
    relativePriceOverGuideEPSMultipleShiftPct:fromPrePriceRatio===null?null:delta(fromPrePriceRatio,fromD3PriceRatio),
    relativePriceOverGuideEPSMultipleCaution:'Adjusted archival prices: only percentage shift over closely spaced dates shown, NOT official absolute P/E'
  },
  afterD3Outcomes_NOT_early_signal:{
    firstFullClosingRecoveryDate:firstFullRec?.[0]??null,
    fullRecovery60:o.fullRecovery60d,
    modeledD4State:o.trade.state,
    modeledD4ExitDate:o.trade.exitDate,
    modeledD4NetStockPct:round(o.trade.hypNetPct),
    futureXLKD0toD60Pct:round(s.features.sectorD0ToD60Pct),
    futureNews:x.knownLater
  },
  historicalConsensusFY1Revision:'UNKNOWN',
  asofCaveats:x.contemporaneousCoverage,
  originalPointInTimeNotes:x.knownByD3
 };
});
if(results.length!==3||outcomes.length!==164)throw Error('unexpected denominator');
process.stdout.write(JSON.stringify({
  experiment:'dell_asof_forward_expectation_v1_2026-10-11',
  status:'SOURCE_CODED_FIRST_THREE_DELL_ONLY_RETROSPECTIVE_DESCRIPTIVE',
  sample:{full164:outcomes.length,earningsCasesCoded:results.length,pending:outcomes.length-results.length,
    missingTrueHistoricalAnalystFY1EPS:results.length},
  outcomeExposure:'All historic stock outcomes were known before coding; no inference, no promotion',
  nullRule:'Unknown comparable period or unobserved, not zero',
  comparisonRule:'Exact same fiscal-year forecast/GAAP basis for changes; FY26 first guide Feb2025 cannot be compared with FY25 prior-year EPS as if an EPS revision',
  results
},null,2)+'\n');
