/**
 * One-shot frozen negative-news impairment contrast over 6 historical
 * company-disjoint AFTER-HOURS D4 winners/nonwinners, original press releases.
 * NOTE: Fully retrospective: pair outcomes and text codes exposed in past.
 * Usage: node research/earnings_recovery/run_ah_6pair_original_release_disclosure_contrast_v1.mjs
 */
import fs from 'node:fs';
import path from 'node:path';
const dir='research/earnings_recovery',load=name=>JSON.parse(fs.readFileSync(path.join(dir,name),'utf8'));
const matched=load('matched_quality164_fundamentals_v1_all_events_pairs_2026-10-11.json');
const releases=load('ah_6matched_pairs_12_original_release_news_coding_v1_2026-10-11.json');
const originalPairs=matched.matched72.d4.pairRows.filter(p=>p.releaseSession==='AH');
const sourceMap=new Map(releases.events.map(e=>[e.ticker+'|'+e.selloffDate,e]));
if(originalPairs.length!==6||releases.events.length!==12)throw Error('Unexpected sample count');
const featureDefs=[
 ['explicitDemandConcerns','PRESENT','hypothesis_no_concern_when_winner'],
 ['explicitMaterialExternalConstraint','PRESENT','hypothesis_no_constraint_when_winner'],
 ['outlookDirection','REAFFIRMED','prior_failed_proxy_negative_control'],
 ['identifiedOneOffCharge','PRESENT','descriptive_only_no_prior_direction']
];
function binomTwoSided(a,b) {
 const n=a+b;if(!n)return null;
 let p=0;
 for(let k=0;k<=Math.min(a,b);k++){
  let combination=1;
  for(let i=1;i<=k;i++)combination=combination*(n-i+1)/i;
  p+=combination/2**n;
 }
 return Math.min(1,2*p);
}
const rows=originalPairs.map((p,i)=>{
 const winner=sourceMap.get(p.case),nonwinner=sourceMap.get(p.control);
 if(!winner||!nonwinner||winner.tradeState!=='TARGET'||!['STOP','TIMEOUT'].includes(nonwinner.tradeState))throw Error('Misjoined pair '+p.case);
 const flags=Object.fromEntries(featureDefs.map(([f,v])=>[f,{
  winner:winner[f],nonwinner:nonwinner[f],winnerHas:winner[f]===v,
  nonwinnerHas:nonwinner[f]===v,anyUnknown:/UNKNOWN|UNREAD/.test(winner[f]+' '+nonwinner[f])}]));
 return {pair:i+1,winner:p.case,nonwinner:p.control,initialSelloffGapPp:p.dropGapPp,flags,originalSourceUrls:[winner.sourceUrl,nonwinner.sourceUrl]};
});
const tests=Object.fromEntries(featureDefs.map(([f,,label])=>{
 const winnerOnly=rows.filter(x=>x.flags[f].winnerHas&&!x.flags[f].nonwinnerHas).length;
 const failureOnly=rows.filter(x=>!x.flags[f].winnerHas&&x.flags[f].nonwinnerHas).length;
 return [f,{
  label,matchedPairs:rows.length,winnerOnly,failureOnly,
  both:rows.filter(x=>x.flags[f].winnerHas&&x.flags[f].nonwinnerHas).length,
  neither:rows.filter(x=>!x.flags[f].winnerHas&&!x.flags[f].nonwinnerHas).length,
  unknown:rows.filter(x=>x.flags[f].anyUnknown).length,
  winnerFlagTotal:rows.filter(x=>x.flags[f].winnerHas).length,
  nonwinnerFlagTotal:rows.filter(x=>x.flags[f].nonwinnerHas).length,
  unfavorableDiscordant:winnerOnly,favorableDiscordant:failureOnly,
  exactTwoSidedDiscordantP:binomTwoSided(winnerOnly,failureOnly)}];
}));
const result={
 id:'ah_release_6pair_frozen_disclosure_contrast_2026-10-11',
 status:'EXPLORATORY_FALSIFICATION_OBSERVED_OUTCOMES_UNBLINDED',
 method:'Previously reviewed 12 issuer releases. Exact paired negative demand/external operating impairment contrasts. No prior-tone or analyst expectation revision inferred.',
 releaseCoverage:releases.events.filter(e=>e.releaseVerified).length,
 totalReleases:releases.events.length,tests,
 analystForwardFiscalEPSPreVsD3Coverage:0,
 conferenceCallPriorToneComparisonCoverage:0,
 actualOptionExecutionQuotesCoverage:0,
 newsSurprisePriorMgmtQuarterlyNumericComparisonsComplete:false,
 externalEventSpecificWarningsHaveDirectExcerptsOnly:true,rows
};
process.stdout.write(JSON.stringify(result,null,2)+'\n');
