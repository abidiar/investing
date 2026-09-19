# Investing OS — Options Positioning Research Status

Updated: 2026-09-19
Status: **CANONICAL TOPIC INDEX**

Detailed prior-work reviews, frozen protocols, code, and machine-readable results remain in `research/`, `research/prior_work/`, and `research/results/`. Governance is controlled by `research/RESEARCH_GOVERNANCE.md`.

## Current production posture
Options-positioning research remains **context-only / research-only** unless a particular decision rule passes its preregistered production gate. No tested OI/gamma feature may independently create direction, add STRENGTH/RUNWAY, manufacture R:R, authorize BUY/SELL/CALL/PUT/HOLD, or authorize overnight carry. **Price gets final vote.**

Every new hypothesis now requires a prior-work review under `research/PRIOR_WORK_REVIEW_STANDARD.md` before the outcome protocol is frozen.

## Pass history

### Pass 1 — Dealer/GEX regime
Verdict: **PROVISIONAL / RESEARCH-ONLY**.
Signed/modelled dealer gamma may characterize amplification/damping after independent price confirmation. Raw GEX direction, exact wall/flip precision, and wall proximity alone are not promoted.

### Pass 2 — QQQ settled OI persistence
Verdict: **NOT SUPPORTED**.
Delta-OI/volume persistence did not predict larger next-session movement or improve continuation. Call-vs-put buildup imbalance had essentially zero directional value.

### Pass 3 — QQQ gamma concentration / pinning
Verdict: **RESEARCH-ONLY**.
Near-spot unsigned gamma associated with smaller next-session RTH range. Dominant-strike pinning failed and walk-forward improvement was insufficient.

### Pass 4 — Overnight vs RTH decomposition
Verdict: **RESEARCH-ONLY**.
Near-spot gamma related more clearly to RTH range compression than overnight-gap magnitude, but predictive improvement remained insufficient.

### Pass 5 — QQQ path efficiency
Verdict: **BROAD HYPOTHESIS FAILED STABILITY**.
Generic high-gamma cleaner-path behavior was unstable across time and bar resolution.

### Pass 6 — QQQ gap-conditioned continuation
Verdict: **RESEARCH-ONLY DISCOVERY**.
A strong 2026 QQQ gap-follow-through association appeared but failed the frozen incremental-utility gate.

### Pass 7 — SPY 2025 independent replication
Verdict: **FAILED REPLICATION**.
The QQQ directional gap-gamma relationship did not generalize to SPY.

### Pass 8 — QQQ 2025 time-shift replication
Verdict: **FAILED REPLICATION**.
The 2026 QQQ directional relationship did not reproduce in QQQ 2025. Treat the original directional effect as regime/source-specific, not durable.

### Pass 9 — Multi-year unsigned near-spot gamma compression
Files: `research/multiyear_near_spot_gamma_compression_v1.md` and matching results.
Verdict: **REPLICATED ASSOCIATION / RESEARCH-ONLY**.
Across 2,221 SPY/QQQ/IWM observations in 2023–2025, higher near-spot unsigned gamma associated with smaller next-session RTH range/excursion. Price-volatility state captured most practical forecast value.

### Pass 10 — Untouched 2020–2022 incremental-value holdout
Files: `research/near_spot_gamma_incremental_value_v1.md` and matching results.
Verdict: **CONDITIONAL ASSOCIATION / RESEARCH-ONLY**.
Across 2,262 untouched observations, the compression relationship survived seven price-volatility controls, instrument/year checks, and non-OPEX robustness. Adding gamma improved walk-forward MAE by 1.26% for next RTH range and 1.33% for max excursion, below the frozen 2% promotion gate. Conclusion: unsigned near-spot gamma contains a small real additive amplitude signal, but not enough for production authority.

### Pass 11 — Decision-level chase/veto falsification
Files:
- `research/gamma_chase_decision_v1.md`
- `research/results/gamma_chase_decision_v1_results.md`

Verdict: **FAILED DECISION-LEVEL OVERLAY**.
Untouched holdout: 1,195 SPY/QQQ/IWM candidates in 2017–2019, trained on 2014–2016. A gamma veto improved T1 precision from 69.39% to 73.97% (+4.58 pp), and vetoed candidates had a 44.0% miss rate versus 30.61% for baseline chases. But it retained only 79.41% of baseline winners versus the frozen >=85% requirement, and Brier improvement was only 0.38% versus the frozen >=2% requirement. **Unsigned gamma must not be used as a hard entry/chase veto.**

### Pass 12 — Target-calibration decision falsification
Files:
- `research/gamma_target_calibration_v1.md`
- `research/results/gamma_target_calibration_v1_results.md`

Verdict: **FAILED DECISION-LEVEL TARGET OVERLAY**.
This test used a wholly untouched 2012–2013 holdout with 799 SPY/QQQ/IWM candidates and a 2011 training seed. Every candidate was retained; gamma could only alter target ambition among a frozen 0.50/0.75/1.00 × trailing-20 median-range ladder.

Results:
- Mean captured target distance was **0.21% for both price-only and price+gamma**: 0.00% relative improvement.
- Target hit rate was **40.55% for both**.
- There were **0 upgrades, 0 downgrades, and 799 unchanged targets**.
- Both models selected T1 on 99.87% of events; neither gamma nor price information provided enough confidence to select a larger target under the frozen 0.60 probability rule.
- Average Brier performance across T1/T2/T3 became **0.82% worse** when gamma was added.
- Frozen capture, bootstrap, and cross-instrument/year gates failed.

Interpretation: the preregistered target-sizing mechanism produced **no incremental decision utility**. This result must not be rescued by lowering the 0.60 threshold or changing the ladder using these same 2012–2013 outcomes.

## Current best interpretation
- Raw OI is not directional.
- Delta-OI persistence is not useful enough for next-session movement/continuation.
- Large gamma walls are not automatic magnets; exact wall/flip levels are not penny-precise trade levels.
- The unsigned-gamma directional gap-continuation idea failed two independent replications.
- Unsigned near-spot gamma has a repeatedly observed **non-directional amplitude/compression association** and a small controlled additive relationship beyond price volatility.
- That unsigned-gamma information has now **failed two separate decision-level uses**: hard chase/entry veto (Pass 11) and target calibration (Pass 12).
- Therefore unsigned near-spot gamma remains research/context-only and should not receive additional production authority from the current evidence.
- Signed/modelled dealer GEX is economically distinct from unsigned gamma concentration and remains the most defensible options-positioning branch for a new clean investigation.

## Prior-work review — signed dealer-GEX branch
File: `research/prior_work/dealer_gex_amplification_damping_prior_work_2026-09-19.md`

The broad signed-gamma mechanism is already well studied rather than novel. Prior academic work supports some version of:
- **negative / short dealer gamma -> momentum, amplification, higher volatility**;
- **positive / long dealer gamma -> reversal, damping, lower volatility**;
with the effect often strongest when hedge demand is large relative to underlying liquidity.

Key prior-work implications:
- public OI does **not** reveal dealer inventory;
- the dealer sign convention is a model assumption unless participant/signed-flow data are available;
- liquidity is an important moderator and must be decided before outcomes are seen;
- gross 0DTE volume is not the same as net hedge demand;
- longer-dated positions aging into 0DTE can matter materially;
- exact strike-local wall/pinning claims have weaker modern evidence than broad regime effects;
- dealer inventory composition (long/short calls vs puts) may contain information beyond net GEX alone.

Therefore our next work should **not** weakly retest `does signed gamma matter?`. The useful question is whether a credible dealer-sign measure adds **incremental decision value beyond price, volatility, and liquidity**, with price continuing to supply direction.

## Rejected / not production-eligible
- Raw OI as bullish/bearish direction.
- Call-vs-put OI buildup as direction.
- Delta-OI/volume persistence as a next-day movement/continuation edge.
- Large gamma wall as an automatic magnet.
- Exact gamma wall/flip as penny-precise trade levels.
- High unsigned gamma as a directional signal.
- High unsigned gamma as a hard entry/chase veto.
- High unsigned gamma as a production target-sizing rule.
- The QQQ 2026 gap-gamma continuation effect as a general market rule.

## Do Not Re-Test Unless
- Do not resurrect the failed QQQ gap-continuation rule by changing gap threshold, DTE, moneyness, near-gamma band, IV filter, or OPEX exclusions.
- Do not tune 2020–2025 unsigned-gamma thresholds to force the 2% forecasting gate.
- Do not soften the failed Pass-11 veto using the same 2017–2019 outcomes and call it validation.
- Do not lower the Pass-12 0.60 target threshold, change the target ladder, or otherwise tune on the same 2012–2013 outcomes to create target changes.
- Do not treat public open interest as observed dealer inventory.
- Do not make exact wall/pinning behavior the next priority without materially stronger data/evidence.
- Further unsigned-gamma testing requires a genuinely new economic question and untouched data; otherwise treat the branch as sufficiently explored for now.

## Next clean research priority
**Dealer-sign data/source audit before a signed-GEX outcome test.** Determine whether accessible historical sources provide participant-class dealer/customer positioning, signed option flow, historical dealer inventory proxies, SPX/SPXW coverage, separate 0DTE vs longer-dated contributions, and intraday underlying liquidity/price data.

If only an OI sign heuristic is available, the next experiment must be explicitly labeled a **proxy-method replication** and include robustness to alternate sign assumptions. Price must continue to supply direction; signed GEX may only modify expected continuation/reversal/amplitude.
