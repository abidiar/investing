# Range-failure + next-session VWAP reclaim: full106 frozen signal-date volume reliability test
Date: 2026-10-11
**VERDICT: SOURCE / CORPORATE-ACTION VOLUME SENSITIVITY TEST COMPLETED; INDEPENDENT VWAP+2/-2 RETURN TEST NOT EXECUTED; NO STOCK / CALL TRADING EDGE PROMOTED.**

## Context and preregistration
Mandatory governance and original unchanged 2026-Oct09 63-event protocol reviewed. Prior work committed BEFORE freeze at research/prior_work/range_failed_support_vwap_replication_prior_review_2026-10-11.md. Frozen v2 49-issuer disjoint universe (all different from original 20), Jan2024–Sep2026, under research/swing_two_session/frozen_issuer_disjoint_range_vwap_replication_v2_2026_10_11.md. Original v1 from 63 selected historical signals: 38 VWAP entries, 24 stock target-first, stock net +0.574% per original daily signal at 20bp hypothetical transaction cost and +0.092% per original signal at 100bp, three stocks 60.4% original sample gains. Cannot promote due unaddressed source data/selection bias and no verified actual calls.

NEW v2 DAILY source acquired 49/49 fixed disjoint tickers × 1,000 D bars, raw saved 5 CSVs; 106 D-reclaim & >=1.2x daily volume signals across 41 stocks (40 in 2024, 39 in 2025, 27 through Sep2026), candidate and original past40 source preserved research/swing_two_session/data/disjoint49_daily_screen_preliminary_2026_10_11.json. These are *candidate signal days*, NOT filled stock trades or option calls.

NEW completed source QA on all106:
- Frozen BEFORE M5 query: research/swing_two_session/data/frozen106_event_day_m5_source_audit_manifest_2026_10_11.json includes all 106 fixed symbol dates, D OHLCV, prior20 trading dates, 20 daily source volume baseline.
- Webull M5 RTH source queried for each event as-of EVENT CLOSE ONLY, excluding all future trading. All 106 event source returned, 105/106 contain 78 RTH M5 bars; one NOC 2024-10-30 returned only 77 (do not call complete). Raw 106 event-day FIVE-MINUTE OHLCV bars (and up-to-15 recent prior day aggregates) saved nine immutable chunks frozen106_source_m5_signalday_chunk01..09_2026_10_11.json.
- Additional historical M5 source fetched per event for 20 sessions preceding original signal day, and aggregate original per-day M5 RTH volume archived nine frozen106_source_m5_prior20_extension_chunk01..09_2026_10_11.json. **106/106 previous20 date histories present** after deduping overlaps by more complete day's bar count. **85/106** had all 20 previous session days exactly 78 RTH M5 bars; 21/106 had at least one historical partial session, some legitimate 41/42 shortened holiday sessions and some 77/78 source holes (not assigned a favorable result). No new post-signal VWAP bar retrieved or outcome scored.

## Critical provider/issuer resolution of split-related discrepancies
Webull documentation https://developer.webull.com/apis/docs/reference/broker-market-data-api/bars-using-get/ explicitly says D/W/M/Y candles are forward adjusted while M1/M5 candles are NOT. Present-day historical DAILY share volumes for splits AFTER the historical candidate event are already adjusted to today's share units. Earlier raw minute data remain as-traded share units. This is not a real 10x short-term participation shock.

Among 106 source daily event cases, raw D share vol / RTH M5 raw share vol median = 1.215, and 14/106 exceeded 2x. Original issuer filings proved SIX very large historical ratio discrepancies caused chiefly by SUBSEQUENT share splits:
- NFLX 10-to-1 EFFECTIVE 2025-Nov17; 2024-Jul25, 2025-Apr07, 2025-Oct02, 2025-Nov03 signals ratios originally ~10.49–11.05, after normalization to same shares ~1.05–1.10. Original 2025-Oct30 release https://ir.netflix.net/investor-news-and-events/financial-releases/press-release-details/2025/Netflix-Announces-Ten-For-One-Stock-Split/default.aspx . One case Nov03 was only known as announcement dated prior Friday, yet split effects not until Nov17; others announced after event.
- NOW 5-to-1 effective 2025-Dec18, 2025-Nov04 event ratio5.977, normalized1.195. 2025-Dec05 issuer approval release https://investor.servicenow.com/news/news-details/2025/ServiceNow-Shareholders-Approve-5-for-1-Stock-Split/default.aspx ; Nov04 issuer board proposed earlier 2025-Oct29, actual final effective after Nov event.
- CRWD 4-to-1 effective 2026-Jul02, 2026-Jan16 event ratio4.473, normalized1.118. 2026-Jun03 issuer announcement https://ir.crowdstrike.com/news-releases/news-release-details/crowdstrike-reports-first-quarter-fiscal-year-2027-financial/ .
Correct only the SOURCE AUDIT volume denominator by confirmed future split factors. Do NOT inject future split event as trading factor. A split effective AFTER candidate and its preceding20 scales all 21 DAILY historical volume bars by same constant, which cancels in the original original 1.2x *daily* RVOL signal. This specific artifact does not imply lookahead in dimensionless same-era relative volume. If exdates between candidate and preceding20, re-adjustments must be applied with event-known dates and new data audit.

After split correction **8/106** still show ratio D historical daily / total RTH 5min **above 2x**: DIS 2026-Jun26, TGT 2025-Mar21, PG 2025-Jul09, KO 2025-Sep19, V 2024-Apr11+Apr16, UNH 2026-Sep18, ABBV 2026-Mar20. All have 78 M5 RTH bars on event day. Unresolved causes include official exchange/closing auction, consolidated vs subscribed/venue data coverage, block volume, or provider bars; **do NOT assign a specific cause without independent source**.

## NEW decisive frozen 20-session volume eligibility *sensitivity*
Original D-series fixed qualifier>=1.2 times preceding20 average was TRUE **106/106** by initial source screening.
The *same numerical threshold* applied to RTH M5 completed-bar aggregated volumes over the actual matching prior20 dates was TRUE **100/106**, FALSE **6/106**.
No entry/return calculations in this diagnostic. Six EXACT disagreement event dates (all have all prior20 M5 date coverage, none are from known split six):
| Date | Ticker | Webull D-source prior20 RVOL | Webull M5 RTH-source prior20 RVOL |
|---|---|---:|---:|
| 2026-06-26 | DIS | 1.2753 | 0.9271 |
| 2025-11-06 | PG | 1.2504 | 1.1649 |
| 2025-09-19 | KO | 1.7815 | 1.0616 |
| 2024-04-11 | V | 1.3164 | 1.0073 |
| 2024-04-16 | V | 1.2732 | 0.8073 |
| 2026-09-18 | UNH | 1.8149 | 0.7552 |
These six all have complete 78 bars on *their signal day* and 20 prior RTH dates present with no recorded non-78 prior sessions. Inconsistent volume in complete RTH intervals demonstrates different provider source aggregation or split/other-volume basis requiring further audit; not a simple missing five-minute bar. PG near threshold 1.165 vs 1.25; DIS/KO/V/UNH much larger conflicts. 2024, 2025 and 2026 each contain two discordances.
**Rule remains frozen as DAILY volume>1.2** and therefore original preliminary daily universe still 106; it is NOT legitimate to drop these six retrospectively or secretly use M5 RTH volume instead.

## Prior frozen 18-case price-quality audit
Source-dated independent 18 original daily candidate audit retrieved event +prior40 M5 RTH O/H/L/C/volume. Raw M5 unadjusted supported 11/18 while normalized-on-price-basis source QA supported 17/18. Seven within/lookback dividend exdates sourced, explaining non-equivalence of raw support to dividend-adjusted support. Raw normalized reconstruction is a QA indicator ONLY and did not prove all 106/49 histories date-verified. On the 18 cases only UNH Sep18 disagreed after source normalized on volume alone. After full106 previous20 measured, UNH actual M5 RTH RVOL =0.7552 vs daily1.8149, consistent with earlier 0.7556 RTH result.

## V2 GO / NO-GO
**DATA SOURCE SENSITIVITY TEST COMPLETED. FROZEN v2 INDEPENDENT STOCK PROFITABILITY EXPERIMENT NOT RUN, by original v2 protocol, because full49 corrected as-of 40-session signal-day split/dividend and source-equivalent OHLC/volume census not fully certified.** Have not accessed or scored even one post-signal VWAP next session, stock first +2/-2, alternative opening benchmark, net at 20/50/100bp, or any historical option ask/bid/IV. The 106/106 and 100/106 figures are signal **coverage** / source eligibility, not 106 trades or target success. Price adjusted basis same-bar high/low differs at some event dates despite per-day normalized close; historical M5 often 77/78 bars. Provider daily volumes and RTH only differ legitimately due coverage, plus forward share split adjustment. Don't assert that all six daily signals are invalid; don't use historical future known split to predict outcomes.

## Reproducible records
- Full original immutable signal+prior20 manifest: research/swing_two_session/data/frozen106_event_day_m5_source_audit_manifest_2026_10_11.json
- Nine raw original M5 signal day chunks and nine prior M5 historical full20 extension source chunks described above.
- Complete 106 D-vs-M5 signal-day audit: research/swing_two_session/data/frozen106_signalday_webull_daily_vs_m5_fullsource_audit_2026_10_11.json
- Original issuer split-adjusted source comparison: research/swing_two_session/data/frozen106_split_explained_daily_vs_rth_volume_2026_10_11.json
- Full 106 prior20 source RVOL results: research/swing_two_session/data/frozen106_full20d_daily_vs_rth_m5_rvol_diagnostic_2026_10_11.json
- Reproducible reducer research/swing_two_session/run_106_prior20_rth_volume_source_audit_2026_10_11.mjs

**Next clean operation** not another moving threshold: provider/issuer-specific corporate-action split/ex-date schedules for 49 issuers and as-of point-in-time 40-session relative support, plus direct reconciliation of eight remaining D/RTH volume ratio outliers with non-adjusted consolidated daily or exchange-qualified data; then full frozen one-pass VWAP entry and +2/-2 2-session event trades vs opening baseline, proper real quote and ticker bootstrap. Until source-gate passes, original63 remains research-only. NO paid feed, scanner/automations change, no trading recommendation.
