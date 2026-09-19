# Investing OS — Options Positioning Research Status

As of: 2026-09-19

This file is a compact status index. Original frozen specifications and result files remain authoritative.

## 1. Dealer Structure / GEX regime
- File: `research/options_positioning_dealer_structure_v1.md`
- Preliminary result: negative-gamma regimes may be associated with larger subsequent moves / amplification after price confirmation; positive gamma may be more damped.
- Direction from gamma sign is **not supported**.
- Status: **PROMISING / RESEARCH-ONLY**.

## 2. QQQ OI Persistence v1.0
- Frozen spec: `research/qqq_oi_persistence_v1.md`
- Results: `research/results/qqq_oi_persistence_v1_results.md`
- 162 eligible sessions.
- Total delta-OI / volume persistence did not predict next-session magnitude or improve continuation.
- Call-vs-put buildup imbalance had essentially zero directional relationship.
- Status: **REJECTED FOR SCANNER PROMOTION**. Do not reintroduce raw OI persistence as a directional or strength factor.

## 3. QQQ Gamma Concentration / Pinning v1.0
- Frozen spec: `research/qqq_gamma_concentration_v1.md`
- Results: `research/results/qqq_gamma_concentration_v1_results.md`
- 165 sessions.
- Near-spot gamma concentration was associated with smaller next-session RTH high-low range; dominant-strike pinning and continuation claims did not hold cleanly.
- Walk-forward incremental gate failed.
- Status: **RESEARCH-ONLY**.

## 4. Overnight vs RTH Decomposition v1.0
- Results: `research/results/qqq_gamma_rth_decomposition_v1_results.md`
- Gamma concentration had little relationship to overnight gap size but stronger association with RTH range compression.
- Secondary finding: among gaps >=0.25%, near-spot gamma was positively associated with same-direction gap follow-through.
- Walk-forward gate failed.
- Status: **RESEARCH-ONLY**.

## 5. QQQ Gamma Path Efficiency v1.0
- Frozen spec: `research/qqq_gamma_path_efficiency_v1.md`
- Results: `research/results/qqq_gamma_path_efficiency_v1_results.md`
- 165 full-history 60m sessions + 40 recent 5m robustness sessions.
- Generic path-efficiency hypothesis did **not** survive chronological stability / 5m robustness / walk-forward promotion gates.
- Descriptively, above-median near gamma had higher 60m path efficiency (0.464 vs 0.376) and fewer reversals, but the relationship was largely first-half-driven and did not hold cleanly in the second half or 5m efficiency metric.
- Secondary gap-conditioned result remained notable: near-gamma share vs `GAP_ALIGNED_EFFICIENCY` rho=+0.267, p=0.0034 over 119 60m gap sessions; first half rho=+0.333, second half +0.191; recent 5m rho=+0.359 (p=0.061, n=28). This result is **not promoted** because it was secondary in the frozen test.
- Status: **RESEARCH-ONLY**.

## Current production policy
No options-positioning research from these tests may independently:
- create BUY / SELL / CALL / PUT / HOLD,
- increase STRENGTH or RUNWAY,
- manufacture R:R,
- override price confirmation, event risk, OPEX/triple-witching warnings, or overnight rules.

Price gets final vote.

## Next clean research candidate
Freeze a dedicated **gap-conditioned gamma continuation** experiment before testing it. The question should be whether, after a meaningful overnight gap has already supplied direction, near-spot gamma predicts cleaner same-direction RTH follow-through / lower reversal risk. This must be treated as a new hypothesis because the encouraging result above was secondary and therefore cannot be promoted from the current test.
