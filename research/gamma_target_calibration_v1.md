# Investing OS Research — Gamma Target Calibration v1.0

Status: **FROZEN BEFORE RESULTS**
Frozen: 2026-09-19

## Purpose
Test the next decision-level question from the unsigned-gamma work:

> After an entry already exists for independent price reasons, can near-spot unsigned gamma improve **target sizing** without changing direction or denying the trade?

This is a **target-only** experiment. Gamma has zero entry/veto authority, cannot choose direction, cannot add STRENGTH/RUNWAY, and cannot manufacture R:R.

Because the historical Investing OS decision ledger does not contain a sufficiently large multi-year live sample, this is explicitly a **proxy decision study on SPY/QQQ/IWM opening-gap continuation candidates**, not a backtest of the full scanner.

## Untouched data split
- Instruments: **SPY, QQQ, IWM**.
- Training seed: **calendar 2011**.
- Untouched decision holdout: **calendar 2012–2013**.
- These years have not been used in any prior Investing OS gamma verdict.
- Options source: `anahatsingh-ui/options-dataset-hist` yearly Parquet files.
- Underlying OHLC: independent daily bars.
- Day-T options snapshot may inform only Day-T+1.

QQQ option history in this source begins in 2011, so 2011 is the common-universe seed year. No 2014–2026 observations may enter the holdout verdict.

## Frozen options construction
Preserve the prior unsigned-gamma definition exactly:
- DTE **1–30 calendar days**.
- Strikes within **±5%** of Day-T close.
- OI non-missing and >=0.
- IV **0.05–2.00** decimal.
- Calls and puts pooled; no directional inference.
- Theoretical gamma recomputed with `r=0`, `q=0`.
- `GAMMA_WEIGHT = theoretical_gamma * open_interest`.

Gamma features:
1. `NEAR_GAMMA_SHARE_0_5`: share of total gamma weight within ±0.50% of spot.
2. `FRONT_NEAR_GAMMA_SHARE`: 1–7 DTE gamma weight within ±0.50% of spot divided by total gamma weight.
3. `WEIGHTED_ABS_DISTANCE`: gamma-weighted mean absolute strike distance from spot.

## Frozen entry / direction rule
At Day-T+1 open:
- `GAP = Open_(T+1) / Close_T - 1`.
- Candidate exists when **abs(GAP) >= 0.25%**.
- Direction comes only from gap sign: up-gap = bullish continuation candidate; down-gap = bearish continuation candidate.
- Every qualifying candidate is retained in both A and B. **Neither model may veto an entry.**

## Frozen price-only features
All are known at the Day-T+1 open:
- absolute gap size;
- gap size / Day-T ATR20;
- gap-up indicator;
- Day-T absolute open-to-close return;
- Day-T RTH range;
- RV5;
- RV20;
- trailing-20 median RTH range;
- ATR20;
- Day-T range / trailing-20 median range.

Instrument dummies are included. No future information is allowed.

## Frozen target ladder
Targets are defined from the Day-T trailing-20 median RTH range, known before the Day-T+1 session:
- **T1 = 0.50 × MEDIAN20_RANGE**
- **T2 = 0.75 × MEDIAN20_RANGE**
- **T3 = 1.00 × MEDIAN20_RANGE**

Same-direction MFE from the Day-T+1 open:
- gap up: `High/Open - 1`;
- gap down: `Open/Low - 1`.

`HIT_K = 1` when same-direction MFE >= target distance K.

Daily OHLC cannot establish stop-before-target ordering. Therefore this experiment makes **no stop-loss P&L, realized R:R, or target-before-stop claim**.

## Frozen models
For each target K separately, use expanding chronological logistic regression:
- L2 penalty;
- `C=1.0`;
- `solver=lbfgs`;
- no class weighting;
- training-only standardization;
- no feature selection, interactions, threshold tuning, or hyperparameter search.

Initial seed is all eligible 2011 candidates. For each holdout date in 2012–2013, train only on prior candidates.

- **Model A — PRICE ONLY:** frozen price features + instrument dummies.
- **Model B — PRICE + GAMMA:** Model A plus exactly the three frozen gamma features.

## Frozen target-selection rule
For each candidate and each model:
1. Compute predicted probability of hitting T1, T2, and T3.
2. Use a fixed probability requirement of **0.60**.
3. Select the **largest** target whose predicted hit probability is >=0.60.
4. If none of T1/T2/T3 clears 0.60, force **T1** rather than denying the trade.

Therefore every candidate receives one target under A and one target under B. Gamma can only change target ambition.

## Frozen utility metrics
For model M on event i:
- `TARGET_M` = selected target distance as a return fraction.
- `HIT_M = 1` if same-direction MFE >= TARGET_M.
- `CAPTURE_M = TARGET_M * HIT_M`.

Primary decision utility:
1. Mean `CAPTURE_B` versus mean `CAPTURE_A`.
2. Relative capture improvement: `(mean(CAPTURE_B)/mean(CAPTURE_A) - 1)`.
3. Paired bootstrap 95% CI for `mean(CAPTURE_B - CAPTURE_A)` using **10,000** resamples and RNG seed **0**.

Guardrail metrics:
4. Target hit rate A vs B.
5. Mean selected target multiple (0.50/0.75/1.00) A vs B.
6. Fraction selecting T1/T2/T3 under each model.
7. Upgrade/downgrade/unchanged target counts.
8. Mean same-direction MFE of upgraded, downgraded, and unchanged subsets.
9. Captured-MFE ratio = `CAPTURE / max(MFE, 1e-9)`, clipped to [0,1], averaged across events.
10. Same metrics by instrument and by holdout year.

Probability-quality diagnostic:
- Compute Brier score for A and B for each of T1/T2/T3 over all holdout candidates; report average relative Brier improvement. This is descriptive and not by itself a promotion gate.

## Frozen success standard
The target overlay is **SUPPORTED FOR SHADOW TARGET CONTEXT TESTING** only if all are true:
1. Mean capture improves by **>=3.0% relative** versus price-only.
2. Paired-bootstrap 95% CI for mean capture difference has lower bound **>0**.
3. Target hit rate worsens by **no more than 2.0 percentage points**.
4. Mean selected target multiple under B is at least **95%** of A (prevents winning by simply shrinking targets).
5. Capture improvement is positive in **at least 2 of 3 instruments** and in **both 2012 and 2013**.

If gates 1, 3, 4, and 5 pass but the bootstrap CI includes zero: verdict = **DECISION UTILITY SIGNAL / RESEARCH-ONLY**.

Otherwise: verdict = **FAILED DECISION-LEVEL TARGET OVERLAY**.

Even a full pass permits only a future **GAMMA TARGET-COMPRESSION / TARGET-AMBITION** shadow context. It does not authorize changes to direction, entry, STRENGTH, RUNWAY, option selection, or overnight carry, and it does not automatically change production targets until tested on actual Investing OS scanner events.

## Do Not Change After Results
- 2011 seed / 2012–2013 holdout
- SPY/QQQ/IWM universe
- gap threshold 0.25%
- unsigned-gamma construction
- price feature list
- target ladder 0.50/0.75/1.00 × median20 range
- logistic model specification
- 0.60 probability threshold
- forced-T1 floor when no target qualifies
- capture definition
- 10,000 bootstrap resamples, seed 0
- 3% / 2pp / 95% / cross-instrument-year success gates
