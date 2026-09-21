# SPY Quarterly Expiration Late-Close → Next-Open — Backward Falsification v1

Date: 2026-09-21
Status: **PRIMARY HYPOTHESIS FAILED LONG-HISTORY STABILITY / RECENT-REGIME CLUSTER REMAINS DESCRIPTIVELY INTERESTING**

## Frozen protocol
Event list was frozen first in:
- `research/spy_quarterly_expiration_frozen_event_panel_v1.md`
- freeze commit: `d9f158f3386d281a89a0fa52a406f6d46c2657d6`

Primary test:
> On each quarterly options/futures expiration session, classify the sign of SPY's 3:30 PM ET → RTH-close move and compare it with the sign of SPY expiration close → next RTH open gap.

The primary start time and outcome were not changed after outcome exposure.

## Data path
- Primary source: existing Webull SPY M5 history.
- Frozen event panel: 79 events from 2007-03-16 through 2026-09-18.
- Webull M5 history was available beginning with 2010-12-17, yielding **64 valid frozen events**.
- The first 15 frozen events (2007-03 through 2010-09) remained missing and were not replaced or dropped based on outcome.
- Massive was checked as an alternate existing source for the missing history, but the current plan returned NOT_ENTITLED for old intraday aggregates.
- Alpaca was also checked for the old window and returned no records.
- No new external data pipeline was built.

## Primary result
Across the 64 available frozen events:

- Directional matches: **33 / 64**
- Match rate: **51.56%**
- 95% Wilson interval: **39.58%–63.37%**
- Exact two-sided binomial p-value versus 50%: **0.901**

**Conclusion: the primary effect does not survive the backward historical falsification.**

The 3:30→close sign has essentially no durable full-sample directional relationship with the next-session opening-gap sign.

Return-level association is also negligible:
- Pearson correlation of 3:30→close return vs next-opening gap return: approximately **-0.009**
- Spearman correlation: approximately **+0.044**

## Era stability
| Era | N | Matches | Match rate |
|---|---:|---:|---:|
| 2010-12 through 2014 | 17 | 7 | 41.18% |
| 2015–2019 | 20 | 10 | 50.00% |
| 2020–2023 | 16 | 7 | 43.75% |
| 2024–2026 | 11 | 9 | 81.82% |

The recent strength is therefore **not representative of the longer history**.

More specifically:
- Pre-2024-09-20 sample: **24 / 55 = 43.64%**, 95% Wilson CI **31.37%–56.73%**.
- 2024-09-20 through 2026-09-18: **9 / 9 directional matches**.

The recent 9/9 run is real as a descriptive streak, but it appears to be a **recent-regime cluster**, not evidence of a durable structural rule. It must not be converted into a live 100% probability or scanner authority.

## Magnitude robustness
Excluding tiny late-day moves does not rescue the effect:

| Minimum absolute 3:30→close move | N | Matches | Match rate |
|---|---:|---:|---:|
| > 0.000% | 64 | 33 | 51.56% |
| > 0.025% | 54 | 29 | 53.70% |
| > 0.050% | 48 | 27 | 56.25% |
| > 0.100% | 34 | 17 | 50.00% |
| > 0.200% | 17 | 7 | 41.18% |

This is a robustness analysis only; thresholds were not allowed to replace the frozen primary rule.

## Directional breakdown
- Late-day UP signals: 15 / 27 matched = **55.56%**
- Late-day DOWN signals: 18 / 37 matched = **48.65%**

No compelling directional asymmetry emerged.

## 2026-09-18 → 2026-09-21
The new event qualifies as another recent-regime match:
- SPY 2026-09-18 3:30 PM open: **760.87**
- SPY expiration close: **761.69**
- Late move: **+0.108%**
- 2026-09-21 RTH open: **766.39**
- Overnight gap: **+0.617%**
- Primary classification: **MATCH**

This extends the recent descriptive streak to **9/9** from 2024-09-20 through 2026-09-18, but does not change the failed long-history result.

## Full available event audit
| Expiration | 3:30→close | Close→next open | Result |
|---|---:|---:|---|
| 2010-12-17 | +0.056% | +0.241% | MATCH |
| 2011-03-18 | +0.149% | +1.229% | MATCH |
| 2011-06-17 | +0.102% | -0.338% | MISS |
| 2011-09-16 | +0.446% | -1.638% | MISS |
| 2011-12-16 | +0.082% | +0.321% | MATCH |
| 2012-03-16 | +0.021% | -0.050% | MISS |
| 2012-06-15 | +0.127% | -0.395% | MISS |
| 2012-09-21 | -0.123% | -0.494% | MATCH |
| 2012-12-21 | +0.028% | -0.224% | MISS |
| 2013-03-15 | +0.096% | -0.937% | MISS |
| 2013-06-21 | -0.348% | -0.984% | MATCH |
| 2013-09-20 | +0.012% | -0.129% | MISS |
| 2013-12-20 | -0.044% | +0.463% | MISS |
| 2014-03-21 | -0.246% | +0.322% | MISS |
| 2014-06-20 | +0.054% | +0.010% | MATCH |
| 2014-09-19 | -0.075% | -0.189% | MATCH |
| 2014-12-19 | -0.299% | +0.102% | MISS |
| 2015-03-20 | -0.033% | +0.000% | MISS |
| 2015-06-19 | -0.076% | +0.684% | MISS |
| 2015-09-18 | -0.056% | +0.517% | MISS |
| 2015-12-18 | -0.394% | +0.730% | MISS |
| 2016-03-18 | -0.068% | -0.181% | MATCH |
| 2016-06-17 | -0.044% | +1.084% | MISS |
| 2016-09-16 | +0.042% | +0.370% | MATCH |
| 2016-12-16 | +0.088% | +0.080% | MATCH |
| 2017-03-17 | -0.177% | -0.021% | MATCH |
| 2017-06-16 | +0.128% | +0.396% | MATCH |
| 2017-09-15 | +0.056% | +0.144% | MATCH |
| 2017-12-15 | -0.159% | +0.582% | MISS |
| 2018-03-16 | -0.198% | -0.314% | MATCH |
| 2018-06-15 | +0.009% | +0.000% | MISS |
| 2018-09-21 | -0.072% | -0.223% | MATCH |
| 2018-12-21 | -0.261% | -0.694% | MATCH |
| 2019-03-15 | -0.019% | +0.078% | MISS |
| 2019-06-21 | -0.207% | +0.075% | MISS |
| 2019-09-20 | -0.147% | -0.245% | MATCH |
| 2019-12-20 | -0.137% | +0.265% | MISS |
| 2020-03-20 | -2.038% | -0.310% | MATCH |
| 2020-06-19 | -0.408% | -0.220% | MATCH |
| 2020-09-18 | -0.172% | -1.494% | MATCH |
| 2020-12-18 | +0.517% | -1.140% | MISS |
| 2021-03-19 | -0.345% | +0.141% | MISS |
| 2021-06-18 | -0.394% | +0.456% | MISS |
| 2021-09-17 | -0.016% | -1.477% | MATCH |
| 2021-12-17 | -0.414% | -1.213% | MATCH |
| 2022-03-18 | +0.108% | -0.040% | MISS |
| 2022-06-17 | -0.569% | +1.645% | MISS |
| 2022-09-16 | +0.169% | -0.840% | MISS |
| 2022-12-16 | -0.213% | +0.047% | MISS |
| 2023-03-17 | -0.192% | +0.218% | MISS |
| 2023-06-16 | -0.025% | -0.462% | MATCH |
| 2023-09-15 | -0.079% | -0.072% | MATCH |
| 2023-12-15 | -0.016% | +0.335% | MISS |
| 2024-03-15 | -0.059% | +0.838% | MISS |
| 2024-06-21 | +0.020% | -0.020% | MISS |
| 2024-09-20 | +0.003% | +0.183% | MATCH |
| 2024-12-20 | -0.121% | -0.034% | MATCH |
| 2025-03-21 | +0.358% | +1.213% | MATCH |
| 2025-06-20 | +0.136% | +0.130% | MATCH |
| 2025-09-19 | -0.014% | -0.226% | MATCH |
| 2025-12-19 | +0.015% | +0.497% | MATCH |
| 2026-03-20 | +0.221% | +1.449% | MATCH |
| 2026-06-18 | +0.098% | +0.112% | MATCH |
| 2026-09-18 | +0.108% | +0.617% | MATCH |

## Research verdict
**Do not promote the late-witching direction rule.**

The long-history primary result is approximately coin-flip. The recent 9/9 cluster is worth preserving as a regime observation, but not as a universal edge and not as a reason to alter live scanner direction.

The existing quarterly-expiration/rebalance risk gate remains valid for a different reason: expiration mechanics can distort late-day price/volume, so the final 30 minutes should continue to receive lower evidentiary weight rather than directional authority.

## Next clean operation
Do **not** optimize the failed primary rule.

The next defensible question is whether the recent 2024-09→2026-09 cluster corresponds to a pre-specified observable regime difference that was known before each next open — for example:
- magnitude/type of closing-auction imbalance,
- expiration/rebalance coincidence,
- volatility regime,
- overnight macro/news shock,
- breadth or dealer-hedging environment.

Any such branch requires a prior-work review and a frozen regime definition before testing.