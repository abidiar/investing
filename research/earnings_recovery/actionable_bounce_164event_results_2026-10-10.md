# Can earnings rebounds be captured with safer entries? 164-event historical test

**Date:** 2026-10-10. **Status:** completed exploration on 92-event original cohort and company-disjoint 72-event holdout. **NOT a validated or profitable options strategy.**

## Protocol and data
[Pre-frozen methods](./actionable_bounce_entry_protocol_2026-10-10.md). 164 previously quality-qualified earnings selloffs (at least −5% from immediately pre-announcement stock close), 61 unique tickers in 2023–June 2026. Each event anchored at the FIRST qualified selloff day's **closing** price, never the hindsight lowest price. Webull connected historical RTH daily OHLC; 92 original events' previously stored five-day close returns were confirmed within 0.005 percentage points of this price feed. **No missing event prices.** Outcomes for all 4 entry rules were saved on all 164 events, even when rules failed to trigger. Previously examined cases mean this is not an untouched or prospective dataset; avoid promotional A+ labels.

Four unchanged entry rules:
1. First regular-session opening price after selloff close (`next_open`).
2. Third regular-session opening price after selloff close (`day3`).
3. `sma5_reversal`: first bar 5–20 following event where close transitions to > current 5-day SMA, prior close ≤ its own 5-day SMA, and close > previous session high; next-session open entry.
4. `three_rising_lows_break`: first post-event bar 3–20 showing three consecutive nondecreasing daily lows and close > highs of previous two daily bars; next open entry.
For rules 3–4 only: skip outright if the next entry opening price >8% above original selloff-day close; no later rescans. No future look-ahead and no fills at trigger-day prices.

Managed stock-price test, NOT option ROI: from entry open, +5% target, −5% or −10% stop; maximum 20/40 entry-inclusive trading sessions. Any ambiguous intraday bar assumes stop before target, overnight gaps fill at opening price, otherwise exit at final closing price. No fees, spreads, slippage, assignment or corporate-action trade processing. Average *per original opportunity* counts untriggered entries as 0%. Underlying calendar-day windows 14,30,45,60 days are only hypothetical +5%/-10% stock-path proxies and do not rank call expirations.

## A. First question: will an early call face substantial drawdown before a bounce?
Stock prices may touch +5% from **selloff close** at ANY time, even after a -5% or -10% drawdown. Stop-first measures distinguish eventual rebound from a survivable price path.

| Time horizon | Original cohort: eventually +5% | Original: +5% before extra −5% | Original: +5% before extra −10% | Holdout: eventually +5% | Holdout: +5% before extra −5% | Holdout: +5% before extra −10% |
|---|---:|---:|---:|---:|---:|---:|
| 20 trading sessions | 56/92 | 40/92 | 52/92 | 38/72 | 34/72 | 38/72 |
| 40 trading sessions | 60/92 | 42/92 | 55/92 | 43/72 | 35/72 | 42/72 |
| 60 trading sessions | 65/92 | 43/92 | 57/92 | 48/72 | 35/72 | 44/72 |

At 60 trading sessions, the median worst further decline below initial selloff CLOSE was -8.60% original, -8.57% holdout, and the median +5% bounce day among successful events was 9.00 / 9.50. The worst low can occur AFTER the initial rebound; never call the median adverse excursion a stop-first statistic.

## B. Capturing the rebound: strict 20-session exit / −5% stop
`Trade winners` means stock price +5% before -5%, with 20-session timeout. This definition is consistent across rules but each triggers a different subset. Compare gross average per all frozen events (skips count 0), not only conditional success rates.

| Cohort | Method | Enters | Wins at +5% | Stops at −5% | Avg gross stock return on entries | Avg gross return per eligible event | Median entry lag |
|---|---|---:|---:|---:|---:|---:|---:|
| original_92 | next_open | 92/92 | 38 | 46 | -0.50% | -0.50% | 1.00 sessions |
| original_92 | day3 | 92/92 | 47 | 35 | 0.77% | 0.77% | 3.00 sessions |
| original_92 | sma5_reversal | 71/92 | 39 | 27 | 1.09% | 0.84% | 9.00 sessions |
| original_92 | three_rising_lows_break | 68/92 | 31 | 28 | 0.22% | 0.16% | 7.00 sessions |
| holdout_72 | next_open | 72/72 | 34 | 34 | -0.20% | -0.20% | 1.00 sessions |
| holdout_72 | day3 | 72/72 | 30 | 36 | -0.76% | -0.76% | 3.00 sessions |
| holdout_72 | sma5_reversal | 57/72 | 21 | 27 | -0.58% | -0.46% | 11.00 sessions |
| holdout_72 | three_rising_lows_break | 52/72 | 27 | 20 | 0.57% | 0.41% | 7.00 sessions |

### The three-rising-lows break: consistency but inadequate profitability evidence
The rule entered 68/92 and 52/72. Including missed opportunities as zero, mean gross profit was **0.16%** in original and **0.41%** in holdout. Its incremental advantage compared with buying next-session open was 0.66 and 0.61 percentage points, respectively. Ticker-cluster bootstrap 95% CIs were **[-0.64, 1.88]** and **[-1.03, 2.16]** pp. Ticker-cluster CIs for the rule's absolute per-event gross mean were [-0.78, 1.07]% original and [-0.76, 1.47]% holdout. These are simple exploratory ticker resampling intervals, not prospective evidence.

Waiting for confirmation also meant it skipped 24/92 and 20/72 events entirely. Among triggered entries, 12/ 68 and 13/52 had ALREADY touched +5% from selloff close before entry. That is a genuine missed-first-bounce risk; the strategy targets *subsequent* gains from a higher entry.

## C. Stop sensitivity: +5% target and −10% instead of −5% stop
| Cohort | Method | 20-session target / stop / timeouts | Average per all events | 40-session target / stop / timeouts | Average per all events |
|---|---|---|---:|---|---:|
| original_92 | next_open | 53/17/22 | 0.38% | 57/25/10 | -0.16% |
| original_92 | day3 | 54/14/24 | 1.00% | 62/20/10 | 0.96% |
| original_92 | sma5_reversal | 43/9/19 | 1.30% | 49/20/2 | 0.57% |
| original_92 | three_rising_lows_break | 37/7/24 | 0.90% | 41/16/11 | 0.47% |
| holdout_72 | next_open | 38/15/19 | -0.39% | 43/23/6 | -0.68% |
| holdout_72 | day3 | 34/14/24 | -0.77% | 40/23/9 | -0.85% |
| holdout_72 | sma5_reversal | 24/6/27 | -0.03% | 34/14/9 | 0.02% |
| holdout_72 | three_rising_lows_break | 29/8/15 | 0.15% | 34/13/5 | 0.12% |

Wider stops mechanically allow more eventual +5% target hits, but also accept larger underlying losses and more time in drawdown. An option may lose most or all of its premium long before the underlying touches -10%.

## D. DTE proxy: how fast do post-entry moves occur, not options P&L
Each window is in **calendar days** from entry open. For the underlying only, +5% target vs −10% stop; timeouts mark no first-passage outcome by nominal calendar cutoff. No actual listed Friday option expirations; no strike, premium, delta, implied volatility, IV crush, theta, or bid/ask spreads.

| Window | Original: three rising lows target-before-stop | Holdout: three rising lows target-before-stop |
|---|---:|---:|
| 14 calendar days | 26/68 | 21/52 |
| 30 calendar days | 37/68 | 29/52 |
| 45 calendar days | 41/68 | 32/52 |
| 60 calendar days | 42/68 | 34/52 |

## Guardrails and next step
- **Do not buy options on this alone.** Gross underlying-stock gains of a few tenths of a percent per opportunity are insufficient to demonstrate a premium-paying option edge. Three-rising-lows signal's benefit over next-open buying is small and subject to data-snooping and clustered-company bias; confidence intervals may include 0. In contrast, the day-three rule failed out-of-company holdout, and the SMA5 rule was not consistent on a 20-session -5% stop.
- **No one tested option DTE profitability**. To answer the user's actual question, verify freely available *historical option quotes* for selected contracts, then hold-out test delta/strike, 30/45/60-day time-to-expiry and realistic bid/ask, or perform explicitly hypothetical IV/theta stress simulations; a price-path hit rate cannot stand in for option ROI.
- Other unmodeled features: actual earnings release timestamps, original-market IV, liquidity, hedging and commissions, selection survivorship, transaction prices at open and uncertain intrabar sequencing, implied volatility changes, post-selloff next catalysts. Results are retrospective across 61 stocks and 2023–2026, not live verified.

## Saved machine-readable audits
- [Original 92-event rows, all rules](./actionable_bounce_92event_outcomes_2026-10-10.csv) (368 entries).
- [Independent-company 72-event rows, all rules](./actionable_bounce_72holdout_outcomes_2026-10-10.csv) (288 entries).
