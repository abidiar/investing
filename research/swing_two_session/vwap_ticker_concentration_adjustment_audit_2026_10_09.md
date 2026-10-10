# VWAP ticker concentration and corporate-action audit — 2026-10-09

Status: PARTIAL AUDIT; not execution certified.

## Ticker concentration
Reconstructed from prior event-level 63-signal simulations (2022–2026). At assumed 0.20 percentage-point round-trip friction, total VWAP net contribution across original signals is +36.163 percentage points, approximately +0.574% per original signal.

19 tickers had at least one eligible signal. Of these, 12 had positive net contribution, 3 negative, and 4 had no VWAP entry. INTC had no eligible signal.

Leading net contribution in summed percentage points: AMZN +9.917 (6 signals/5 trades), QCOM +7.210 (4/4), XOM +4.702 (4/4). Top three sum +21.829, or 60.4% of total; remaining 16 tickers sum +14.334. Other positive: META +3.600, JPM +3.600, ORCL +3.600, CRM +2.535, CAT +2.024, PYPL +1.800, UBER +1.800, HD +0.461, MSFT +0.420. Negative: COST -3.335, GOOG -1.771, DELL -0.400. No entry: AAPL, LLY, AMD, BAC.

## Price adjustment audit
Webull historical daily OHLC is not on the same price basis as five-minute OHLC. Verified example daily open vs first five-minute open: ORCL 2025-04-01 136.892154 vs 139.76; COST 2025-12-11 872.011341 vs 875.28; PYPL 2025-01-13 81.283534 vs 82.11; AAPL 2024-03-04 174.250382 vs 175.84. In LLY 2023-01-24 daily open 373.611461 vs five-minute 365.22, an especially large difference. The audit cannot attribute all differences exclusively to dividends or splits without provider adjustment metadata and corporate action history. Intraday fills use a single intraday price basis, but event detection uses daily adjusted series; point-in-time eligibility remains unverified.

## Quality gates
- Completed: strict 78+78 RTH bar coverage for 63 events in two-period test, identical frozen entry cutoff, stock-concentration sensitivity, total friction scenarios 0.20/0.50/1.00%.
- Outstanding: verify adjustment factors and corporate action dates, reconstruct as-traded daily bars from intraday or point-in-time adjusted daily feed, rederive signals and compare membership, event-level persisted canonical data, check entry timestamps and intrabar ambiguity with finer data, real spread/slippage, untouched forward paper-trading.
- Do not promote to automated BUY or claim an 80% target-first rate.

Note: this is a summary of already completed event-level tests; not a new full 63-event raw-bar download.
