/**
 * node research/earnings_recovery/run_rsi5_sma5_asofD3_quality164_v1.mjs
 * Reproduces one prespecified daily D3 Cutler RSI5 + SMA5 descriptive experiment.
 * No future OHLC used in any input; historical outcomes already exposed.
 */
import fs from 'node:fs';import path from 'node:path';
const dir='research/earnings_recovery';
const get=f=>JSON.parse(fs.readFileSync(path.join(dir,f),'utf8'));
const ev=[...get('actionable_bounce_price_windows_92events_2026-10-10.json').events,
...get('actionable_bounce_price_windows_72events_2026-10-10.json').events];
const pre=get('matched_quality164_fundamentals_v1_all_events_pairs_2026-10-11.json');
const pairs=get('quality164_asofD3_sector_market_factors_fullmatched_results_2026-10-11.json').matched;
const known=new Map(pre.events.map(x=>[x.ticker+'|'+x.selloffDate,x]));
function mean(x){return x.length?x.reduce((a,b)=>a+b,0)/x.length:null}
function median(x){if(!x.length)return null;x=[...x].sort((a,b)=>a-b);return(x[Math.floor((x.length-1)/2)]+x[Math.floor(x.length/2)])/2}
function ma5(b,j){return mean(b.slice(j-4,j+1).map(row=>row[4]))}
function rsi5(b,j){let g=0,l=0;for(let k=j-4;k<=j;k++){let d=b[k][4]-b[k-1][4];if(d>=0)g+=d;else l-=d;}return(g+l)?100*g/(g+l):50}
const rows=ev.map(e=>{const t=known.get(e.ticker+'|'+e.selloff_date),b=e.bars,j=e.event_index+3;
 if(!t||j<6)throw Error('Misaligned '+e.ticker+e.selloff_date);
 return{ticker:e.ticker,date:e.selloff_date,cohort:e.cohort,session:t.session,year:t.year,
 d4TargetFirst:t.tradeWin,fullRecovery60d:t.fullRecovery60d,earlyLowByD3:t.earlyLowerLowByD3,
 features:{rsi5CutlerD3:rsi5(b,j),rsi5ChangeD1ToD3:rsi5(b,j)-rsi5(b,j-2),
 sma5DistanceD3Pct:100*(b[j][4]/ma5(b,j)-1),
 sma5SlopeD2ToD3Pct:100*(ma5(b,j)/ma5(b,j-1)-1)}}});
if(rows.length!==164)throw Error('Wrong cohort');
const names=Object.keys(rows[0].features),lookup=new Map(rows.map(x=>[x.ticker+'|'+x.date,x]));
function desc(all,label){const w=all.filter(x=>x[label]),l=all.filter(x=>!x[label]);
return{n:all.length,w:w.length,l:l.length,features:Object.fromEntries(names.map(k=>[k,{
 winnerMedian:median(w.map(x=>x.features[k])),loserMedian:median(l.map(x=>x.features[k])),
 winnerMean:mean(w.map(x=>x.features[k])),loserMean:mean(l.map(x=>x.features[k]))}]))}}
const group=a=>({d4:desc(a,'d4TargetFirst'),full60:desc(a,'fullRecovery60d')});
function p2(a,b){let n=a+b;if(!n)return null;let v=0;for(let k=0;k<=Math.min(a,b);k++){let c=1;for(let i=1;i<=k;i++)c=c*(n-i+1)/i;v+=c/2**n}return Math.min(1,2*v)}
function matched(group){
 const rs=group.pairs.map(x=>{
 let a=lookup.get(x.case),b=lookup.get(x.control);
 if(!a||!b)throw Error('Lost sector matched pair');
 return{case:x.case,control:x.control,sector:x.sector,session:x.session,caseCohort:a.cohort,controls:b.cohort,year:x.year,
 diffs:Object.fromEntries(names.map(k=>[k,a.features[k]-b.features[k]]))}});
 return{n:rs.length,ah:rs.filter(x=>x.session==='AH').length,
 features:Object.fromEntries(names.map(k=>{
  const a=rs.map(x=>x.diffs[k]),up=a.filter(x=>x>0).length,down=a.filter(x=>x<0).length;
  return[k,{pairedCount:a.length,caseHigher:up,caseLower:down,tied:a.length-up-down,
    medianCaseMinusControl:median(a),meanCaseMinusControl:mean(a),twoSidedSignP:p2(up,down),
    originalCaseHigher:rs.filter(x=>x.caseCohort==='original92'&&x.diffs[k]>0).length,
    originalCases:rs.filter(x=>x.caseCohort==='original92').length,
    disjointCaseHigher:rs.filter(x=>x.caseCohort==='separate72'&&x.diffs[k]>0).length,
    disjointCases:rs.filter(x=>x.caseCohort==='separate72').length,
    ahCaseHigher:rs.filter(x=>x.session==='AH'&&x.diffs[k]>0).length,
    ahCases:rs.filter(x=>x.session==='AH').length}]})),pairs:rs}};
const result={id:'rsi5_sma5_164_asofD3_2026-10-11',
 protocol:'frozen_d3_rsi5_sma5_quality164_exploratory_2026-10-11.md',
 classification:'Previously outcome exposed; historical 5d Cutler RSI not conventional 14d Wilder; daily close at D3 before D4 stock OPEN; no VWAP measured',
 coverage:rows.length,features:names,
 groups:{all164:group(rows),AH91:group(rows.filter(x=>x.session==='AH')),
  original92:group(rows.filter(x=>x.cohort==='original92')),
  disjoint72:group(rows.filter(x=>x.cohort==='separate72')),
  AH54Early:group(rows.filter(x=>x.session==='AH'&&x.earlyLowByD3))},
 matched:{d4:matched(pairs.d4StockFirstHit),full60:matched(pairs.fullRecovery60)},rows};
process.stdout.write(JSON.stringify(result,null,2)+'\n');
