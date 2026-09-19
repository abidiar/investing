# Investing OS Research — Modelled Dealer-GEX Gap Follow-Through v1.0

Status: **FROZEN BEFORE RESULTS**
Frozen: **2026-09-19**

Prior-work review: `research/prior_work/dealer_gex_amplification_damping_prior_work_2026-09-19.md`
Data/sign audit: `research/prior_work/dealer_gex_data_method_audit_2026-09-19.md`

## Purpose
Test a narrow incremental question that prior research has not answered for Investing OS:

> After price independently supplies an opening directional impulse, does a **MODELLED DEALER-GEX PROXY** improve prediction of same-session continuation vs reversal and excursion beyond price, volatility, and liquidity?

This is not a test of whether GEX creates bullish/bearish direction. Direction comes only from price.

## Critical measurement label
Dealer side is **not observed**. Public open interest does not identify dealer inventory.

The test uses the published call-minus-put structural proxy family used in prior academic work:
- calls treated as dealer long gamma;
- puts treated as dealer short gamma.

All results must be labelled **MODELLED DEALER-GEX PROXY**.

## Frozen untouched sample
- Instruments: **SPY, IWM**.
- Seed/model-development year: **2008**.
- Untouched holdout: **2009-2010**.
- QQQ excluded because source history begins in 2011.
- Options source: `anahatsingh-ui/options-dataset-hist`, preserved Dubach archive.
- Underlying source: matching `underlying_prices.parquet` OHLCV from the same archive.
- Day-T option snapshot may inform only Day-T+1.
- No 2011-2026 observation may enter the holdout verdict.

## Frozen option universe and GEX construction
Use every valid Day-T option row with:
- expiration after Day-T (`DTE >= 1`);
- finite vendor gamma > 0;
- non-missing open interest >= 0;
- valid call/put type.

No moneyness filter and no maximum DTE. This follows the whole-book proxy logic more closely than the prior unsigned near-spot-gamma tests.

For each contract:

`DOLLAR_GAMMA_1PCT = gamma * open_interest * 100 * spot^2 * 0.01`

Signed proxy:

`SIGNED_DGEX = sum(DOLLAR_GAMMA_1PCT for calls) - sum(DOLLAR_GAMMA_1PCT for puts)`

Gross magnitude for diagnostics only:

`GROSS_DGEX = sum(abs(DOLLAR_GAMMA_1PCT))`

Underlying liquidity:

`ADV20_DOLLAR = trailing mean over the prior 20 sessions of Close * Volume`, using only information known at Day-T close.

Primary GEX feature:

`SIGNED_GEX_TO_ADV = SIGNED_DGEX / ADV20_DOLLAR`

Interpretation: more negative values represent stronger modelled short-dealer-gamma pressure relative to underlying liquidity.

No alternate dealer-sign convention may be chosen after outcomes are viewed.

## Frozen price impulse / candidate rule
At Day-T+1 open:

`GAP = Open_(T+1) / Close_T - 1`

Candidate exists when:

`abs(GAP) >= 0.25%`

Direction is supplied only by the gap sign:
- gap > 0 = bullish impulse;
- gap < 0 = bearish impulse.

GEX may not create, reverse, or veto direction.

## Frozen outcomes
Let `DIR = sign(GAP)`.

Primary outcomes:
1. **FOLLOWTHROUGH_OC** = `DIR * (Close_(T+1)/Open_(T+1) - 1)`.
   - positive = session closes in gap direction;
   - negative = session reverses against gap direction.
2. **CONTINUED** = 1 if `FOLLOWTHROUGH_OC > 0`, else 0.
3. **EXCURSION_EFFICIENCY** = `MFE / (MFE + MAE)` when denominator > 0.

Open-centered excursions:
- bullish gap: `MFE = max(High/Open - 1, 0)`, `MAE = max(1 - Low/Open, 0)`;
- bearish gap: `MFE = max(1 - Low/Open, 0)`, `MAE = max(High/Open - 1, 0)`.

Secondary outcomes:
- MFE;
- MAE;
- RTH range `(High-Low)/Open`.

Daily OHLC cannot determine event ordering inside the session. Therefore no target-before-stop, stop-loss P&L, or exact intraday path claim is allowed.

## Frozen price/volatility/liquidity baseline
All Model-A features are known at Day-T+1 open:
- `abs_gap`;
- `gap_atr20` = abs(gap) / Day-T ATR20;
- `gap_up` indicator;
- Day-T absolute open-to-close return;
- Day-T RTH range;
- RV5;
- RV20;
- trailing-20 median RTH range;
- ATR20;
- Day-T range / trailing-20 median range;
- log(ADV20_DOLLAR);
- `prior_cc_aligned` = DIR * Day-T close-to-close return;
- `prior_oc_aligned` = DIR * Day-T open-to-close return.

Instrument dummy is included.

## Frozen models
Use expanding chronological walk-forward prediction.

Initial seed: all eligible 2008 candidates.
For each holdout date in 2009-2010, train only on prior candidates.
Training-only standardization.

### Binary continuation
- Logistic regression;
- L2 penalty;
- `C=1.0`;
- `solver=lbfgs`;
- no class weighting.

Model A: frozen price/volatility/liquidity baseline.
Model B: Model A + exactly `SIGNED_GEX_TO_ADV`.

### Continuous follow-through and excursion efficiency
- Ridge regression;
- `alpha=1.0`;
- no hyperparameter search.

Model A and Model B use the same feature split as above.

No feature selection, interactions, nonlinear transforms, threshold tuning, or model search after results.

## Frozen descriptive mechanism tests
On the untouched 2009-2010 holdout:
1. Spearman correlation of `SIGNED_GEX_TO_ADV` with `FOLLOWTHROUGH_OC`; expected sign **negative**.
2. Spearman correlation with `EXCURSION_EFFICIENCY`; expected sign **negative**.
3. Compare negative-proxy (`SIGNED_GEX_TO_ADV < 0`) vs positive-proxy sessions for:
   - continuation rate;
   - mean follow-through;
   - MFE;
   - MAE;
   - excursion efficiency.
4. Report the primary correlations separately for SPY, IWM, 2009, and 2010.

These descriptive tests do not substitute for incremental predictive value.

## Frozen primary incremental metrics
Across the untouched holdout:
1. CONTINUED Brier score: Model A vs B.
2. FOLLOWTHROUGH_OC MAE: Model A vs B.
3. EXCURSION_EFFICIENCY MAE: Model A vs B.
4. Prediction-vs-actual Spearman for each continuous target.
5. Same metrics by instrument and holdout year.

Relative improvement is `(A_error - B_error) / A_error`.

## Frozen success standard
The proxy is **SUPPORTED FOR FURTHER DEALER-DATA REPLICATION** only if all are true:
1. Full-holdout descriptive relation has the expected negative sign for both `FOLLOWTHROUGH_OC` and `EXCURSION_EFFICIENCY`.
2. The expected sign is preserved in **at least 3 of 4** prespecified subgroups: SPY, IWM, 2009, 2010.
3. Model B improves CONTINUED Brier score by **>=2.0%** versus Model A.
4. Model B improves FOLLOWTHROUGH_OC MAE by **>=2.0%**.
5. Model B does not worsen EXCURSION_EFFICIENCY MAE by more than **1.0%**.

If gates 1-2 pass but either gate 3 or 4 fails: verdict = **MECHANISM-CONSISTENT / INCREMENTAL UTILITY NOT SUPPORTED**.

If descriptive signs are unstable or opposite: verdict = **PROXY FAILED / NOT SUPPORTED**.

Even a full pass does **not** authorize scanner changes because dealer inventory is model-assumed. A pass only justifies a stronger replication using participant-class or signed-flow data.

## Robustness fixed before results
- Report negative vs positive proxy states without tuning a magnitude threshold.
- Report full sample and the four prespecified subgroups only.
- Gross unsigned gamma is diagnostic only and cannot replace signed proxy if signed results fail.
- No exclusion of crisis/high-volatility days after results.
- No OPEX exclusion unless reported descriptively; it cannot change the primary verdict.

## Do Not Change After Results
- 2008 seed / 2009-2010 holdout;
- SPY/IWM universe;
- abs(gap) >=0.25% candidate threshold;
- call-positive / put-negative sign convention;
- whole-book option universe;
- dollar-gamma formula;
- ADV20 normalization;
- baseline feature list;
- logistic/ridge specifications;
- outcomes;
- subgroup definitions;
- 2% / 2% / 1% promotion gates.

## Production implication ceiling
Maximum possible conclusion from this experiment:

> A published **modelled dealer-GEX proxy** adds enough incremental information to justify seeking stronger dealer-side data and testing the mechanism on actual Investing OS intraday scanner events.

It can never, by itself, change direction, STRENGTH, RUNWAY, R:R, BUY/WAIT, target sizing, options selection, or overnight carry.
