// Research calculation for options_execution_model_protocol_2026-10-10.md
// Input: JSON research/earnings_recovery/actionable_bounce_event_price_windows_164_2026-10-10.json
const fs=require('fs'); const data=JSON.parse(fs.readFileSync(process.argv[2],'utf8')); const results=(function analyze(data){
 const idx=data.eventIndexWithinBars;
 const MS=86400000;const dateN=d=>Date.parse(d+"T12:00:00Z");const cdf=x=>{const t=1/(1+0.2316419*Math.abs(x)),d=.3989422804014327*Math.exp(-x*x/2);const p=1-d*t*(.319381530+t*(-.356563782+t*(1.781477937+t*(-1.821255978+t*1.330274429))));return x>=0?p:1-p};
 function call(s,k,iv,caldays){const T=Math.max(0.0000001,caldays)/365,r=.04,sigma=Math.max(.10,iv);const z=Math.log(s/k)+(r+.5*sigma*sigma)*T;const d1=z/(sigma*Math.sqrt(T)),d2=d1-sigma*Math.sqrt(T);return Math.max(s*cdf(d1)-k*Math.exp(-r*T)*cdf(d2),0)}
 function entries(e){
  const bars=e.bars,ev=idx,anchor=bars[ev][4],res={next_open:ev+1,day3:ev+3,sma5_reversal:null,three_rising_lows_break:null};
  for(let t=ev+5;t<=ev+20 && t+1<bars.length;t++){
   const ma=bars.slice(t-4,t+1).reduce((a,b)=>a+b[4],0)/5,pma=bars.slice(t-5,t).reduce((a,b)=>a+b[4],0)/5;
   if(bars[t][4]>ma&&bars[t-1][4]<=pma&&bars[t][4]>bars[t-1][2]){if(bars[t+1][1]<=1.08*anchor)res.sma5_reversal=t+1;break}
  }
  for(let t=ev+3;t<=ev+20 && t+1<bars.length;t++){
   if(bars[t-2][3]<=bars[t-1][3]&&bars[t-1][3]<=bars[t][3]&&bars[t][4]>Math.max(bars[t-2][2],bars[t-1][2])){if(bars[t+1][1]<=1.08*anchor)res.three_rising_lows_break=t+1;break}
  }
  return res;
 }
 const scenarios=[],rows=[];
 for(const e of data.series){
  const ent=entries(e);
  for(const method of Object.keys(ent)){
   const i=ent[method];if(i===null||i>=e.bars.length)continue;
   const S=e.bars[i][1],entTime=dateN(e.bars[i][0]);
   for(const dte of [14,30,45,60,90])for(const iv0 of [.25,.4,.6])for(const drift of [-.1,0,.1]){
    const init=call(S,S,iv0,dte);
    const debit=100*init*1.01+.65;
    const ivAt=day=>Math.max(.1,iv0+drift*Math.min(10,Math.max(0,day))/10);
    const liquid=(spot,elapsed)=>Math.max(0,100*call(spot,S,ivAt(elapsed),Math.max(.1,dte-elapsed))*.99-.65);
    let reason="timeout", exitIdx=i, exitPrice=S,exitElapsed=0,expiryEdge=false,minimum=debit;
    for(let j=i;j<Math.min(e.bars.length,i+20);j++){
     const bar=e.bars[j],el=(dateN(bar[0])-entTime)/MS;
     if(el>=dte)break;
     const elTouch=el+.5,elEnd=el+.95;
     const lowNet=liquid(bar[3],elTouch);
     if(lowNet<minimum)minimum=lowNet;
     let px=0;
     if(j>i&&bar[1]<=S*.95){reason="stop";px=bar[1]}
     else if(j>i&&bar[1]>=S*1.05){reason="target";px=bar[1]}
     else if(bar[3]<=S*.95){reason="stop";px=S*.95}
     else if(bar[2]>=S*1.05){reason="target";px=S*1.05}
     const next=e.bars[j+1];
     const nextDays=next?(dateN(next[0])-entTime)/MS:1e9;
     const lastByDTE=nextDays>=dte || !next;
     const lastByHold=j===i+19;
     if(px){exitIdx=j;exitPrice=px;exitElapsed=elTouch;break}
     if(lastByDTE||lastByHold){exitIdx=j;exitPrice=bar[4];exitElapsed=elEnd;reason=lastByDTE?"pre_expiry_close":"time_close";expiryEdge=lastByDTE;break}
    }
    const proceeds=liquid(exitPrice,exitElapsed),ret=100*(proceeds-debit)/debit;
    rows.push({cohort:e.cohort,ticker:e.ticker,event:e.date,method,dte,iv0,drift,entry:e.bars[i][0],entryPrice:S,exit:e.bars[exitIdx][0],reason,returnPct:ret,drawdownPct:100*(minimum-debit)/debit,debit,proceeds,expiryEdge});
   }
  }
 }
 const stats=v=>{const sorted=v.map(x=>x.returnPct).sort((a,b)=>a-b),n=v.length;return {n,wins:v.filter(x=>x.returnPct>0).length,winPct:100*v.filter(x=>x.returnPct>0).length/n,avg:sorted.reduce((a,b)=>a+b,0)/n,median:(sorted[Math.floor((n-1)/2)]+sorted[Math.floor(n/2)])/2,p10:sorted[Math.floor(n*.1)],meanMaxDrawdownPct:v.reduce((a,b)=>a+b.drawdownPct,0)/n,stops:v.filter(x=>x.reason==="stop").length,targets:v.filter(x=>x.reason==="target").length,expiryCloses:v.filter(x=>x.expiryEdge).length}}
 const grouped=[],keyOf=x=>[x.cohort,x.method,x.dte,x.iv0,x.drift].join("|");
 const groups={};for(const x of rows)(groups[keyOf(x)]??=[]).push(x);
 for(const [key,v] of Object.entries(groups)){const [cohort,method,dte,iv0,drift]=key.split("|");grouped.push({cohort,method,dte:+dte,iv0:+iv0,drift:+drift,...stats(v)})}
 const defaultRows=grouped.filter(x=>x.iv0===.4&&x.drift===-.1).sort((a,b)=>a.cohort.localeCompare(b.cohort)||a.method.localeCompare(b.method)||a.dte-b.dte);
 const sensitivities=grouped.filter(x=>x.method==="three_rising_lows_break"&&x.dte===45).sort((a,b)=>a.cohort.localeCompare(b.cohort)||a.iv0-b.iv0||a.drift-b.drift);
 const matched=[];const es=Object.fromEntries(data.series.map(e=>[e.cohort+"|"+e.ticker+"|"+e.date,e]));
 const methods=["sma5_reversal","three_rising_lows_break"];
 for(const cohort of ["original92","holdout72"])for(const method of methods)for(const dte of [14,30,45,60,90]){
  const ix=rows.filter(x=>x.cohort===cohort&&x.method===method&&x.dte===dte&&x.iv0===.4&&x.drift===-.1);
  const comparison=rows.filter(x=>x.cohort===cohort&&x.method==="day3"&&x.dte===dte&&x.iv0===.4&&x.drift===-.1);
  const look=Object.fromEntries(comparison.map(x=>[x.ticker+"|"+x.event,x]));
  const matchedEntries=ix.map(x=>({name:x.ticker,entry:x,day3:look[x.ticker+"|"+x.event]})).filter(x=>x.day3);
  matched.push({cohort,method,dte,n:matchedEntries.length,entryAvg:matchedEntries.reduce((a,x)=>a+x.entry.returnPct,0)/matchedEntries.length,day3Avg:matchedEntries.reduce((a,x)=>a+x.day3.returnPct,0)/matchedEntries.length,diffPpt:matchedEntries.reduce((a,x)=>a+x.entry.returnPct-x.day3.returnPct,0)/matchedEntries.length});
 }
 return {metadata:{events:data.series.length,original:data.series.filter(x=>x.cohort==="original92").length,holdout:data.series.filter(x=>x.cohort==="holdout72").length,scenarioTrades:rows.length,uniqueExecutions:rows.length/45,generatedDate:"2026-10-10"},defaultRows,sensitivities,matched,grouped,rows,code:analyze.toString()};
})(data); console.log(JSON.stringify({metadata:results.metadata,defaultRows:results.defaultRows,sensitivities:results.sensitivities,matched:results.matched,fullScenarioAggregates:results.grouped},null,2));
