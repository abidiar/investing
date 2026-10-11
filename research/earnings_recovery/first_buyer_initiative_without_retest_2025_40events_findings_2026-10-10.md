# First buyer initiative after an earnings shock — independently dated 2025, 40-announcement test
Date: 2026-10-10. **Completed, result: NO verified trading rule.** All records and reproducible five-minute source price bars retained. No historical CALL entry/exit premiums verified.

## What was frozen before historical cohort was examined for this specific rule
Forty BMO/AH earnings announcements from July 1–Aug 29, 2025, each at a DIFFERENT issuer in prior holdout's 65-name historical Quant500 source list. No hindsight filtering for losing/gaining stocks. Fixed universe `frozen_2025_jul_aug_40_announcements_for_first_buyer_initiative_2026-10-10.json` committed `44b3192a2d9999c848fa465c97d419be5a9f0f59` before complete 2025 M5 outcome retrieval. Fixed rule `frozen_2025_first_buyer_initiative_without_retest_protocol_2026-10-10.md` committed `c6bb7fc9e7f0c6569f66e4273c2979d083c0f055` before full cohort inspection. Two-stocks AON/CHTR source format had been probed beforehand (not their outcomes). Cohort is a different calendar year from 2026 events but prior broad research had inspected some historical 2025 returns; **do not claim true unseen prospective validation**. Historical point-in-time financial quality of all 40 not freshly recertified.

**As-of definition:** earn reaction-session 09:30–16:00 five-minute RTH stock prices; first completed bar low <=95% of last AS-TRADED previous trading session 15:55 5m closing price, first breach by 11:30am ET. AH earnings next regular session, BMO same trading day. **No day-end hindsight close qualifier.**
**First buyer initiation candidate**, within max 8 bars/40mins after first -5% bar i: earliest pair of adjacent completed 5-minute bars with both GREEN `C>O`, second higher close plus non-decreasing low, second CLOSE > first HIGH, second volume >= median volume of previous three full 5m bars. Enter NEXT 5m opening same day at/before 12:20 only if no more than +2.0% above as-of lowest intraday price since first bar i; else skip entire setup, not rescan. Does NOT require initial-low retest, SMA or VWAP. Benchmark buys at OPEN next 5m bar immediately after first completed -5% bar. Both underlying first +1.5% stock target vs −1% stock stop within three entry-inclusive RTH sessions, adverse stop-first same-bar ambiguity, gap at open, else day3 end close. Stock returns before fees; separate 0.20%/trade illustrative transaction cost.

## Full test results
- All **40** companies/announcements in event roster and result. Webull historical M5 batch returned 39 tickers; **BK** raised INVALID_SYMBOL, replaced using connected Massive's unadjusted historical 5m source. **FICO** had incomplete prior/reaction trading five-minute bars, so ineligible as MISSING SOURCE rather than scored a non-trade or loss. **39/40** reaction sessions had complete pre-day and reaction-day RTH coverage.
- **28** complete events NEVER touched −5% intraday, **two** first reached −5% only AFTER 11:30am (VLO 12:30, WAB 11:40), **NINE** had an early as-of-completed five-minute −5% stock selloff.
- Of those nine, two recovered enough by 4pm that they **did not close down 5%**: EQT closed about −4.38%, STX −3.45%; EQT was one of three benchmark profitable trades. EOD-only selection would again systematically omit real intraday shock and some profitable initial rebounds.
- The FULL two-green 5-minute + rising-close/low + volume ≥ recent three-volume median + <=2% non-extended buyer initiative rule produced **ZERO executable signal entries**. **Seven** of nine had NO valid combined two-green volume-confirmed signal within the first eight 5m bars, while **two** had a candle pattern with volume but first possible entry already +5.92% above the known intraday low (STX) or +3.81% (TPR), so both were skipped by frozen +2% anti-chase cap. Neither of those latter two succeeded as immediate-buy comparator, but this anecdote cannot validate cap.
- Simple blind FIRST -5% shock NEXT candle buy: **9 stocks**, **3** hit underlying +1.5% profit target before −1% stop (AMAT, EQT, PPG), **six** hit stock stop first. Gross mean per traded stock **−0.1667%**, hypothetical 20bps roundtrip yields **−0.3667%**. No timeouts. Only 9 eligible early shocks, underpowered for strategy confidence. ALL frozen go/nogo gates failed. For combined buyer pattern entries zero, do NOT report a 0% win rate: THERE WERE NO TRADES.
- The stock-price target/stop (1.5%/1%) does NOT correspond to +30%/-30% CALL payoff because historical buy ask, delta, implied volatility, time decay and contract choice were never observed.

| Category | Events |
|---|---:|
| All eligible historic BMO/AH earnings announcements in 2025 roster | 40 |
| Complete price source history on event day | 39 |
| Event never falls ≥5% during reaction session | 28 |
| First -5% touch too late (after 11:30 ET) | 2 |
| First valid early -5% shock | **9** |
| First two-green + price/volume buyer breakout without retest | 2 potential signals |
| Potential buyer breakout already >2% above as-of intraday low | 2 (both blocked) |
| Buyer-trades after full rule | **0** |
| Immediate after-shock stock comparator trades | 9 |
| Immediate comparator +1.5% target first | 3 |
| Immediate comparator -1% stop first | 6 |

## Descriptive mechanism diagnosis (NOT new signal optimization)
Among three benchmark winners:
- **AMAT:** two-green higher-close / breakout existed as early as third completed 5-minute bar (k=2), but that green breakout bar's volume did NOT reach the recent-three-bar median and the NEXT bar already entered **+2.53% above its known session low**; even a modified green-only signal would be getting late. Early winner's rapid price advance happened before required confirmation.
- **PPG:** similar two-green price breakout at k=4, volume below rolling-three-bar median, with next opening price **+3.08% above known low**. A full 2% anti-chase cap correctly says "not an early entry", but whether earlier higher-risk entry would've succeeded is unknown.
- **EQT:** never produced the precise two-adjacent-green pattern within first 40mins, despite reaching stock target on the simple shock entry. It had later isolated green rising/breakout candlesticks that did not meet the fixed two-green morphology.
- Among losers, **STX** and **TPR** produced late signal candidates with adequate volume but buy price well above first low (+5.92%, +3.81%), showing that breakout-and-volume conditions do not by themselves rule out a failed rebound. The remaining losing names similarly often did not show two-green follow-through, but selected nine-case anecdotes are not inferential evidence.

**Interpretation:** The popular notion that first strong volume buyer candle happens before call repricing is not established. On these events it often lags the price bounce; high opening auction/first-break bar volume can make later ordinary buyer candles appear low-volume even when price rebounds. A rigid morphological pattern then misses first fast moves entirely, even without same-low retest. Green 5m volume is NOT signed market-buy aggressor flow and so cannot establish seller exhaustion.

## Research decision
**STOP adding layers of volume/price confirmation around first post-earnings −5% shock and claiming an automatic A+ call edge.** We have now pre-frozen, fully run, and found zero eligible trades for TWO consecutive distinct cohorts/rules: strict first-low retest 2026 0/19 triggers, and no-retest two-green price/volume buyer initiative 2025 0/9 triggers. This does NOT prove no tradeable rebounds occur—immediate stock rebound targets were real: 7/19 in 2026, 3/9 in 2025. It means no verified prospective selection criterion currently separates wins vs losers.

A truly valuable next direction is to reconstruct ALL real prior CALL transactions, including losses and partial exits (for known user's trades) and compare them with option delta/gamma/expirations; or explicitly choose a new *separate* objective such as next 30-minute STOCK maximum favorable excursion vs minimum adverse excursion using time-stamped bars, then preregister ONE signal before a larger never-observed quarterly cohort. Do not fit a new recipe to AMAT/EQT/PPG examples; they are known winners. Option premiums can move +30% even on <1% stock recovery; stock +1.5/-1 first-touch may be an ill-fitting proxy for a fast small-account premium scalp.

## Reproduction
- `frozen_2025_jul_aug_40_announcements_for_first_buyer_initiative_2026-10-10.json`.
- `frozen_2025_first_buyer_initiative_without_retest_protocol_2026-10-10.md`.
- `early_buyer_initiative_no_retest_2025_40events_actual_2026-10-10.json` — ALL forty complete results/unknowns, exact times, raw outcomes and skips.
- Seven Webull M5 historical week files `buyer_initiative_2025_weekYYYY-MM-DD_M5_webull_2026-10-10.json`, plus `buyer_initiative_2025_BK_fallback_M5_massive_2026-10-10.json` (one additional vendor, as-traded historical).
- `run_first_buyer_initiative_without_retest_2025_40events.py` and `.github/workflows/earnings-first-buyer-initiative-2025.yml` reproduce.
