# Mag-7 3M/6M/12M Rank Signal v1.0 — Results

Run date: 2026-09-24
Protocol: `research/mag7_3m_6m_12m_rank_v1_frozen_2026-09-24.md`
Dataset: `data/historical/canonical_monthly_2017_2026.csv`

## Primary result
- Eligible formation months: **103** (2018-01 through 2026-07)
- Mean monthly Spearman IC: **0.0396**
- Median monthly IC: **0.0357**
- IC > 0: **51.5%** of months
- Bootstrap 95% CI for mean IC: **[-0.0512, 0.1291]**
- Direction: **positive/momentum-like**

## Full-sample descriptive performance
| Arm | Mean monthly | Growth of $1 | Annualized return | Annualized vol | Max drawdown | Positive months |
|---|---:|---:|---:|---:|---:|---:|
| Momentum | 4.11% | 23.06 | 44.14% | 52.74% | -60.79% | 58.3% |
| Contrarian | 3.54% | 20.20 | 41.93% | 38.30% | -42.36% | 63.1% |
| Equal-weight Mag-7 | 2.63% | 10.54 | 31.58% | 27.99% | -45.91% | 63.1% |
| QQQ | 1.58% | 4.23 | 18.30% | 20.15% | -32.99% | 64.1% |
| SPY | 1.09% | 2.72 | 12.37% | 16.52% | -24.78% | 66.0% |

## Prespecified era stability
| Era | N | Mean IC | IC > 0 | Momentum - EW mean | Contrarian - EW mean |
|---|---:|---:|---:|---:|---:|
| 2018-2020 | 36 | 0.1036 | 58.3% | 4.11% | -0.47% |
| 2021-2023 | 36 | 0.0404 | 47.2% | -0.46% | 1.94% |
| 2024-2026 | 31 | -0.0356 | 48.4% | 0.67% | 1.32% |

## Frozen promotion gates
- Same IC sign in all three eras: **FAIL**
- At least 55% of months share that sign: **FAIL**
- Corresponding arm beats equal-weight Mag-7 on mean monthly return: **PASS**
- Corresponding arm beats equal-weight Mag-7 on cumulative return: **PASS**
- No single calendar year contributes >40% of positive log excess return: **FAIL**

**Promotion result: FAIL — do not promote or tune on this sample.**

## Interpretation limits
This is a fixed retrospective present-day Mag-7 cohort, so survivorship/hindsight selection is built into the universe. The month-end-close to next-month-end-close return is a signal-research approximation, not executable after-close P&L. No filters, horizon weights, selected-count changes, or post-result rescue tuning are permitted under v1.0.
