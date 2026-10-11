# Frozen 52-contract historical options data bottleneck: complete access and traded-volume audit
Research finalized 2026-10-10 (U.S. Eastern). **Research-only: not verified option execution, no A+ edge.**

## Research question and fully fixed candidate list
After the 100-event 2024/25 earnings-rebound historical EOD quote study, exactly 52 **method×expiry cells** had an affordable observed *EOD ASK* on entry calendar date. They were pre-enumerated, with exact historical OCC symbols and entry/exit dates, in `frozen_100event_52_eod_affordable_contracts_for_volume_repair_2026-10-10.json`. All 52 have now been subjected to provider historical option-trade data access checks (some requests yielded entitlement/rate errors). The 52 are NOT randomly sampled, NOT every actual listed call, and not the strict frozen **first-option-trade, >=10 total entry-day option-contracts** strategy. Source results: `frozen_52_contract_volume_reconciliation_2026-10-10.json`; reproducible Node reconciliation: `reconcile_52_contract_volume_research_2026-10-10.cjs`. Historical primary market data retrieved using connected Massive options daily trade OHLCV; the earlier free DoltHub EOD bid/ask snapshot remains the source of the initial 52 candidates. No paid data.

### Historical data availability and entry rule audit

| Exact frozen candidate cell status | 2024 | 2025 | Total |
|---|---:|---:|---:|
| Frozen EOD-ask-affordable contract candidates | **21** | **31** | **52** |
| Historical option daily TRADE bars successfully returned | 8 | 29 | **37** |
| First option trade debit <=$50 incl $0.65, >=10 contracts traded on entry DATE | **5** | **12** | **17** |
| First trade price exceeds $50 budget | 0 | 2 | **2** |
| Recorded entry trade but <10 option contracts traded that date | 2 | 9 | **11** |
| No recorded option trade on specific entry date in returned bars | 1 | 6 | **7** |
| Provider NOT_ENTITLED for older history | 10 | 0 | **10** |
| Provider response EMPTY (contract history unavailable) | 1 | 2 | **3** |
| Other unresolved provider errors/rate limits | 2 | 0 | **2** |

Source statuses are **not outcomes** and aren't counted as winners/losers. Date-volume `v` is count of option contracts traded; `n` is number of transactions. The DoltHub EOD `vol` field means implied volatility, **not traded volume**. All 31 sampled **2025 contracts had provider requests completed**; the two EMPTY remain unknown market histories, not worthless options. Many 2024 dates prior to Oct 2024 were NOT_ENTITLED on connected free access, while late-2024 histories were often returned successfully.

**What is not proven:** closest affordable strike from the *full* as-of-event listed chain, actual 9:30 call ask, an exit bid synchronized to underlying barrier, or reliable ability to purchase/sell at daily first/last prints. The 52 candidate cells were EOD ASK-selected, so even a passing first-trade/volume contract is merely eligible *among sampled EOD candidates*, not necessarily the strike that original strict strategy would select.

### Observed quote-independent historical TRADE-PRINT marks
Among the 17 sampled-contract budget + daily-volume passes, **15** have an option last TRADE price recorded ON the recomputed unadjusted stock exit DATE. Using first option trade price that day for purchase and final option trade that same date for sale, plus $0.65 fee EACH way, yields:
- **2024:** 5 markable candidate cells, 3 positive and 2 negative; arithmetic mean +104.0%, median +1.7% (large 2024 PayPal +323.9% and Target +323.6%).
- **2025:** 10 markable candidate cells, 2 positive and 8 negative; arithmetic mean −44.0%, median **−78.6%**.
- **Combined:** 15 markable cells, 5 positive and 10 negative; conditional arithmetic mean **+5.4%**, conditional median **−64.7%**. The average is driven by large, non-independent, time-mismatched historical outliers. **These are NOT a strategy win rate, return, or fill record.**

Some specific 2025 *daily first-to-last trade-print* examples after hypothetical fees:
| Contract | Entry first trade ×100 plus $0.65 | Entry daily contracts traded | Exit-day last trade mark ×100 minus $0.65 | Conditional print-to-print return |
|---|---:|---:|---:|---:|
| AMAT June 20 $195C (May21 entry) | $31.65 | 20 | $4.35 | **−86.3%** |
| AMAT Sep 19 $190C (Aug20 entry) | $39.65 | 1,510 | $11.35 | **−71.4%** |
| CSCO Sep19 $70C (Aug20 entry) | $45.65 | 3,981 | $2.35 | **−94.9%** |
| CSCO Sep26 $73C (Aug27 entry) | $22.65 | 22 | $0.35 | **−98.5%** |
| Disney Dec19 $120C (Nov18 entry) | $21.65 | 432 | $9.35 | **−56.8%** |
| Comcast Mar7 $35C (Feb4 entry) | $23.65 | 63 | $61.35 | **+159.4%** |
| HPE Apr17 $17C (Mar18 entry) | $27.65 | 44 | $43.35 | **+56.8%** |

**Date and fill corrections:** UPS Feb4 entry, March7 $121C has first trade $0.29 with 27 entry-day contracts, so it passes the historic first-trade/volume screen. Original dividend-adjusted stock +5% exit Feb18 was WRONG; unadjusted first +5% stock touch was Feb24 at 09:50 ET and first subsequent five-minute option trade 09:55 ET at $0.52, an **illustrative +73.2%** first-to-next option print outcome. Prior original Feb18 last option print at $0.25 MUST NOT be used as the actual stock-trigger exit or a −17.9% trade. See `raw_stock_price_dividend_exit_audit_100events_2026-10-10.json` and `repair_exit_timestamp_raw_stock_CMCSA_UPS_2026-10-10.json`. Comcast's +5% stock target first hit Feb6 12:25 ET with next option trade 12:35 ET at $0.55 vs Feb4 first print $0.23, or **illustrative +129.8%**. NONE of these prints is an observed executable option bid at the instant stock crossed target; thus the separate +159.4% day-last mark is not the realized +5% target trade.

Other remaining marked losses include DOW Mar21 $42.5C ~−85.9%, PYPL Mar21 $90C ~−64.7%, ZBH Dec19 $110C ~−97.8%. 2024 KDP same-event 30/60D calls had approximately −71.4%/−57.6% print-to-print returns, while PYPL late2024 and Target late2024 had >+320% each. **Do not pool multiple expirations on the same underlying event as independent wins/losses**.

### NEW methodological bottleneck: historical daily volume is forward-looking for next-open entry
Even for the 17 EOD-selected cells meeting 10 or more entry-DATE contracts traded in hindsight, **total entry-DATE option trade volume is NOT KNOWN at the STOCK's NEXT OPEN (the frozen entry time)**. The first option trade of the day may take place after that stock opening; an observed trade price cannot be assumed available to buy at 09:30. Therefore `first option trade on entry date + whole-entry-day traded volume >=10` is a **RETROSPECTIVE feasibility screen, NOT a non-lookahead, executable 9:30 stock-trigger rule**. Using it to pick contracts when backtesting a 09:30 call purchase would create selection/timing leakage.

To properly study a *historical* actionable version, freeze and evaluate an **as-of-entry liquid-contract selection rule** using only:
1. Actual **previous trading day** contract-level volume and bid/ask/open interest, where archived;
2. Or strictly option trade prints/option quote spread observed **at/before** the proposed option purchase timestamp (e.g., enter following confirmation at 9:45/10:00 rather than pretend full-day volume was known at 9:30).
3. Full as-of-date listed strike and expiration coverage, with $50 contemporaneous ask, strict no lookahead and correct historical unadjusted equity stock targets.
4. Real contemporaneous bid at stock-trigger exits if a freely available dataset can supply it; otherwise report best-available next option trade and uncertainty, **never call it realized fill**.

This is a FURTHER research experiment, not a revision of today's frozen 52 candidates, and should be precommitted prior to examining its returns. No shadow test or paid feed is required to continue historical TRADE feasibility analysis, but no-cost intraday NBBO quote series for 2024/25 currently has NOT been verified.

## Bottom line
**Completed 52/52 source checks** (37 price/volume returns, 10 inaccessible older option histories, 3 empty, 2 source failures); screened affordability/volume for 37 returned histories, of which 17 EOD-selected calls passed. Only 15 had both daily option first-entry print and correct raw-stock-date exit last print to compute limited print-to-print sensitivity. These historical observations are conditional, correlated, often illiquid and far OTM, inconsistent between 2024/25, and do NOT establish a profitable options-rebound trading edge or justify scanner promotion.

### Source documents
- `frozen_100event_52_eod_affordable_contracts_for_volume_repair_2026-10-10.json` (all exactly frozen 52 candidate events and OCC contracts)
- `frozen_52_contract_volume_reconciliation_2026-10-10.json` (all source statuses, actual contract volume, first/last print prices, raw exit diagnostics)
- `reconcile_52_contract_volume_research_2026-10-10.cjs` (repeatable offline aggregation)
- `volume_repair_massive_historical_trade_probes_phase[1/2]_2026-10-10.json` and all historical `volume_repair_2024/2025_remaining_phase*.json` probe archives
- `raw_stock_price_dividend_exit_audit_100events_2026-10-10.json`
- `repair_exit_timestamp_raw_stock_CMCSA_UPS_2026-10-10.json`
