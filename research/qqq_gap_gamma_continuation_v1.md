# Investing OS Research — QQQ Gap-Conditioned Gamma Continuation v1.0

Status: **FROZEN BEFORE RESULTS**
Frozen: 2026-09-19

## Question
When QQQ opens with a meaningful overnight gap, does the prior session's near-spot gamma concentration improve our ability to distinguish a clean same-direction continuation from a failed-gap reversal?

This experiment follows the prior gamma path-efficiency work. The gap supplies direction; gamma is permitted only to describe the expected *quality/path* of the next regular session. Gamma may not independently choose bullish or bearish direction.

## Data discipline
- Instrument: QQQ.
- Gamma features come from the already-frozen `qqq_gamma_concentration_v1_session_panel.csv`.
- Day-T gamma features may predict only Day T+1.
- Day T+1 direction anchor is the overnight gap from Day-T close to Day-T+1 open.
- Qualifying gap is frozen at **absolute gap >= 0.25%**, unchanged from the prior secondary test.
- No same-day use of settled OI.
- Unsigned theoretical gamma concentration is not dealer GEX and has no independent directional authority.

## Frozen gamma features
Primary:
1. `near_gamma_share_0_5`
2. `front_near_gamma_share`

Opposite-structure robustness:
3. `weighted_abs_distance`

Expected interpretation, frozen in advance:
- Higher near-spot gamma: cleaner / more orderly follow-through in an already-established gap direction.
- Higher weighted distance: weaker / less orderly follow-through.

## Frozen Day-T+1 gap direction
`GAP = Open_T+1 / Close_T - 1`

`GAP_SIGN = sign(GAP)`

Only sessions with `abs(GAP) >= 0.0025` are eligible.

## Frozen outcomes
All returns are expressed positively when favorable to the overnight-gap direction.

### 1. GAP_FOLLOWTHROUGH
`GAP_SIGN * (Close_T+1 / Open_T+1 - 1)`

Positive means RTH continued in the gap direction; negative means RTH reversed against it.

### 2. GAP_DIRECTION_SUCCESS
Binary: `GAP_FOLLOWTHROUGH > 0`.

### 3. MFE_FROM_OPEN
Maximum favorable excursion from the T+1 open in the gap direction:
- gap up: `High/Open - 1`
- gap down: `Open/Low - 1`

### 4. MAE_FROM_OPEN
Maximum adverse excursion from the T+1 open against the gap direction:
- gap up: `Open/Low - 1`
- gap down: `High/Open - 1`

### 5. EXCURSION_EFFICIENCY
`MFE / (MFE + MAE)` when denominator > 0.

Higher means the session's available excursion was more favorable than adverse relative to the gap direction.

### 6. GAP_FILL
Binary indicator that price touched the prior close intraday:
- gap up: `Low <= prior close`
- gap down: `High >= prior close`

A lower gap-fill rate is consistent with stronger gap retention.

### 7. GAP_RETENTION_CLOSE
`GAP_SIGN * (Close_T+1 / Close_T - 1)`

Positive means the close remained on the original gap side of the prior close; larger positive values indicate greater retained displacement.

## Primary hypotheses
### H1 — Near gamma improves directional follow-through quality
`near_gamma_share_0_5` and `front_near_gamma_share` should have positive association with:
- GAP_FOLLOWTHROUGH
- EXCURSION_EFFICIENCY
- MFE_FROM_OPEN
- GAP_RETENTION_CLOSE

### H2 — Near gamma reduces failed-gap behavior
The same features should have negative association with:
- MAE_FROM_OPEN
- GAP_FILL

### H3 — Farther/diffuse gamma should show the opposite tendency
`weighted_abs_distance` should show the opposite signs from H1/H2.

## Stability checks
For each primary feature/outcome association report:
- full eligible sample
- chronological first half
- chronological second half

A relationship that flips sign between halves fails stability even if the full-sample p-value is attractive.

## Descriptive split
Report above/below the full eligible-sample median of `near_gamma_share_0_5` for readability only. This median is **not** a scanner threshold and may not be promoted from this pass.

Report at least:
- continuation rate
- average GAP_FOLLOWTHROUGH
- average MFE
- average MAE
- average EXCURSION_EFFICIENCY
- gap-fill rate
- average GAP_RETENTION_CLOSE

## Incremental price-baseline test
Walk-forward one-step-ahead regression, minimum 60 eligible gap sessions.

Baseline features available before T+1 RTH:
- absolute overnight gap
- Day-T absolute open-to-close return
- Day-T range
- Day-T trailing 5-session realized volatility

Extended model adds exactly:
- near_gamma_share_0_5
- front_near_gamma_share
- weighted_abs_distance

Targets tested separately:
- GAP_FOLLOWTHROUGH
- EXCURSION_EFFICIENCY
- MAE_FROM_OPEN

No hyperparameter tuning and no feature selection after results.

## Promotion standard
This gap-conditioned gamma idea may advance from research-only to a compact scanner context tag only if all are true:

1. At least one near-gamma primary relationship has the expected sign in the full sample **and both chronological halves**, with full-sample p < 0.10 on GAP_FOLLOWTHROUGH or EXCURSION_EFFICIENCY; and
2. Near gamma is directionally coherent on at least one failure-control outcome (MAE_FROM_OPEN or GAP_FILL); and
3. The extended walk-forward model improves MAE by at least **2%** on GAP_FOLLOWTHROUGH or EXCURSION_EFFICIENCY while not worsening MAE_FROM_OPEN by more than **1%**; and
4. The effect is not created solely by monthly/quarterly OPEX sessions.

If these are not all met, verdict remains RESEARCH-ONLY.

Even if promoted, maximum scanner authority is a contextual tag such as:
- `GAP PATH: ORDERLY / MIXED / FAILURE-RISK`
- `GAP-GAMMA SUPPORT: YES / NO`

It may not add STRENGTH, RUNWAY, R:R, create BUY/SELL/CALL/PUT authority, or override price confirmation, event risk, extension, or the triple-witching/rebalance gate.

## OPEX check
Report qualifying gap outcomes separately for monthly-OPEX-week vs ordinary sessions. This is descriptive only; no optimization/filtering.

## Do Not Re-Test Unless
- a materially larger or independent options-chain sample becomes available;
- intraday signed dealer positioning becomes available without lookahead;
- a new gap threshold is frozen in a separate experiment before outcomes are inspected; or
- the data-generation methodology materially changes.

## Results
PENDING — rules above were frozen before outcome calculation.
