# Mag-7 3M/6M/12M Rank Signal v1.0 — FROZEN PROTOCOL

Frozen: 2026-09-24
Outcome status at freeze: NOT EXPOSED
Data source: data/historical/canonical_monthly_2017_2026.csv

## 1. Purpose
Test whether relative trailing performance across a fixed seven-stock retrospective Mag-7 cohort predicts the next calendar month's relative performance.

This v1.0 is a reconstruction because the earlier exact rule was not recoverable. It is intentionally symmetric so the research does not choose momentum versus contrarian after outcomes are visible.

## 2. Fixed stock universe
AAPL, MSFT, AMZN, GOOGL, META, NVDA, TSLA.

QQQ and SPY are benchmarks only and are never eligible for selection.

Important limitation: this is a fixed present-day cohort applied retrospectively. It contains survivorship / hindsight selection and therefore is a cohort study, not a claim that an investor in 2017 could have selected the same basket ex ante.

## 3. Formation dates
Use each completed calendar month-end in the canonical monthly panel.

A formation month is eligible only when all seven stocks have valid current, 3-month-lag, 6-month-lag, and 12-month-lag closes and a valid next-month close.

The partial September 2026 month is excluded from all completed-month outcomes.

## 4. Trailing returns
For stock i at formation month t:
- R3 = P(t) / P(t-3) - 1
- R6 = P(t) / P(t-6) - 1
- R12 = P(t) / P(t-12) - 1

Use split-adjusted price closes from the canonical store. Do not dividend-adjust and do not substitute adjusted total-return series.

## 5. Cross-sectional ranks
At each formation month independently:
- rank R3 from weakest=1 to strongest=7
- rank R6 from weakest=1 to strongest=7
- rank R12 from weakest=1 to strongest=7

Ties receive average ranks.

Composite Score = (rank3 + rank6 + rank12) / 3.

Higher score always means stronger trailing relative performance.

No z-score, volatility scaling, benchmark-relative transformation, sector adjustment, or tuned horizon weighting is allowed in v1.0.

## 6. Pre-registered arms
Both arms must be reported. Neither may be hidden based on results.

MOMENTUM ARM:
- Select the stock with the highest Composite Score.
- Tie-break 1: higher 12M rank.
- Tie-break 2: higher 6M rank.
- Tie-break 3: higher 3M rank.
- Final exact tie: equal-weight tied names.

CONTRARIAN ARM:
- Select the stock with the lowest Composite Score.
- Tie-break 1: lower 12M rank.
- Tie-break 2: lower 6M rank.
- Tie-break 3: lower 3M rank.
- Final exact tie: equal-weight tied names.

EQUAL-WEIGHT MAG-7:
- Equal-weight all seven each month as the cohort baseline.

## 7. Forward outcome
Primary forward outcome for each stock is:
F1 = P(t+1) / P(t) - 1.

This is month-end-close to next-month-end-close and is a signal-research approximation. Because the formation close is used in the signal itself, this is not presented as executable after-close trading P&L.

## 8. Primary scientific test
For each formation month, compute Spearman correlation across the seven stocks between Composite Score at t and F1.

Primary aggregate statistic:
- mean monthly Spearman IC.

Also report:
- median monthly IC;
- percentage of months with IC > 0;
- two-sided bootstrap 95% confidence interval for mean IC using months as the resampling unit.

Interpretation:
- positive IC = momentum-like ranking information;
- negative IC = contrarian/reversal-like ranking information;
- near zero = no useful directional rank information.

No sign is designated as the desired result.

## 9. Decision-level descriptive results
Report separately:
- Momentum arm monthly return;
- Contrarian arm monthly return;
- Equal-weight Mag-7 monthly return;
- QQQ monthly return;
- SPY monthly return.

For each, report:
- arithmetic mean monthly return;
- cumulative growth of $1;
- annualized return;
- annualized volatility;
- maximum drawdown;
- positive-month rate.

Also report active monthly return of each arm versus equal-weight Mag-7 and QQQ.

These are descriptive because of the fixed retrospective cohort and same-close signal approximation.

## 10. Stability / falsification splits
Without changing rules, report the same primary IC and arm spreads for:
- 2018-2020
- 2021-2023
- 2024-2026 completed months

If a boundary has insufficient eligible months, report it rather than changing the boundary.

Also report calendar-year results.

## 11. Promotion standard
This is research-only. No scanner or live-trading rule may be created from v1.0 solely because one arm has the highest cumulative return.

For the signal to merit a separate preregistered replication:
1. Mean monthly IC must have the same sign in all three prespecified eras.
2. At least 55% of eligible months must have IC with that same sign.
3. The corresponding extreme arm (momentum if positive, contrarian if negative) must outperform equal-weight Mag-7 on mean monthly return and cumulative return over the full sample.
4. No single calendar year may account for more than 40% of the arm's cumulative log excess return versus equal-weight Mag-7.
5. Results remain research-only until replicated on an independently defined universe or untouched later period.

Failure of these gates means do not tune the 3/6/12 weights, change the selected count, change formation frequency, or add filters on this same sample to rescue the rule.

## 12. Forbidden post-result changes
After this commit, do not:
- change 3/6/12 to another horizon set;
- optimize weights;
- decide to show only the better of momentum or contrarian;
- switch top/bottom 1 to top/bottom 2 or 3;
- add trend, valuation, volatility, macro, earnings, or market-regime filters;
- change era boundaries;
- replace price returns with total returns;
- change tie-break rules;
- exclude losing names/months.

Any such idea is a new hypothesis requiring a new prior-work review, new frozen protocol, and untouched validation.

## 13. Next operation
After this protocol and its prior-work review are committed, run v1.0 once on the frozen canonical panel and save machine-readable signals/results plus a readable verdict.
