# Affordable OTM historical earnings-call pilot — fixed four events
As of 2026-10-10. **Status: PARTIAL EXECUTION / RESEARCH-ONLY; option trade-bar data, no bid/ask or executable P&L.**

## Precommitted four historical events
From original frozen `options_execution_model_protocol_2026-10-10.md`: DELL 2025-03-03, QCOM 2025-07-31, PYPL 2025-02-04, AMAT 2025-02-14. Keep exactly two stock entries (session 3 opening; first three rising lows + two-high breakout opening) and 30/60 calendar-day expiry targets. OTM-extension frozen first in `affordable_otm_tradebar_pilot_protocol_2026-10-10.md`. Fixed purchase debit <=$50, including illustrative $0.65 entry fee; opening-day option trade volume >=10; OTM strike above unadjusted stock entry OPEN and <=125% of it; closest qualifying strike rule. All outcomes are *exploratory*.

## Verification results
- Massive historical contract listing as of each entry date, using actual unadjusted stock prices from historical Massive stock OHLC. Historical expiry menu and strike lists preserved in `affordable_otm_contract_listing_2026-10-10.json` (DELL and QCOM); results of later PYPL and AMAT listing checks summarized below.
- Eight entry situations × 30/60 nominal DTE windows = 16 planned selections. In the protocol's narrow [entry+target DTE, entry+target DTE+7 calendar days] range, all 8 thirty-day windows contained listed contracts; only DELL rising-lows and QCOM rising-lows 60-day windows contained historically listed contracts. The six other nominal 60-day windows had no listed expiry **within that narrow range as of entry**; other later-listed/monthly options may exist outside it. Do not say that longer-dated options did not exist.
- Thirty individual **options contract history probes** (price available or empty), spanning fixed four tickers. Five of the probes showed BOTH entry first-trade debit <=$50 and entry-day volume >=10. They represent only three event/entry pairings (QCOM day3, PYPL day3, PYPL rising), and NOT five independent successful entry strategies. The closest qualifying strike is not fully established for all chains because not every intervening strike was fetched; rate limits sometimes intervened.
- Historical **NBBO quotes NOT ENTITLED** on current connector; actual fills, timestamp-aligned stock/option trades, vol surface and spreads not known. Provider free options tier is 5 calls/minute; during collection multiple calls returned RATE_LIMIT. No paid data acquired.

## Entry/exit observation matrix
Underlying stock exit dates, as pre-frozen stock-only +5% target / −5% stop within up to 20 sessions:
| Symbol | Entry | Actual unadjusted stock open | Stock exit date | 30-day listed expiry | 60-day listed expiry in strict range |
|---|---|---:|---|---|---|
| DELL | day3: 2025-03-06 | $94.25 | 2025-03-07 (stock stop) | 2025-04-11 | none |
| DELL | rising lows: 2025-03-13 | $93.95 | 2025-03-17 (stock target) | 2025-04-17 | 2025-05-16 |
| QCOM | day3: 2025-08-05 | $148.52 | 2025-08-13 (stock target) | 2025-09-05 | none |
| QCOM | rising lows: 2025-08-13 | $153.97 | 2025-09-05 (stock target) | 2025-09-12 | 2025-10-17 |
| PYPL | day3: 2025-02-07 | $79.00 | 2025-02-21 (stock stop) | 2025-03-14 | none |
| PYPL | rising lows: 2025-02-18 | $78.20 | 2025-02-24 (stock stop) | 2025-03-21 | none |
| AMAT | day3: 2025-02-20 | $175.14 | 2025-02-25 (stock stop) | 2025-03-28 | none |
| AMAT | rising lows: 2025-02-21 | $176.13 | 2025-02-25 (stock stop) | 2025-03-28 | none |

## Observed affordable contract probes (NOT trading execution)
Amounts are standard 100-share listed contracts. Option entry is the actual day's FIRST REPORTED TRADE (not necessarily 9:30); option exit is last reported trade that day, not a quote contemporaneous with the stock-price threshold. Illustrative cost: $0.65 per side, excluding bid/ask/slippage. The $50 rule is checked using first-trade price ×100 + entry fee.

| Ticker, entry | Call contract (expiry / strike) | First trade + volume on entry date | Last trade + volume on stock exit date | Illustrative option result | Screening interpretation |
|---|---|---|---|---|---|
| QCOM day3 | 2025-09-05 $175 call | $0.14; 21 contracts | $0.25; 15 contracts | debit $14.65, proceeds $24.35, **+66.2%** | Passes price/volume for this probed strike, nearer strikes still not exhaustively screened |
| PYPL day3 | 2025-03-14 $89 call | $0.38; 10 contracts | **NO trade on 2025-02-21** | debit $38.65; **return unavailable** | Passes entry screen, but not feasible to assign observed last-trade exit |
| PYPL day3 | 2025-03-14 $90 call | $0.43; 359 contracts | $0.15; just 2 contracts | debit $43.65, proceeds $14.35, **−67.1%** | Illustrative alternative, not valid as chosen 'closest' because $89 also passed entry screen |
| PYPL rising | 2025-03-21 $90 call | $0.40; 733 contracts | $0.15; 871 contracts | debit $40.65, proceeds $14.35, **−64.7%** | Passes price/volume; $87.50 nearest checked strike cost $51.65, over budget |
| PYPL rising | 2025-03-21 $92.50 call | $0.25; 34 contracts | $0.12; 393 contracts | debit $25.65, proceeds $11.35, **−55.8%** | Cheaper but farther OTM than the $90 call; supplementary only |

## Negative feasibility probes
- DELL day3 2025-04-11: $115 cost $70.65 with 11 entry-day trades, $116 cost $50.65 with 3 trades, $117 no entry-day trade. The 110/112 strikes also had entry premium greater than $50. No qualifying contract verified among probed strikes.
- DELL rising 2025-04-17: $110 entry first print $0.84 with 116 trades (over budget), $115 $0.48 with only 6 trades (under budget but below 10-volume floor). For the 60-day 2025-05-16 $115, entry $1.12 (over budget). No qualifying contract verified.
- QCOM day3 cheaper nearer 2025-09-05 strikes $165 first print $0.40 but 3 trades, $170 $0.19 but 1 trade; $175 did meet volume and budget. The 160 contract attempt was rate-limited; **closest-strike status not established**.
- QCOM rising: 2025-09-12 $190 no option trades over query window; $180/$185 requests rate-limited. 2025-10-17 $190 had no trade ON entry date; first trade occurred next session, $0.50. **No strict affordable entry verified**, not evidence of impossibility.
- AMAT day3: 2025-03-28 $210 first print $0.50 (debit $50.65, 3 entry-day contracts), $215 no entry-day trade; $205 no entry-day trade. No eligible contract verified.
- AMAT rising: $200 first print $0.75 with 4 entry-day contracts, $205 $0.55 with 5, $210 and $215 no entry-day trades, $220 $0.15 with 1. No eligible contract verified.
- PYPL day3 $88 was above budget at $0.54 first trade, and $89 was below it at $0.38 first trade; this is a narrow observed frontier, but untested closer strikes and asynchronous first prints leave some uncertainty. $89 had no exit-day print, unlike farther $90.

## What this demonstrates
1. The 4-event sample does contain *historically traded, affordable* out-of-the-money call contracts, including QCOM and PYPL, but not consistent profitability even under favorable first/last print approximations.
2. The seemingly optimal cheap option is often a **very low-delta/far-OTM contract** which may have few trades, no exit-day print, and price discontinuities across adjacent strikes. A +5% stock rebound does not guarantee a profitable far-OTM call. A putative $50 strategy cannot treat absent exit trades as an executable sale or an automatic $0 mark.
3. *Non-monotone* first prints are actually present: PYPL March 14 $89 call opened at $0.38, $90 call at $0.43 on Feb 7 despite higher strike. This confirms that day-level first prints across strikes do NOT represent a synchronous option chain and are unsafe for real-time optimal strike selection.
4. Historical trade OHLC is a feasibility source, NOT adequate proof that $50 budget, 30/60 DTE calls can be bought/sold at prices shown. No IV, bid, ask, or spreads; no statistically meaningful win rate from 4 cases.
5. **Verdict: INCONCLUSIVE / NO A+ OPTION ENTRY EDGE.** No scanner promotion; none of these isolated prints is a trading recommendation.

## Next scientifically clean step
- Keep the frozen *same four events* and missing rows explicit. Once provider permits additional calls, finish cheaper-strike scan for QCOM day3 ($160) and rising ($180/$185), candidate exit-trade availability for PYPL day3, and prove missing-vs-expensive status for DELL/AMAT where necessary. The provider rate limit is not a reason to buy data.
- More importantly, if the aim is A+ call trades, gather point-in-time executable option bid/ask and delta/IV for **new unseen earnings events**. Only then assess budget-constrained net expectancy and max drawdown; record no-signal and untradeable candidates. These four historical outcomes are too small and have been observed previously.
- Keep new findings with existing prior work and research ledger; no changes to live scanner.

**Machine readable:** `affordable_otm_tradebar_pilot_observations_2026-10-10.json` plus `affordable_otm_contract_listing_2026-10-10.json`.