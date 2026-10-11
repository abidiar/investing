# Frozen exploratory *audit* of D3-observable traits shared by winners vs losers
Freeze: 2026-10-11, BEFORE new comparisons of already-exposed stock price paths. NOT prospective validation and no threshold optimization.
Prior review: research/prior_work/earnings_recovery_winner_loser_asof_features_review_2026-10-11.md.
Source frozen 164 quality-company 2023–Jun2026 events archived as two actionable_bounce_price_windows JSONs, plus earnings-session CSV roster and asof_near_low_limit_ah_v1_results_2026-10-11.json with pre-observed D4 trade outcomes. Focus all AH n91, eligible D1-D3 observed further low than D0 intraday low n54. Full denominator retained; outcomes already observed elsewhere.
Question: **Among initially QUALIFIED, objectively early-dipped earnings selloffs, which as-of-D3 characteristics do D4 stock +3%-before−5% winners share more often than D4 failures?** Distinguish from eventual D60 full price reclaim, which is NOT the trading label. No price data after D3 may enter features; D4 entry only sets outcome.
Features calculated at D3 close:
A. initialShockClosePct = 100*(D0 close/preearnings RTH close - 1); if preearnings close can be extracted from same saved price sequence and actual reaction index, otherwise missing.
B. secondaryDipDepthPct = 100*(min LOW D1..D3 / D0 LOW - 1) <0 for eligible;
C. closeAboveKnownLowPct =100*(D3 CLOSE / MIN(D0..D3 LOW) -1);
D. lastCloseChangePct=100*(D3 CLOSE / D0 CLOSE -1);
E. D0..D3 stock return minus same D0..D3 SPY RTH close-to-close return IN PERCENTAGE POINTS. Use timestamp-align SPY daily RTH bars; if missing, null. No SPY hindsight.
F. averageD1toD3DailyRangePct=100*MEAN[(high-low)/prior close] on D1..D3.
For each group show COUNT, individual median and mean (skip missing with count explicit), not thresholds/categorical optimizations; D4 target-first vs stop-first, full outcome denominator; report original65 vs company-disjoint26 to see direction. Secondary comparison: among all 91 AH events, early further low by D3 versus NOT. Decomposition of full recovery 60d vs early tradable win may be considered separately only when full recoveries have known anchored preearnings close, not as same success.
Record if first 2022 frozen external replication consistent with any apparent patterns but do NOT cut the 2022 sample again into adjusted optimized filters. No bootstrap significance claims from feature shopping; this is an observational *mechanism search* to prioritize exactly one candidate. No scanner changes.
