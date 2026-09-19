# Investing OS Research — Near-Spot Unsigned Gamma Incremental Value v1.0

Status: **FROZEN BEFORE RESULTS**
Frozen: 2026-09-19

## Purpose
Test the specific unresolved question from the multi-year compression study:

> After controlling for the market's already-observable volatility/range regime at Day-T close, does prior-day near-spot **unsigned** gamma concentration still add independent information about Day-T+1 regular-session compression?

This is not a directional test. Gamma cannot choose up/down, create BUY/SELL authority, or rescue the failed gap-continuation hypothesis.

## Untouched holdout sample
To avoid reusing the 2023–2025 discovery/replication panel for the verdict:
- Instruments: **SPY, QQQ, IWM**.
- Years: **2020, 2021, 2022** only.
- Options source: `anahatsingh-ui/options-dataset-hist`, yearly Parquet files.
- Underlying OHLC: independent daily bars.
- Day-T options snapshot predicts **Day T+1 only**.
- No 2023–2026 observations are allowed in the primary holdout verdict.

2020 is intentionally retained as a stress regime rather than excluded after seeing outcomes.

## Frozen options construction
Exactly preserve the prior unsigned-gamma construction:
- DTE: **1–30 calendar days**.
- Moneyness: strike within **±5.0%** of Day-T close.
- Open interest: non-missing and >= 0.
- Implied volatility: finite and **0.05–2.00** decimal.
- Calls and puts retained together.

Recompute theoretical gamma with `r=0`, `q=0`:

`T = DTE / 365`

`d1 = [ln(S/K) + 0.5*sigma^2*T] / [sigma*sqrt(T)]`

`gamma = phi(d1) / [S*sigma*sqrt(T)]`

`GAMMA_WEIGHT = gamma * open_interest`

Frozen gamma features:
1. `NEAR_GAMMA_SHARE_0_5`: share of total gamma weight within ±0.50% of spot.
2. `FRONT_NEAR_GAMMA_SHARE`: share of total gamma weight from 1–7 DTE contracts also within ±0.50% of spot.
3. `WEIGHTED_ABS_DISTANCE`: gamma-weighted mean absolute strike distance from spot.

## Frozen Day-T+1 outcomes
Primary:
1. `NEXT_RTH_RANGE = (High - Low) / Open`.
2. `NEXT_MAX_EXCURSION = max(High/Open - 1, Open/Low - 1)`.

Secondary:
3. `NEXT_ABS_OC = abs(Close/Open - 1)`.

Expected compression signs:
- near-gamma features: **negative** versus all outcomes.
- weighted absolute distance: **positive** versus all outcomes.

## Frozen richer volatility-only controls
All controls must be known by Day-T close:
- `DAY_ABS_OC`: abs(Day-T Close/Open - 1).
- `DAY_RANGE`: Day-T (High-Low)/Open.
- `RV5`: trailing 5-session close-to-close standard deviation.
- `RV20`: trailing 20-session close-to-close standard deviation.
- `MEDIAN20_RANGE`: trailing 20-session median RTH range.
- `ATR20`: trailing 20-session mean normalized true range, where normalized true range is `max(H-L, abs(H-prevClose), abs(L-prevClose))/prevClose`.
- `RANGE20_RATIO`: Day-T RTH range divided by trailing-20 median RTH range.

No next-day gap, next-day volatility, future VIX, or any Day-T+1 information may enter the baseline.

## Frozen tests
### Test A — Controlled regression
For each primary outcome, run OLS on **log(outcome)** using:
- the seven frozen volatility controls, log-transformed with a small fixed epsilon where required;
- categorical instrument fixed effects;
- categorical calendar-year fixed effects.

Then add `NEAR_GAMMA_SHARE_0_5` as the single primary gamma variable.
Use HC3 robust standard errors.

Primary controlled hypothesis: coefficient on `NEAR_GAMMA_SHARE_0_5` is **negative**.

Repeat the coefficient-sign check separately by instrument and separately by year using the same volatility controls but no redundant fixed effect for the split dimension.

### Test B — Residual association
Fit the volatility-only pooled regression above. Define:

`VOL_RESIDUAL = actual log(NEXT_RTH_RANGE) - volatility-only fitted log range`.

Test Spearman correlation between `NEAR_GAMMA_SHARE_0_5` and `VOL_RESIDUAL`.
Expected sign: **negative**.

Repeat for `NEXT_MAX_EXCURSION`.

### Test C — Walk-forward incremental prediction
Chronological pooled expanding-window OLS:
- minimum training rows: **500**;
- training-only standardization;
- volatility-only baseline = exactly the seven frozen controls plus instrument dummy variables;
- extended model adds exactly the three frozen gamma features;
- targets = `NEXT_RTH_RANGE`, `NEXT_MAX_EXCURSION`, `NEXT_ABS_OC`;
- no feature selection, threshold optimization, or hyperparameter tuning.

### Test D — Non-OPEX robustness
Repeat the pooled controlled primary coefficient and residual-direction tests excluding Day-T monthly-OPEX week observations.

## Frozen success standard
Gamma has **SUPPORTED ADDITIVE VALUE** only if all are true:
1. Pooled controlled coefficient for `NEAR_GAMMA_SHARE_0_5 -> log(NEXT_RTH_RANGE)` is negative with HC3 p < 0.05.
2. The controlled range coefficient is negative in **all 3 instruments** and in at least **2 of 3 years**.
3. Pooled controlled coefficient for `NEXT_MAX_EXCURSION` is negative, and the pooled volatility-residual Spearman relationship is negative with p < 0.05 for **both** primary outcomes.
4. Non-OPEX pooled controlled coefficients remain negative for both primary outcomes.
5. Walk-forward extended-model MAE improves by at least **2%** on either primary target without worsening the other primary target by more than **1%**.

If 1–4 pass but 5 fails: verdict = **CONDITIONAL ASSOCIATION / RESEARCH-ONLY**.

If the controlled relationship loses sign/stability after volatility controls: verdict = **MOSTLY VOLATILITY PROXY / NOT ADDITIVE**.

No result, including a full pass, independently creates direction, STRENGTH, RUNWAY, R:R, option-selection authority, or overnight-carry authority. A full pass could only justify later evaluation of a compact **EXPECTED RTH AMPLITUDE** context tag.

## Do Not Change After Results
- 2020–2022 holdout window
- SPY/QQQ/IWM universe
- 1–30 DTE
- ±5% moneyness
- ±0.50% near-gamma zone
- 1–7 DTE front bucket
- IV 0.05–2.00
- seven volatility controls
- outcome definitions
- HC3 controlled regression
- 500-row walk-forward start
- 2% / 1% predictive promotion gate
