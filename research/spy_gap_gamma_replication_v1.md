# Investing OS Research — SPY Gap-Conditioned Gamma Independent Replication v1.0

Status: **FROZEN BEFORE RESULTS**
Frozen: 2026-09-19

## Purpose
Replicate the previously observed QQQ gap-conditioned gamma relationship on an independent instrument and non-overlapping time period, without changing thresholds after seeing results.

Prior finding being replicated: when the next session opens with an absolute overnight gap >= 0.25%, higher prior-day near-spot unsigned gamma concentration was associated with better same-direction RTH follow-through, better excursion efficiency, and less adverse excursion. The prior QQQ result remains research-only because its walk-forward incremental prediction gate failed.

## Independent replication sample
- Instrument: **SPY**.
- Time period: **calendar year 2025 only**.
- This is non-overlapping in time with the 2026 QQQ discovery sample and uses a different underlying.
- Options source: `anahatsingh-ui/options-dataset-hist`, file `spy/options_2025.parquet`.
- Underlying OHLC source: independent SPY daily bars.
- Day-T options snapshot may predict **Day T+1 only**.
- No 2026 observations are allowed in this replication.

## Frozen contract universe
Exactly preserve the prior gamma-concentration construction:
- DTE: **1–30 calendar days**.
- Moneyness: strike within **±5.0%** of Day-T SPY close.
- Open interest: non-missing and >= 0.
- Implied volatility: finite and **0.05 to 2.00** decimal.
- Calls and puts retained together; no directional inference from option type.

## Frozen theoretical gamma
To preserve methodology across data sources, do **not** use the dataset's supplied gamma field as the primary weight. Recompute theoretical unsigned gamma with the same frozen formula used in QQQ v1:

`T = DTE / 365`

`d1 = [ln(S/K) + 0.5*sigma^2*T] / [sigma*sqrt(T)]`

`gamma = phi(d1) / [S*sigma*sqrt(T)]`

with `r = 0` and `q = 0`.

`GAMMA_WEIGHT = gamma * open_interest`

This is unsigned theoretical gamma concentration, **not signed dealer GEX**.

## Frozen session features
Computed on Day T:
1. `NEAR_GAMMA_SHARE_0_5` = share of total gamma weight within ±0.50% of SPY close.
2. `FRONT_NEAR_GAMMA_SHARE` = share of total gamma weight from 1–7 DTE contracts also within ±0.50% of spot.
3. `WEIGHTED_ABS_DISTANCE` = gamma-weighted mean absolute strike distance from spot.

No thresholds or feature definitions may change after results.

## Frozen gap eligibility
On Day T+1:
- `GAP = Open_(T+1) / Close_T - 1`.
- Qualifying session requires **abs(GAP) >= 0.25%**.
- Gap direction is supplied only by the observed Day-T+1 open; gamma cannot choose direction.

## Frozen outcomes
Let `sign = +1` for gap-up and `-1` for gap-down.

Primary:
- `GAP_FOLLOWTHROUGH = sign * (Close/Open - 1)` on T+1.
- `EXCURSION_EFFICIENCY = MFE / (MFE + MAE)` from the T+1 open in gap direction.

Failure-control outcomes:
- `MFE_FROM_OPEN` in gap direction.
- `MAE_FROM_OPEN` against gap direction.
- `GAP_FILL` = whether T+1 trades back to or through Day-T close.
- `GAP_RETENTION_CLOSE = sign * (Close_(T+1)/Close_T - 1)`.

## Frozen price-only baseline
Exactly preserve the prior walk-forward baseline:
- absolute gap size
- Day-T absolute open-to-close return
- Day-T high-low range / prior close
- trailing 5-session realized close-to-close volatility

Extended model adds exactly:
- `NEAR_GAMMA_SHARE_0_5`
- `FRONT_NEAR_GAMMA_SHARE`
- `WEIGHTED_ABS_DISTANCE`

Walk-forward OLS:
- minimum training window **60 qualifying gap sessions**
- expanding training window
- training-only standardization
- no hyperparameter tuning or feature selection

Targets:
- gap follow-through
- excursion efficiency
- adverse excursion from open

## Frozen hypotheses
H1: higher `NEAR_GAMMA_SHARE_0_5` is associated with **greater** same-direction gap follow-through.

H2: higher `NEAR_GAMMA_SHARE_0_5` is associated with **greater** excursion efficiency.

H3: higher `NEAR_GAMMA_SHARE_0_5` is associated with **lower** MAE against the gap direction.

H4: `FRONT_NEAR_GAMMA_SHARE` should be directionally coherent with H1–H3, but it is secondary to total near-spot gamma.

H5: `WEIGHTED_ABS_DISTANCE` should have the opposite sign if diffuse/farther gamma is less supportive of orderly gap continuation.

## Stability checks
Report all primary relationships for:
- FULL 2025 replication sample
- chronological FIRST HALF
- chronological SECOND HALF
- NON-OPEX sessions

Monthly OPEX is descriptive/exclusion robustness only; do not optimize around it.

## Frozen replication success standard
The independent replication is considered **SUPPORTED** only if all are true:

1. `NEAR_GAMMA_SHARE_0_5` has the expected sign for both `GAP_FOLLOWTHROUGH` and `EXCURSION_EFFICIENCY` in the full sample, first half, second half, and non-OPEX sample; and at least one of the two full-sample p-values is < 0.10.
2. The full-sample relationship between `NEAR_GAMMA_SHARE_0_5` and `MAE_FROM_OPEN` is negative.
3. The non-OPEX sample preserves the same directional interpretation.
4. Walk-forward extended-model MAE improves by at least **2%** on at least one core target (`GAP_FOLLOWTHROUGH` or `EXCURSION_EFFICIENCY`) while worsening `MAE_FROM_OPEN` prediction by no more than **1%**.

If 1–3 pass but 4 fails, verdict = **REPLICATED ASSOCIATION / RESEARCH-ONLY**.
If the expected-sign relationship fails materially across halves or the full sample, verdict = **FAILED REPLICATION**.
Only a full pass may justify considering a compact scanner context tag; even then, no direct directional authority, STRENGTH, RUNWAY, R:R, or action-state authority is granted automatically.

## Descriptive-only comparison
For readability only, split qualifying sessions at the replication-sample median of `NEAR_GAMMA_SHARE_0_5` and report continuation rate, average follow-through, MFE, MAE, excursion efficiency, gap-fill rate, and gap retention. The median split is not a scanner threshold.

## Do Not Change After Results
- gap threshold 0.25%
- 1–30 DTE
- ±5% moneyness
- ±0.50% near-gamma zone
- 1–7 DTE front bucket
- IV filter 0.05–2.00
- walk-forward features or promotion gates
- 2025 SPY sample window
