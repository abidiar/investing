# Investing OS Research — QQQ 2025 Gap-Conditioned Gamma Time-Shift Replication v1.0

Status: **FROZEN BEFORE RESULTS**
Frozen: 2026-09-19

## Purpose
Test whether the 2026 QQQ gap-conditioned gamma relationship replicates on the **same underlying (QQQ) in a non-overlapping earlier year (2025)**. This is the cleanest available test of whether the prior signal was instrument-specific versus 2026-regime-specific, while preserving the already-frozen thresholds and promotion gates.

This test is independent in time from the discovery sample. It also uses a separate historical options archive, which improves source independence but means a failure could reflect either regime instability or source/measurement differences.

## Prior finding being replicated
In the 2026 QQQ discovery sample, when the next session opened with an absolute overnight gap >= 0.25%, higher prior-day near-spot unsigned gamma concentration was associated with:
- greater same-direction RTH gap follow-through;
- higher excursion efficiency;
- lower adverse excursion.

That finding remained research-only because the walk-forward incremental-usefulness gate failed. A later independent SPY 2025 replication failed the core primary relationship.

## Replication sample
- Instrument: **QQQ**.
- Time period: **calendar year 2025 only**.
- No 2026 QQQ observations are allowed.
- Options source: `anahatsingh-ui/options-dataset-hist`, file `qqq/options_2025.parquet`.
- Underlying OHLC source: independent QQQ daily bars.
- Day-T options snapshot may predict **Day T+1 only**.

## Frozen contract universe
Exactly preserve the prior construction:
- DTE: **1–30 calendar days**.
- Moneyness: strike within **±5.0%** of Day-T QQQ close.
- Open interest: non-missing and >= 0.
- Implied volatility: finite and **0.05 to 2.00** decimal.
- Calls and puts retained together; no directional inference from option type.

## Frozen theoretical gamma
Do **not** use the archive's supplied gamma field as the primary weight. Recompute the same unsigned theoretical gamma used in the original QQQ test and the SPY replication:

`T = DTE / 365`

`d1 = [ln(S/K) + 0.5*sigma^2*T] / [sigma*sqrt(T)]`

`gamma = phi(d1) / [S*sigma*sqrt(T)]`

with `r = 0` and `q = 0`.

`GAMMA_WEIGHT = gamma * open_interest`

This is unsigned theoretical gamma concentration, **not signed dealer GEX**.

## Frozen session features
Computed on Day T:
1. `NEAR_GAMMA_SHARE_0_5` = share of total gamma weight within ±0.50% of QQQ close.
2. `FRONT_NEAR_GAMMA_SHARE` = share of total gamma weight from 1–7 DTE contracts also within ±0.50% of spot.
3. `WEIGHTED_ABS_DISTANCE` = gamma-weighted mean absolute strike distance from spot.

## Frozen gap eligibility
On Day T+1:
- `GAP = Open_(T+1) / Close_T - 1`.
- Qualifying session requires **abs(GAP) >= 0.25%**.
- Gap direction comes from the observed Day-T+1 open only; gamma cannot choose direction.

## Frozen outcomes
Let `sign = +1` for gap-up and `-1` for gap-down.

Primary:
- `GAP_FOLLOWTHROUGH = sign * (Close/Open - 1)` on T+1.
- `EXCURSION_EFFICIENCY = MFE / (MFE + MAE)` from the T+1 open in gap direction.

Failure controls:
- `MFE_FROM_OPEN` in gap direction.
- `MAE_FROM_OPEN` against gap direction.
- `GAP_FILL` = whether T+1 trades back to or through Day-T close.
- `GAP_RETENTION_CLOSE = sign * (Close_(T+1)/Close_T - 1)`.

## Frozen price-only baseline
Exactly preserve the prior walk-forward baseline:
- absolute gap size;
- Day-T absolute open-to-close return;
- Day-T high-low range / prior close;
- trailing 5-session realized close-to-close volatility.

Extended model adds exactly:
- `NEAR_GAMMA_SHARE_0_5`;
- `FRONT_NEAR_GAMMA_SHARE`;
- `WEIGHTED_ABS_DISTANCE`.

Walk-forward OLS:
- minimum training window **60 qualifying gap sessions**;
- expanding training window;
- training-only standardization;
- no hyperparameter tuning or feature selection.

Targets:
- gap follow-through;
- excursion efficiency;
- adverse excursion from open.

## Frozen hypotheses
H1: higher `NEAR_GAMMA_SHARE_0_5` is associated with **greater** same-direction gap follow-through.

H2: higher `NEAR_GAMMA_SHARE_0_5` is associated with **greater** excursion efficiency.

H3: higher `NEAR_GAMMA_SHARE_0_5` is associated with **lower** MAE against the gap direction.

H4: `FRONT_NEAR_GAMMA_SHARE` should be directionally coherent with H1–H3, but remains secondary.

H5: `WEIGHTED_ABS_DISTANCE` should generally have the opposite sign if diffuse/farther gamma is less supportive of orderly continuation.

## Stability checks
Report all primary relationships for:
- FULL 2025 sample;
- chronological FIRST HALF;
- chronological SECOND HALF;
- NON-OPEX sessions.

Monthly OPEX is descriptive robustness only. Do not optimize around it.

## Frozen replication success standard
The 2025 QQQ replication is **SUPPORTED** only if all are true:

1. `NEAR_GAMMA_SHARE_0_5` has the expected positive sign for both `GAP_FOLLOWTHROUGH` and `EXCURSION_EFFICIENCY` in FULL, FIRST HALF, SECOND HALF, and NON-OPEX, and at least one full-sample p-value is < 0.10.
2. Full-sample `NEAR_GAMMA_SHARE_0_5` vs `MAE_FROM_OPEN` is negative.
3. NON-OPEX preserves the same directional interpretation.
4. Walk-forward extended-model MAE improves by at least **2%** on at least one core target (`GAP_FOLLOWTHROUGH` or `EXCURSION_EFFICIENCY`) while worsening `MAE_FROM_OPEN` prediction by no more than **1%**.

Verdicts:
- all four pass -> **SUPPORTED**;
- 1–3 pass but 4 fails -> **REPLICATED ASSOCIATION / RESEARCH-ONLY**;
- core expected-sign relationship materially fails -> **FAILED REPLICATION**.

Even a full pass would authorize only consideration of a compact context tag. It would not independently create direction, add STRENGTH/RUNWAY, manufacture R:R, or create BUY/SELL/CALL/PUT/HOLD/overnight authority.

## Descriptive-only comparison
Split qualifying sessions at the 2025 QQQ sample median of `NEAR_GAMMA_SHARE_0_5` and report continuation rate, average follow-through, MFE, MAE, excursion efficiency, gap-fill rate, and gap retention. This split is descriptive only and is not a scanner threshold.

## Interpretation matrix after results
- QQQ 2025 passes while SPY 2025 failed -> evidence favors **instrument-specific QQQ behavior** over a broad ETF effect.
- QQQ 2025 fails similarly to SPY 2025 -> evidence favors **2026-regime/source-specific discovery** and substantially downgrades the original QQQ signal.
- QQQ 2025 has association but fails walk-forward -> keep as **QQQ research-only structural context**.

## Do Not Change After Results
- 0.25% gap threshold
- 1–30 DTE
- ±5% moneyness
- ±0.50% near-gamma zone
- 1–7 DTE front bucket
- IV filter 0.05–2.00
- walk-forward baseline/features
- promotion gates
- calendar-year 2025 QQQ sample
