# Investing OS Research — Master Status

Updated: 2026-09-19
Status: **CANONICAL CROSS-TOPIC INDEX**

This file is the concise cross-chat research state. Detailed frozen protocols, code, and results remain in their topic files. Governance is defined in `research/RESEARCH_GOVERNANCE.md`.

## Current production posture
- **Price gets final vote.**
- No research-only options-positioning feature may independently create direction, add STRENGTH/RUNWAY, manufacture R:R, or authorize BUY/SELL/CALL/PUT/HOLD/overnight carry.
- Quarterly expiration/rebalance risk is a standing scanner gate and must be surfaced prominently.
- A finding enters production only after its preregistered promotion standard passes.

## Options-positioning / gamma research status

### Pass 1 — Dealer/GEX regime
Verdict: **PROVISIONAL / RESEARCH-ONLY**.
Signed/modelled dealer-gamma regime may be useful for amplification/damping conditional on independent price confirmation. Raw GEX direction, exact wall/flip precision, and wall proximity alone are not promoted.

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
A strong 2026 QQQ gap-follow-through association appeared, but it was not promoted because walk-forward incremental utility failed.

### Pass 7 — SPY 2025 independent replication
Verdict: **FAILED REPLICATION**.
The QQQ directional gap-continuation relationship did not generalize to SPY.

### Pass 8 — QQQ 2025 time-shift replication
Verdict: **FAILED REPLICATION**.
The QQQ 2026 directional gap-gamma result did not replicate in QQQ 2025. Treat the original directional effect as regime/source-specific, not durable.

### Pass 9 — Multi-year unsigned near-spot gamma compression
Verdict: **REPLICATED ASSOCIATION / RESEARCH-ONLY**.
Across 2,221 SPY/QQQ/IWM observations in 2023–2025, higher near-spot unsigned gamma associated with smaller next-session RTH range and excursion. The raw association was broad and stable, but price-volatility variables captured most practical forecasting value.

### Pass 10 — Untouched 2020–2022 incremental-value holdout
Verdict: **CONDITIONAL ASSOCIATION / RESEARCH-ONLY**.
Across 2,262 untouched observations, the compression relationship survived seven price-volatility controls, instrument/year checks, and non-OPEX robustness. Gamma improved walk-forward MAE only 1.26% for next RTH range and 1.33% for max excursion, below the frozen 2% promotion gate. Conclusion: gamma contains a small real additive amplitude signal, but not enough for production authority.

### Pass 11 — Decision-level chase/veto falsification
Files:
- `research/gamma_chase_decision_v1.md`
- `research/results/gamma_chase_decision_v1_results.md`

Verdict: **FAILED DECISION-LEVEL OVERLAY**.
Untouched holdout: 1,195 SPY/QQQ/IWM candidates in 2017–2019, trained on 2014–2016. A gamma compression veto improved T1 precision from 69.39% to 73.97% (+4.58 pp), and vetoed candidates had a worse T1 miss rate (44.0% vs 30.61%), so gamma identified some weaker chases. But the overlay retained only 79.41% of baseline winners versus the frozen >=85% requirement, and price+gamma Brier improvement was only 0.38% versus the frozen >=2% requirement. **Unsigned gamma must not be used as a hard entry/chase veto.**

### Pass 12 — Target-calibration decision falsification
Files:
- `research/gamma_target_calibration_v1.md`
- `research/results/gamma_target_calibration_v1_results.md`

Verdict: **FAILED DECISION-LEVEL TARGET OVERLAY**.
Untouched holdout: 799 SPY/QQQ/IWM candidates in 2012–2013, trained from a 2011 seed. All entries were retained and gamma could only alter target ambition on a frozen 0.50/0.75/1.00 × trailing-20 median-range ladder. Price-only and price+gamma both produced 0.21% mean captured target distance, 40.55% hit rate, and identical targets on all 799 candidates. Both chose T1 on 99.87% of events. Adding gamma worsened average Brier performance across T1/T2/T3 by 0.82%. Frozen capture, bootstrap, and cross-instrument/year gates failed. **Unsigned gamma must not be used as a production target-sizing rule.**

## What is rejected / not production-eligible
- Raw OI as bullish/bearish direction.
- Call-vs-put OI buildup as direction.
- Delta-OI/volume persistence as a next-day movement/continuation edge.
- Large gamma wall as an automatic magnet.
- Exact gamma-wall/flip levels as penny-precise trade levels.
- High unsigned gamma as a directional signal.
- High unsigned gamma as a hard chase/entry veto.
- High unsigned gamma as a production target-sizing rule.
- The QQQ 2026 gap-gamma continuation effect as a general market rule.

## What remains alive
- Signed/modelled dealer GEX as a potentially distinct amplification/damping mechanism, still needing larger independent validation.
- Unsigned near-spot gamma as a small, non-directional next-session amplitude/compression association, **research/context-only** after failing two practical decision-level overlays.

## Do Not Re-Test Unless
- Do not resurrect the failed QQQ gap-continuation rule by changing gap threshold, DTE, moneyness, near-gamma band, IV filter, or OPEX exclusions.
- Do not tune the 2020–2025 unsigned-gamma thresholds to force the 2% forecast gate.
- Do not convert the failed Pass-11 veto into a softer threshold chosen from the same 2017–2019 outcomes and call it validation.
- Do not lower the Pass-12 0.60 target threshold, change the target ladder, or tune on the same 2012–2013 outcomes to create target changes.
- Further unsigned-gamma work requires a genuinely new economic question plus untouched data; otherwise treat this branch as sufficiently explored.

## Next clean research priority
**Shift to signed/modelled dealer-GEX amplification/damping.** Before outcome testing, freeze a source/methodology audit because dealer-side sign is model-assumed and GEX formulas differ by provider. Then test on an independent multi-year sample where **price supplies direction** and signed GEX is allowed only to modify expected move behavior (amplification/damping), never direction. Require a price-only baseline and preregistered promotion gates.

## Key locations
- Governance: `research/RESEARCH_GOVERNANCE.md`
- Start-here bootstrap: `INVESTING_OS_RESEARCH_START_HERE.md`
- Detailed options status: `research/options_positioning_research_status.md`
- Frozen protocols/code/results: `research/` and `research/results/`
- Google Doc human-readable ledger: **Investing OS Research Ledger — Canonical**, document ID `1MxHv5HPlr1Ab9A8cb3diPUtBJv6fWgNZwhhrw72zAus`
- Live Investing OS Sheet: spreadsheet ID `14lTnD-on91I4F5E5FAQ8-39zTRv2GzBjyd1b4_uCzjc`
