# Frozen Grimes-inspired price-only failure diagnostic — 2023 archived M5 (exploratory)

**As run:** 2026-10-11. **Status:** Retrospective exploratory / prior 2023 outcomes already exposed under the buyer-volume study. NOT an untouched holdout, not Adam Grimes's authentic prior significant-support-pivot pattern, not a demonstrated option strategy. Frozen specification pre-outcome-derivation commit: `fcab1cb3b4032ab54964af149120d3d8f38b1f45`.

## Conclusion

**No positive net edge in the frozen primary test.** A price-only failure of the previous session's low selectively entered 20/54 complete events (34 skips), with 6 target-first / 13 stop-first / 1 timeouts. Target-first rate **30.000%**; average **-0.605% per entered stock trade**, or **-0.224% per evaluable event** counting all skips as zero after 50 basis points roundtrip costs. These are modeled stock-level returns; no option bid/ask, implied volatility, theta, spread, commissions, or affordability was tested.

## Frozen outcomes and comparators

| Rule | Evaluable | Entries | Skips | Target first | Stop first | Timeouts | Target first / entry | Mean net / entry | Mean net / signal |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| Primary prior-session-low failure, structural stop | 54 | 20 | 34 | 6 | 13 | 1 | 30.000% | -0.605% | -0.224% |
| Descriptive same pattern, fixed +2/-2 | 54 | 23 | 31 | 8 | 13 | 2 | 34.783% | -0.986% | -0.420% |
| Secondary 20-session-low failure, structural stop | 54 | 15 | 39 | 5 | 9 | 1 | 33.333% | -0.615% | -0.171% |
| Previously tested next-D1-open +2/-2 | 54 | 54 | 0 | 18 | 34 | 2 | 33.333% | -1.117% | -1.117% |
| Previously tested buyer-volume entry | 54 | 11 | 43 | 4 | 6 | 1 | 36.364% | -0.931% | -0.190% |

Primary paired per-event improvement versus always entering at D1 next open was **+0.893 percentage points**, but the primary strategy still loses on its entered trades and on the complete event denominator. Improvement reflects selective abstention as well as different exits; it is not evidence of positive expected profit. Compared to buyer-volume the paired difference in returns per eligible event was **-0.035 percentage points**. These variants have different stop mechanics and entry thresholds; their per-entry statistics are not apples-to-apples head-to-head matched trades.

## Data and decision audit

- Frozen **57** ticker/date events: **54** evaluable with full 78 D0 + 78 D1 + 78 D2 Webull regular-hours M5 bars. Three remain **UNKNOWN**: HUBS 2023-02-03; CMG 2023-07-27; AEO 2023-11-21. These were never counted as failures, winners, or zeros.
- Primary skip reasons: `SKIP_NO_PATTERN` 30, `SKIP_EXTENDED` 1, `SKIP_RISK_INVALID` 3.
- Exit handling: 0 gap-through-stop and 2 gap-through-target fills at actual subsequent bar open, 0 same-bar both-touched cases resolved stop-first. No forward-confirmation candle or future volume condition used.
- Primary D0 low is *not* an independently validated significant support pivot. Secondary 20-d as-of daily lows were reconstructed from already-archived 2022-2023 daily files, rebased to each D0 M5 close; require >=20 prior sessions and <=3% D0 daily-vs-M5 rebased low mismatch. It is still not a human/algorithmically confirmed significant pivot.
- Original M5 archives and the frozen candidate manifest were fetched unmodified from the repository. JSON output provides their blob SHAs and all per-event prices, timestamps, decisions and outcomes.

## Uncertainty (descriptive, NOT validation)

Deterministic 10,000-replicate resampling by symbol: 37 issuer clusters. 95% percentile intervals: mean net per entered trade [-1.224%, 0.039%], mean net per evaluable event [-0.476%, 0.013%], and paired primary-minus-next-open event return [0.415, 1.400] percentage points. Resampling by 35 signal-date clusters as dependence sensitivity: event-return interval [-0.505%, 0.052%]; paired improvement [0.394, 1.416] points. These intervals do not correct for reuse of previously exposed outcomes and cannot validate an 80% success objective.

## Decision and next test

**Reject this precise previous-day-low price-only trigger as a profitable or 80%-target-first stock entry.** Do not add it to live scanners as a validated buy signal. This does *not* rule out authentic Grimes-style significant swing support, a stronger market context, or variants in a genuinely untouched issuer/date cohort. The next defensible independent experiment would define significant pivot support ex ante (e.g., algorithmic pivots detectable before the selloff) before revealing next-session M5 outcomes, predefine pivot penetration/reclaim/execution/cost/option constraints, compare against same-regime similar-volatility control events, and then freeze an unused multi-year cohort. No thresholds here were optimized.

Primary machine-readable results: [2023 Grimes exploratory results](data/grimes_priceonly_prior_session_low_2023_exploratory_results_2026_10_11.json).

Frozen source protocol: [Price-only frozen rules](frozen_grimes_priceonly_prior_session_low_2023_exploratory_2026_10_11.md).
