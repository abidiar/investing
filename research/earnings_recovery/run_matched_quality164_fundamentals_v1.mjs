/** 
 * Investing OS 164-event matched preearnings fundamentals audit.
 * node research/earnings_recovery/run_matched_quality164_fundamentals_v1.mjs
 * No network, paid API, historical analyst consensus, or post-event features.
 * Emits stdout JSON of all 164 events, matched pairs, group summaries.
 * The original92 numeric preannouncement fundamentals are unavailable.
 */
import fs from 'node:fs';
import path from 'node:path';
const dir='research/earnings_recovery',read=n=>fs.readFileSync(path.join(dir,n),'utf8');
function csv(text){
 const fields=line=>{let v='',q=false,a=[];for(let i=0;i<line.length;i++){let c=line[i];if(c==='"'&&q&&line[i+1]==='"'){v+='"';i++}else if(c==='"')q=!q;else if(c===','&&!q){a.push(v);v=''}else v+=c}a.push(v);return a};
 const lines=text.trim().split(/\r?\n/),hdr=fields(lines.shift());
 return lines.map(l=>Object.fromEntries(fields(l).map((x,i)=>[hdr[i],x])));
}
const ev=[
 ...JSON.parse(read('actionable_bounce_price_windows_92events_2026-10-10.json')).events,
 ...JSON.parse(read('actionable_bounce_price_windows_72events_2026-10-10.json')).events];
const rosters=new Map([
 ...csv(read('earnings_selloff_recovery_92events_2026-10-10.csv')),
 ...csv(read('holdout_final_136events_2026-10-10.csv'))
].map(x=>[x.ticker+'|'+x.selloff_date,x]));
const long=new Map(csv(read('quality_164_long_horizon_recovery_2026-10-10.csv')).map(x=>[x.ticker+'|'+x.source_selloff_date,x]));
const quality=new Map(Array.from({length:9},(_,i)=>JSON.parse(read('holdout_quality_batch_'+i+'_2026-10-10.json')).rows)
 .flat().filter(x=>x.quality==='PASS').map(x=>[x.ticker+'|'+x.earnings_date+'|'+x.selloff_date,x]));
function trade(b,k){
 const entry=b[k][1],up=entry*1.03,down=entry*.95;
 for(let z=k;z<k+20;z++){
  const bar=b[z];if(!bar)throw Error('Missing complete D4+20 history '+b[k][0]);
  let state=null,exit=null,exitReason=null;
  if(z>k&&bar[1]<=down){state='STOP';exit=bar[1];exitReason='GAP_STOP'}
  else if(z>k&&bar[1]>=up){state='TARGET';exit=bar[1];exitReason='GAP_TARGET'}
  else if(bar[3]<=down){state='STOP';exit=down;exitReason=bar[2]>=up?'STOP_FIRST_BOTH':'STOP_TOUCH'}
  else if(bar[2]>=up){state='TARGET';exit=up;exitReason='TARGET_TOUCH'}
  else if(z===k+19){state='TIMEOUT';exit=bar[4];exitReason='TIMEOUT'}
  if(state){const grossReturnPct=100*(exit/entry-1);return {
   state,entryDate:b[k][0],entryPrice:entry,exitDate:bar[0],exitPrice:exit,
   exitReason,grossReturnPct,hypNetPct:grossReturnPct-.2,holding:z-k+1}}
 }
}
const rows=[];
for(const e of ev){
 const key=e.ticker+'|'+e.selloff_date;
 const m=rosters.get(key),h=long.get(key);
 if(!m||!h||h.h60_eligible!=='true')throw Error('Missing event metadata or D60 '+key);
 const b=e.bars,d=e.event_index,q=quality.get(e.ticker+'|'+e.earnings_date+'|'+e.selloff_date);
 if((e.cohort==='separate72')!==Boolean(q))throw Error('Financial coverage mismatch '+key);
 const fundamentals=q?{
   revenueGrowthYoYPct:+q.yoy_growth_pct,debtEquity:+q.debt_equity,
   cashConversion:+q.ttm_fcf/+q.ttm_income,
   ttmIncome:+q.ttm_income,ttmFCF:+q.ttm_fcf
  }:null;
 rows.push({ticker:e.ticker,earningsDate:e.earnings_date,selloffDate:e.selloff_date,
 cohort:e.cohort,session:m.session,year:+e.selloff_date.slice(0,4),
 selloffPct:+m.selloff_pct,
 earlyLowerLowByD3:Math.min(...b.slice(d+1,d+4).map(x=>x[3]))<b[d][3],
 trade:trade(b,d+4),fullRecovery60d:h.h60_fullclose==='true',
 fullRecoveryDay60:h.h60_fullclose_day||null,fundamentals});
}
for(const x of rows)x.tradeWin=x.trade.state==='TARGET';
if(rows.length!==164||rows.filter(x=>x.fundamentals).length!==72||rows.filter(x=>x.session==='AH').length!==91)throw Error('Bad sample coverage');
const avg=a=>a.length?a.reduce((x,y)=>x+y,0)/a.length:null;
const median=a=>{if(!a.length)return null;a=[...a].sort((x,y)=>x-y);return(a[Math.floor((a.length-1)/2)]+a[Math.floor(a.length/2)])/2};
const fspec=['revenueGrowthYoYPct','debtEquity','cashConversion'];
function summary(a){return {
 n:a.length,issuers:new Set(a.map(x=>x.ticker)).size,ah:a.filter(x=>x.session==='AH').length,
 d3EarlyLow:a.filter(x=>x.earlyLowerLowByD3).length,
 d4Target:a.filter(x=>x.trade.state==='TARGET').length,
 d4Stop:a.filter(x=>x.trade.state==='STOP').length,
 d4Timeout:a.filter(x=>x.trade.state==='TIMEOUT').length,
 d4WinRatePct:100*a.filter(x=>x.trade.state==='TARGET').length/a.length,
 d4GrossMeanPct:avg(a.map(x=>x.trade.grossReturnPct)),
 d4HypNetMeanPct:avg(a.map(x=>x.trade.hypNetPct)),
 fullRecovery60d:a.filter(x=>x.fullRecovery60d).length,
 fullRecovery60Pct:100*a.filter(x=>x.fullRecovery60d).length/a.length,
 fundamentalCoverage:a.filter(x=>x.fundamentals).length
}}
const n72=rows.filter(x=>x.cohort==='separate72');
const unpaired=Object.fromEntries(fspec.map(k=>[k,Object.fromEntries([
 ['D4Winners',x=>x.tradeWin],['D4NonWinners',x=>!x.tradeWin],
 ['Recovery60Winners',x=>x.fullRecovery60d],['Recovery60NonWinners',x=>!x.fullRecovery60d]
].map(([nm,fn])=>{const xs=n72.filter(fn).map(x=>x.fundamentals[k]);return[nm,{n:xs.length,mean:avg(xs),median:median(xs)}]}))]));
function pval(pos,neg){
 const n=pos+neg;if(!n)return null;let p=2**(-n),s=0;for(let k=0;k<=Math.min(pos,neg);k++){
 let choose=1;for(let i=1;i<=k;i++)choose*=(n-i+1)/i;s+=choose*p;
 }return Math.min(1,s*2);
}
function match(list,win,label){
 const cases=list.filter(win).sort((x,y)=>Math.abs(x.selloffPct)-Math.abs(y.selloffPct)||x.ticker.localeCompare(y.ticker)||x.selloffDate.localeCompare(y.selloffDate)),
 controls=list.filter(x=>!win(x)),used=new Set(),pairRows=[],unmatchedCases=[];
 for(const a of cases){
  const choices=controls.filter(b=>b.year===a.year&&b.session===a.session&&a.ticker!==b.ticker&&!used.has(b.ticker+'|'+b.selloffDate)
   &&Math.abs(Math.abs(a.selloffPct)-Math.abs(b.selloffPct))<=5)
   .sort((x,y)=>Math.abs(Math.abs(a.selloffPct)-Math.abs(x.selloffPct))-Math.abs(Math.abs(a.selloffPct)-Math.abs(y.selloffPct))
   ||x.ticker.localeCompare(y.ticker)||x.selloffDate.localeCompare(y.selloffDate));
  if(!choices.length){unmatchedCases.push({case:a.ticker+'|'+a.selloffDate,reason:'NO_CONTROL_SAME_YEAR_RELEASE_SESSION_DIFF_ISSUER_WITHIN_5PP'});continue}
  const b=choices[0];used.add(b.ticker+'|'+b.selloffDate);
  pairRows.push({case:a.ticker+'|'+a.selloffDate,control:b.ticker+'|'+b.selloffDate,
   cohortCase:a.cohort,year:a.year,releaseSession:a.session,
   earlyLowCase:a.earlyLowerLowByD3,earlyLowControl:b.earlyLowerLowByD3,
   dropGapPp:Math.abs(Math.abs(a.selloffPct)-Math.abs(b.selloffPct)),
   factors:Object.fromEntries(fspec.map(k=>[k,{case:a.fundamentals[k],control:b.fundamentals[k],difference:a.fundamentals[k]-b.fundamentals[k]}]))});
 }
 const factors=Object.fromEntries(fspec.map(k=>{
  const xs=pairRows.map(p=>p.factors[k].difference);
  let pos=xs.filter(x=>x>0).length,neg=xs.filter(x=>x<0).length,ties=xs.filter(x=>x===0).length;
  return[k,{pairCount:xs.length,meanDeltaCaseMinusControl:avg(xs),medianDeltaCaseMinusControl:median(xs),caseHigher:pos,caseLower:neg,ties,exactTwoSidedSignP:pval(pos,neg)}]}));
 return {label,eligibleN:list.length,cases:cases.length,controls:controls.length,
 pairs:pairRows.length,unmatched:unmatchedCases.length,
 meanSelloffGapPp:avg(pairRows.map(p=>p.dropGapPp)),
 factors,pairRows,unmatchedCases};
}
const result={
 experiment:'matched_quality164_fundamentals_v1_2026-10-11',
 status:'RETROSPECTIVE_DISCOVERY_PRIOR_OUTCOME_EXPOSURE',
 protocol:'frozen_164_match_fundamental_winners_losers_v1_2026-10-11.md',
 dataCoverage:{events:rows.length,continuousFundamentals:72,missingContinuousFundamentals:92,sourceOriginal92BinaryPreAnnouncementQualityPass:true,usedAnalystEPSRevisions:false},
 population:{all164:summary(rows),original92:summary(rows.filter(x=>x.cohort==='original92')),
 companyDisjoint72:summary(n72),AH91:summary(rows.filter(x=>x.session==='AH')),
 BMO73:summary(rows.filter(x=>x.session==='BMO')),
 earlyD3All:summary(rows.filter(x=>x.earlyLowerLowByD3)),
 AHearlyD3:summary(rows.filter(x=>x.earlyLowerLowByD3&&x.session==='AH')),
 yearSplit:Object.fromEntries([2023,2024,2025,2026].map(y=>[y,summary(rows.filter(x=>x.year===y))]))},
 fundamentalUnpaired72:unpaired,
 matched72:{
  d4:match([...n72],x=>x.tradeWin,'D4_TARGET_FIRST_VS_NOT'),
  recovery60:match([...n72],x=>x.fullRecovery60d,'FULL_RECOVERY_D60_VS_NOT'),
  d4EarlyLow:match(n72.filter(x=>x.earlyLowerLowByD3),x=>x.tradeWin,'D4_EARLY_LOW_BY_D3_ONLY')},
 events:rows
};
process.stdout.write(JSON.stringify(result,null,2)+'\n');
