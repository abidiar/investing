# Modelled Dealer-GEX Gap Follow-Through v1.0 — Frozen Results

Generated: 2026-09-19T18:32:21.700801+00:00

## Measurement warning
This experiment uses a **MODELLED DEALER-GEX PROXY**, not observed dealer inventory. Calls are assumed dealer-long-gamma and puts dealer-short-gamma, following the frozen published proxy convention.

## Coverage
- Total panel rows (2008-2010): **1128**
- 2008 seed candidates: **387**
- Untouched 2009-2010 holdout candidates: **741**
- SPY holdout: **362**
- IWM holdout: **379**
- Exclusions: `{'SPY': {'no_price': 0, 'no_next': 0, 'no_history': 0, 'no_gex': 0, 'small_gap': 195}, 'IWM': {'no_price': 0, 'no_next': 0, 'no_history': 0, 'no_gex': 0, 'small_gap': 190}}`

## Frozen mechanism tests
- Signed GEX/ADV -> gap-direction open-to-close follow-through: **rho=-0.0759, p=0.03889** (expected <0)
- Signed GEX/ADV -> excursion efficiency: **rho=-0.0758, p=0.03913** (expected <0)
- Prespecified subgroups with both expected signs: **4/4**

### Subgroup correlations
| sample     |   n |     rho_ft |      p_ft |    rho_eff |     p_eff |
|:-----------|----:|-----------:|----------:|-----------:|----------:|
| FULL       | 741 | -0.0758896 | 0.0388941 | -0.0757974 | 0.0391325 |
| SYMBOL_SPY | 362 | -0.0946275 | 0.0721419 | -0.0646352 | 0.219898  |
| SYMBOL_IWM | 379 | -0.0726936 | 0.157836  | -0.090006  | 0.0801192 |
| YEAR_2009  | 386 | -0.0511199 | 0.316467  | -0.0533539 | 0.295754  |
| YEAR_2010  | 355 | -0.113988  | 0.0317839 | -0.0918402 | 0.0839966 |

## Negative vs positive modelled proxy states
| metric | Negative proxy | Positive proxy |
|---|---:|---:|
| n | 547 | 194 |
| continuation rate | 51.37% | 44.33% |
| mean gap-direction O/C follow-through | 0.03% | 0.01% |
| mean MFE | 1.10% | 0.81% |
| mean MAE | 1.21% | 0.95% |
| mean excursion efficiency | 47.28% | 45.19% |
| mean RTH range | 2.31% | 1.76% |

## Incremental predictive value
- Continuation Brier A (price/vol/liquidity): **0.254155**
- Continuation Brier B (+ modelled GEX): **0.252609**
- Relative Brier improvement: **0.61%**
- Follow-through MAE A: **1.14%**
- Follow-through MAE B: **1.14%**
- Relative follow-through MAE improvement: **0.15%**
- Excursion-efficiency MAE A: **0.263762**
- Excursion-efficiency MAE B: **0.264046**
- Relative efficiency-MAE improvement: **-0.11%**

### Robustness metrics
| sample     |   n |   brier_a |   brier_b |   brier_improvement_rel |   ft_mae_a |   ft_mae_b |   ft_mae_improvement_rel |   eff_mae_a |   eff_mae_b |   eff_mae_improvement_rel |   ft_pred_rho_a |   ft_pred_rho_b |   eff_pred_rho_a |   eff_pred_rho_b |
|:-----------|----:|----------:|----------:|------------------------:|-----------:|-----------:|-------------------------:|------------:|------------:|--------------------------:|----------------:|----------------:|-----------------:|-----------------:|
| FULL       | 741 |  0.254155 |  0.252609 |              0.0060835  | 0.0114416  | 0.011424   |               0.00153613 |    0.263762 |    0.264046 |              -0.00107611  |     -0.0132516  |      0.00177231 |       -0.0733127 |       -0.0534321 |
| SYMBOL_SPY | 362 |  0.253483 |  0.252183 |              0.00512888 | 0.00952232 | 0.00950738 |               0.00156911 |    0.255043 |    0.25552  |              -0.00186961  |     -0.00643073 |      0.0118351  |       -0.0767575 |       -0.0528038 |
| SYMBOL_IWM | 379 |  0.254797 |  0.253016 |              0.00699059 | 0.0132747  | 0.0132546  |               0.00151353 |    0.272091 |    0.27219  |              -0.000365695 |     -0.0193933  |     -0.00488645 |       -0.0724588 |       -0.0567713 |
| YEAR_2009  | 386 |  0.254689 |  0.253346 |              0.0052723  | 0.0127974  | 0.0127726  |               0.00194507 |    0.265128 |    0.265062 |               0.000249891 |     -0.0266069  |     -0.0088576  |       -0.074959  |       -0.0592794 |
| YEAR_2010  | 355 |  0.253575 |  0.251807 |              0.0069694  | 0.00996728 | 0.00995766 |               0.00096523 |    0.262277 |    0.262942 |              -0.00253358  |      0.0251463  |      0.0320109  |       -0.061902  |       -0.0394034 |

## Frozen gates
- Full-sample expected sign for both primary outcomes: **PASS**
- Expected sign in >=3/4 prespecified subgroups: **PASS**
- Continuation Brier improvement >=2%: **FAIL**
- Follow-through MAE improvement >=2%: **FAIL**
- Efficiency MAE not worse by >1%: **PASS**

## Overall frozen verdict
**MECHANISM-CONSISTENT / INCREMENTAL UTILITY NOT SUPPORTED**

## Interpretation constraint
This is an old-regime (2009-2010), daily-OHLC proxy study using an assumed dealer sign. Even a positive result cannot authorize an Investing OS scanner change. It can only justify replication with stronger participant/signed-flow data and modern intraday outcomes.
