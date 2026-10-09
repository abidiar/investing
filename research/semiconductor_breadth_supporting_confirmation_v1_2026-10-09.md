# Semiconductor breadth — supporting confirmation v1.0

Status: operational interpretation overlay, NOT a new validated signal or modification of frozen A+ detector. Adopted 2026-10-09 at user request. No backtest edge claimed.

## Inputs
- SPY: primary 5-minute price, VWAP, structure, volume and frozen A+ gates remain authoritative.
- SMH: semiconductor sector proxy; check its own intraday VWAP and 5-minute structure.
- Breadth watch: NVDA, AMD, AVGO, MU, each evaluated versus its own VWAP and recent 5-minute structure. Four names are contextual, not a statistically calibrated universe. SOXX can be a substitute for SMH if data unavailable; do not double-count as independent confirmation.
- Observe only timestamp-aligned regular-hours quotes; if stale/missing, say UNAVAILABLE, not bearish or bullish.

## Qualitative supporting labels
- SEMI CONFIRMS CALL: SMH above own VWAP and at least 3 of 4 watch names above their own VWAP, with no obvious opposing lower-high structure. Supports an otherwise independently confirmed SPY bullish setup.
- SEMI CONFIRMS PUT: SMH below own VWAP and at least 3 of 4 watch names below their own VWAP, with no obvious opposing higher-low/reclaim structure. Supports an otherwise independently confirmed SPY bearish setup.
- SEMI DIVERGENCE: SPY and SMH have opposite VWAP positioning or direction; caution / reduce confidence, NOT automatic reversal prediction.
- SEMI MIXED: no 3/4 alignment or SMH ambiguous; no directional confirmation.
- SEMI UNAVAILABLE: insufficient fresh data.

These are simple operational heuristics, not fitted thresholds or demonstrated alpha. Do not call a mere VWAP cross a completed five-minute hold. Prefer completed five-minute candles and note if first 5–15 minutes are noisy.

## Decision authority and output
- Frozen A+ CALL/PUT/WATCH/NO TRADE logic remains unchanged. Semi labels appear as secondary context only, never veto or upgrade a failed gate to A+.
- Savino timing and Crom alerts remain separate contextual overlays; never double-count as independent statistical evidence.
- On each requested live assessment, display: SPY price vs VWAP; SMH price vs VWAP; watchlist breadth n/4; semi label; whether it supports or conflicts with the SPY price setup. Report unavailable data honestly.
- Do not claim causation, forward predictive ability, hit rate, or option return without separate preregistered validation. No new scheduled tasks or alerts.
