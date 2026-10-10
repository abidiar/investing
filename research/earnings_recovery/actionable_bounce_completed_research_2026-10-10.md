# Capturing earnings-selloff rebounds without premature entries — completed audit

**October 10, 2026 | Status: exploratory and unvalidated for actual call options.**
Research frozen before this run: [rules](./actionable_bounce_entry_protocol_2026-10-10.md).

## Data and method
- Original financial-quality event cohort: 92 earnings selloffs across 32 companies.
- Separate contemporary-company holdout: 72 financial-quality selloffs across 29 companies; same historical period, not a time-out-of-sample live test.
- Both sets re-queried and event-validated using connected Webull regular-hours daily OHLC (2023–June 2026 events).
- First-hit outcomes from selloff-day CLOSE anchor: any +5% upside touch, +5% before additional −5% drawdown, and +5% before additional −10% drawdown, within 20, 40 and 60 *trading* sessions.
- Independently, four entry rules at the next open: (a) immediate, (b) third session, (c) first session 5–20 close above 5-SMA after prior close at or below SMA plus close above prior day's high, (d) first session 3–20 with three nondecreasing lows and close above past two highs. Enter next session's open. New confirmation signals skipped when entry open >8% above original selloff close. Only the first signal counts. All entries are observable at time of trade.
- +5% target; stops −5% or −10%; maximum holding 20 or 40 entry-inclusive sessions, OHLC stop-first when both touched in same bar and open-price gap fills. Stocks, not options. Skipped events counted at 0 in per-opportunity results. No bid/ask, fees, slippage, IV, theta, actual options premium or actual option fill considered.

## Central distinction: eventual bounce versus surviving it

| Event group | Events | Any +5% rebound within 60 trading sessions | +5% reached BEFORE additional −5% | +5% reached BEFORE additional −10% | Median lowest intraday price vs original selloff close within 60 sessions |
|---|---:|---:|---:|---:|---:|
| Original | 92 | 65 (70.7%) | 43 (46.7%) | 57 (62.0%) | −8.60% |
| Independent | 72 | 48 (66.7%) | 35 (48.6%) | 44 (61.1%) | −8.57% |

The price-path rates are hypothetical observations from the original selloff close, not executable trades. Allowing −10% rather than −5% captures more paths, but cannot be interpreted as a recommendation to use a wider options stop. Median +5%-touch time of rebounders was 9–9.5 trading sessions by day 60. Since price can rise 5% AFTER it first plunged 10%, eventually rebounding does not imply a buying opportunity for a call position that entered immediately.

## Objective-entry comparison: stock +5% target, −10% stop, 20 trading sessions

| Rule | Original 92: traded; reached target; mean gross STOCK return | Independent 72: traded; reached target; mean gross STOCK return |
|---|---|---|
| Next open | 92; 53 (57.6%); +0.38% | 72; 38 (52.8%); −0.39% |
| Third session open | 92; 54 (58.7%); +1.00% | 72; 34 (47.2%); −0.77% |
| 5-day SMA reclaim + prior-high break, skip >8% chase | 71; 43 (60.6%); +1.69% | 57; 24 (42.1%); −0.04% |
| 3 nondecreasing lows + 2-day high breakout, skip >8% chase | 68; 37 (54.4%); +1.22% | 52; 29 (55.8%); +0.21% |

Moving-average entry is better looking in original group but does not repeat in the independent group. Three-rising-lows is slightly positive in both, but much too weak to establish a favorable call setup. Conditional signal win rates omit no-trade cases and must not be judged without coverage.

Matched comparison with day-three baseline only on the events that would trigger each signal:
- SMA signal, 20-session 10% stop: original +0.71pp versus day-three on identical events, 95% bootstrap CI [−1.14,+2.22]; holdout +0.42pp, CI [−0.54,+1.42].
- Three rising lows, 20-session 10% stop: original −0.75pp, bootstrap CI [−2.34,+0.69]; holdout −0.38pp, CI [−1.90,+1.13].
These ticker-cluster bootstraps include zero and are not independently validated.

## Nominal calendar-time windows (stock PRICE proxy ONLY)

Count how often underlying stock reaches +5% BEFORE −10% measured from a specific strategy's entry open, or expires unresolved, over 14/30/45/60 *calendar* days. Calendar cutoffs are not standardized listed option expirations. They are not option win rates.

| Method and cohort | 14 calendar days | 30 calendar days | 45 calendar days | 60 calendar days |
|---|---:|---:|---:|---:|
| Original: 5-SMA confirm | 30/71 | 44/71 | 47/71 | 49/71 |
| Holdout: 5-SMA confirm | 18/57 | 24/57 | 30/57 | 35/57 |
| Original: 3 rising lows | 26/68 | 37/68 | 41/68 | 42/68 |
| Holdout: 3 rising lows | 21/52 | 29/52 | 32/52 | 34/52 |

The longer holding window gives more time for gains **and losses**: time-to-hit outcomes by themselves cannot identify the profitable option DTE, especially given earnings IV crush, calendar-day theta, strike selection, liquidity, and varying premium expense. A fully correct underlying rebound can still lose money in calls. No historical contract bid/ask IV data were available in this analysis.

## Decision and next discriminating study
**No entry method is validated enough to promote to A+ calls.** These results undermine the fixed-day3 method and show that a simple turning-price confirmation alone is not a robust solution to options timing. The next attempt should not retune thresholds on the same 164 events. More discriminating predictors could include forward earnings revision magnitude, sector- and SPY-relative momentum, realized volatility (ATR-normalized drawdown), trend of earnings expectations and the 'first low' stabilization duration, collected with true point-in-time timestamps. Freeze minimal new rules on previously untouched companies and a later period, then obtain historical executable contract premium/IV series or clearly label a hypothetical sensitivity model.

## Frozen results and audit
- [Original 92-event entry-level audit](./actionable_bounce_dev92_checkpoint_2026-10-10.json).
- [Independent 72-event entry-level audit](./actionable_bounce_holdout72_checkpoint_2026-10-10.json).
- [164-event path-by-stop outcomes](./actionable_bounce_path_risk_164events_2026-10-10.csv).
- [Matched-entry test with ticker-cluster bootstrap](./actionable_bounce_paired_compare_2026-10-10.json).
- [Calendar DTE underlying stock proxy](./actionable_bounce_calendar_proxy_164events_2026-10-10.json).
