# Frozen earnings-recovery strategy: independent-company holdout and missing-factor audit

**Completed October 10, 2026. Verdict: FAILS frozen day-three gross-stock return and target-rate gates. NOT an A+ call options strategy.**

## Source and provenance
- [Pre-outcome frozen selection and protocol](./holdout_protocol_65new_tickers_2026-10-10.md), committed **before** accessing the new stock returns.
- 65 entirely new contemporary tickers, disjoint from 92-event cohort's 50-company selection, earlier 57-ticker exploratory holdout, and seven original discovery firms.
- [Frozen earnings-announcement roster](./holdout_source_dates_65tickers_2026-10-10.csv): 625 SEC 8-K-linked events from Quant500 (https://quant500.com/data), years 2023 to June 2026. 18 companies had no session-verified dates; 47 had at least one.
- Webull connected RTH stock prices for 46 of 47 tickers: BK could not be fetched (INVALID_SYMBOL). 609 announcement dates with adequate prices; 136 met a >=5% close drawdown in the first two regular sessions following qualified before-open/after-close earnings news, across 43 stocks; 106 first-session, 30 second-session.
- Historical financial statements from connected Webull, accepted only with **publish_date before earnings event**. Four prior sequential quarters: TTM net income >0, TTM CFO + capex >0, last available quarterly revenue YoY >0, most recent debt/equity in [0,2) and positive equity; incomplete => UNKNOWN.
- Financial screen: 72 PASS / 43 FAIL / 21 UNKNOWN. PASS cohort spans 29 companies.
- A stock-only simulation: next opening price of the third regular session after selloff closing day; +5% target, −5% stop, first touch within 20 entry-inclusive sessions. Intraday daily bar with both = stop first, overnight gaps filled at opening price. Exit at session 20 close if neither. No spreads, fees, taxes, dividend adjustment or option IV or premium. This is a retrospective company-disjoint historical holdout, **not** a prospective live out-of-time record.

## Test result
| Cohort | Number | Reached +5% target | Reached −5% stop | Timeouts | Mean gross stock P&L |
|---|---:|---:|---:|---:|---:|
| Previously studied 92-event benchmark | 92 | 47 (51.09%) | 35 | 10 | +0.77% |
| NEW quality PASS, frozen holdout | 72 | 30 (41.67%) | 36 | 6 | -0.76% |
| NEW quality FAIL | 43 | 22 | 17 | 4 | 0.79% |
| NEW quality UNKNOWN | 21 | 12 | 8 | 1 | 0.86% |

The new versus old quality-qualified mean-return difference is -1.53 percentage points. A simple **ticker-cluster bootstrap** (10,000 draws per cohort, resampling tickers with replacement and retaining all their events) has exploratory 95% interval **[-3.26, 0.16] percentage points**: do not claim statistical significance from an interval crossing zero. New sample's Wilson 95% interval for target-hit rate is **[30.99%, 53.19%]**. The new cohort does NOT meet the frozen >60% target-hit goal, or net mean >0 before fees.

### Performance by original earnings-announcement year
| Year | Qualified selloffs | Targets | Mean gross return |
|---|---:|---:|---:|
| 2023 | 17 | 7 | -0.63% |
| 2024 | 16 | 5 | -2.36% |
| 2025 | 26 | 12 | 0.24% |
| 2026 | 13 | 6 | -0.95% |

## Exploratory diagnostics: observable information missing from first strategy
Analyses below are SUBGROUP EXPLORATION within the already evaluated holdout. Thresholds tested include simple −1% SPY reaction day, −10% stock selloff and 20-day return signs; no factor is now validated for live use, and these are not prospective independent tests.

| Factor | Condition present (events; targets; mean gross) | Condition absent (events; targets; mean gross) |
|---|---|---|
| SPY declined ≥1% during earnings-reaction window | 13; 4; -2.91% | 59; 26; -0.29% |
| Earnings selloff ≥10% (versus 5–10%) | 18; 11; 0.40% | 54; 19; -1.15% |
| SPY preceding 20 sessions negative | 16; 9; 1.37% | 56; 21; -1.37% |
| SPY above prior 20-session mean at entry | 56; 23; -0.57% | 16; 7; -1.43% |
| Stock preceding 20 sessions positive | 41; 18; -0.72% | 31; 12; -0.82% |

One plausible explanation to test: market-wide drops are less favorable for isolated reversal attempts; quality screens alone cannot distinguish an earnings-driven *re-rating of future profits* from a temporary liquidity shock. An earnings miss, guidance cut, and especially analyst **forward estimate revisions** may be necessary labels in the dataset. Short-horizon market/sector-relative weakness, revisions, rising spreads/IV, balance-sheet stress, dividends and new catalysts need explicit event-time histories.

## Important caveats
- The filing date/session is SEC receipt time, not necessarily when the press release hit public media. 18 of 65 companies had no valid session classifications and were dropped by frozen protocol, so this is not representative of all listed equities.
- Some reactions qualified on the *second* trading day, when unrelated news or market moves could be involved.
- Webull prices may be corporate-action adjusted and fundamentals may be restated after original availability despite publication cutoff.
- Today-selected companies create survivorship and availability biases; specific sector weights and uneven event clusters need independent checking.
- All observed returns are UNDERLYING stock gross returns. No DTE, contract premiums, delta, IV crush, bid/ask liquidity or options P&L tested.
- Preliminary exploratory factor differences must not be retroactively incorporated into the frozen day-three strategy or promoted to A+ without an untouched later period or forward register.
- Failed performance doesn't imply shorting works: short trade execution, borrow availability, downside tails, and options convexity differ.

## Research next step
At each independently timestamped earnings release, record: EPS & revenue surprise vs pre-release consensus; management NEXT-quarter and FY guidance changes vs earlier guidance/consensus; analyst **forward** EPS revisions within 1–5 days; earnings-specific sector ETF relative returns; prior 20-day momentum, surprise magnitude, ATR-scaled drop, realized/IV volatility, and next major event date. Freeze a single minimal two-factor entry thesis and validate out-of-company/in-time; if data unavailable, run only descriptive feasibility. Avoid paying for a historical options feed without approval.

[Final event-level audit: 136 entries including all financial classifications and SPY factors](./holdout_final_136events_2026-10-10.csv)
