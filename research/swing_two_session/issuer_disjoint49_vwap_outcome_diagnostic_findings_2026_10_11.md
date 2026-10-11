# Range false-break + VWAP reclaim: frozen 49-issuer independent-stock two-session diagnostic RESULTS
Date: 2026-10-11
**VERDICT: FAILED INDEPENDENT-ISSUER PRICE OUTCOME REPLICATION (DIAGNOSTIC). FROZEN v2 SOURCE/PIT CERTIFICATION INCOMPLETE -> research-only, NOT a production-certified test. NO TRADABLE STOCK OR $50 CALL EDGE.**

## Experiment lineage and integrity
Prior review **committed before protocol** research/prior_work/range_failed_support_vwap_replication_prior_review_2026-10-11.md .
Immutable frozen protocol research/swing_two_session/frozen_issuer_disjoint_range_vwap_replication_v2_2026_10_11.md ; source QA and outcome execution detail written BEFORE any future M5 downloaded: research/swing_two_session/source_gate_106_pre_outcome_memo_2026_10_11.md .
The source roster: Webull adjusted DAILY 1000 bars for each of 49 different tickers (original 20 all excluded), signals 2024-01-02 to 2026-09-30. Unchanged 40-day support/touches/break-reclaim/volume original v1 yielded EXACT **106** daily candidates in **41** tickers, year counts 40/39/27. Price/candidate lists ALL committed before the post-signal minute history. No earnings-date or ticker cherry-pick, no filtering by PnL. Not an OOS-in-time cohort, but genuine company-disjoint original 20 list and partially overlapping calendar years.
Source QA: **all 106 event days M5 fetched** 105 complete 78 bar normal RTH; NOC Oct30 2024 had 77. Webull D forward-adjusted prices and M5 unadjusted are explicit in operator documentation https://developer.webull.com/apis/docs/reference/broker-market-data-api/bars-using-get/ . Same-date ratio rebasing D close divided by as-traded M5 close makes high/low match almost exactly across 105/106, one discrepancy >0.5%. D volumes are greater than RTH-minute total in 106/106, median1.215x, >=2x in14, five >=5x; extraordinary ratios Netflix pre-10for1 Nov17 2025, ServiceNow pre-5for1 Dec18 2025, CrowdStrike pre-4for1 Jul02 2026, independently dated SEC original filings https://www.sec.gov/Archives/edgar/data/1065280/000106528025000407/nflx-20251030.htm ; https://www.sec.gov/Archives/edgar/data/1373715/000137371525000321/now-20251205.htm ; https://www.sec.gov/Archives/edgar/data/1535527/000153552726000022/crwd-20260603.htm . Future share-split adjustments apply uniformly to old periods; annual and 20-day relative volume ratios invariant if factors are consistent. But no full historical 49-name calendar of intrawindow corporate actions and exact venue/extended-hours volume mapping fully certified. Daily signal reused exactly Webull D in original v1, never substituted raw M5 volume for its prespecified >1.2x rule. **Therefore formal FULL v2 certification still FAILED at source gate regardless of stats.**
Raw all106 signal-day M5 archived research/swing_two_session/data/qa_106_signal_day_m5_batch01..06_2026_10_11.json and source summary research/swing_two_session/data/all106_frozen_signal_day_m5_source_qa_results_2026_10_11.json .
ALL post-event historical two-session Webull raw M5 paths 106 retrieved only AFTER frozen execution memorandum, six archive batches research/swing_two_session/data/forward_two_session_m5_diagnostic_batch01..06_2026_10_11.json . 3 unknown incomplete: ADBE 2025-07-02 -> next July03 42 bars holiday session; FDX 2024-12-23 -> Dec24 42 bars Christmas Eve half day; NOC 2024-10-30 source signal day only77, Oct31/Nov01 followup76/67 missing. NO favorable filtering; all three excluded as UNKNOWN DATA, not losses or zero-return events. 103/106 fully evaluable price paths across 41 names.
Machine per-event outcomes and grouping research/swing_two_session/data/issuer_disjoint49_vwap_106event_raw_m5_outcome_diagnostic_2026_10_11.json , saved executable Node algorithm research/swing_two_session/run_disjoint49_m5_vwap_outcome_diagnostic_v2_2026_10_11.mjs . The Node runner is committed but its exact local Node execution has NOT been independently verified; numeric study was actually computed in functions.exec using the same described logic and saved result (no need to claim script run if not).

## Frozen execution
Cumulative RTH VWAP uses raw M5 typical-price (H+L+C)/3 times M5 volume. Need at least one COMPLETED close below VWAP, followed by FIRST two CONSECUTIVE completed closes above current cumulative VWAP. Next completed bar OPEN, not later than 12:00 pm ET. If no such signal/too late, NO ENTRY, zero outcome per original daily signal. Compare to first 9:30 M5 opening purchase in same event universe. From entry to close SECOND complete 78-bar post-signal regular session, target +2% vs stop -2% first (stop-first 5m both-high-and-low), next-session adverse or favorable gap fills actual opening price, otherwise second-session last 15:55 candle CLOSE. Total roundtrip hypothetical fees/slippage 0 / 0.20% / 0.50% / 1.00%; NOT actual exchange execution or options PnL. Benchmark and candidate trade horizon consistent to SECOND post-signal trading session, meaning late VWAP entries sacrifice time relative to benchmark.
Exact 103 evaluable: VWAP **76 ENTERED** (first entry as early as 9:45 ET and as late as 11:50 ET) and **27 SKIPPED** (14 too late; 13 no complete trigger). Of 76 trades, +2 target first **18**, stop first **25**, TIMEOUT **33**, zero 5min ambiguous both-hit bars. Conditional target-first 18/76=23.68%, *not a win rate after timeouts*; other 58 did not touch +2 before deadline.

## The defining failure: prior cohort versus genuinely other issuers
| Measure | Original 2022-26 20-name 63-candidate study (result exposed previously, itself selected) | Frozen different-issuer 2024-Sep2026 106 D-candidate / 103 source-evaluable diagnostic |
| --- | ---: | ---: |
| Eligible source events | 63 | 106 candidates / 103 complete and evaluated |
| VWAP entries | 38 | 76 |
| +2 before -2 first-hit targets | 24 | 18 |
| Target/entries | 63.16% | 23.68% |
| Net stock PnL per eligible original event 0.20% fees | +0.574% | **-0.335%** |
| Net per eligible event 0.50% fees | +0.393% | **-0.557%** |
| Net per entered position 0.50% fees | n/a | **-0.754%** |

**New 103-event paired opening vs waiting-for-VWAP** (averaged per complete event):
| Total round-trip cost | VWAP net/event | Open net/event | VWAP incremental pp/event |
|---|---:|---:|---:|
| ZERO cost | -0.1876% | -0.3225% | +0.1348pp |
| 0.20% | **-0.3352%** | -0.5225% | +0.1873pp |
| 0.50% | **-0.5565%** | -0.8225% | +0.2659pp |
| 1.00% | **-0.9255%** | -1.3225% | +0.3970pp |

Why incremental VWAP over opening rises with costs: VWAP skips 27/103 cases while opening pays fee for all103. A seemingly positive relative difference does NOT make absolute VWAP trading profitable, and its statistical evidence is not convincing.

## Frozen 95% ticker-cluster bootstrap at 0.50% total friction, 41 issuers, 10k deterministic replicates
VWAP mean net per daily eligible event CI **[-0.8193%, -0.2777%]**, entirely BELOW zero in this tested issuer panel.
Paired VWAP minus open mean CI **[-0.0529pp, +0.5680pp]**, INCLUDES ZERO. Additional date-cluster (88 distinct signal dates, 8k replicates, diagnostic only): net CI **[-0.8667%, -0.2523%]**; paired difference CI **[-0.0106pp,+0.5406pp]**.
The signal **was negative in ALL three prespecified calendar splits** at 50bps:
2024 n38, entries29, targets10, net/event -0.318%; 2025 n38, entries29, targets4, net/event -0.799%; 2026 n27, entries18, targets4, net/event -0.551%. Original positive apparent stability across periods doesn't generalize across issuer groups.
Top3 positive contributing issuer SLB+MCD+CVX =47.40% of positive issuer contributions; 50% concentration gate formally not violated, but absolute mean/gate are FAILED, irrelevant. 103 first-open benchmark trades: 27 +2 targets / 37 -2 stops / 39 timeouts; gross mean -0.322%.

## Verdict, execution/source uncertainties and next priority
Frozen promotion checks: sample>=40 PASS, >=12 issuer PASS, >=25 entries PASS, top3 positive issuer contribution share<=50 PASS, positive 50bp mean and ticker bootstrap lower >0 **FAIL**, paired improvement confidence lower>0 **FAIL**, fully certified source PIT/exdate/volume **NOT MET**. These outcome numbers are DIAGNOSTIC ONLY because the stricter source gate is still not fully certified, but the signal fails meaningful profitable-expectancy metrics in each year and BEFORE any modeled fees. This is substantive negative evidence for generalizing the former 63 case edge, not a rescue opportunity.
**DO NOT** optimize VWAP closes from two to one, expand noon cutoff, change support touches/tolerance, shift +2/-2 barrier, cherry-pick the 2024 winners, switch to an easier baseline, or use this same 2024-26 cohort as an untouched test again. This diagnostic sample is now OUTCOME EXPOSED. Original 63 and new106 exact inputs/results retained separately for audit.

No buying actual calls or puts on these rules based on this study. No scanner/automation A+ promotion. For future range reversal work, one materially DIFFERENT hypothesis or independent year/security panel + mandatory fresh prior review/freeze is necessary. More sensible research priority may be **identify truly nonfundamental liquidity shocks** ahead of a rebound instead of chart-only false support reclaim, but only after assembling an as-of news/flow taxonomy and genuine new holdout with executable stock/option data. Do not buy paid history or reoptimize this failed VWAP rule.
