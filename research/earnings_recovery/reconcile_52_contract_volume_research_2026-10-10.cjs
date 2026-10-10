#!/usr/bin/env node
'use strict';
// Reproducible offline consolidation of frozen 52 historical option contracts.
// No API calls, never imputes missing volume/quotes, no P&L from raw stock exit mismatches.
const fs=require('fs');
const root='research/earnings_recovery/';
const read=p=>JSON.parse(fs.readFileSync(root+p,'utf8'));
const src=read('frozen_100event_52_eod_affordable_contracts_for_volume_repair_2026-10-10.json');
const raw=read('raw_stock_price_dividend_exit_audit_100events_2026-10-10.json');
const rawMap=new Map(raw.all_setups.map(z=>[z.year+'|'+z.ticker+'|'+z.event+'|'+z.method,z]));
const paths=[
 'volume_repair_massive_historical_trade_probes_phase1_2026-10-10.json',
 'volume_repair_massive_historical_trade_probes_phase2_2026-10-10.json',
 'volume_repair_2025_remaining_phase3_2026-10-10.json',
 'volume_repair_2025_remaining_phase4_2026-10-10.json',
 'volume_repair_2024_remaining_phase5_2026-10-10.json'
];
const key=z=>[z.occ,z.entry,z.exit].join('|');
const observations=new Map();
for(const file of paths){
 if(!fs.existsSync(root+file)) continue;
 const obj=read(file);
 let arr=obj.probes||obj.cases||obj.observations;
 if(!arr && obj.records) arr=obj.records.map(([ticker,occ,entry,exit,first,volume,last,exitVolume])=>({ticker,occ,entry,exit,first,volume,last,exitVolume}));
 for(const z of arr||[]){
  const k=key(z);if(!src.entries.some(c=>key(c)===k))continue;
  const entryPrice=z.firstTrade!==undefined?z.firstTrade:(z.firstTradePrice!==undefined?z.firstTradePrice:(z.first!==undefined?z.first:null));
  const entryVol=z.entryVolume!==undefined?z.entryVolume:(z.entryContractVolume!==undefined?z.entryContractVolume:(z.volume!==undefined?z.volume:null));
  const exitPrice=z.exitTrade!==undefined?z.exitTrade:(z.exitLastTradePrice!==undefined?z.exitLastTradePrice:(z.last!==undefined?z.last:null));
  const exitVol=z.exitVolume!==undefined?z.exitVolume:(z.exitContractVolume!==undefined?z.exitContractVolume:null);
  const status=(z.status || 'OK').slice(0,120);
  observations.set(k,{provider_status:status,entry_option_first_trade:entryPrice,entry_option_volume:entryVol,exit_option_last_trade:exitPrice,exit_option_volume:exitVol,source_file:file});
 }
}
const rows=src.entries.map(c=>{
 const r=rawMap.get([c.year,c.ticker,c.event,c.method].join('|'))||{};
 const o=observations.get(key(c));
 const result={...c,raw_stock_exit:r.raw_exit||null,raw_stock_exit_reason:r.raw_exit_reason||null,raw_stock_exit_matches_saved:r.original_exit_matches_raw??null,
  source_status:o?.provider_status||'UNQUERIED',source_file:o?.source_file||null,entry_option_first_trade:o?.entry_option_first_trade??null,
  entry_option_volume:o?.entry_option_volume??null,exit_option_last_trade:o?.exit_option_last_trade??null,exit_option_volume:o?.exit_option_volume??null};
 const goodSource=result.source_status==='OK';
 const first=result.entry_option_first_trade,volume=result.entry_option_volume;
 if(!goodSource){
  result.entry_screen='UNKNOWN_SOURCE_'+(result.source_status==='UNQUERIED'?'UNQUERIED':result.source_status.includes('RATE_LIMIT')?'RATE_LIMIT':result.source_status.includes('ENTITLED')?'NOT_ENTITLED':result.source_status.includes('EMPTY')?'EMPTY':'OTHER');
 }else if(first===null||volume===null){
  result.entry_screen='NO_RECORDED_OPTION_ENTRY_TRADE';
 }else if(first*100+.65>50){
  result.entry_screen='BUDGET_FAIL';
 }else if(volume<10){
  result.entry_screen='VOLUME_FAIL';
 }else{
  result.entry_screen='PASS_BUDGET_AND_ENTRY_DAY_VOLUME_FOR_SAMPLED_CONTRACT';
 }
 result.first_trade_debit=first===null?null:+(first*100+.65).toFixed(2);
 result.exit_available_on_correct_raw_stock_exit_day=goodSource&&r.raw_exit===c.exit&&result.exit_option_last_trade!==null;
 result.first_to_last_trade_proxy_return_pct=result.entry_screen==='PASS_BUDGET_AND_ENTRY_DAY_VOLUME_FOR_SAMPLED_CONTRACT'&&result.exit_available_on_correct_raw_stock_exit_day?
   +(((result.exit_option_last_trade*100-.65)/(first*100+.65)-1)*100).toFixed(3):null;
 result.strict_closest_strike_verified=false;
 result.executable_quote_verified=false;
 return result;
});
const count=(arr,name)=>Object.fromEntries([...new Set(arr.map(z=>z[name]))].map(k=>[k,arr.filter(z=>z[name]===k).length]).sort());
const summary={candidate_count:rows.length,by_year:count(rows,'year'),source_status:count(rows,'source_status'),entry_screen:count(rows,'entry_screen'),
 checked:rows.filter(x=>x.source_status!=='UNQUERIED').length,remaining_unqueried:rows.filter(x=>x.source_status==='UNQUERIED').length,
 pass_sampled_entry_screen:rows.filter(x=>x.entry_screen.startsWith('PASS_')).length,
 sampled_pass_with_correct_raw_exit_print:rows.filter(x=>x.first_to_last_trade_proxy_return_pct!==null).length};
const out={run_date:'2026-10-10',scope:'The frozen 52 EOD ask selected calls, not a full historical options chain or first-trade chosen option strategy. 2024/2025 data already inspected previously.',disclaimer:'Daily option trade first/last prices are ASYNCHRONOUS and are not executable NBBO at opening or stock target. Missing option trade does not prove option worthless. Strict closest-affordable strike not checked. Neither successful screens nor conditional quote returns establish expectancy.',summary,rows};
const dest=root+'frozen_52_contract_volume_reconciliation_2026-10-10.json';
fs.writeFileSync(dest,JSON.stringify(out,null,2)+'\n');
console.log(JSON.stringify({saved:dest,summary,verified_examples:rows.filter(x=>x.first_to_last_trade_proxy_return_pct!==null).map(x=>({ticker:x.ticker,date:x.entry,ret:x.first_to_last_trade_proxy_return_pct}))},null,2));
