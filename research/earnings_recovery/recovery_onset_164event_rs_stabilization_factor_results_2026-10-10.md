# Which observable factors separate fast profitable stock recovery-onset moves from failures?
Study completed October 10, 2026. Saved in Investing OS. **This is NOT a backtest of historical executable options call P&L.** Signal and risk thresholds frozen BEFORE this particular 164-event 3-session factor run. Both original92 and separate-company holdout72 have had prior outcomes inspected in earlier studies, therefore they are not blind forward tests.

## Question and fixed setup
Among 164 previously quality-qualified earnings selloff events (2023–June 2026, all 61 original/holdout names), can two extra as-of-entry filters tell us which price-repair signals achieve a rapid move capable of repricing a call?
First baseline *SMA5 reversal* after event: first daily close on post-event sessions 5–20 that crosses above current SMA5, had previous close <= previous SMA5, and closes above previous day's high. Enter the NEXT regular-session stock OPEN, unless >+8% above original selloff-day close (skip). This is a STOCK daily-price signal, not morning VWAP.
Each successful stock trade needs high to touch **+1.5% relative to its entry open** before low touches **−1.0%**, in 3 entry-inclusive stock sessions. Stop-first for ambiguous within-day OHLC; follow-through gap exit at open; otherwise exit third session CLOSE. No option premium, Greek or historically executable NBBO, and gross returns exclude market spreads, slippage and commissions.
Feature #1 predeclared **3-session stock price relative strength ≥+1.0 percentage point compared with SPY** as measured at signal close; #2 **three nondecreasing daily lows** at signal close. Evaluate each, and BOTH together without tuning. Original92 development vs company-disjoint holdout72 independent-name *replication* (but both previously outcome-inspected). Source: saved frozen 164 event list plus complete Yahoo unadjusted-for-cash-dividend quote OHLC for 61 tickers and SPY; reverse post-event splits. All 62 stock/ETF sources retrieved, 164/164 matched event and SPY data, none missing. The frozen event list preceded these actual short-horizon factor computations.

## Results by cohort

| Group and filter | Entry-qualified | +1.5 before −1 (3 sessions) | Target-first% among entries | Mean gross return / ALL eligible events (skips 0) |
|---|---:|---:|---:|---:|
| Original 92 price repair alone | 73 | 32 | 43.84% | +0.1298% |
| Original 92 + RS/SPY >=+1pp | 35 | 11 | 31.43% | −0.0527% |
| Original 92 + 3 stabilized lows | 29 | 13 | 44.83% | +0.0669% |
| Original 92 + both | 18 | 5 | 27.78% | −0.0310% |
| Separate-company 72 price repair alone | 57 | 20 | 35.09% | −0.0595% |
| Holdout 72 + RS/SPY >=+1pp | 22 | 7 | 31.82% | −0.0625% |
| Holdout 72 + 3 stabilized lows | 15 | 5 | 33.33% | −0.0347% |
| Holdout 72 + both | 7 | 3 | 42.86% | +0.0069% |

- As-of-only price repair triggered **130/164**; **52/130 (40%)** touched +1.5% target before −1% stop over 3 sessions, 75 stopped, three timed out. Average stock gross return on 130 entered: +0.0589%, across all 164 with skip=0 +0.0467%. No proven edge after trading costs. The +1.5% and −1% asymmetric barriers mean fewer than half target hits may still earn a gross nonnegative total; do NOT equate wins to profitability of calls.
- Day3 comparison with EXACT same +1.5%/-1%, 3-day stock barrier: 52/164 target wins (31.71%), mean gross stock return **−0.1869%** across all 164, while repair is 52 wins out of 130 entries and mean +0.0467% across all 164. A small approximately +0.234 percentage-point apparent improvement per event before any execution costs, concentrated in ORIGINAL92; in holdout72 first repair mean −0.0595% vs day3 −0.0817%. The paired repair-minus-day3 gross return difference on the 130 events with entry in both was +0.326 percentage points, but cohort-split original92 +0.551pp, holdout72 only +0.037pp. NO deployment evidence.
- Relative strength >=+1pp REDUCED target rate among triggered trades in **both** cohorts. Original92 from 43.84% to 31.43% (company-resampled bootstrap CI for difference **[−23.57,−2.50] percentage points**); holdout72 from 35.09% to 31.82% (CI **[−20.54,+12.00]**). These uncertain exploratory CIs are NOT independently validated.
- Stabilized rising daily lows showed no reliably better effect: original92 44.83% vs 43.84%, holdout72 33.33% vs 35.09%.
- Both filters in original92 5/18 target hits (27.8%); holdout72 3/7 (42.9%), apparently higher conditional rate with ONLY 7 signals. Two-company/ticker-cluster effective sample much smaller and wide bootstrap CI [−32.14,+42.16]pp relative to base holdout. **Fails all three PREDECLARED confirmation gates**: <20 holdout entries, <+10pp incremental win rate (42.86% vs 35.09%=+7.77pp), and combined target captures only 3 versus 20 of entire 72-event base signals. Never claim this is an A+ combination.

## Exploratory as-of-entry winner vs failure descriptive clue — NOT a predeclared entry filter
Among SAME price-repair signals, compared only winner and nonwinner based on 3-session underlying outcome:
- Original92 32 winning, 41 failing: mean preceding 3-session STOCK rise **+1.10% winners vs +2.06% failures**. Three-day relative strength versus SPY **+0.46pp winners vs +1.56pp failures**. Mean signal lag ~10.09 vs 9.93 post-selloff sessions.
- Holdout72 20 winning, 37 failing: mean preceding 3-session STOCK rise **+0.59% winners vs +1.14% failures**. Relative strength vs SPY **+0.24pp winners vs +0.51pp failures**. Mean signal lag ~10.20 vs 10.86 sessions.
- Winners tended to have LESS preceding price extension in both cohorts. A plausible interpretation is **don't wait until a short recovery is already overextended**. However this is observational and can arise from regression to mean, different volatility/regimes, the SMA5 trigger's selectivity, market context, and sampling; these are NOT statistically independently tested or a license to retro-optimize a +1% cutoff.

## Interpretation and bounded research decision
The user's personal META/AAPL/UBER/PYPL profitable calls are real successes but may reflect DIFFERENT mechanisms (near-expiry overnight repricing or intraday momentum) and a much smaller stock move can generate a large percent option gain via delta/gamma/IV. Earlier tests with +5% underlying profit and strict exits do NOT invalidate this user-specific trading mode. But we have no complete ledger of *all* attempted calls including losers and not-taken signals, and no verified historical timestamped option bid/ask. Never infer option expectancy from their selected wins nor from a +1.5% stock move.
One frozen 164-event stock factor test **does NOT support adding daily SPY outperformance or three rising daily lows** to a late daily-SMA5 price-repair entry for fast 3-session calls; it indicates high selectivity can miss opportunity. The NEXT *single* sensible hypothesis to test on truly unseen events (without threshold mining this sample) is whether **an EARLIER intraday stabilization/reclaim signal with sufficient remaining price room, not a late daily-SMA cross,** yields more actionable early option reprice opportunities. That would need historical intraday stock VWAP/volume and matched SPY/sector bars, and ultimately actual as-of option asks/bids; keep modes distinct and don't pay for data or promote the scanner based on this preliminary result.

Reproducible source: `frozen_recovery_onset_rs_stabilization_threeday_protocol_2026-10-10.md`; result full event-by-event `recovery_onset_rs_stabilization_164events_actual_2026-10-10.json`; raw source bars `recovery_onset_rs_stabilization_164events_market_price_sources_2026-10-10.json`; script `run_recovery_onset_rs_stabilization_threeday_164events.py`; automation workflow `recovery-onset-164-three-day-factor-audit.yml`.
