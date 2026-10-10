# Unified frozen VWAP entry rerun — 2026-10-09

Protocol: `vwap_entry_protocol_2026_10_09.md`. This is research only, not a validated live trading signal.

## Execution
All 22 later-period events (2025–2026) re-executed with identical frozen next-day five-minute VWAP condition and cutoff; 78 RTH M5 candles in each of two sessions for every event. No intra-bar simultaneous stop/target in these 22 event simulations. Entries use next-bar opening price, stop-first on ambiguity, +2% target, -2% stop, second-session close expiration, missed signals zero return. VWAP computed from typical price times volume.

## Results

2022–2024 (41 original signals): open 41 entries, 16 target-first, gross sum +1.604 percentage points, net per signal -0.161% at 0.20% per trade; VWAP 23 entries, 15 target-first, gross sum +26.786 points, net per signal +0.541%, net per entry +0.965%.

2025–2026 (22 original signals): open 22 entries, 11 target-first, gross sum +9.158 points, net per signal +0.216%; VWAP 15 entries, 9 target-first, gross sum +16.9768 points, net per signal +0.635%, net per entry +0.932%.

Pooled descriptive, not independent holdout (63 original signals): open 63 entries, 27 target-first (42.9%), gross sum +10.762 points; VWAP 38 entries, 24 target-first (63.2%), gross sum +43.7628 points. At 0.20% total round-trip cost: open net per original signal -0.029%; VWAP +0.574%, VWAP net per entered trade +0.952%. At 0.50% friction: open -0.329% per original signal, VWAP +0.393%. At 1.00% friction: open -0.829%, VWAP +0.092%.

## Remaining quality gates
Daily signal series has different corporate-action adjustment basis from as-traded intraday candles. Need point-in-time daily-signal consistency checks and split/dividend reconciliation, gap/slippage and spread sensitivity, event-level immutable dataset, cross-ticker robustness, independent forward paper trading. Prior period and universe were researched, not pristine out-of-sample. Do not promote to live BUY.
