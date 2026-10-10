# Next data bottleneck audit — free missing historical options exits, actual volume, and raw stock target alignment
Completed on 2026-10-10. **Research-only, exploratory, not a complete or executable options backtest.**

## Pre-frozen scope
Use all 100 previously qualified 2024–2025 events and their fixed day3 and rising-lows stock entry definitions, $50 total initial debit including $0.65 entry commission, >=10 entry-date option contracts traded, +5% stock profit vs −5% stop or 20 sessions, and 30/60 target-calendar-DTE with seven-day expiry grace. Retain all source-missing and non-signals. 2024–25 historical outcomes previously inspected; this is not a fresh OOS study.

Earlier completed source `free_100event_2024_2025_otm_options_results_2026-10-10.md` described 52 EOD-ask-affordable method×expiry observations, of which just 20 had same contract's EOD exit bid (17 separate events, 13 tickers). Exact frozen 52 metadata and OCC contract identifiers now permanently saved in `frozen_100event_52_eod_affordable_contracts_for_volume_repair_2026-10-10.json` **before** independent contract histories were fetched. Do not treat this option sample as the strict closest-first-trade affordable-strike selection (EOD selection differs).

## Provider access / exact-missing diagnostic — completed
1. **Public 104-symbol historical option parquet download is NOT currently accessible.** Actual HTTP HEAD from a GitHub Actions runner for QCOM/PYPL/TGT/TXN/ADBE/SPY files at `https://static.philippdubach.com/data/options/<ticker>/options.parquet` returned HTTP **404**; QCOM/PYPL Range GET returned **404** as well. Archived public repo URL is also unavailable; source-specific descriptions on cached search results are not present-day availability proof. Do not claim this provider supplied any data.
2. All **32 prior DoltHub exact-contract EOD exit-date gaps** were queried again, this time by **ticker+precise date+expiration+strike+call_put**, *without any spot/25%-OTM/expiry filters*. All queries returned status **Success** but **0 rows**. Thus the prior gaps are genuine SOURCE SNAPSHOT OMISSIONS, not an error from the original filtered SQL. This is NOT evidence that actual listed options lacked a price or volume on those days.
3. **Massive historical options daily TRADE OHLC**, when entitled and not rate-limited, does sometimes cover those same missing Dolt contract dates and gives per-day **option contracts traded** in `v`; `n` is number of trade transactions. This can repair the frozen volume check without paying for data, though it supplies trades, **not executable NBBO bids/asks**, and entitlement/rate limits vary by year/date. Preserved 13 targeted requests in `volume_repair_massive_historical_trade_probes_phase1_2026-10-10.json` and `volume_repair_massive_historical_trade_probes_phase2_2026-10-10.json`. Nine returned actual price bars, three rate-limited, one returned no records. These are TARGETED NONRANDOM investigations, not a 52-row audit or random estimate.

### Resolved 2025 contract-level volume evidence
All costs below are first observed option-trade OPEN ×100 +$0.65, not guaranteed opening ask/fill. The DOLT end-of-day ASK selection that nominated a contract is not the same selection as the frozen first-trade-at-entry/volume threshold. On this specific sampled strike:

| Frozen EOD candidate | First print | Contracts actually traded on ENTRY day | $50 / >=10-volume admissible? | Actual trade recorded on previous stock-exit calendar date? |
|---|---:|---:|---|---|
| DOW Mar7 $41C, Feb4 entry | $0.20 | 7 | **NO** volume | YES, last print $0.18 (was missing in Dolt) |
| UPS Mar7 $121C, Feb4 entry | $0.29 | 27 | **YES** on entry | YES, last print Feb18 $0.25 (Dolt missing, but wrong raw stock-target day—see below) |
| FIS Apr17 $77.50C, Feb14 entry | $0.25 | 1 | **NO** volume | No trade on recorded exit date |
| HPE Apr11 $16C, Mar12 entry | $0.49 | 1 | **NO** volume | No trade on recorded exit date |
| HPE May16 $17C, Mar12 entry | $0.52 | 30 | **NO** budget ($52.65) | YES, Mar18 last print $0.57. Apparent original EOD +47% candidate DOES NOT pass original first-trade $50 condition |
| FTNT Jun13 $118C, May13 entry | missing bars | unavailable | **UNVERIFIED** | no data |
| AMAT Jun20 $195C, May21 entry | rate limit | unavailable | **UNVERIFIED** | unknown |
| TPR Sep19 $115C, Aug19 entry | **NO entry-day trade** | unavailable | **NO verified entry** | YES, Sep3 last trade $0.39; Dolt EOD bid was $0.10, showing source/timing discrepancy |
| QCOM Sep05 $170C, Aug05 entry | $0.19 | 1 | **NO** volume | YES, Aug13 last trade $0.53; cheap but untradeably thin under frozen filter |
| CMCSA Mar07 $35C, Feb04 entry | $0.23 | 63 | **YES** on entry | YES, Feb06 last print $0.62 |
| TXN Aug29 $215C, Jul30 entry | $0.35 | 1 | **NO** volume | YES, Jul31 $0.26 |
| FTNT Sep12 $88C, Aug12 entry | rate limit | unavailable | **UNVERIFIED** | unknown |
| ZBH Dec19 $110C, Nov13 entry | rate limit | unavailable | **UNVERIFIED** | unknown |

Two observed sampled contracts met the exact $50 first-trade price AND >=10 entry-day volume conditions (UPS and CMCSA), but the strict **closest affordable historical strike across the FULL listed chain remains unproven**. Another previously probed PYPL Mar21 $90C Feb18 entry was also cheap/liquid but lost ~65% by the observed stock-stop next-trade mark; QCOM Sep05 $175C Aug05 first trade also cheap/liquid with a positive subsequent print. THESE are not an unbiased win-rate sample. Remaining 39 of 52 candidates not independently tested for historical trade volume in this new phase; some previously tested original four-stock options are separate and not among these 52.

## Critical stock-adjustment execution risk — NEW FROZEN AUDIT
The saved original stock event source uses **dividend-adjusted** OHLC; actual options price and their strike/underlying price operate on historically **unadjusted traded stock OHLC**. On CASH EX-DIVIDEND dates, a dividend-adjusted +5% underlying target can be marked before raw stock has actually moved +5%. Pre-registered independently in `frozen_dividend_adjusted_vs_raw_stock_exit_audit_2026-10-10.md`, then ran `run_adjusted_vs_raw_stock_exit_100events_2026-10-10.py` and permanently archived complete 200-setup findings in `raw_stock_price_dividend_exit_audit_100events_2026-10-10.json`.

Full 200 setups: 22 NO SIGNAL, leaving **178 auditable setups** with raw daily price history successfully retrieved for 49 distinct tickers. **171/178** originally adjusted-series exit dates agreed with raw stock +5/-5 first-bar exit date; **7/178 differed**. **26/178** had a cash dividend during the relevant hold; **6 of 7 differences** coincided with a cash dividend. Seven changed exit outcomes include:
- NOC Jan31 2024 entry: original Feb26 target vs raw Feb28 TIME
- LEN Jan16 2025 entry from 2024 event: original Feb3 stop gap vs raw Jan29 stop, ex-dividend
- **UPS Feb4 2025 entry: original adjusted +5% target Feb18 vs actual raw +5% target FEB24**, ex-dividend $1.64 on Feb18
- UPS Feb7 2025 rising entry: original adjusted target Feb24 vs raw target Feb28
- HON Feb11 2025: original March3 target vs raw March10 target (also source corporate-scale conflict in strict 100-event option study; do not treat as tradable)
- TXN Jul28 2025 entry: original adjusted +5% target Aug19 vs raw -5% STOP Aug1, ex-dividend July31
- NFLX Nov11 2025: original Nov20 stop vs raw Nov17 stop-gap, **not a dividend case**, possible split/price source differences.

The 20 historical EOD ask-to-bid comparisons belong to **18 distinct setup cases**. **All 18/18** same-setup original exit dates matched the recomputed raw daily first-trigger dates; their end-of-day returns therefore DO NOT need a different exit DATE from this particular audit, but remain nonexecutable EOD snapshot proxies with unknown entry daily traded volume and uncertain intraday time.

### Actual five-minute stock-target AND OPTION print reconstructions (new)
First stock threshold is a five-minute stock BAR: underlying high or low, exact crossing timestamp within bar not observed. Option prices are actual reported subsequent option TRADE prints, not sellable bids. Illustrative $0.65 side fees.

**CMCSA Jan30 2025 selloff / day3 Feb4 entry**: raw stock entry $32.680001, raw +5% $34.3140. Feb6 first target-touch 5m bar **12:25 ET** (stock high $34.32). Mar07 $35C Feb4 first entry-option trade $0.23, entry-day option volume 63; first option trade after stock target bar **Feb6 12:35 ET at $0.55** in 66-contract bar. First-trade-to-first-next-bar mark **+129.81%** net premium proxy. Prior SAME contract EOD ask $0.40 / exit bid $0.60 gave +46.00% EOD-only proxy, and last exit-day trade $0.62 implied +159.41% first-to-last print. Three different plausible hindsight marks on same trade; NO observed executable sale at 12:25.

**UPS Jan30 2025 selloff / day3 Feb4 entry**: raw entry $111.339996, target $116.906996. UPS $1.64 cash ex-dividend **Feb18 2025**. Prior stock adjusted series first marked target on Feb18, but raw high on Feb18 only **$115.78**, BELOW $116.907. Recomputed actual raw +5% first hit **Feb24 at 09:50 ET**, first stock five-minute bar high $117.31. Mar07 $121C original Feb4 first trade $0.29 (27 contracts entry day), option same target-bar trade range $0.40–$0.46 and first post-bar five-minute trade **09:55 ET at $0.52** (12 option contracts in that bar). First-trade-to-next-bar net premium proxy **+73.19%**. The PRIOR February18 option last print $0.25 yielded -17.88% but was on the **WRONG STOCK EXIT DATE**, must NOT be used as actual +5% stock target option outcome. This directly demonstrates a SIGN REVERSAL just from original adjusted/barrier-vs-raw and option execution timestamp mistakes. Neither plus 73% nor the plus 129.81% is guaranteed bid/ask.

Machine-readable time/price evidence `repair_exit_timestamp_raw_stock_CMCSA_UPS_2026-10-10.json`. Official UPS dividend https://investors.ups.com/quarterly-earnings-and-financials/dividends corroborates ex-date/amount.

## Research conclusion and next justified data operation
- **Solved in part**: EOD source had REAL omission and Massive's free historical TRADE OHLC provides historical option trade volume and restores some exact exit-day trade prices. Free archives have enough detail for an approximate research-only, time-aligned first-next-trade mark on some candidate strikes. Public 104-stock full-chain archive is actually unavailable (404); Dolt exact-quote requests do not restore missing rows.
- **Cannot yet claim** strict historical call-option expectancy, optimal entry/expiry, or executable fills. Needed: full historical listed option strikes and same-time bid/ask at true stock barrier, plus volume for remaining 39+ quote-screened contracts. A 5min OPTION trade is not NBBO and may be minutes after trigger; even quote timestamps EOD are unsuitable for immediate execution. There are 100 historical stock events; cannot generalize from two verified cheap, relatively active contracts.
- **Critical correction for future**: always compute raw underlying target/stop FIRST before attempting options matching, and flag dividend/split events. Never use adjusted stock target date for option liquidation without reconciliation.
- Preserve all codes and raw audit outputs in GitHub; no paid data, no prospective shadow test, no live scanner update.
