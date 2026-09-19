# Investing OS — Options Positioning Research Status

Updated: 2026-09-19

## Current production posture
Options-positioning research remains **context-only / research-only**. No tested options-positioning feature may independently create direction, add STRENGTH/RUNWAY, manufacture R:R, or authorize BUY/SELL/CALL/PUT/HOLD/overnight carry. Price gets final vote.

## Pass 1 — Dealer/GEX regime
File: `research/options_positioning_dealer_structure_v1.md`

Provisional finding: signed/modelled dealer-gamma regime appears more useful for expected move behavior than direction. Negative gamma may amplify an independently confirmed move; positive gamma may dampen it. Small sample; not promoted to action gate.

Rejected/not promoted: raw GEX direction, exact wall/flip precision, wall proximity alone.

## Pass 2 — QQQ settled OI persistence
Files:
- `research/qqq_oi_persistence_v1.md`
- `research/results/qqq_oi_persistence_v1_results.md`

Verdict: **NOT SUPPORTED**.

Across 162 sequential sessions, delta-OI/volume persistence did not predict larger next-session movement and did not improve continuation after a meaningful Day-T move. Call-vs-put buildup imbalance had essentially zero directional relationship with next-session return. Do not promote raw delta OI, persistence, or call/put buildup direction.

## Pass 3 — QQQ gamma concentration / pinning
Files:
- `research/qqq_gamma_concentration_v1.md`
- `research/results/qqq_gamma_concentration_v1_results.md`

Verdict: **RESEARCH-ONLY**.

Near-spot unsigned gamma concentration was associated with smaller next-session RTH high-low range, with expected-sign stability and stronger evidence in the second half. However, it did not materially reduce absolute close-to-close movement, pinning to a dominant strike failed, and the extended walk-forward model did not satisfy the frozen promotion gate.

## Pass 4 — Overnight vs RTH decomposition
Files:
- `research/qqq_gamma_rth_decomposition_v1.md`
- `research/results/qqq_gamma_rth_decomposition_v1_results.md`

Verdict: **RESEARCH-ONLY**.

Near-spot gamma concentration was more clearly associated with RTH range compression than overnight-gap magnitude. Full-sample rho for near-spot gamma vs RTH range was -0.220 (p=0.0045) versus -0.061 for absolute overnight gap. Walk-forward improvement was insufficient for promotion.

## Pass 5 — QQQ gamma path efficiency
Files:
- `research/qqq_gamma_path_efficiency_v1.md`
- `research/results/qqq_gamma_path_efficiency_v1_results.md`

Verdict: **RESEARCH-ONLY / BROAD PATH-EFFICIENCY HYPOTHESIS FAILED STABILITY**.

The apparent relationship between higher near-spot gamma and cleaner RTH path was concentrated in the first half and disappeared in the second half and recent 5-minute robustness sample. Walk-forward prediction worsened. A narrower secondary gap-conditioned signal remained interesting but required a dedicated test.

## Pass 6 — QQQ gap-conditioned gamma continuation
Files:
- `research/qqq_gap_gamma_continuation_v1.md`
- `research/results/qqq_gap_gamma_continuation_v1_results.md`

Verdict: **RESEARCH-ONLY**.

On 119 QQQ sessions with abs(overnight gap) >=0.25%, higher prior-day near-spot gamma was associated with better same-direction follow-through (rho=+0.277, p=0.0023), better excursion efficiency (rho=+0.286, p=0.0016), and lower adverse excursion (rho=-0.355, p=0.0001). The expected sign persisted across chronological halves for the two primary relationships and outside OPEX. However, the extended walk-forward model failed the frozen incremental-usefulness gate, so no promotion was allowed.

## Pass 7 — SPY 2025 independent replication
Files:
- `research/spy_gap_gamma_replication_v1.md`
- `research/results/spy_gap_gamma_replication_v1_results.md`

Verdict: **FAILED REPLICATION**.

This replication used SPY rather than QQQ and calendar-2025 options snapshots, with no 2026 QQQ observations. There were 129 qualifying abs(gap)>=0.25% sessions and the same frozen gamma construction/thresholds.

The primary QQQ relationship did **not** generalize:
- near gamma -> gap follow-through: rho=+0.054, p=0.547 full sample; second half rho=-0.172
- near gamma -> excursion efficiency: rho=-0.036, p=0.690 full sample; second half rho=-0.202
- near gamma -> MFE was significantly negative rather than positive (rho=-0.308, p=0.0004)

A lower-adverse-excursion relationship survived in the full SPY sample (near gamma -> MAE rho=-0.248, p=0.0045) and non-OPEX sample, but it failed chronological stability because the second-half sign turned slightly positive. Descriptively, higher-gamma SPY gaps continued 53.1% vs 46.2% for lower gamma, far smaller than the prior QQQ 61.0% vs 36.7% separation.

Walk-forward performance materially worsened when gamma features were added: follow-through MAE -18.4% improvement (worse), excursion-efficiency MAE -2.8% (worse), and MAE-from-open prediction -21.7% (worse). Therefore the QQQ gap-gamma effect must be treated as **sample/instrument-specific until proven otherwise**, not as a general scanner edge.

## Current best interpretation
- Raw OI: not directional.
- Delta-OI persistence: not useful enough for next-session movement/continuation.
- Large gamma wall: not automatically a magnet.
- Near-spot unsigned gamma concentration may relate to RTH range/excursion structure in some samples, but its relationship with directional gap continuation is **not independently replicated across SPY 2025**.
- The QQQ gap-conditioned result is downgraded from promising-generalizable to **QQQ/2026-specific hypothesis requiring further independent replication**.
- Signed/modelled dealer GEX may still matter for amplification/damping, but requires larger independent validation.

## Next clean falsification
Use the same frozen gap-conditioned gamma rules on **QQQ 2025** from the independent historical-options archive. This isolates whether the failed SPY replication reflects an instrument difference (SPY vs QQQ) or a regime/sample difference (2025 vs 2026). Do not alter the >=0.25% gap threshold, 1–30 DTE universe, ±5% moneyness, ±0.50% near-gamma zone, 1–7 DTE front bucket, IV filter, or promotion gates before that test.
