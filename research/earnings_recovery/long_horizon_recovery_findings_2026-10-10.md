# Long-horizon recovery audit: independent companies + DELL/META/QCOM/ORCL

**Date:** October 10, 2026 (last completed daily price session October 9). **Status:** descriptive retrospective price-path research, not a tested options strategy or live recommendation.

## Correction to the research question

Previous earnings-selloff strategy tests conflated (A) a +5%-before-−5% short-duration stock trade with (B) *eventual* return to pre-earnings price. A stock can fail a short-term call/stop but ultimately regain its pre-announcement close months later. This study isolates B and explicitly measures elapsed sessions and intervening downside.

## Panel 1: broad quality-company earnings dislocations

Input: existing [original 92-event quality cohort](./earnings_selloff_recovery_92events_2026-10-10.csv) and disjoint [independent-company 72-event quality cohort](./holdout_final_136events_2026-10-10.csv), total **164 qualifying earnings selloffs, 61 distinct contemporary companies**. Financial-quality screens selected on historical publish dates; current ticker universe selection still creates survival, industry-weight and data-availability biases.

All 164 input events were validated against historical Webull RTH OHLC on qualifying selloff date (selloff drop matches underlying prices); 1,200 daily bars per symbol ending Oct 9. Pre-announcement closing price = final trading close preceding earnings-reaction day (BMO same session, AH following regular session). An event was a first-/second-session closing decline of at least 5%. **Full recovery:** any later DAILY CLOSE >= pre-announcement closing price; touch of that level INTRADAY separately. **Partial bounce:** any subsequent INTRADAY HIGH >= 1.05 × selloff close. Test future cumulative first achievement within 20/40/60/90/120/180/252 trading sessions; event must have all h future sessions available to enter that h denominator; no censoring imputation and no guarantee price remains recovered at horizon. No trade entry/exit or premiums required for these descriptive counts.

| Horizon (trading sessions) | Original quality cohort recovered/eligible | Separate-company quality holdout recovered/eligible | Combined |
|---:|---:|---:|---:|
| 20 | 25/92 (27.2%) | 17/72 (23.6%) | 42/164 (25.6%) |
| 40 | 33/92 (35.9%) | 29/72 (40.3%) | 62/164 (37.8%) |
| 60 | 48/92 (52.2%) | 38/72 (52.8%) | 86/164 (52.4%) |
| 90 | 56/91 (61.5%) | 44/72 (61.1%) | 100/163 (61.3%) |
| 120 | 62/87 (71.3%) | 43/64 (67.2%) | 105/151 (69.5%) |
| 180 | 60/79 (75.9%) | 42/59 (71.2%) | 102/138 (73.9%) |
| 252 | 58/72 (80.6%) | 40/52 (76.9%) | 98/124 (79.0%) |

**Censoring warning:** the longer-horizon denominators shrink as more recent 2026 events have not yet had enough time to recover. Do NOT naively interpret the above increasing percentage as a within-same-denominator survival curve. In the *fixed* 52 quality holdout events that have all 252 sessions observed, cumulative pre-earnings closing-price recoveries were 10/52 by 20d, 20/52 by 40d, 24/52 by 60d, 29/52 by 90d, 34/52 by 120d, 37/52 by 180d and **40/52 (76.9%) by 252 sessions**.

### Path dependence and short-stop contradiction

Within 64 independent quality events having 120 sessions of data, 43 fully regained the pre-earnings closing price within 120 sessions. Of these 43 recovered cases:
- **16/43 (37.2%)** had hit the originally modeled **−5% stop on a stock bought on third session** during its first 20 entry-inclusive sessions (so eventual recovery and early trade failure genuinely coexist).
- **20/43** declined at least 5% *below the earnings selloff closing price* before their first closing-price recovery, **10/43** declined at least 10%, and **2/43** declined at least 20%.
- Median time to first recovery was **34 trading sessions** for these 43 eventual 120-day recoverers (conditional on recovery, not unbiased waiting time). Median worst low before closing recovery was −4.42% below selloff close. Intraday sequence within a daily candle is unknown, but the full pre-recovery path is tracked.
- These results are UNDERLYING STOCK paths, and do not imply buying a call on the selloff close or at day three would be profitable. A long-dated call can expire worthless before recovery or lose value due to IV/theta/strike despite correct stock-path direction.

### Failure examples in full-year eligible cohort

Not everything recovered: among qualifying holdout companies with 252 future sessions, 12/52 did not CLOSE back to their pre-earnings price even once, including significant continuing weakness in some DLTR, FIS, GPN, and LEN episodes. Some did have intermittent rebounds. This invalidates any 'almost guaranteed' recovery characterization.

### Detailed broad cohort file

[164-event long-horizon audit](./quality_164_long_horizon_recovery_2026-10-10.csv) with individual observed recovery horizons, price drawdowns, bounce timings, and matched day-three stop outcomes.

## Panel 2: user's named examples (hindsight-selected CASE STUDY)

Frozen [case selection and earnings date protocol](./four_exemplars_long_horizon_protocol_2026-10-10.md) and [event-level results](./four_exemplars_long_horizon_events_2026-10-10.csv). DELL, META, QCOM, and ORCL named before analysis (but chosen because user noticed their rebounds). 55 historic earnings announcement dates 2023 through June 2026, 19 post-earnings selloffs meeting first-two-trading-day close <=−5% of pre-earnings closing price. META 8-K listing does NOT say BMO/AH; modeled as *after-close* provisional scenario, checked against media for April 2024 but not independently timestamp validated for all fourteen events. Treat META totals as PROVISIONAL.

Among the 19 selected selloff events, 10/19 regained pre-announcement price by 60 sessions and 13/17 whose full 120 sessions elapsed did so by that horizon (one other could recover at 120 after severe interim losses). These examples should NEVER be pooled into a randomized estimate of trading success.

| Company | Earnings announcement | Full initial close drop | Sessions until closing back to pre-earnings close | Important |
|---|---|---:|---:|---|
| META | 2024-04-24 | −10.56% | 28 | At the time, after-close Q1 release according to contemporary reporting; time needs archived verification |
| QCOM | 2025-07-30 | −7.73% | 18 | Fast rebound case |
| DELL | 2025-02-27 | −11.38% | 50 | Another very large further decline occurred before/within 60-session interval |
| ORCL | 2025-12-10 | −10.83% | 115 | Recovery took far longer than short-DTE option |
| DELL | 2024-05-30 | −17.87% | Not within 120 | Case-study failure shows danger of cherry-picked winners |

Data: Webull split-adjusted stock OHLC, SEC 8-K historical calendars at https://quant500.com/data; independent example of online accessible post-earnings stock return matrix at https://www.trefis.com/stock/dell/articles2/600479/how-will-dell-technologies-stock-react-to-its-upcoming-earnings/2026-05-27.

## Decision / next meaningful operation

There is stronger descriptive historical support for *partial and eventual stock-price recovery over months* than for a profitable immediate day-three call entry. But this sample is NOT proof that quality improves returns relative to the whole investable universe; prior quality-vs-fail comparisons have been mixed, and losses can be prolonged.

Most valuable next test is to distinguish **dislocation identification (watchlist)** from **tradable recovery onset (entry)**. Freeze a minimal signal using only known-by-entry information: (1) initial earnings selloff >=5% and prior profitability/revenue data, (2) post-selloff price stabilization / reclaim of short-term trend, and (3) relative strength versus sector and SPY (where prices permit); use matched controls and independent future samples. Record one or two trigger variants, how many events trigger, median calendar waiting time, probability of +5% and +10% BEFORE −5% and −10% from the entry price within 20/40/60 sessions, and net expectancy after trading costs. Reversal trigger should be judged on its own performance, *not* just whether the stock eventually recovers.

Only after the entry edge survives independent validation, test actual option strike, premium, DTE, IV crush, theta, bid/ask and spreads with free historical data. With a recovery at 115 trading sessions, 30/45/60-calendar-day options can easily expire before the stock recovers; longer calls cost more. Do not pay for data without explicit user approval.
