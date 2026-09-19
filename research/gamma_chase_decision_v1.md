# Investing OS Research — Gamma Compression Chase Decision v1.0

Status: **FROZEN BEFORE RESULTS**
Frozen: 2026-09-19

## Purpose
Test the first decision-level question from the unsigned-gamma work:

> Can near-spot unsigned gamma improve a **CHASE vs WAIT** decision by identifying opening continuation attempts whose moderate same-direction target is unlikely to be reached because the session is in a compression environment?

This is a **veto-only context test**. Gamma cannot create direction, upgrade a setup, or turn WAIT into CHASE.

Because the historical Investing OS decision ledger does not contain a sufficiently large multi-year live sample, this is explicitly a **proxy decision study on SPY/QQQ/IWM opening-gap continuation attempts**, not a claim that the full scanner has been backtested.

## Frozen data split
- Instruments: **SPY, QQQ, IWM**.
- Model-development/training seed: **2014–2016**.
- Untouched decision holdout: **2017–2019**.
- Options source: `anahatsingh-ui/options-dataset-hist` yearly Parquet files.
- Underlying OHLC: independent daily bars.
- Day-T option snapshot may inform only Day-T+1.

No 2020–2026 data may enter the holdout verdict.

## Frozen options construction
Preserve the prior unsigned-gamma definition exactly:
- DTE **1–30 calendar days**.
- Strikes within **±5%** of Day-T close.
- OI non-missing and >=0.
- IV **0.05–2.00** decimal.
- Calls and puts pooled; no directional inference.
- Theoretical gamma recomputed with r=0, q=0.
- `GAMMA_WEIGHT = theoretical_gamma * open_interest`.

Gamma features:
1. `NEAR_GAMMA_SHARE_0_5`: share of gamma weight within ±0.50% of spot.
2. `FRONT_NEAR_GAMMA_SHARE`: 1–7 DTE gamma weight within ±0.50% of spot divided by total gamma weight.
3. `WEIGHTED_ABS_DISTANCE`: gamma-weighted mean absolute strike distance from spot.

## Frozen candidate / direction rule
At Day-T+1 open:
- `GAP = Open_(T+1) / Close_T - 1`.
- Candidate exists when **abs(GAP) >= 0.25%**.
- Direction is supplied only by gap sign: up-gap = bullish continuation attempt; down-gap = bearish continuation attempt.
- Gamma is not allowed to choose direction.

## Frozen target and outcome
This first decision test isolates **target feasibility**, not stop-ordering or full trade P&L.

- `T1_DISTANCE = 0.50 * MEDIAN20_RANGE`, where `MEDIAN20_RANGE` is the median Day-T RTH range over the prior 20 sessions and is known before Day-T+1.
- Same-direction MFE from Day-T+1 open:
  - gap up: `High/Open - 1`;
  - gap down: `Open/Low - 1`.
- `T1_HIT = 1` when same-direction MFE >= T1_DISTANCE.

Secondary descriptive target only:
- `T2_DISTANCE = 0.75 * MEDIAN20_RANGE`.
- `T2_HIT` uses the same-direction MFE definition.

Daily OHLC cannot establish whether a stop or target was hit first if both occurred. Therefore **no stop-loss P&L, realized R:R, or target-before-stop claim is allowed in this experiment**.

## Frozen price-only baseline
All baseline features are available at the Day-T+1 open:
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

## Frozen models
Use expanding chronological logistic regression with L2 penalty, `C=1.0`, `solver=lbfgs`, no class weighting.

Initial training set: all eligible 2014–2016 candidates.
For each holdout date in 2017–2019, train using only prior candidates, then predict that date.
Training-only standardization.

- **Model A — PRICE ONLY:** frozen baseline features + instrument dummies.
- **Model B — PRICE + GAMMA:** Model A plus exactly the three frozen gamma features.

No feature selection, interactions, threshold tuning, or hyperparameter search.

## Frozen decision rule
Probability threshold: **0.60**.

- Baseline `CHASE_A = 1` if Model A P(T1_HIT) >=0.60.
- Gamma overlay is **veto-only**:
  - `CHASE_B = 1` only when `CHASE_A=1` **and** Model B P(T1_HIT) >=0.60.
  - Model B may never convert a baseline WAIT into CHASE.
- `GAMMA_VETO = 1` when `CHASE_A=1` and Model B probability <0.60.

## Frozen primary decision metrics
Across 2017–2019 holdout:
1. Baseline CHASE count and T1 precision = T1 hit rate among `CHASE_A`.
2. Overlay CHASE count and T1 precision = T1 hit rate among `CHASE_B`.
3. Precision improvement in percentage points.
4. Veto count and T1 miss rate among vetoed events.
5. **Retained baseline winners** = overlay T1 hits / baseline T1 hits.
6. Brier score for Model A vs Model B over every holdout candidate.
7. Same metrics by instrument and by year.

Secondary descriptive metrics:
- T2 hit rate for baseline CHASE, overlay CHASE, and vetoed subset.
- mean same-direction MFE for each decision group.

## Frozen success standard
The veto overlay is **SUPPORTED FOR SHADOW CONTEXT TESTING** only if all are true:
1. Overlay T1 precision improves by **>=3.0 percentage points** versus baseline.
2. Vetoed-event T1 miss rate is at least **10 percentage points higher** than baseline CHASE miss rate.
3. Overlay retains **>=85%** of baseline T1 winners.
4. Model B improves holdout Brier score by **>=2%** versus Model A.
5. Overlay precision improvement is positive in **at least 2 of 3 instruments** and **at least 2 of 3 holdout years**.

If 1–3 and 5 pass but 4 fails: verdict = **DECISION UTILITY SIGNAL / RESEARCH-ONLY**.
If the precision/veto gates fail: verdict = **FAILED DECISION-LEVEL OVERLAY**.

Even a full pass only permits a future **GAMMA COMPRESSION / CHASE CAUTION** shadow tag. It does not alter STRENGTH, RUNWAY, direction, R:R, option selection, or production BUY/WAIT logic without a second test on actual Investing OS scanner events.

## Do Not Change After Results
- 2014–2016 seed / 2017–2019 holdout
- SPY/QQQ/IWM
- gap threshold 0.25%
- T1 = 0.50 × trailing-20 median RTH range
- T2 = 0.75 × trailing-20 median RTH range
- options construction and gamma features
- price-only feature list
- logistic model specification
- 0.60 decision threshold
- veto-only rule
- frozen success gates
