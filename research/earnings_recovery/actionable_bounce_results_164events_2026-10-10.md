# Earnings selloff rebound entry: frozen-rule historical test of 164 quality-qualified events

**Run on October 10, 2026.** Status: completed retrospective exploratory study. This research is NOT an independently validated options strategy, NOT a live-forward record, and does NOT include historical option premium, IV crush, theta, spread, or traded listed contracts.

**Protocol committed before this calculation:** [actionable bounce entry protocol](./actionable_bounce_entry_protocol_2026-10-10.md). Inputs: 92 earnings-selloff events from original quality cohort and 72 quality-passing events from the distinct company holdout. Historical prices re-read from connected Webull daily regular-session adjusted OHLC (1200 bars per symbol), verified for all **164 of 164 events** against their original five-session return or day-three entry open (61 symbols, zero missing/failed validations). Input event windows frozen in [original event price bars](./actionable_bounce_price_windows_92events_2026-10-10.json) and [company-disjoint holdout bars](./actionable_bounce_price_windows_72events_2026-10-10.json).

## Critical finding: what does "eventually rebounds" hide?

A +5% rebound from the first qualifying earnings-selloff CLOSE is very different from reaching +5% BEFORE another −5% or −10% decline. Intraday high/low from the NEXT trading session through day 20, 40, or 60; worst-case stop-first assumption when both touch same bar; no hindsight trough anchoring. All denominators count EVERY qualified event.

| Horizon (trading sessions) | Original: ever +5% | Holdout: ever +5% | Original: +5 before −5 | Holdout: +5 before −5 | Original: +5 before −10 | Holdout: +5 before −10 |
|---|---:|---:|---:|---:|---:|---:|
| 20 | 56/92 | 38/72 | 40/92 | 34/72 | 52/92 | 38/72 |
| 40 | 60/92 | 43/72 | 42/92 | 35/72 | 55/92 | 42/72 |
| 60 | 65/92 | 48/72 | 43/92 | 35/72 | 57/92 | 44/72 |

Median time to first +5% bounce, conditional on touch by 60: **9** sessions (original) and **9.5** sessions (holdout). Median lowest daily low within 60 relative to selloff closing price was **−8.60%** (original) and **−8.57%** (holdout), even when some bounces happened first.

## Four prespecified entry models

All four enter at regular-session OPEN, not retrospectively at a low. Original rule meanings below.

1. Next open after qualifying selloff; all events.
2. Third session open; prior established baseline, all events.
3. **5DMA breakout**: first post-selloff 5–20th session close crossing above 5-day close SMA from below while closing above previous day's high, enter next open; discard first entry if opening price >8% over initial selloff close, otherwise no signal = skip.
4. **Three rising lows breakout**: first post-selloff 3–20th session with 3 non-decreasing daily lows and close above the highs of preceding two days; enter next open; same +8% no-chase cap and first-signal skip.

Trading result: underlying STOCK +5% profit target / −10% stop / up to 20 entry-inclusive sessions. If both reached within one candle, stop first, and opening gaps filled at their opens. Gross prices (no trading costs); skipped events counted as zero in alternate population-level averages and never retroactively deleted.

| Rule | Original trades | Original mean per trade | Holdout trades | Holdout mean per trade |
|---|---:|---:|---:|---:|
| Next open | 92/92 | 0.38% | 72/72 | -0.39% |
| Third-session open | 92/92 | 1.00% | 72/72 | -0.77% |
| 5DMA reclaim/breakout | 71/92 | 1.69% | 57/72 | -0.04% |
| Three rising lows/breakout | 68/92 | 1.22% | 52/72 | 0.21% |

For completeness, +5% target/−5% stop/20 sessions: next open **−0.50% vs −0.20%**, day three **+0.77% vs −0.76%**, 5DMA reclaim **+1.09% vs −0.58%**, and three rising lows **+0.22% vs +0.57%**, original vs holdout, respectively. These are conditional-trade gross results and include no option P&L. Stop-loss widening changes hit rates and losses, not a proven edge.

The three-rising-lows model has a median entry **7 sessions** after the initial selloff in BOTH cohorts; it triggers 68 of 92 original and 52 of 72 holdout opportunities. Among entries, **12/68** original and **13/52** holdout stocks had already touched +5% above original selloff close *before* the purchase open: confirmation can arrive after the fastest recovery. Across all initial events, the rule also skipped **24/92** and **20/72** events due to no signal or +8% chase cap.

## Fair matched opportunity comparison

Important selection correction: if entry signals trade different event subsets, the raw per-trade means above are NOT a valid proof that the signal improves timing. For each signaled trade, compare it to buying the exact SAME event on session three at the same exit rules:

| Cohort | Trigger | Matched events | Signal mean | Day-three same-events mean | Difference (signal minus baseline) | Ticker-cluster bootstrap 95% interval, exploratory |
|---|---|---:|---:|---:|---:|---|
| original92 | 5DMA reclaim/breakout | 71 | 1.69% | 0.97% | 0.71 pp | -1.16 to 2.29 pp |
| original92 | Three rising lows/breakout | 68 | 1.22% | 1.97% | -0.75 pp | -2.31 to 0.75 pp |
| separate72 | 5DMA reclaim/breakout | 57 | -0.04% | -0.45% | 0.42 pp | -0.56 to 1.44 pp |
| separate72 | Three rising lows/breakout | 52 | 0.21% | 0.58% | -0.38 pp | -1.97 to 1.12 pp |

The three-rising-lows rule did NOT improve returns over day-three entry on matched triggered opportunities in either cohort, even though its unconditional traded means were slightly positive in both. The difference's bootstrap intervals contain zero in both cohorts. This may reflect selecting better-rebounding situations rather than entering them better. These results are not independent forward validation.

## Calendar time available, NOT call option backtest

For the rising-lows entry and a +5% underlying stock target before −10% stop, the target/stop first-hit counts by 14/30/45/60 calendar days after entry were:

| Calendar days | Original target hits | Original stops | Holdout target hits | Holdout stops |
|---|---:|---:|---:|---:|
| 14 | 26/68 | 3/68 | 21/52 | 4/52 |
| 30 | 37/68 | 7/68 | 29/52 | 9/52 |
| 45 | 41/68 | 12/68 | 32/52 | 12/52 |
| 60 | 42/68 | 16/68 | 34/52 | 13/52 |

For instance, 30 calendar days give **37/68** vs **29/52** target-first events in the original and holdout triggered subsamples. A positive stock-price target is not a profitable call; a 10% stock decline may severely damage the option before the stop, and longer-dated options can be much more expensive. This analysis supplies no IV or actual strike/expiry/premium data. Do not label a DTE the best or claim an options win percentage.

## Research decision and next defensible operation
- **Eventual stock rebound** is a real descriptive pattern, but the price may suffer significant additional drawdown first.
- **No tested timing rule has proved better than a same-event day-three comparison consistently.** The rising-lows rule is useful as an OBSERVABLE stabilization candidate but not an A+ entry and not cleared for automated call-buy recommendations.
- For actual calls, obtain historical contract-level bid/ask and implied volatility for fixed strike/delta and actual listed 30/45/60 calendar-day expirations. Compare entry-at-signal with entry-at-day3 on identical events, realistic spreads, and premium drawdown. If historical option quotes are inaccessible without paying, run explicitly hypothetical priced scenarios at different IV/decay assumptions. Do not silently relabel a theoretical scenario as an executed backtest.
- Crucially, test newly frozen single entry rule on a truly unseen chronological window/forward log, including absent signals and unchanged risk limits. This whole 164-event analysis is **exploratory** because these cohorts were previously inspected, and 4 entries x 2 stops x 2 holds imply multiple comparisons.

### Reproducibility
- [First-hit event path audit (492 rows)](./actionable_bounce_path_164events_2026-10-10.csv)
- [All entry/exit attempts (2624 rows)](./actionable_bounce_trades_164events_2026-10-10.csv)
- [Underlying calendar-time scenarios (2304 rows)](./actionable_bounce_calendar_proxy_164events_2026-10-10.csv)
- [Structured aggregate statistics](./actionable_bounce_summary_164events_2026-10-10.json)
