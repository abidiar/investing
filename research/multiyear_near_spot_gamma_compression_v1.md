# Investing OS Research — Multi-Year Near-Spot Unsigned Gamma Compression v1.0

Status: **FROZEN BEFORE RESULTS**
Frozen: 2026-09-19

## Purpose
Test the narrower hypothesis that high prior-day near-spot **unsigned** gamma concentration compresses the following regular-session excursion/range **regardless of market direction**.

This is deliberately different from the failed gap-continuation hypothesis. We are not asking whether gamma predicts up/down or whether a gap continues. We are asking only whether market path amplitude is smaller when unsigned theoretical gamma is more concentrated close to spot.

## Independent sample
- Instruments: **SPY, QQQ, IWM**.
- Years: **2023, 2024, 2025**.
- Options source: `anahatsingh-ui/options-dataset-hist`, yearly parquet files for each ETF.
- Underlying OHLC: independent daily bars for each ETF.
- Day-T options snapshot may predict **Day T+1 only**.
- No 2026 observations are allowed.

## Frozen contract universe
For each Day-T ETF chain:
- DTE: **1–30 calendar days**.
- Moneyness: strike within **±5.0%** of Day-T close.
- Open interest: non-missing and >= 0.
- Implied volatility: finite and **0.05 to 2.00** decimal.
- Calls and puts retained together; no directional inference from option type.

## Frozen theoretical unsigned gamma
Recompute theoretical gamma rather than using vendor gamma:

`T = DTE / 365`

`d1 = [ln(S/K) + 0.5*sigma^2*T] / [sigma*sqrt(T)]`

`gamma = phi(d1) / [S*sigma*sqrt(T)]`

with `r = 0`, `q = 0`.

`GAMMA_WEIGHT = gamma * open_interest`

This is **unsigned** concentration only. It is not signed dealer GEX and has no directional authority.

## Frozen Day-T features
1. `NEAR_GAMMA_SHARE_0_5` = share of total gamma weight within **±0.50%** of Day-T close.
2. `FRONT_NEAR_GAMMA_SHARE` = share of total gamma weight from **1–7 DTE** contracts also within ±0.50% of spot.
3. `WEIGHTED_ABS_DISTANCE` = gamma-weighted mean absolute strike distance from spot.

## Frozen Day-T+1 outcomes
Primary:
1. `NEXT_RTH_RANGE = (High - Low) / Open`.
2. `NEXT_MAX_EXCURSION = max(High/Open - 1, Open/Low - 1)`.

Secondary:
3. `NEXT_ABS_OC = abs(Close/Open - 1)`.
4. `NEXT_RANGE_VS_20D = NEXT_RTH_RANGE / median(prior 20 sessions' RTH range)` using information available before Day T+1.

The hypothesis is **compression**, so expected signs are:
- `NEAR_GAMMA_SHARE_0_5` vs all outcomes: negative.
- `FRONT_NEAR_GAMMA_SHARE` vs all outcomes: negative.
- `WEIGHTED_ABS_DISTANCE` vs all outcomes: positive.

## Frozen baseline controls
Price-only baseline features available at Day-T close:
- Day-T absolute open-to-close return.
- Day-T RTH high-low range / open.
- trailing 5-session realized close-to-close volatility.
- trailing 20-session median RTH range.

Extended model adds exactly:
- `NEAR_GAMMA_SHARE_0_5`
- `FRONT_NEAR_GAMMA_SHARE`
- `WEIGHTED_ABS_DISTANCE`

## Frozen tests
Report Spearman relationships for:
- pooled full sample
- each instrument separately
- each calendar year separately
- non-OPEX sessions

Also report a descriptive median split within **each instrument-year** so that a pooled result is not driven by scale differences between ETFs or years.

For pooled descriptive comparison, define HIGH vs LOW gamma using each instrument-year's own median near-gamma share, then combine the buckets.

## Frozen walk-forward test
Use chronological expanding-window OLS on the pooled panel:
- minimum training rows: **500**
- training-only standardization
- fixed price-only baseline above
- extended model adds the three frozen gamma features
- targets: `NEXT_RTH_RANGE`, `NEXT_MAX_EXCURSION`, `NEXT_ABS_OC`
- no hyperparameter tuning or feature selection

## Frozen promotion standard
The compression hypothesis is **SUPPORTED** only if all are true:

1. Full pooled `NEAR_GAMMA_SHARE_0_5 -> NEXT_RTH_RANGE` rho is negative with p < 0.05.
2. The same relationship is negative in **all three instruments** and in at least **2 of 3 calendar years**.
3. `NEAR_GAMMA_SHARE_0_5 -> NEXT_MAX_EXCURSION` is negative in the full pooled sample and in at least 2 of 3 instruments.
4. Non-OPEX sessions preserve the negative full-sample relationship for both primary outcomes.
5. The extended walk-forward model improves MAE by at least **2%** on either primary target without worsening the other primary target by more than **1%**.

If 1–4 pass but 5 fails: verdict = **REPLICATED ASSOCIATION / RESEARCH-ONLY**.
If stability across instruments/years fails: verdict = **FAILED GENERAL COMPRESSION HYPOTHESIS**.

No successful result automatically changes STRENGTH, RUNWAY, R:R, BUY/WAIT, option selection, or overnight carry. At most it may later justify a context tag describing expected path amplitude.

## Do Not Change After Results
- 2023–2025 sample
- SPY/QQQ/IWM universe
- 1–30 DTE
- ±5% moneyness
- ±0.50% near-gamma zone
- 1–7 DTE front bucket
- IV 0.05–2.00
- outcome definitions
- baseline features
- promotion gates
