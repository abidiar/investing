# Investing OS — Free historical affordable OTM recovery call research: completed 2024–2025 expansion
Research run/final audit date: 2026-10-10.
**Research status: 100-event, source-complete historical EOD QUOTE SENSITIVITY study. NOT a strict first-trade/entry-day-volume or time-aligned executable options backtest. NO validated A+ call scanner edge.**

## Scope and preregistration
- 100 **previously quality-qualified and previously outcome-observed** earnings-selloff events from canonical 164-event saved daily stock OHLC: ALL 45 events with qualifying selloff in 2024 (29 original, 16 independent-company cohort), plus ALL 55 in 2025 (29 original, 26 independent-company cohort). Total 100 events, not untouched out-of-sample.
- Each event receives (1) third-session STOCK opening and (2) frozen earliest three-rising-lows + two-high break signal, enter NEXT opening, skip signal if >8% chase. Exact original stock exit: first +5% target or −5% stop relative to entry open with stop-first high/low convention, otherwise after 20 sessions. No entry or stop optimization.
- 2025 protocol frozen before broad option outcomes at `frozen_2025_free_eod_otm_scaling_protocol_2026-10-10.md`; 2024 cohort frozen prior to its results at `frozen_2024_eod_otm_expansion_protocol_2026-10-10.md`.
- Source price alignment: Yahoo Finance chart **non-dividend-adjusted historical daily opening** restored to historical as-of-event strike units by reversing later split factors and flagging unresolvable price-scale or splits during hold. This corrected a material initial source bug for NFLX, NOW, CRWD and other retrospectively split-adjusted tickers; the archived final 2025 and 2024 output uses the fixed split conversion. E.g. original HON records with ~0.3x source scale were excluded, not assigned manufactured strikes. All data accessed at no dataset cost.
- Free DoltHub historical `option_chain` EOD bid/ask/delta/IV queries, no API key; 2024: **139/139 successful** case-level ticker/date/spot queries; 2025: **192/192 successful**; **331/331** successful. Saved raw JSON source cache in corresponding `.json.gz` plus readable per-event JSON results. Multiple events may share date/quote observations.
- Same frozen budget and expiry parameters: standard one 100-share CALL contract, strictly OTM and strike <=125% of contemporaneous stock entry raw open; $50 INCLUDING $0.65 illustrated entry commission, +$0.65 on exit; target expiries on/after +30 or +60 days, no later than +37/+67 days; earliest *sampled* expiry before affordability evaluation, nearest affordable strike on that expiry.

**CRITICAL contract-rule divergence, unavoidable from FREE DOLT quote source:**
The original strict frozen options rule selects by ACTUAL **first option trade price** at stock-entry date and >=10 option contracts traded that session; actual exit requires **bid at first intraday stock target/stop time**. DoltHub instead provides EOD option ASK/BID and NO option trade volume; its `vol` column is **implied volatility**, NOT volume. Therefore 100-event results are an EOD ask-to-bid *sensitivity/test* with exact frozen underlying entry/exit DATE and same OTM debit/expiry parameters, but **NOT verification of the original trade selection or fills**. Dolt also has only about 3 sampled expirations per symbol/date; absent expiry means missing in this dataset, NOT unlisted in 2024/2025. A match is historical EOD entry ask AND exact same contract bid at stock-exit calendar date. Never treat unobserved premiums as $0 or a loser. Any same-day entry/exit EOD comparison is just an instantaneous ask-to-bid spread test, not actual path performance.

## Historical option quote coverage

| Metric | 2024 | 2025 | Combined |
|---|---:|---:|---:|
| Frozen quality-qualified underlying selloff events | 45 | 55 | **100** |
| Stock-entry setups considered, day3 + rising | 90 | 110 | **200** |
| Potential options method×30/60 DTE windows | 180 | 220 | **400** |
| Setups with eligible frozen stock signal and successfully read EOD quote API | 71 | 98 | **169** |
| Entry method skipped: no rising-lows trigger | 13 | 9 | **22** |
| Excluded: corporate price-scale conflict | 4 | 2 | **6** |
| Excluded: split or deliverable change during stock holding | 2 | 1 | **3** |
| Potentially affordable EOD ASK candidates (method/DTE windows; volume UNKNOWN) | 21 | 31 | **52** |
| Exact contract present as EOD bid quote on stock exit DATE | 10 | 10 | **20** |
| Matched EOD quoted option outcomes >0% after illustrated fees | 6 | 2 | **8** |
| Matched EOD quoted outcomes <=0% | 4 | 8 | **12** |

Only **20/400 = 5%** of possible event/method/DTE cells had both price-matched EOD quote endpoints. Just **20/52** ask-affordable candidate windows had exit quotes, and even those still lack entry-day traded volume and exact intraday executable quotes. Most losses/wins in the population are simply **unknown** from this free EOD archive. Historic missing exit quote should NEVER be counted as zero option value. These 20 rows correspond to **17 distinct earnings events** across **13 unique symbols**, with correlated repeated methods/expirations (CPRT 2024 has two DTE marks from same event).

## Historical EOD ask-to-bid outcomes — descriptive ONLY

| | 2024 | 2025 | Combined |
|---|---:|---:|---:|
| Price-matched option quote combinations | 10 | 10 | 20 |
| Positive comparisons | 6 | 2 | 8 |
| Mean modeled based on REAL EOD bid/ask | **+87.4%** | **−40.4%** | **+23.5%** |
| Median | **+27.0%** | **−54.1%** | **−39.0%** |

The combined arithmetic mean is heavily dominated by a few hundred-percent 2024 winners: TGT +309.8%, CPRT +380.5% and +131.4% (same stock event, 30/60-DTE), PYPL +304.2%; they CANNOT be interpreted as expected profits for the 100 events or affordable calls in general. They also were cherry-*observed* by available paired data, not cherry-selected by this test. Year-by-year sign reversal (+87% vs −40% conditional means), extreme losses (e.g. ZBH −100% because exit-day recorded BID zero), and only 20/400 coverage indicate **no supported stable edge**. Across matched rows with an underlying +5% stock target, HPE rising (−0.9% option quote), FTNT day3 (−33.5% same-day quote spread), TPR day3 (−77.0%), and ZBH rising (−100% quoted exit bid) STILL showed negative option EOD return.

**NO valid paired day3-vs-rising comparison on the exact same earnings event and exact same DTE** exists in these 20 price-matched observations. Therefore ranking signals/expiries by these conditional numbers is improper. Do not claim 2024 rising lows better or a 60-DTE edge; coverage and original strategy differ.

## Frozen Dell/Applied Materials pilot close-out, 2025 data

The historical as-of listed contract menus were retrieved from Massive; entries from fixed four-event pilot: DELL March03 selloff, AMAT Feb14 selloff. The only admissible 30-day expiry within +7 after nominal window: DELL day3 April11, rising April17; AMAT day3/rising March28. DELL rising had 60-day May16 expiry; DELL day3 60-day and both AMAT 60-day *strict target windows* had none observed as of entry (NOT proof no longer expiry existed outside window).

- **DELL day3**, stock opens $94.25 March06, April11 OTM options from strike 95 to 117 as-of listing. Sampled upper tail: $108 and $111 and $114 and $117 no entry-day trades; $109 first print $1.35/2 entry-day contracts; $110 first $0.86/8 trades; $112 first $1.16/4 trades; $113 first $0.73/1 trade; $115 first $0.70/**11** entry-day contracts but costs $70.65 after fee; $116 first $0.50/**3** entry-day contracts, **$50.65 incl fee**, exceeds budget. None of the candidate prices/volume verified as BOTH affordable and liquid. Some lower strikes not individually read (likely more expensive; don't claim full exhaustive theorem).
- **DELL rising**, stock opens $93.95 March13; April17 OTM strikes 95/100/105/110/115. Actual recorded: $100 first $3.30 (803 entry-day contracts); $105 first $1.83 (218 entry-day contracts); $110 first $0.84 (116 entry-day contracts); **$115 first $0.48 but only 6 contracts traded that day**, too little volume. May16 60-day $100 first $4.89, $105 $2.94, $110 $1.87, $115 **$1.12**, all over budget. $95 not individually read but is closer to spot. **No verified eligible contract**.
- **AMAT day3**, stock opens $175.14 Feb20, Mar28 OTM strikes 180 to 215 in listed menu. Actual $180 $6.15/36 contracts, $185 $4.50/26, $190 $2.79/19, $195 $1.76/30, $200 $1.31/25, $205 no trade on entry, $210 **$0.50, 3 trades (cost $50.65)**, $215 no entry print; all observed are over the $50 debit or below 10 traded contracts. **No eligible recorded**.
- **AMAT rising**, stock opens $176.13 Feb21, Mar28 OTM strikes 180 to 220. $180 $5.74/119 contracts, $185 $3.55/6, $190 $2.21/17, $195 $1.64/12, $200 $0.75/4, $205 $0.55/5, $210/$215 missing, **$220 $0.15 but only 1 contract**; none met BOTH rules. **No verified eligible contract**.

These screened pilot rows are best classified **NO VERIFIED ELIGIBLE CONTRACT FOUND WITH OBSERVED FREE HISTORY**, NOT a zero-return trade, not a proof of no actual exchange option liquidity. No late/imputed entry or substitution. The 2025 AMAT later separate earnings selloffs (May/Aug) remain in expanded cohort; don't confuse them with original fixed Feb pilot.

## Source checks and data quality
- DoltHub free dates returned every requested SQL successfully for both years, but it samples expiries and has NO volume. Yahoo split-restoration handled later splits (2025 NFLX 10:1, NOW 5:1; 2026 CRWD split, etc.). HON asymmetric corporate structure/spinoffs generated large data-source ratio errors; excluded rather than misstriking.
- Separate 2025 Massive FIVE-MINUTE stock/option trade timing audit on frozen QCOM and PYPL pilot remains the only current partial near-target timestamp test; it found sizable 10–35 minute delays to next observed option trade, and a PYPL day3 stop where NO option traded after actual stop. This underlines why 20 EOD quote returns are NOT real exits.
- Requested free Massive 2024 option bars for TGT 2024 May and CPRT Sep returned NOT_ENTITLED, whereas PYPL Nov 2024 option daily bars were returned, independently supporting that its EOD bid/ask +304% scenario corresponded to a real rising options trade series (first $0.36 on entry, last $1.56 on exit; NOT executable contemporaneous ask/bid). Inconsistent free entitlement, never pay or fill in missing prints.
- Both 2024/2025 option dataset outputs and compressed exact historical quote cache are in `research/earnings_recovery/`. They are from public historical data with no subscription payment. All 100 preselected events included with SKIP/MISSING diagnostics.

## Decision and next legitimate research priority
**No A+ call-buying strategy, signal timing preference, or optimal 30/60-day expiry established.** The newly observed paired EOD data shows BOTH outsized conditional wins in 2024 and substantial conditional losses in 2025, which is precisely why the 4-stock anecdote alone could mislead. But low paired-quote availability and EOD versus intraday timing create profound selection bias. Do not call 8/20 a population win probability; no first-trade volume or real executable fills.

Continue exact historical study for unobserved exit quotes by finding a broader no-cost historical archive of actual issuer-specific contracts or time-aligned quote API; don't silently switch to a forward shadow study or paid data. Preserve source misses and freeze before any new feature/rule comparison.

## Links within repository
- `research/earnings_recovery/free_2024_eod_otm_45event_results_2026-10-10.json`
- `research/earnings_recovery/free_2025_eod_otm_55event_results_2026-10-10.json`
- `research/earnings_recovery/free_2024_eod_otm_45event_raw_quotes_2026-10-10.json.gz`
- `research/earnings_recovery/free_2025_eod_otm_55event_raw_quotes_2026-10-10.json.gz`
- `research/earnings_recovery/four_event_free_historical_bidask_intraday_audit_2026-10-10.md`
