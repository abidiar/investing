# FROZEN PRIOR TO INDEPENDENT OUTCOME EXPOSURE: support-failure -> VWAP reclaim issuer-disjoint v2
Freeze date: 2026-10-11. Status: **FROZEN / NO NEW SIGNALS OR OUTCOMES SEEN** before this commit.
Prior review COMPLETED and committed first: research/prior_work/range_failed_support_vwap_replication_prior_review_2026-10-11.md .
Original not-to-be-optimized protocol: research/swing_two_session/vwap_entry_protocol_2026_10_09.md .
Earlier aggregate only: research/swing_two_session/vwap_unified_63_event_rerun_2026_10_09.md . No raw event panel for earlier 63 currently committed; data extraction must not claim direct validation of them.

## Economic claim
Apparent break below repeated historical support that closes back above support, then reaccepts intraday VWAP the next session, yields better 2-session stop-managed stock results AFTER modeled friction than buying the next RTH open, on issuers not in the original 20-name selected universe.

## FROZEN universe, period and source
Only original 2022–26 v1 issuer-disjoint stocks; immutable 49-name fixed universe:
NVDA, AVGO, MU, TXN, KLAC, LRCX, AMAT, ASML, TSM, CSCO, ANET, PANW, CRWD, FTNT, NOW, ADBE, SNOW, DDOG, NFLX, DIS, TGT, WMT, PG, KO, PEP, MCD, SBUX, NKE, V, MA, GS, MS, C, WFC, UNH, ABBV, JNJ, MRK, PFE, NOC, GE, HON, DE, UPS, FDX, BA, CVX, SLB, COP.
Original 20 EXCLUDED only for independence: META, ORCL, DELL, AMZN, AAPL, AMD, MSFT, GOOG, CRM, QCOM, JPM, CAT, HD, COST, XOM, BAC, LLY, INTC, UBER, PYPL.
U.S.-listed liquid common shares and large ADRs with all ticker histories accessible, split/ex-date mapping confirmed; names that fail data entitlement remain MISSING DATA, not discarded based on price or outcome. Preselected universe is STILL survivorship-biased: selected from known 2026 names, not a reconstructed original-date constituent list. **Primary calendar signal dates 2024-01-02 through 2026-09-30** with historical source starting no later than 2023-09-01 for 40-session lookback. Selection period fixed irrespective of any results. Avoid October 2026 until 2 full RTH followup sessions exist. Include each eligible event >=2 complete future sessions, no hindsight skipped trade.
Read connected Webull original unadjusted intraday M5 RTH where possible and 1200-bar D snapshot; save provider account link to reproduce without exposing private account metadata; do NOT use actual user trading account positions/orders. Use 1200 or 1650 max as described. Use UTC milliseconds for from/to. All output timestamps normalized to NY exchange timezone.

## CRITICAL basis gate BEFORE outcome read
Historically adjusted Webull DAILY OHLC has previously diverged from as-traded Webull RTH M5. For every eligible candidate in daily scan:
1. Verify D event O/H/L/C against same-day RTH M5 reconstructed O/H/L/C, and previous available 40 sessions by reconstructing complete M5 RTH daily candles OR a documented point-in-time ex-date split/dividend factor schedule; mere same-day proportional rebasing is NOT enough if ex-dividend inside prior40.
2. Use source-consistent OHLC on *one price basis* to rederive prior support, range width, prior touches, volume and signal qualification. Prices after adjustments must be as would have been known on historical event date, not factors from future corporate actions. Log all daily-screen vs correct-event membership changes BOTH directions by rescanning all dates with correct historical basis; if correct-source 49-name FULL universe recomputation infeasible, mark v2 OUTCOME TEST NOT EXECUTED, only partial data-quality audit. Do not show optimistic 20bp P&L as independent corroboration.
3. M5 RTH exact 78 each required session, absent sessions/no prints flagged; splits within hold adjust fill quantities accordingly; missing source remains UNKNOWN.

## Original v1 frozen daily signal EXACT (do not vary)
At each candidate date, compute preceding **40 completed trading sessions** min LOW = support; max HIGH = resistance; range-width >=6%, with at least **two** prior low touches <=1.012×support separated by >=5 completed trading sessions (>=5 index distance); signal-day LOW < support, signal CLOSE > support, and 0.995×support <= signal CLOSE <=1.025×support; signal volume >=1.2× mean previous 20 trading-session volume. Minimum calendar spacing 5 days between successive eligible signals of a ticker, applied chronologically before any outcome; all otherwise eligible signals preserved in exclusions log.

## v1 frozen next RTH VWAP and entry EXACT
Cumulative from 9:30 RTH 5min VWAP from typical-price HLC/3 weighted by volume; require a COMPLETED M5 close below its completed-time cumulative VWAP, then TWO CONSECUTIVE completed M5 closes above their current cumulative VWAP, entry at next M5 bar OPEN no later than 12:00 ET; if not a valid next-bar open before noon, SKIP, not a loser. No lookahead on future candles. Frozen open benchmark always enters next RTH 9:30 OPEN and holds identical barrier rule.

## Outcome, costs, interpretation
Stock exit from first tradable entry through EOD SECOND RTH session after signal, TARGET +2% or STOP −2% first, gaps at actual next open adverse fill, ambiguous both-in-bar=STOP, otherwise close of second RTH session. Score net per TRADE and net PER ORIGINAL SIGNAL with skips zero; never count no-entry as losing trade. Required 0.20%, 0.50% and 1.00% **total roundtrip** flat hypothetical friction sensitivity; disclose fees and slippage not actual NBBO, and 0% gross for comparison. Historical call 1-contract premiums and NBBO are NOT measured.
Controls: next RTH opening buy all identical signal events; and next RTH M5 **first** above-VWAP crossing as optional PREDECLARED descriptive sensitivity without optimizing selection; any later model only new future v3.
Primary metrics: full 49 issuer universe source coverage, complete signals N, entrants N, target/stop/timeout counts; absolute net per eligible signal at 0.5%, and paired VWAP minus open per eligible signal at 0.5%; ticker-cluster bootstrap 95% CI, leave-one-ticker-out, 2024 vs2025 vs2026, top-three-ticker aggregate share and worst year, same-date clustering. Do not pool partial timestamp-inconsistent data.

## Precommitted go/no-go
No 'tradable stock edge' claim unless >=40 independently qualifying original signals from >=12 distinct issuers, source-basis verified full 49-name period denominator, >=25 actual VWAP trades, primary >=0.5% total friction net per eligible event positive **with ticker-cluster bootstrap 95% lower bound above zero**, paired VWAP improvement vs opening baseline ticker-cluster 95% lower bound >0, 2024/2025/2026 era subperiods not disastrously negative, and top3 ticker contribution <=50% of total positive contributions. Even passing this stage supports STOCK simulation only; options need separately preregistered as-of affordable one-contract ask, exit bid, spread, IV/DTE/cap, execution evidence. If history source cannot pass basis gate or n<40, verdict INSUFFICIENT / DATA BLOCKED, do not tune old 63 winners.
Do not infer 80% hit chance. No scheduled notifications, scanner, trade instruction or actual trade changes.

## Reproduction / data provenance
Save raw vendor responses or losslessly normalized bars with retrieval datestamps and hash; signal candidates separate from outcome labels, summary by year/issuer, exclusions, provider coverage. Commit raw price inputs in GitHub AFTER respecting size/rate constraints. Source unavailable => a clear test not run.
