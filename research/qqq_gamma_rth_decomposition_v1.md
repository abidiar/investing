# Investing OS Research — QQQ Gamma Overnight vs RTH Decomposition v1.0

Status: **FROZEN BEFORE RESULTS**
Frozen: 2026-09-19

## Question
The prior gamma-concentration experiment found that near-spot gamma concentration was associated with a smaller next-session intraday high-low range, while not materially reducing absolute close-to-close movement. This follow-up asks whether that apparent damping is concentrated in the **regular trading session (RTH)** rather than the **overnight gap**.

This is a mechanism/decomposition test, not independent out-of-sample proof. It reuses the previously frozen QQQ gamma-concentration session panel but tests new, predeclared outcome decompositions that were not used for the prior promotion decision.

## Information hierarchy
1. Price remains primary. Price gets final vote.
2. Gamma structure is tested only as a behavior/path overlay.
3. No feature in this experiment may choose bullish vs bearish direction.
4. No result may add STRENGTH, RUNWAY, R:R, or create BUY/SELL/CALL/PUT/HOLD authority.

## Frozen input panel
Use `research/results/qqq_gamma_concentration_v1_session_panel.csv` exactly as previously generated.

Required fields:
- Day-T price context: `day_abs_oc`, `day_range`, `rv5`
- Gamma features: `near_gamma_share_0_5`, `front_near_gamma_share`, `weighted_abs_distance`, `strike_hhi`
- T+1 outcomes: `next_gap`, `next_oc`, `next_range`, `next_cc`

No gamma feature is re-estimated or threshold-optimized in this pass.

## Frozen derived outcomes
For each Day-T observation:
- `ABS_GAP = abs(next_gap)` = magnitude of prior-close -> T+1 open move.
- `ABS_RTH_OC = abs(next_oc)` = magnitude of T+1 open -> close move.
- `RTH_RANGE = next_range` = T+1 regular-session high-low range normalized by Day-T close.
- `ABS_CC = abs(next_cc)` = total close-to-close movement, retained for reference.
- `GAP_FOLLOWTHROUGH = sign(next_gap) * next_oc` when `next_gap != 0`. Positive = RTH continued the overnight gap direction; negative = RTH faded it.

## Frozen primary features and expected behavior
### Damping features
- `near_gamma_share_0_5`
- `front_near_gamma_share`

Expected:
- little or materially weaker relationship with `ABS_GAP`
- negative relationship with `ABS_RTH_OC`
- negative relationship with `RTH_RANGE`

### Expansion feature
- `weighted_abs_distance`

Expected:
- little or materially weaker relationship with `ABS_GAP`
- positive relationship with `ABS_RTH_OC`
- positive relationship with `RTH_RANGE`

`strike_hhi` is retained as a secondary structural control because it failed to add much in v1.0; it is not required for promotion.

## Primary hypotheses
### H1 — Near-spot gamma dampens RTH more than overnight movement
For each damping feature, compute Spearman correlations with `ABS_GAP`, `ABS_RTH_OC`, and `RTH_RANGE`.

Expected signs:
- `rho(feature, ABS_RTH_OC) < 0`
- `rho(feature, RTH_RANGE) < 0`

Frozen damping differential:
- `RTH_OC_DIFFERENTIAL = rho(ABS_GAP) - rho(ABS_RTH_OC)`
- `RANGE_DIFFERENTIAL = rho(ABS_GAP) - rho(RTH_RANGE)`

A positive differential means the feature is more damping-sensitive during RTH than overnight.

### H2 — Farther/diffuse gamma is more expansion-friendly during RTH
For `weighted_abs_distance`, expected signs are:
- `rho(ABS_RTH_OC) > 0`
- `rho(RTH_RANGE) > 0`

Frozen expansion differential:
- `RTH_OC_DIFFERENTIAL = rho(ABS_RTH_OC) - rho(ABS_GAP)`
- `RANGE_DIFFERENTIAL = rho(RTH_RANGE) - rho(ABS_GAP)`

### H3 — Stability
Report every primary correlation for:
- FULL sample
- FIRST_HALF chronologically
- SECOND_HALF chronologically

A proposed RTH behavior effect is considered unstable if its RTH correlation flips sign between chronological halves.

### H4 — Gap follow-through, secondary
On sessions with `abs(next_gap) >= 0.25%` (threshold frozen from existing meaningful-move research), test whether higher near-spot gamma concentration is associated with lower `GAP_FOLLOWTHROUGH`. This is secondary and cannot by itself trigger promotion.

## Descriptive splits
For readability only, split `near_gamma_share_0_5` at the eligible-sample median and report:
- average ABS_GAP
- average ABS_RTH_OC
- average RTH_RANGE
- average ABS_CC
- average GAP_FOLLOWTHROUGH

The median is not a scanner threshold.

## Incremental walk-forward test
Expanding one-step-ahead linear forecast, minimum training window **60 sessions**, no hyperparameter tuning.

Baseline features:
- `day_abs_oc`
- `day_range`
- `rv5`

Extended features add exactly:
- `near_gamma_share_0_5`
- `front_near_gamma_share`
- `weighted_abs_distance`

Targets tested separately:
- `ABS_GAP`
- `ABS_RTH_OC`
- `RTH_RANGE`

Compare MAE and prediction-vs-actual Spearman correlation.

## Promotion standard
A compact scanner context tag such as `RTH GAMMA STRUCTURE: DAMPING / EXPANSION-FRIENDLY / NEUTRAL` may advance from research-only only if ALL of the following hold:

1. At least one damping feature has the expected negative sign for `RTH_RANGE` or `ABS_RTH_OC` in FULL, FIRST_HALF, and SECOND_HALF, with full-sample p < 0.10; and
2. For that feature, the corresponding RTH-vs-gap differential is at least **+0.10** in the expected direction; and
3. The walk-forward extended model improves MAE by at least **2%** on `ABS_RTH_OC` or `RTH_RANGE`, while not worsening the other RTH target by more than **1%**; and
4. The RTH-target MAE improvement exceeds the ABS_GAP MAE improvement by at least **1 percentage point**, supporting an RTH-specific rather than generic-volatility interpretation.

If these conditions fail, the decomposition remains research-only.

Even if promoted, the tag remains contextual only and cannot independently alter direction, STRENGTH, RUNWAY, R:R, or action state.

## Do Not Re-Test Unless
- a materially larger/independent sample becomes available;
- intraday 0DTE/dealer-position data becomes available without lookahead;
- or the decomposition/model is changed and frozen before results.

## Results
PENDING — all rules above were frozen before calculation.
