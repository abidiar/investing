# Gamma Compression Chase Decision v1.0 — Frozen Results

Generated: 2026-09-19T17:51:58+00:00

## Coverage
- Total candidate panel rows (2014–2019): **2381**
- Untouched holdout candidate rows (2017–2019): **1195**
- Training seed candidates (2014–2016): **1186**
- Holdout T1 base hit rate: **44.02%**
- Median eligible option contracts/candidate: **242**
- Exclusions: {'SPY': {'no_price': 0, 'no_next_price': 0, 'no_history': 0, 'no_gamma': 0, 'small_gap': 797}, 'QQQ': {'no_price': 0, 'no_next_price': 0, 'no_history': 0, 'no_gamma': 0, 'small_gap': 648}, 'IWM': {'no_price': 0, 'no_next_price': 0, 'no_history': 0, 'no_gamma': 0, 'small_gap': 695}}

## Decision metrics
| sample     |   n_candidates |   baseline_chases |   overlay_chases |   vetoes | baseline_t1_precision   | overlay_t1_precision   |   precision_improvement_pp | baseline_miss_rate   | veto_miss_rate   |   veto_miss_minus_baseline_pp | retained_baseline_winners   | baseline_t2_hit_rate   | overlay_t2_hit_rate   | veto_t2_hit_rate   | baseline_mean_mfe   | overlay_mean_mfe   | veto_mean_mfe   |
|:-----------|---------------:|------------------:|-----------------:|---------:|:------------------------|:-----------------------|---------------------------:|:---------------------|:-----------------|------------------------------:|:----------------------------|:-----------------------|:----------------------|:-------------------|:--------------------|:-------------------|:----------------|
| FULL       |           1195 |                98 |               73 |       25 | 69.39%                  | 73.97%                 |                       4.58 | 30.61%               | 44.00%           |                         13.39 | 79.41%                      | 65.31%                 | 68.49%                | 56.00%             | 0.96%               | 1.04%              | 0.75%           |
| SYMBOL_SPY |            357 |                33 |               28 |        5 | 63.64%                  | 71.43%                 |                       7.79 | 36.36%               | 80.00%           |                         43.64 | 95.24%                      | 60.61%                 | 67.86%                | 20.00%             | 0.89%               | 0.98%              | 0.39%           |
| SYMBOL_QQQ |            449 |                33 |               25 |        8 | 75.76%                  | 80.00%                 |                       4.24 | 24.24%               | 37.50%           |                         13.26 | 80.00%                      | 72.73%                 | 76.00%                | 62.50%             | 1.04%               | 1.08%              | 0.90%           |
| SYMBOL_IWM |            389 |                32 |               20 |       12 | 68.75%                  | 70.00%                 |                       1.25 | 31.25%               | 33.33%           |                          2.08 | 63.64%                      | 62.50%                 | 60.00%                | 66.67%             | 0.96%               | 1.06%              | 0.79%           |
| YEAR_2017  |            306 |                34 |               21 |       13 | 47.06%                  | 47.62%                 |                       0.56 | 52.94%               | 53.85%           |                          0.90 | 62.50%                      | 47.06%                 | 47.62%                | 46.15%             | 0.51%               | 0.49%              | 0.54%           |
| YEAR_2018  |            447 |                27 |               17 |       10 | 77.78%                  | 88.24%                 |                      10.46 | 22.22%               | 40.00%           |                         17.78 | 71.43%                      | 70.37%                 | 76.47%                | 60.00%             | 1.26%               | 1.48%              | 0.89%           |
| YEAR_2019  |            442 |                37 |               35 |        2 | 83.78%                  | 82.86%                 |                      -0.93 | 16.22%               | 0.00%            |                        -16.22 | 93.55%                      | 78.38%                 | 77.14%                | 100.00%            | 1.16%               | 1.15%              | 1.36%           |

## Probability calibration
- Price-only Brier score: **0.23792**
- Price+gamma Brier score: **0.23701**
- Brier improvement: **0.38%**

## Frozen decision gates
- Overlay precision improvement >=3.0pp: **PASS**
- Veto miss-rate lift >=10.0pp vs baseline miss rate: **PASS**
- Retain >=85% of baseline T1 winners: **FAIL**
- Brier improvement >=2%: **FAIL**
- Positive precision improvement in >=2/3 instruments and >=2/3 years: **PASS**
- Overall frozen verdict: **FAILED DECISION-LEVEL OVERLAY**

## Interpretation constraint
This is a proxy opening-gap chase/target-feasibility study, not a backtest of the full Investing OS scanner. Daily OHLC cannot determine target-before-stop ordering. No result changes production STRENGTH, RUNWAY, direction, R:R, option selection, or BUY/WAIT logic automatically.