# Early Range Reversal Detector v1.0 (research-only)

Purpose: detect support approaches BEFORE the bounce; do not change frozen A+ rules. No orders.

Stages: NO TRADE -> EARLY WATCH (within 0.5 ATR of precommitted support, >=2 dated touches, range >=1.5 ATR) -> FAILURE TEST WATCH (completed-bar penetration, failed extension and reclaim) -> ENTRY WINDOW (higher low and completed-bar price/volume proxy) -> BUY ON TRIGGER only with future trigger, structural stop, >=2:1 executable R:R, remaining runway and market checks; otherwise EXPIRED/NO CHASE.

Require support published timestamp preceding test; record support weakening, range age, ATR/ADR, sector/SPY/QQQ, catalysts and gap risk. Experimental alert if no more than 25–35% of range consumed. VWAP and RSI never establish expectancy. Rob Hanna proprietary/stale measures UNKNOWN/RESEARCH ONLY. No options recommendations without live ask, spread, strike, expiry, DTE, delta, IV, theta and budget verification. Negative independent 49-issuer replication remains the base-rate caution.

At 3pm future 10:30–12 confirmation: NEXT SESSION 10:30–12 CONFIRMATION PENDING. Log immutable timestamp, all alerts and abstentions, first target/stop, overnight gap, MFE/MAE, and same-date sector/volatility benchmarks. Compare first reclaim vs higher-low vs late confirmation using frozen rules and failed cases; no hindsight relabeling.

Implementation draft available as early_range_reversal_v1.py in this conversation. This document specifies experimental rules, not a validated live scanner.