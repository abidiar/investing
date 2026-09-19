# QQQ Gap-Conditioned Gamma Continuation v1.0 — Frozen Results

Generated: 2026-09-19T17:10:01+00:00

## Coverage
- Qualifying abs(gap) >= 0.25% sessions: **119**
- First Day-T: **2026-01-21**; last Day-T: **2026-09-17**
- Monthly-OPEX-week qualifying sessions: **29**
- Day-T gamma predicts only Day-T+1; gap direction comes from Day-T+1 open.

## Primary correlations
| sample      | feature                | outcome              |   expected_sign |   n |     rho |   p_value |
|:------------|:-----------------------|:---------------------|----------------:|----:|--------:|----------:|
| FULL        | near_gamma_share_0_5   | gap_followthrough    |               1 | 119 |  0.2766 |    0.0023 |
| FULL        | near_gamma_share_0_5   | excursion_efficiency |               1 | 119 |  0.2862 |    0.0016 |
| FULL        | near_gamma_share_0_5   | mfe_from_open        |               1 | 119 |  0.1910 |    0.0374 |
| FULL        | near_gamma_share_0_5   | gap_retention_close  |               1 | 119 |  0.1425 |    0.1222 |
| FULL        | near_gamma_share_0_5   | mae_from_open        |              -1 | 119 | -0.3551 |    0.0001 |
| FULL        | near_gamma_share_0_5   | gap_fill             |              -1 | 119 | -0.1277 |    0.1662 |
| FULL        | front_near_gamma_share | gap_followthrough    |               1 | 119 |  0.2336 |    0.0106 |
| FULL        | front_near_gamma_share | excursion_efficiency |               1 | 119 |  0.2336 |    0.0106 |
| FULL        | front_near_gamma_share | mfe_from_open        |               1 | 119 |  0.1223 |    0.1851 |
| FULL        | front_near_gamma_share | gap_retention_close  |               1 | 119 |  0.0910 |    0.3247 |
| FULL        | front_near_gamma_share | mae_from_open        |              -1 | 119 | -0.3267 |    0.0003 |
| FULL        | front_near_gamma_share | gap_fill             |              -1 | 119 | -0.0974 |    0.2919 |
| FULL        | weighted_abs_distance  | gap_followthrough    |              -1 | 119 | -0.0499 |    0.5898 |
| FULL        | weighted_abs_distance  | excursion_efficiency |              -1 | 119 | -0.0090 |    0.9222 |
| FULL        | weighted_abs_distance  | mfe_from_open        |              -1 | 119 |  0.0570 |    0.5381 |
| FULL        | weighted_abs_distance  | gap_retention_close  |              -1 | 119 |  0.0528 |    0.5686 |
| FULL        | weighted_abs_distance  | mae_from_open        |               1 | 119 |  0.1104 |    0.2319 |
| FULL        | weighted_abs_distance  | gap_fill             |               1 | 119 | -0.0204 |    0.8259 |
| FIRST_HALF  | near_gamma_share_0_5   | gap_followthrough    |               1 |  59 |  0.3140 |    0.0154 |
| FIRST_HALF  | near_gamma_share_0_5   | excursion_efficiency |               1 |  59 |  0.2946 |    0.0235 |
| FIRST_HALF  | near_gamma_share_0_5   | mfe_from_open        |               1 |  59 |  0.2171 |    0.0987 |
| FIRST_HALF  | near_gamma_share_0_5   | gap_retention_close  |               1 |  59 |  0.2473 |    0.0590 |
| FIRST_HALF  | near_gamma_share_0_5   | mae_from_open        |              -1 |  59 | -0.3088 |    0.0173 |
| FIRST_HALF  | near_gamma_share_0_5   | gap_fill             |              -1 |  59 | -0.1763 |    0.1817 |
| FIRST_HALF  | front_near_gamma_share | gap_followthrough    |               1 |  59 |  0.3880 |    0.0024 |
| FIRST_HALF  | front_near_gamma_share | excursion_efficiency |               1 |  59 |  0.3709 |    0.0038 |
| FIRST_HALF  | front_near_gamma_share | mfe_from_open        |               1 |  59 |  0.2517 |    0.0544 |
| FIRST_HALF  | front_near_gamma_share | gap_retention_close  |               1 |  59 |  0.2456 |    0.0607 |
| FIRST_HALF  | front_near_gamma_share | mae_from_open        |              -1 |  59 | -0.4082 |    0.0013 |
| FIRST_HALF  | front_near_gamma_share | gap_fill             |              -1 |  59 | -0.1884 |    0.1529 |
| FIRST_HALF  | weighted_abs_distance  | gap_followthrough    |              -1 |  59 | -0.1191 |    0.3691 |
| FIRST_HALF  | weighted_abs_distance  | excursion_efficiency |              -1 |  59 |  0.0181 |    0.8917 |
| FIRST_HALF  | weighted_abs_distance  | mfe_from_open        |              -1 |  59 |  0.0916 |    0.4900 |
| FIRST_HALF  | weighted_abs_distance  | gap_retention_close  |              -1 |  59 | -0.0117 |    0.9296 |
| FIRST_HALF  | weighted_abs_distance  | mae_from_open        |               1 |  59 |  0.0790 |    0.5519 |
| FIRST_HALF  | weighted_abs_distance  | gap_fill             |               1 |  59 | -0.0263 |    0.8430 |
| SECOND_HALF | near_gamma_share_0_5   | gap_followthrough    |               1 |  60 |  0.2441 |    0.0602 |
| SECOND_HALF | near_gamma_share_0_5   | excursion_efficiency |               1 |  60 |  0.2282 |    0.0794 |
| SECOND_HALF | near_gamma_share_0_5   | mfe_from_open        |               1 |  60 |  0.1183 |    0.3680 |
| SECOND_HALF | near_gamma_share_0_5   | gap_retention_close  |               1 |  60 |  0.1019 |    0.4387 |
| SECOND_HALF | near_gamma_share_0_5   | mae_from_open        |              -1 |  60 | -0.3830 |    0.0025 |
| SECOND_HALF | near_gamma_share_0_5   | gap_fill             |              -1 |  60 | -0.0986 |    0.4536 |
| SECOND_HALF | front_near_gamma_share | gap_followthrough    |               1 |  60 |  0.0800 |    0.5436 |
| SECOND_HALF | front_near_gamma_share | excursion_efficiency |               1 |  60 |  0.0510 |    0.6987 |
| SECOND_HALF | front_near_gamma_share | mfe_from_open        |               1 |  60 | -0.0342 |    0.7951 |
| SECOND_HALF | front_near_gamma_share | gap_retention_close  |               1 |  60 | -0.0342 |    0.7955 |
| SECOND_HALF | front_near_gamma_share | mae_from_open        |              -1 |  60 | -0.2050 |    0.1161 |
| SECOND_HALF | front_near_gamma_share | gap_fill             |              -1 |  60 |  0.0010 |    0.9941 |
| SECOND_HALF | weighted_abs_distance  | gap_followthrough    |              -1 |  60 |  0.0649 |    0.6225 |
| SECOND_HALF | weighted_abs_distance  | excursion_efficiency |              -1 |  60 |  0.0488 |    0.7112 |
| SECOND_HALF | weighted_abs_distance  | mfe_from_open        |              -1 |  60 |  0.1210 |    0.3572 |
| SECOND_HALF | weighted_abs_distance  | gap_retention_close  |              -1 |  60 |  0.1109 |    0.3988 |
| SECOND_HALF | weighted_abs_distance  | mae_from_open        |               1 |  60 |  0.1111 |    0.3981 |
| SECOND_HALF | weighted_abs_distance  | gap_fill             |               1 |  60 | -0.0166 |    0.8999 |
| NON_OPEX    | near_gamma_share_0_5   | gap_followthrough    |               1 |  90 |  0.2357 |    0.0253 |
| NON_OPEX    | near_gamma_share_0_5   | excursion_efficiency |               1 |  90 |  0.3002 |    0.0040 |
| NON_OPEX    | near_gamma_share_0_5   | mfe_from_open        |               1 |  90 |  0.2404 |    0.0225 |
| NON_OPEX    | near_gamma_share_0_5   | gap_retention_close  |               1 |  90 |  0.1308 |    0.2192 |
| NON_OPEX    | near_gamma_share_0_5   | mae_from_open        |              -1 |  90 | -0.3480 |    0.0008 |
| NON_OPEX    | near_gamma_share_0_5   | gap_fill             |              -1 |  90 | -0.1586 |    0.1353 |
| NON_OPEX    | front_near_gamma_share | gap_followthrough    |               1 |  90 |  0.1957 |    0.0645 |
| NON_OPEX    | front_near_gamma_share | excursion_efficiency |               1 |  90 |  0.2566 |    0.0146 |
| NON_OPEX    | front_near_gamma_share | mfe_from_open        |               1 |  90 |  0.1702 |    0.1087 |
| NON_OPEX    | front_near_gamma_share | gap_retention_close  |               1 |  90 |  0.0812 |    0.4467 |
| NON_OPEX    | front_near_gamma_share | mae_from_open        |              -1 |  90 | -0.3477 |    0.0008 |
| NON_OPEX    | front_near_gamma_share | gap_fill             |              -1 |  90 | -0.1317 |    0.2160 |
| NON_OPEX    | weighted_abs_distance  | gap_followthrough    |              -1 |  90 | -0.0211 |    0.8432 |
| NON_OPEX    | weighted_abs_distance  | excursion_efficiency |              -1 |  90 | -0.0286 |    0.7891 |
| NON_OPEX    | weighted_abs_distance  | mfe_from_open        |              -1 |  90 |  0.0393 |    0.7132 |
| NON_OPEX    | weighted_abs_distance  | gap_retention_close  |              -1 |  90 |  0.0542 |    0.6120 |
| NON_OPEX    | weighted_abs_distance  | mae_from_open        |               1 |  90 |  0.1383 |    0.1937 |
| NON_OPEX    | weighted_abs_distance  | gap_fill             |               1 |  90 |  0.0561 |    0.5997 |

## Near-gamma median split — descriptive only
| bucket             |   n |   mean_near_share | continuation_rate   | avg_followthrough   | avg_mfe   | avg_mae   | avg_efficiency   | gap_fill_rate   | avg_retention   |
|:-------------------|----:|------------------:|:--------------------|:--------------------|:----------|:----------|:-----------------|:----------------|:----------------|
| ABOVE_MEDIAN       |  59 |            0.2505 | 61.02%              | 0.24%               | 0.80%     | 0.59%     | 55.86%           | 35.59%          | 1.06%           |
| AT_OR_BELOW_MEDIAN |  60 |            0.1610 | 36.67%              | -0.23%              | 0.60%     | 1.09%     | 37.87%           | 46.67%          | 0.72%           |

## Walk-forward incremental test
| target               |   n_test | baseline_mae   | extended_mae   |   mae_improvement_pct |
|:---------------------|---------:|:---------------|:---------------|----------------------:|
| gap_followthrough    |       59 | 0.67%          | 0.68%          |                 -1.08 |
| excursion_efficiency |       59 | 25.18%         | 24.82%         |                  1.44 |
| mae_from_open        |       59 | 0.53%          | 0.56%          |                 -5.16 |

## Mechanical promotion screen
- Stable full/half/non-OPEX primary relationship gate: **PASS**
  - near_gamma_share_0_5 -> gap_followthrough: rho=0.2766, p=0.0023
  - near_gamma_share_0_5 -> excursion_efficiency: rho=0.2862, p=0.0016
  - front_near_gamma_share -> gap_followthrough: rho=0.2336, p=0.0106
  - front_near_gamma_share -> excursion_efficiency: rho=0.2336, p=0.0106
- Failure-control directional-coherence gate: **PASS**
- Walk-forward >=2% core MAE and <=1% MAE-adverse degradation gate: **FAIL**
- Non-OPEX persistence gate: **PASS**
- Overall verdict: **RESEARCH-ONLY**

No result may alter STRENGTH, RUNWAY, R:R or action state unless the frozen promotion standard passes.