# Investing OS — Options Positioning Research Status

Updated: 2026-09-19

## Current production posture
Options-positioning research remains **context-only**. No tested options-positioning feature may independently create direction, add STRENGTH/RUNWAY, manufacture R:R, or authorize BUY/SELL/CALL/PUT/HOLD/overnight carry. Price gets final vote.

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

Key result: near-spot gamma concentration is much more clearly associated with **RTH range compression** than with overnight-gap magnitude. Full-sample Spearman rho for near-spot gamma vs RTH range was -0.220 (p=0.0045) versus -0.061 for absolute overnight gap. The frozen range differential was +0.159 and remained negative for RTH range in both chronological halves.

However, near-spot gamma did **not** consistently damp absolute RTH open-to-close displacement in the full sample, and the walk-forward model improved RTH-range MAE only 1.18%, below the frozen 2% threshold while worsening absolute RTH O/C MAE by 1.35%. Therefore no scanner promotion.

Secondary result requiring independent retest: on sessions with an overnight gap >=0.25%, higher near-spot gamma was positively associated with same-direction gap follow-through (rho=0.277, p=0.0023), contrary to a simple 'high gamma means fade' story. This may indicate a narrower/cleaner directional path rather than mean reversion, but it was secondary and cannot be promoted from this pass.

## Current best interpretation
The surviving hypothesis is narrower than common gamma narratives:

- Raw OI: not directional.
- Delta-OI persistence: not useful enough for next-session movement/continuation.
- Large gamma wall: not automatically a magnet.
- Near-spot gamma concentration: may compress **intraday excursion/range**, especially in recent data, without necessarily suppressing overnight displacement or net directional close-to-close movement.
- Signed/modelled dealer GEX may still matter for amplification/damping, but requires larger independent validation.

## Next clean falsification
Use historical intraday QQQ bars to decompose the RTH path into predeclared windows (open->10:10, 10:10->12:00, 12:00->15:30, 15:30->close), plus MFE/MAE and path efficiency. Test whether high near-spot gamma predicts a narrower/more efficient path rather than generic mean reversion. Freeze the windows and metrics before reading outcomes. Prefer an independent/expanded sample if a compatible options archive becomes available.
