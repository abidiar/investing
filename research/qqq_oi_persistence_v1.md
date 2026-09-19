# Investing OS Research — QQQ OI Persistence v1.0

Status: FROZEN BEFORE RESULTS
Frozen: 2026-09-19

## Question
Does settled contract-level QQQ open-interest change, especially relative to same-contract trading volume, add next-session information beyond price alone?

## Data discipline
- Instrument: QQQ options and QQQ underlying price.
- Snapshot Day T may predict only the next trading session T+1.
- Never treat settled OI as intraday/same-day information.
- Only compare sequential snapshots when the prior snapshot is the immediately preceding available trading-session snapshot; missing-session gaps are excluded from persistence-ratio tests.
- Raw OI, delta OI, and put/call labels are not assumed to reveal buyer/seller direction.

## Frozen contract universe
- Expiration DTE: 1–30 calendar days from snapshot date.
- Moneyness: strike within +/-3.0% of Day-T QQQ close.
- Calls and puts retained separately and combined.
- Exclude rows with missing OI; treat missing/blank volume as zero only for descriptive raw counts, but exclude zero-total-volume aggregates from persistence-ratio calculations.

## Frozen features
For each matched contract between T-1 and T:
- delta_OI = OI_T - OI_T-1
- OI_BUILD = max(delta_OI, 0)
- OI_UNWIND = max(-delta_OI, 0)

Aggregate by session and side:
- CALL_BUILD, PUT_BUILD, TOTAL_BUILD
- CALL_UNWIND, PUT_UNWIND, TOTAL_UNWIND
- CALL_VOLUME, PUT_VOLUME, TOTAL_VOLUME
- CALL_PERSISTENCE = CALL_BUILD / CALL_VOLUME
- PUT_PERSISTENCE = PUT_BUILD / PUT_VOLUME
- TOTAL_PERSISTENCE = TOTAL_BUILD / TOTAL_VOLUME
- BUILD_IMBALANCE = (CALL_BUILD - PUT_BUILD) / (CALL_BUILD + PUT_BUILD), when denominator > 0

No ratio clipping or outcome-driven winsorization in this pass. Obvious source-data impossibilities will be reported as data-quality failures rather than silently repaired.

## Frozen price baseline
- Day-T price direction = sign of QQQ open-to-close return.
- Meaningful Day-T move = |open-to-close| >= 0.25%, retained from Dealer Structure v1.0 for consistency.

## Primary hypotheses
H1 — Persistence / movement, non-directional:
Higher TOTAL_PERSISTENCE is associated with larger next-session absolute close-to-close movement and/or larger high-low range.
Primary statistic: Spearman rank correlation. This avoids optimizing a high/low persistence threshold.

H2 — Raw option-side buildup is not reliably directional:
BUILD_IMBALANCE should not be promoted unless it shows stable association with next-session signed return and survives basic robustness checks. A null result is acceptable and expected given long/short ambiguity.

H3 — Price-conditioned continuation:
Among sessions with |Day-T open-to-close| >= 0.25%, test whether TOTAL_PERSISTENCE improves the probability/magnitude of next-session continuation in the already-established Day-T price direction. This is an overlay test, not a direction-creation test.

## Secondary descriptive cuts — exploratory only
- 1–7 DTE vs 8–30 DTE
- calls vs puts
- ordinary sessions vs monthly/quarterly OPEX where sample size permits
- persistence above/below the eligible-sample median for readable continuation tables; median split is descriptive and may not become a frozen scanner threshold from this pass.

## Outcomes
- T+1 close-to-close return
- absolute T+1 close-to-close return
- T+1 high-low range / Day-T close
- T+1 opening gap
- T+1 open-to-close return
- same-direction T+1 continuation after a meaningful Day-T move

## Promotion standard
This experiment may support a compact OPTIONS POSITIONING tag only if it adds stable information beyond price. It may not add to STRENGTH, RUNWAY, R:R, or create BUY/SELL/CALL/PUT authority from this pass alone.

## Data source identified
Daily QQQ chain snapshots from `oceanyang2024/qqq-option`, which store strike, type, daily volume, settled open interest, IV and related fields by snapshot date/expiration. Underlying outcomes use independent QQQ daily bars.

## Results
PENDING — rules above were frozen before outcome calculation.
