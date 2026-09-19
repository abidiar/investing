# Near-Spot Unsigned Gamma Incremental Value v1.0 — Frozen Holdout Results

Generated: 2026-09-19T17:38:12+00:00

## Coverage
- Total matched Day-T observations: **2262**
- Instruments: **SPY, QQQ, IWM**
- Untouched holdout years: **2020, 2021, 2022**
- Median eligible contracts/session: **627**
- Monthly-OPEX-week observations: **527**
- Exclusions: {'SPY': {'no_price': 0, 'no_next_price': 0, 'no_gamma': 0, 'no_history': 0}, 'QQQ': {'no_price': 0, 'no_next_price': 0, 'no_gamma': 0, 'no_history': 0}, 'IWM': {'no_price': 0, 'no_next_price': 0, 'no_gamma': 0, 'no_history': 0}}

## Controlled HC3 gamma coefficients
| sample     | target             |    n |   gamma_coef |   hc3_p_value |      r2 |
|:-----------|:-------------------|-----:|-------------:|--------------:|--------:|
| POOLED     | next_rth_range     | 2262 |     -0.72230 |       0.00000 | 0.54021 |
| POOLED     | next_max_excursion | 2262 |     -0.74748 |       0.00000 | 0.44651 |
| NON_OPEX   | next_rth_range     | 1735 |     -0.88775 |       0.00000 | 0.53955 |
| NON_OPEX   | next_max_excursion | 1735 |     -0.89680 |       0.00000 | 0.44793 |
| SYMBOL_SPY | next_rth_range     |  755 |     -1.19109 |       0.00000 | 0.54293 |
| SYMBOL_SPY | next_max_excursion |  755 |     -1.15248 |       0.00007 | 0.45828 |
| SYMBOL_QQQ | next_rth_range     |  754 |     -0.56000 |       0.01512 | 0.47661 |
| SYMBOL_QQQ | next_max_excursion |  754 |     -0.53793 |       0.06115 | 0.36913 |
| SYMBOL_IWM | next_rth_range     |  753 |     -0.37354 |       0.03126 | 0.44462 |
| SYMBOL_IWM | next_max_excursion |  753 |     -0.47251 |       0.02478 | 0.34556 |
| YEAR_2020  | next_rth_range     |  756 |     -0.47685 |       0.02328 | 0.61394 |
| YEAR_2020  | next_max_excursion |  756 |     -0.52471 |       0.04153 | 0.51549 |
| YEAR_2021  | next_rth_range     |  753 |     -1.21022 |       0.00000 | 0.48679 |
| YEAR_2021  | next_max_excursion |  753 |     -1.30405 |       0.00000 | 0.41515 |
| YEAR_2022  | next_rth_range     |  753 |     -0.48995 |       0.01275 | 0.20340 |
| YEAR_2022  | next_max_excursion |  753 |     -0.42434 |       0.07820 | 0.13872 |

## Volatility-only residual associations
| sample   | target             |    n |   residual_rho |   residual_p_value |
|:---------|:-------------------|-----:|---------------:|-------------------:|
| POOLED   | next_rth_range     | 2262 |       -0.09038 |            0.00002 |
| POOLED   | next_max_excursion | 2262 |       -0.07235 |            0.00057 |
| NON_OPEX | next_rth_range     | 1735 |       -0.09959 |            0.00003 |
| NON_OPEX | next_max_excursion | 1735 |       -0.07717 |            0.00130 |

## Walk-forward incremental prediction
| target             |   n_test | baseline_mae   | extended_mae   |   mae_improvement_pct |
|:-------------------|---------:|:---------------|:---------------|----------------------:|
| next_rth_range     |     1761 | 0.581%         | 0.573%         |                  1.26 |
| next_max_excursion |     1761 | 0.542%         | 0.535%         |                  1.33 |
| next_abs_oc        |     1761 | 0.559%         | 0.556%         |                  0.64 |

## Frozen promotion gates
- Controlled pooled range coefficient negative, HC3 p<0.05: **PASS**
- Controlled range sign stable across all 3 instruments and >=2/3 years: **PASS**
- Controlled max-excursion + both primary residual tests negative/significant: **PASS**
- Non-OPEX controlled/residual direction preserved: **PASS**
- Walk-forward >=2% primary MAE improvement without >1% degradation of other primary: **FAIL**
- Overall frozen verdict: **CONDITIONAL ASSOCIATION / RESEARCH-ONLY**

No result has directional authority or permission to alter STRENGTH, RUNWAY, R:R, action state, option selection, or overnight carry.