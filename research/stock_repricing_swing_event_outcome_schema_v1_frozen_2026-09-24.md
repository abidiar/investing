# Stock Repricing Swing Study — Event/Outcome Schema v1.0 (FROZEN)

**Frozen:** 2026-09-24  
**Status:** FROZEN BEFORE EVENT-PANEL CONSTRUCTION OR OUTCOME SCORING  
**Purpose:** Test whether information available at entry can identify liquid-stock repricing/continuation setups that reach +5%, +10%, or +15% before -3% or -5% within the next 2–10 trading sessions.

## 1. Research question

Using only information available at the defined entry timestamp, can a systematic liquid-stock event/confirmation framework identify asymmetric long setups that subsequently reach +5%, +10%, or +15% before -3% or -5% over a maximum 10-session horizon?

This protocol does **not** target or optimize a 30% monthly portfolio return. Portfolio returns, position sizing, and options amplification are downstream analyses only after the underlying-stock edge is established out of sample.

## 2. Anti-leakage rule

Candidate/event construction and all entry-time features must be computed without forward information. Forward highs/lows/returns/barrier labels are appended only after the candidate panel is frozen for the applicable partition. No event may be removed because its later return is poor. Delisted/failed names remain if they met the contemporaneous universe rules and data are available.

## 3. Historical partitions — FROZEN

Partitions are chronological, never randomly shuffled.

- **DISCOVERY / TRAIN:** 2018-01-02 through 2022-12-30.
  - May be used to study feature relationships and propose a compact rule.
  - Any threshold learned here must be frozen before validation.
- **VALIDATION:** 2023-01-03 through 2024-12-31.
  - Used once to accept/reject the frozen discovery rule and diagnose broad failure modes.
  - No threshold optimization on validation outcomes.
- **FINAL UNTOUCHED OOS:** 2025-01-02 through 2026-08-31.
  - Must remain sealed until a rule is frozen after discovery/validation.
  - No redesign using OOS outcomes. If the rule fails here, it fails v1.

September 2026 and later are excluded from v1 historical development and reserved for prospective/live shadow evaluation.

## 4. Universe schema

The event panel is intended for tradable U.S.-listed common equities and highly liquid ADRs; ETFs, closed-end funds, preferreds, warrants, units, rights, OTC securities, leveraged/inverse products, and obvious shell/SPAC instruments are excluded.

Universe eligibility is determined using information available on the event date. Required fields are saved even if a later study changes eligibility thresholds:

- symbol
- permanent/security identifier where available
- event_date
- exchange
- security_type
- close_before_event
- market_cap available contemporaneously where available
- 20-session median dollar volume
- 20-session median share volume
- 20-session ATR and ATR percent
- 20-session ADR percent
- sector / industry
- benchmark and relevant peer/cluster identifiers

**Important:** v1 panel construction should err toward a broad liquid universe. Tight liquidity/price/market-cap cutoffs are not to be outcome-optimized. Exact mechanical source-specific minimums required to obtain reliable bars must be documented in the panel manifest.

## 5. Event families

Events are generated objectively without seeing forward outcomes. Preserve the raw measurements so alternate pre-registered definitions can be tested without repulling data.

Each event receives one or more event-family flags:

1. **GAP / REPRICING:** material opening gap or overnight dislocation relative to prior close and recent ATR/ADR.
2. **ABNORMAL RTH MOVE:** material same-session displacement relative to recent ATR/ADR.
3. **VOLUME / PARTICIPATION SHOCK:** abnormal volume or relative volume accompanying displacement.
4. **STRUCTURAL BREAKOUT:** break/acceptance above a pre-existing, mechanically measurable resistance/range/high using only prior bars.
5. **KNOWN CATALYST:** earnings, guidance, analyst/corporate/regulatory/macro/industry information when a timestamped catalyst source is available.

Catalyst availability is a feature, not permission to backfill a narrative after observing the outcome. `catalyst_known=false/unknown` must be retained rather than excluding the event.

## 6. Entry observations

Where intraday data are available, preserve standardized decision snapshots at:

- 09:50 ET
- 10:10 ET
- 10:20 ET
- 11:00 ET
- session close

The primary swing-entry comparison will be selected/frozen from DISCOVERY before VALIDATION is exposed. Until then, these are parallel observations, not multiple independent trades.

If intraday data are unavailable for an event, retain the event for daily-only analyses and mark intraday fields missing; do not impute future-derived values.

## 7. Entry-time feature schema

Save raw values plus deterministic derived fields where possible:

### Price / structure
- entry_price (snapshot last/close according to bar convention)
- session open, prior close
- gap percent
- return from open
- distance from session high/low
- distance from prior-day high/low/close
- distance from 20d/50d/252d high
- 5m structure state where available
- higher-low / lower-high counts using a frozen mechanical pivot definition documented by the builder
- VWAP and distance-to-VWAP
- VWAP hold/reclaim/acceptance state
- anchored VWAP fields only when anchor can be defined without hindsight

### Participation
- cumulative volume
- RVOL versus same-time historical profile where available
- push-volume / pullback-volume measurements
- volume contraction on pullback

### Relative strength / cluster
- return versus SPY
- return versus QQQ where relevant
- return versus sector benchmark
- return versus predefined peer/cluster basket
- peer breadth / cluster confirmation
- cluster leader rank

### Extension / runway
- ATR consumed
- ADR consumed
- distance to nearest pre-existing structural destination
- destination source/type
- underlying destination reward
- structural invalidation level
- structural risk
- destination R:R
- first-wave extension flag

### Market context
- SPY/QQQ direction and VWAP state
- sector benchmark direction
- volatility proxy/context where available
- scheduled major-event flag
- quarterly-expiration/triple-witching/rebalance flag

### Catalyst
- catalyst flag
- catalyst category
- catalyst timestamp
- catalyst source/reference where available
- whether catalyst was public before entry snapshot

## 8. Duplicate-event handling

A symbol may produce multiple snapshot rows for the same underlying event, but these are linked by a single `event_id`. Repeated qualification on adjacent days is not treated as an independent event unless a new objectively identifiable catalyst/dislocation occurs or the prior event window has ended. Exact deduplication logic must be frozen in the event-builder code before outcomes are appended.

## 9. Forward outcome schema — FROZEN

Forward horizon: through the end of the **10th trading session after entry**, including the remainder of entry day only for intraday-entry path statistics but reporting separate next-session horizons where appropriate.

For each event/snapshot calculate from the frozen entry price:

### Excursion
- MFE through 1, 2, 3, 5, and 10 sessions
- MAE through 1, 2, 3, 5, and 10 sessions
- close-to-entry return at 1, 2, 3, 5, and 10 sessions
- session/time of MFE and MAE

### Barrier-first outcomes
Evaluate all six combinations independently:

- +5% before -3%
- +5% before -5%
- +10% before -3%
- +10% before -5%
- +15% before -3%
- +15% before -5%

For each combination save:
- upper barrier hit Y/N
- lower barrier hit Y/N
- first barrier: TARGET / STOP / NEITHER / AMBIGUOUS_SAME_BAR
- trading session and timestamp/bar of first hit when resolution permits
- time-to-target / time-to-stop

**Same-bar ambiguity:** If both barriers are crossed inside the same bar and finer data cannot establish ordering, label `AMBIGUOUS_SAME_BAR`; never assume the favorable ordering. Primary conservative scoring counts ambiguous cases as failures for the target-first rate, with a sensitivity analysis reported separately.

## 10. Primary evaluation metrics

For each frozen rule and relevant cohort report:

- N events and N independent event clusters
- target-before-stop rate for all six barrier pairs
- Wilson 95% confidence interval
- NEITHER and AMBIGUOUS rates
- median and mean MFE/MAE
- median time to target
- expectancy under a simple predefined barrier exit, before and after conservative transaction-cost/slippage assumptions
- performance by calendar year and partition
- performance by market regime, sector, event family, and catalyst availability as diagnostics
- maximum losing streak
- bootstrap confidence interval clustered by date/event where practical

No result is considered established from win rate alone.

## 11. Minimum evidence / promotion rules

Before calling a stock-selection rule useful:

1. It must show positive expectancy in VALIDATION under conservative costs.
2. The direction of edge must not depend on one calendar year or one symbol/cluster.
3. It must improve meaningfully over an unconditional eligible-event baseline constructed with the same universe and timestamps.
4. Final promotion requires positive expectancy in FINAL UNTOUCHED OOS and no catastrophic degradation in target-before-stop behavior.
5. Sample size and confidence intervals must be reported; small-N spectacular returns are not sufficient.

The exact compact feature rule and numerical promotion threshold will be frozen **after DISCOVERY and before VALIDATION**, not now.

## 12. Portfolio analysis is downstream

Only after a rule survives FINAL OOS may we simulate portfolio construction. Portfolio simulation must include overlapping positions, capital constraints, transaction costs, slippage, position sizing, concentration, drawdown, and cash drag. The desired 30% monthly return is an aspirational benchmark to measure, never an optimization target used to select the rule.

## 13. Permanent files to create

The builder should eventually save:

- `data/historical/stock_repricing_events_v1_features.csv` — event/snapshot features with no forward outcomes during construction.
- `data/historical/stock_repricing_events_v1_outcomes.csv` — keyed outcome table appended only after applicable feature panel freeze.
- `data/historical/stock_repricing_events_v1_manifest.md` — sources, coverage, exclusions, missingness, deduplication, hashes/checksums and build timestamp.
- `research/results/stock_repricing_swing_v1_*` — analyses/results.

Feature and outcome tables remain separate so the untouched OOS feature panel can be built/frozen without casually exposing labels.

## 14. Governance

This document is frozen v1.0. Any substantive change creates v1.1+ with an explicit reason and must not retroactively redefine a test after its outcomes have been viewed.
