# Investing OS Research — QQQ Gamma Concentration / Pinning v1.0

Status: **FROZEN BEFORE RESULTS**
Frozen: 2026-09-19

## Question
Can **gamma-weighted options concentration**, its distance from spot, and DTE structure distinguish next-session **damping/pinning** from **expansion/continuation** better than price alone?

This is intentionally different from the rejected OI-persistence experiment. We are not asking whether new call/put OI predicts direction. We are asking whether the *shape and location* of gamma-weighted outstanding positioning changes the expected behavior of a price move that is determined independently by price.

## Information hierarchy
1. Price remains primary. Price gets final vote.
2. This experiment tests market-behavior / structure only: damping, pinning, expansion, continuation.
3. No unsigned gamma/OI feature may independently choose bullish vs bearish direction.
4. No result from this pass may add STRENGTH or RUNWAY, manufacture R:R, excuse extension, or override event risk.

## Data discipline
- Instrument: QQQ options + QQQ underlying.
- Options source: daily QQQ chain snapshots from `oceanyang2024/qqq-option`.
- Day-T chain snapshot may predict **T+1 only**.
- No same-day/intraday use of settled OI.
- No customer/dealer side is observed; therefore this experiment uses **unsigned theoretical gamma weight**, not signed dealer GEX.
- The source IV is used only to estimate contract gamma. We do not infer trade direction from call/put labels.

## Frozen contract universe
- DTE: **1–30 calendar days**.
- Moneyness: strike within **±5.0%** of Day-T QQQ close.
- Open interest: non-missing and >= 0.
- Implied volatility: finite and **0.05 to 2.00** in decimal units. Contracts outside this range are excluded as likely stale/pathological for this structural calculation.
- Calls and puts are both retained.

## Frozen theoretical gamma
For each contract, using Day-T QQQ close `S`, strike `K`, IV `sigma`, and `T = DTE / 365`:

`d1 = [ln(S/K) + 0.5*sigma^2*T] / [sigma*sqrt(T)]`

`gamma = phi(d1) / [S*sigma*sqrt(T)]`

For this relative-concentration experiment, `r = 0` and `q = 0` are deliberately used so that rate assumptions do not inject a second model. Call/put gamma is positive in the pricing model; side/sign is not inferred.

Frozen contract weight:

`GAMMA_WEIGHT = gamma * openInterest`

The 100-share multiplier and common spot-scaling terms are omitted because they cancel in concentration shares. This is **not signed GEX** and must never be labeled as such.

## Frozen session features
Computed across the eligible 1–30 DTE, ±5% universe:

1. **TOTAL_GAMMA_WEIGHT** = sum(GAMMA_WEIGHT).
2. **NEAR_GAMMA_SHARE_0_5** = share of total gamma weight within ±0.50% of spot.
3. **NEAR_GAMMA_SHARE_1_0** = share within ±1.00% of spot.
4. **FRONT_GAMMA_SHARE** = share from 1–7 DTE contracts.
5. **FRONT_NEAR_GAMMA_SHARE** = share from 1–7 DTE contracts that are also within ±0.50% of spot.
6. Aggregate GAMMA_WEIGHT by strike across calls, puts, and expiries.
7. **DOMINANT_STRIKE** = strike with maximum aggregate gamma weight.
8. **DOMINANT_STRIKE_SHARE** = dominant-strike gamma weight / total gamma weight.
9. **DOMINANT_STRIKE_DISTANCE** = abs(DOMINANT_STRIKE / spot - 1).
10. **WEIGHTED_ABS_DISTANCE** = gamma-weighted mean absolute strike distance from spot.
11. **STRIKE_HHI** = sum of squared strike gamma-weight shares. Higher = more spatially concentrated.
12. **EFFECTIVE_STRIKES** = 1 / STRIKE_HHI.

No feature thresholds will be optimized after outcomes are seen.

## Frozen price context
- Day-T direction = sign of QQQ open-to-close return.
- Meaningful Day-T move = **|open-to-close| >= 0.25%**, retained unchanged from prior research.
- Day-T price baseline features for incremental forecasting:
  - absolute open-to-close return
  - Day-T high-low range / prior close
  - trailing 5-session close-to-close realized volatility

## Outcomes
Primary:
- T+1 absolute close-to-close return
- T+1 high-low range / Day-T close

Secondary:
- T+1 signed close-to-close return
- T+1 opening gap
- T+1 open-to-close return
- continuation return = sign(Day-T open-to-close) * T+1 close-to-close, conditional on meaningful Day-T move
- binary same-direction continuation, conditional on meaningful Day-T move
- pin improvement = Day-T distance to dominant strike minus T+1 close distance to the same Day-T dominant strike; positive means the next close moved closer to the dominant strike

## Primary hypotheses
### H1 — Near-spot gamma concentration is damping
Higher `NEAR_GAMMA_SHARE_0_5`, `FRONT_NEAR_GAMMA_SHARE`, and `STRIKE_HHI` should be associated with **smaller** T+1 absolute close-to-close moves and/or smaller T+1 high-low ranges.

Primary statistic: Spearman rank correlation. Expected sign: **negative**.

### H2 — Diffuse / farther gamma structure is expansion-friendly
Higher `WEIGHTED_ABS_DISTANCE` and more `EFFECTIVE_STRIKES` should be associated with **larger** T+1 movement/range.

Primary statistic: Spearman rank correlation. Expected sign: **positive**.

### H3 — Dominant gamma strike can create a pinning tendency
When the Day-T dominant strike is within **1.00%** of spot, larger `DOMINANT_STRIKE_SHARE` should be associated with greater positive `pin_improvement`.

The 1.00% distance rule is frozen before results and may not be changed in this pass.

### H4 — Gamma concentration should damp continuation after price already moved
Among sessions where |Day-T open-to-close| >= 0.25%, higher `FRONT_NEAR_GAMMA_SHARE` and `STRIKE_HHI` should be associated with a smaller `continuation_return` and a lower probability of same-direction continuation.

This is an overlay test only. It cannot create direction.

## Incremental price-baseline test
To answer whether the structure actually improves Investing OS rather than merely correlating with volatility, run a **walk-forward one-step-ahead linear forecast** with no hyperparameter tuning.

Minimum training window: **60 eligible sessions**.

Baseline features:
- abs Day-T open-to-close return
- Day-T range / prior close
- trailing 5-session realized volatility

Extended features add exactly:
- NEAR_GAMMA_SHARE_0_5
- FRONT_GAMMA_SHARE
- FRONT_NEAR_GAMMA_SHARE
- STRIKE_HHI
- WEIGHTED_ABS_DISTANCE
- DOMINANT_STRIKE_SHARE
- DOMINANT_STRIKE_DISTANCE

Targets, tested separately:
- T+1 absolute close-to-close return
- T+1 high-low range

Compare walk-forward MAE and prediction/actual Spearman correlation. No feature selection after results.

## Stability checks
For every primary feature/outcome association, report:
- full sample
- chronological first half
- chronological second half

A relationship that flips sign across halves is considered unstable even if the full-sample p-value is attractive.

Also report monthly-OPEX-week vs non-OPEX descriptively, but OPEX is not an optimization filter in this pass.

## Promotion standard
This module may advance from research-only to a compact scanner context tag only if:

1. At least one primary damping/expansion feature has the expected sign in the full sample **and both chronological halves**, with full-sample p < 0.10 on at least one primary outcome; **and**
2. The walk-forward extended model improves MAE by at least **2%** on at least one primary target while not worsening the other target by more than **1%**; **and**
3. The continuation/pinning tests are directionally coherent with the proposed interpretation.

If these are not met, gamma concentration remains research-only.

Even if promoted, the maximum allowed scanner impact from v1.0 is contextual tags such as:
- OPTIONS STRUCTURE: DAMPING / EXPANSION-FRIENDLY / NEUTRAL
- GAMMA CONCENTRATION: HIGH / NORMAL / LOW
- DOMINANT GAMMA ZONE: distance from spot

No v1.0 result may independently create BUY, SELL, CALL, PUT, HOLD, STRENGTH, RUNWAY, or overnight-carry authority.

## Do Not Re-Test Unless
- a materially larger or independent sample becomes available;
- signed dealer-position estimates become available with documented methodology;
- intraday 0DTE positioning becomes available without lookahead;
- or the feature construction is changed and frozen in advance.

## Results
PENDING — all rules above were frozen before calculation.
