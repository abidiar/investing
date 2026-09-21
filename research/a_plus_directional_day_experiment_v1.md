# A+ Directional Day Experiment v1

Frozen: 2026-09-21
Status: **PREREGISTERED BEFORE HISTORICAL OUTCOME EXPOSURE**

## Objective
The Investing OS should optimize for precision and abstention, not daily trade frequency.

Primary question:
> Can information genuinely available by 10:20 ET identify a small subset of sessions with unusually clean intraday directional opportunity, symmetrically for CALLS and PUTS, while classifying normal/mixed sessions as NO TRADE?

Secondary question:
> Conditional on an A+ market day, does selecting a confirmed individual leader/laggard improve the opportunity relative to simply trading SPY/QQQ?

No market state is guaranteed. The target is an unusually high conditional hit rate with controlled adverse excursion and low trade frequency.

## Research prior
External research supports trend/time-series momentum, cross-market trend information, momentum/reversal state dependence, and the usefulness of reducing exposure in unfavorable/high-volatility states. This supports a selective regime-gating architecture but does not establish the specific intraday A+ rule below.

## Decision states
Exactly three primary outputs:
- A+ CALL DAY
- A+ PUT DAY
- NO TRADE

NO TRADE is the default state.

## Primary decision time
10:20 ET.

Secondary diagnostics may evaluate 9:50 and 10:00 ET, but they cannot replace 10:20 as the primary preregistered decision time after outcomes are seen.

## Hard-gate architecture
A+ is not an additive score. A session must pass every required gate. Several mediocre factors cannot sum into A+.

### Gate 1 — DRIVER / CATALYST
There must be a material, identifiable directional driver known by 10:20 ET, such as:
- scheduled macro surprise / repricing (CPI, payrolls, Fed, etc.);
- material overnight geopolitical/policy development;
- major rates/oil/currency/credit repricing relevant to equities;
- major earnings/read-through or broad industry catalyst;
- capitulation/reversal catalyst with objectively abnormal prior/current price behavior.

If there is no material driver and the day is merely drifting/trending normally, Gate 1 fails.

### Gate 2 — CROSS-ASSET COHERENCE
At least two relevant non-equity or independent market channels must agree with the directional equity thesis when such channels are economically relevant. Examples: Treasury yields/rates, oil/commodities, USD, credit, volatility, international equity futures.

Do not require a mechanically fixed asset pair when the catalyst does not economically implicate it. Contradictory cross-asset behavior fails the gate unless the contradiction has an explicit event-specific explanation declared before outcome exposure.

### Gate 3 — BROAD-MARKET CONFIRMATION
By 10:20, SPY and/or QQQ must have accepted the directional thesis on M5 structure. Required evidence:
- directionally consistent move from the RTH open;
- accepted price structure rather than a single spike;
- VWAP hold/acceptance for CALL or loss/failed reclaim for PUT where VWAP is available;
- no major failed-break/reversal already invalidating the thesis.

Price gets the final vote.

### Gate 4 — BREADTH / LEADERSHIP CONFIRMATION
The move must have credible participation. Use available breadth plus sector/cluster leadership. A narrow index move driven by one or two megacaps without supporting participation is not A+ unless the catalyst itself is explicitly concentrated and the chosen vehicle belongs to that concentrated leadership cluster.

### Gate 5 — RUNWAY / EXTENSION
At 10:20 the trade must still have realistic destination runway. Reject sessions where the market has already consumed most realistic intraday range/ADR or where the nearest credible destination does not offer approximately >=2:1 reward/risk from an executable confirmed entry.

### Gate 6 — EVENT / DISTORTION VETO
No unresolved scheduled event or known mechanical distortion may make direction unreliable after 10:20. Quarterly expiration/rebalance, major imminent data/Fed events, abnormal closing-flow effects, or similar mechanics cannot improve A+ status and may veto it.

## Direction
CALL requires all gates to support/accept higher prices.
PUT requires all gates to support/accept lower prices.
Mixed directional evidence = NO TRADE.

A bull market does not prohibit A+ PUT days; it raises the burden of evidence against the prevailing trend. Likewise, bear regimes do not prohibit A+ CALL reversal days when the reversal is independently confirmed.

## Market-level vehicle
Primary benchmark outcome is SPY. QQQ is a secondary benchmark where the catalyst/leadership is technology/growth concentrated.

## Outcomes — frozen before testing
From the first executable accepted M5 entry at/after 10:20, or 10:20 benchmark price when no more precise entry is available:
1. Directional close win: close in predicted direction from entry.
2. +0.50% before -0.50% in predicted direction.
3. +0.75% before -0.50%.
4. +1.00% before -0.50% where daily range makes this feasible.
5. MFE through close.
6. MAE through close.
7. MFE/MAE ratio.
8. Close return in predicted direction.
9. Whether thesis invalidation occurred before T1.
10. Trade frequency / abstention rate.

Primary success criterion is **precision plus excursion quality**, not number of trades. Report confidence intervals; do not promote tiny-sample perfect records.

## Comparators
Compare A+ sessions against:
- all sessions;
- sessions classified NO TRADE;
- a simple 10:20 SPY directional-momentum baseline;
- where feasible, ordinary scanner-qualified continuation/reversal sessions without the A+ day gate.

This is required to establish incremental value from abstention/regime gating.

## Individual-name second stage
Only after the market-level A+ classification is frozen, evaluate whether the existing Investing OS can choose a better expression of the direction.

Individual candidate still independently requires:
- STRENGTH >=4/5;
- RUNWAY >=4/5;
- accepted M5 trigger;
- current realistic destination R:R >= ~2:1;
- acceptable ADR/extension;
- sponsorship/RS appropriate to the thesis;
- acceptable event risk;
- option viability if an option is proposed.

A+ DAY status cannot add STRENGTH or RUNWAY points and cannot rescue a weak ticker.

## External signals — CROM / Discord
CROM and Discord signals are excluded from v1 A+ classification to preserve independence.

After v1 is tested, evaluate each external signal source separately for incremental value:
- timestamp signal before entry;
- direction;
- market regime/A+ state at signal time;
- subsequent MFE/MAE and target-before-stop outcomes;
- whether signal adds information after controlling for Investing OS state.

Only validated incremental information may become a confirmation layer. External signals cannot override a failed A+ hard gate.

## Anti-overfitting / falsification rules
- Freeze gates before exposing historical outcomes.
- Candidate historical days must be discovered from contemporaneous information, not selected because they are remembered as large winners/losers.
- Do not begin with 'obvious easy days' selected from charts and call that a backtest.
- Preserve NO TRADE as the default; do not relax gates merely to increase N.
- Do not optimize thresholds after seeing returns.
- Any calibration change creates a new version and must be tested on untouched data.
- Report false positives and false negatives, including spectacular trend days the gate missed.
- Do not surface historical hit rate as a live probability without separate OOS validation.

## Clean experimental sequence
1. Build a date-indexed discovery panel using only information timestamped <=10:20 ET for a historical calibration period.
2. Apply the frozen gates mechanically and classify CALL / PUT / NO TRADE before exposing post-10:20 returns.
3. Expose outcomes and conduct false-positive/false-negative autopsy.
4. If calibration changes are justified, freeze v2.
5. Take the unchanged rule to an untouched period/universe.
6. Only after OOS validation evaluate CROM/Discord as incremental overlays.

## Data sufficiency
Existing price data should be sufficient for market price confirmation, VWAP/structure, MFE/MAE and outcome measurement. Historical catalyst, macro and cross-asset state must be reconstructed from timestamped contemporaneous/public data or already stored research. Missing contemporaneous information must be marked missing; do not infer it from later knowledge.

## Production rule
No live scanner change from this preregistration alone. Production authority requires successful untouched out-of-sample validation.
