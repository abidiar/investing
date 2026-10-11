# Frozen 2019–2021 Grimes-style support failure × SPY as-of-entry market proxy

**Completed:** 2026-10-11. **Not a replication of Adam Grimes or Rob Hanna.** Objective: identify whether a stock's pre-noon failed breakdown of a *pre-existing double-pivot support* performs better when SPY is already higher than its opening price. The result is **NO** for this exact proxy and stock setup.

## Protocol and pre-outcome audit

- Protocol pre-committed: [2019-21 market recovery pre-registration](frozen_grimes_market_recovery_2019_2021_v1_2026_10_11.md), **commit `ba13fdd32df497425148a467fa89854b900f9fcd`**. The exact 90-symbol issuer universe was already frozen in the prior 2022 diagnostic, with survivorship limitations.
- Archived 2018–2021 DAILY as-of candidate discovery data in `data/grimes_marketcontext_2019_2021_daily_preoutcome_batch_01..05_2026_10_11.json`.
- Pre-outcome 2019–2021 manifest committed **`b4cb144e9708cd46b0601d230b7a16884e79c44d` BEFORE any D1/D2 M5 was retrieved**: 198 events, 76 tickers, 126 dates, 48/70/80 yearly events.
- Archived unmodified stock D0/D1/D2 five-minute vendor bars in `data/grimes_marketcontext_2019_2021_m5_source_batch_01..14_2026_10_11.json` and SPY RTH M5 bars in `data/grimes_marketcontext_2019_2021_spy_m5_source_batch_01..05_2026_10_11.json`. Original 2019 request end time limited to D0, then corrected **before scoring** to capture three sessions with source coverage intact; incomplete candles still marked UNKNOWN.
- Evaluable: **174/198**. Unknown: **24** due to incomplete stock M5 (including March 2020 shock sessions; could include halts or provider limitations). **0** missing SPY D1 among evaluated; SPY D1 complete on 113 distinct sessions.
- Historical survivor-biased 90-equity cohort drawn from a later 2023 universe. Historical 2019–2021 in previously unused calendar interval; not a prospective 2026 study and not necessarily untouched relative to every earlier research project. No retuning after outcomes.

## Entry, exits and market measurement

- Primary stock pattern: after D0 >=3% daily stock selloff with RVOL20 >=1.20, support is formed by **two previously confirmed daily swing lows** from as-of preceding 120d, proximity <=1%, spaced >=5 trading sessions, untouched after later pivot and D0 close within 4% above it.
- On D1 09:30–11:45 RTH a five-minute bar LOW pierces below 0.999 × support, closes back above support same or immediately next bar; execute next M5 OPEN by 12:00. Stop low of breach/reclaim candles *0.999 with risk distance .35%-2%. Target +2%; D2 15:55 final exit if not stopped/targeted. Intrabar both-touch STOP-first, open gap-through fills at actual opening price. Modeled stock-equivalent friction 0.50% per filled trade. No options pricing or options claim.
- **SPY market recovering** iff last completed SPY D1 5m close immediately *before* stock entry is strictly ABOVE SPY 09:30 session opening price. NO future SPY candles. No shift in stock entry time: positive = take exact same stock trade, nonpositive = abstain. Evaluated the alternative nonpositive group descriptively, NOT marketed as optimized live filter.
- Benchmark buy D1 initial 09:30 stock M5 open for all evaluable D0, +2% target/-2% stop, 0.5% cost and same D2 timeout. All skips zero for per eligible-event average.

## Frozen results

| Group | Fills | +2% first | Stop first | Target / filled | Net / filled | Net / all 174 evaluable D0 |
| --- | ---: | ---: | ---: | ---: | ---: | ---: |
| No SPY gate, failure test | 28 | 9 | 19 | 32.143% | -0.396% | -0.064% |
| SPY rising relative to 09:30 open | 10 | 1 | 9 | 10.000% | -1.120% | -0.064% |
| SPY flat/down relative to 09:30 open (descriptive) | 18 | 8 | 10 | 44.444% | 0.006% | 0.001% |
| Always buy next stock open +2/-2 | 174 | n/a | n/a | n/a | -0.680% | -0.680% |

With the frozen SPY-positive gate, 10 executed trades, **1 target / 9 stops**, mean net **-1.120% per fill**, mean net **-0.064% per eligible signal**; the gate was no better than ungated (-0.001 percentage points per signal). SPY-negative or flat setups had 8 target / 10 stops in 18 entries, mean **0.006% per fill**, effectively break-even *stock-equivalent* after modeled costs, with high uncertainty; **not an actionable edge**. Difference among filled trades, SPY-positive minus nonpositive = **-1.126 percentage points**.

The gate improved per-signal returns compared with blindly buying next-open (+0.616pp), mainly due to trading far less, but is still net-negative and the unfiltered mechanical failure-test strategy also loses. Avoiding bad trades is not the same as making profitable trades.

## 10:30–12:00 ET predeclared subset

| Group | Entries | Target first | Average net / fill |
| --- | ---: | ---: | ---: |
| All eligible price-only entries | 14 | 5 | -0.184% |
| SPY rising | 4 | 0 | -1.273% |
| SPY not rising | 10 | 5 | 0.251% |

No parameter optimization, not statistically robust; note small (4 and 10) subgroup sizes and overlapping dates.

## Dependence-adjusted uncertainty and regime

- 10,000 deterministic resamples by ticker (73 clusters): 95% interval of mean SPY-positive filled return **[-1.583%, -0.413%]**; SPY-nonpositive filled return **[-0.594%, 0.650%]**; conditional mean difference (positive−nonpositive) **[-1.985, -0.171]** pp. Date-clustered sensitivity is in JSON. This interval is retrospective/conditional and does not establish causality or regime transportability.
- Year splits: 2019 3 entries/2 targets, SPY rising gate had ZERO entries; 2020 9 entries/1 target overall, SPY rising 0/4; 2021 16 entries/6 targets overall, SPY rising 1/6. Structural context and regime remain unaccounted for.
- Completeness exclusions are nonrandom (especially crash days). This could bias results either direction and prevents strong claims for extreme market stress. Per-trade confidence intervals are not adjusted for original candidate-selection or hypothesis search across the wider program.
- No options NBBO, DTE, spread or slippage, and no proof of $50 affordability. Short calls are a distinct trading product.

## Original research comparison (why not a contradiction)

**Adam Grimes:** The 2011 explanation and his interview with Rayner Teo explicitly emphasize a *market-visible significant pivot* and broader pattern / trend context, including bullish failure tests within a complex bull-flag. His work spans markets and timeframes and emphasizes a fast reaction, discretionary chart structure and trade management. See:
- https://adamhgrimes.com/failure-test/
- https://www.tradingwithrayner.com/art-and-science-of-technical-analysis-with-adam-grimes/
- https://adamhgrimes.com/library/fundamental-trading-patterns/

Our experiment requires an imposed **-3% daily selloff** near a daily-level double pivot, not the original detailed bull-flag continuation setup. Grimes himself notes the strength of the overall context and that a failure test after a single downthrust can be weaker. A mechanical reproduction could fail while his context-sensitive strategy has favorable conditional results. **We have not reproduced his published strategy, nor independently verified 80% profitable option trades.**

**Rob Hanna:** his quantification includes the proprietary CBI breadth indicator (S&P 100 stock capitulation) and the NYSE closing-TICK TomOscillator; he reported *23 of 25 next-day SPX closes higher* after extreme indicator readings on 2026-06-07. That is not our stock first +2% before structural stop or the path/option result of entry 10:30-noon. His CBI buy-SPX/exit-on-breadth-normalization involves a different signal, instrument, clock and stopping rule, and some extreme drawdowns. Sources:
- https://quantifiableedges.com/blog/
- https://quantifiableedges.com/page/84/?cat=-1
- https://quantifiableedges.com/page/42/?cat=-1
- https://proactiveadvisormagazine.com/finding-quantifiable-edge-capitulation-selling-analysis/

Hanna's claim can be accurate even when a stock support-gate proxy fails. Neither our results nor the claimed market studies establishes >80% net-profitable sub-$50 short-call executions.

## Decision and next research

**Reject** the exact SPY-above-09:30-open market confirmation gate as an A+ entry filter for our stock failure tests. It was worse, not better. **Do not** invert it to SPY-down as a new strategy: the 18 observed SPY-down fills were break-even net, and the apparent edge in the 10:30-noon subgroup rests on 10 trades.

**Next distinct hypothesis, motivated by actual source discrepancy:** Grimes's *bullish failure test within an existing bullish trend / complex bull flag* is genuinely different from our crash-driven support reclaim. Freeze an as-of-trend and intraday-pivot definition *without a prior-day -3% shock requirement*; use an unused calendar and broader population with 5m data before outcome access. Separately, research genuine Hanna TICK/CBI source data if a different market-timing direction is desired. One hypothesis and holdout at a time.

Complete outcomes: [market-context event results](data/grimes_marketcontext_2019_2021_final_event_results_2026_10_11.json).
