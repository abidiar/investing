# VWAP execution-quality audit — 2026-10-09

Status: RESEARCH ONLY; NOT EXECUTION-CERTIFIED.

Frozen rule: see vwap_entry_protocol_2026_10_09.md.

## Findings

1. Webull daily historical OHLC prices differ materially from intraday five-minute OHLC prices on the same dates, consistent with different corporate-action adjustment bases. Examples daily open versus first 5-minute open: ORCL 2025-04-01 136.892154 vs 139.76; COST 2025-12-11 872.011341 vs 875.28; PYPL 2025-01-13 81.283534 vs 82.11; AAPL 2024-03-04 174.250382 vs 175.84. Daily signal filters used daily series; execution simulation used only intraday series, so percentage outcomes are not directly generated from mixed prices, but signals need point-in-time corporate action verification.
2. Earlier-period 2022-2024 pilot: 41 original eligible signals; 41 next-open trades; 23 VWAP-confirmed trades, 18 no entries. Modeled target-first 16/41 at open and 15/23 at VWAP. Gross summed returns +1.604 percentage-points across 41 open trades and +26.786 percentage-points across 23 VWAP trades; after 0.20% per trade: open -0.161% net per signal, VWAP +0.541% net per original signal and +0.965% per entered trade.
3. Sensitivity to total round-trip friction: VWAP net per original signal at 0.20% cost +0.541%; 0.50% cost +0.373%; 1.00% cost +0.092%. The latter is very fragile. This does not include gap/market-impact uncertainty beyond modeled fills.
4. Earlier-period simulation requested 220 historical 5-minute bars ending after the second trading session, and required exactly 78 RTH bars on each of the two sessions; 41 of 41 passed this session-count check. This does not independently certify minute-level price quality, halts, or all corporate actions.
5. The 2025-2026 pilot used a different VWAP entry cutoff implementation and a weaker completeness check, so its 22 events are not directly poolable. Rerun all 22 under the frozen rule and strict 78+78 bar coverage before pooled reporting.
6. Intra-bar target-versus-stop sequence remains unobservable from 5-minute OHLC; stop-first rule is conservative but real fills and spreads may differ. A next-bar open fill is hypothetical. Provider historical prices and live tradability remain distinct.
7. Prior seven-stock and 20-stock universes were selected, not point-in-time market-wide cohorts. Earlier years are retrospective validation, not a fully untouched holdout.

## Gate to promote

Do not label validated or automatically issue BUY. Reconcile daily vs intraday corporate-action adjustments; independently check opening prices against as-traded source; rerun all 63 events under same frozen rule; add cost and slippage stress tests; verify sample robustness across tickers and time periods; forward paper trade without rule changes.
