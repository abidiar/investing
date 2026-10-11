# 2023 large selloff recovery: original-date profit/order/margin NEWS vs two-session assumptions — source-frozen test
Study date: 2026-10-11
Verdict: **UNCONDITIONAL +3/-5 20-session STOCK rebound diagnostic positive but NOT validated; fundamental-good vs fundamental-deteriorating PRIMARY hypothesis NOT TESTABLE given missing source labels. No options edge.**

## Exact ex-ante governance / reproducibility
- Before candidate selection, GitHub protocol **committed** `research/swing_two_session/frozen2023_historical_fundamental_shock_protocol_2026_10_11.md` at `4d737db4`. 49 issuers from prior frozen issuer-disjoint list, Jan03-Dec01 2023 close-to-close <=-7% signal and >=1.2 prior20 volume. First candidate per ticker, no event selected by forward return, all otherwise eligible included, exclude exact 2023 older 45 support signals and +/-2 trading days around exposed 164 post-earnings selloffs.
- All 13 candidates frozen BEFORE forward outcome retrieval as `research/swing_two_session/data/frozen2023_sharp_selloff_fundamental_manifest_2026_10_11.json` commit `f636c231`.
- Original historic sources and annotated caution classes frozen BEFORE forward outcome computation `research/swing_two_session/data/frozen2023_actual_historical_issuer_evidence_before_outcomes_2026_10_11.json` commit `b8faaf40`.
- Actual results computed AFTER source freeze, saved in `research/swing_two_session/data/frozen2023_fundamental_actual_dated_sources_forward20d_outcome_results_2026_10_11.json` commit `2a1b76d4`.
- Source: Webull 2022-26 archived daily adjusted 49-stock OHLCV batches under `data/disjoint49_daily_webull_batch_01..05_2026-10-11.csv`. 2026 survivor list / corporate-actions lookback, historical daily bid-ask not verified. First-day open next session, 20 sessions max, +3 target/-5 stop, actual daily opening gap price, ambiguous high/low STOP-first, 0.20/0.50/1.00 percent hypothetical complete friction. No ambiguous OHLC both-hit in this 13-event set. These are model prices not validated fill quotes or affordable call asks/bids.
- External theory (not a validation of these rules): https://www.newyorkfed.org/research/staff_reports/sr513.html; https://doi.org/10.1287/mnsc.2013.1766. Published quantitative analyses use analyst forecast revisions; our sample lacks actual historical before/after Wall Street consensus EPS revisions.

## Actual price test
**13/13 evaluable dates, 13 distinct issuers** (11 distinct event dates), each own first qualifying 2023 sharp selloff. ALL +3 target before -5 stop **10**; STOP **2**, time-exit **1**. 20 trading-session horizon.
- Mean gross +1.498867% per signal; net +1.298867% @20bps, **+0.998867% @50bps**, +0.498867% @100bps.
- Mean unconditional close-to-close relative entry at D+5 +3.20594%, D+20 +5.89291% (descriptive, NOT managed target/stop return). Recovered PRE-selloff close by at least one D20 close **6/13**, so short profit can be attained without full recovery.
- Ticker bootstrap 10,000 95% mean net @50bps **[-0.8473%, +2.5019%]**; EVENT-DATE cluster 10,000 and 11 groups **[-1.2639%, +2.6815%]**. Both include zero, not statistically validated.
- Same date Mar13 2023 bank shock: C -5.50%, WFC -5.50%. Excluding C/WFC post hoc gives +2.18% but is hindsight and NOT an ex-ante trade filter. Do not call stop robust without prospective bank-specific source gate.
- Prior 2023 support-break 45 exposures excluded by exact signal date; 164 close-to-earnings events excluded by timestamp. Same underlying issuers and partial overlapping economic regime across broader research; NOT independent issuer test nor forward trial.

| Ticker shock day | D1-> 20 session managed stock outcome @50bps |
| --- | ---: |
| CRWD 2023-01-05 | TARGET +2.50% |
| DDOG 2023-01-05 | TARGET GAP +3.68% |
| SNOW 2023-02-03 | TARGET +2.50% |
| ADBE 2023-02-24 | TARGET +2.50% |
| C 2023-03-13 | STOP -5.50% |
| WFC 2023-03-13 | STOP -5.50% |
| SLB 2023-03-15 | TARGET +2.50% |
| UPS 2023-04-25 | TARGET +2.50% |
| ABBV 2023-04-27 | TARGET +2.50% |
| PANW 2023-07-12 | TARGET +2.50% |
| FTNT 2023-08-04 | TARGET +2.50% |
| ANET 2023-10-26 | TARGET +2.50% |
| WMT 2023-11-16 | TIMEOUT -2.1946% |

## Actual issuer/company NEWS source analysis
Strict ex ante class thresholds: MATERIAL_BAD when verified same FY EPS/revenue -5%+, same-quarter orders or EPS >=10% below prior guided, comparable gross/operating margin >=1pp below prior guided, or explicit lost contract/material impairment/profit warning; INTACT_VERIFIED only with dated same-period updated guidance non-decreasing and no documented relevant order/margin shortfall; otherwise UNKNOWN.
Class results **MATERIAL_BAD N=0, INTACT_VERIFIED N=1 (WMT net -2.19%), UNKNOWN N=12 (10 target, 2 stop, net mean +1.26499%)**.
**NOT an inferential fundamental comparison. UNKNOWN DOES NOT MEAN NO BAD NEWS.** In hindsight one might label the market-contagion dates 'nonfundamental' and some demand shocks 'fundamental', but this is unmeasured and cannot establish a signal.

Four same-FY actual ORIGINAL management company disclosures measured in historical original releases:
- **UPS Apr25**: Prior Jan31 FY23 revenue midpoint $98.2B -> $97.0B (−1.22%); adjusted operating margin midpoint13.2% -> 12.8% (−0.4pp). Actual Q1 adjusted EPS -27.9% YoY NOT a same-quarter forecast revision. Management documented softer volumes, guidance trending toward low end. Frozen severe threshold not reached -> UNKNOWN. Sources https://investors.ups.com/sec-filings/all-sec-filings/content/0001090727-23-000003/exhibit991-q42022earningsp.htm and https://investors.ups.com/news-events/press-releases/detail/2090/ups-releases-1q-2023-earnings .
- **ABBV Apr27**: Prior/new FY23 adjusted EPS guidance midpoint10.82 ->10.92 (+0.92%). HOWEVER contemporaneous Humira sales -25.2% YoY, newer Rinvoq/Skyrizi missed market forecasts, causing investor concern that EPS forecast improvement did not capture persistent lost-patent drug erosion; company forecast positive but underlying key drug drivers mixed -> UNKNOWN, no clean intact classification. Original https://news.abbvie.com/2023-04-27-AbbVie-Reports-First-Quarter-2023-Financial-Results ; contemporary Reuters https://www.investing.com/news/stock-market-news/abbvie-raises-as-humira-demand-holds-steady-3066277 .
- **FTNT Aug04**: Aug03 after-market original Q2 release vs May Q1: FY23 revenue midpoint $5.455B -> $5.400B (-1.01%), FY23 billings midpoint6.78B ->6.54B (−3.54%), FY23 adjusted EPS midpoint1.46 ->1.51 (+3.42%); Q2 actual billings 1.54B vs prior Q2 guided midpoint1.58B (−2.53%). Actual critical demand drop but no one item passes frozen severe numeric cutoffs -> UNKNOWN. Sources https://www.sec.gov/Archives/edgar/data/1262039/000126203923000013/ftntq1-2023ex991.htm ; https://www.sec.gov/Archives/edgar/data/1262039/000126203923000027/ftntq2-2023ex991.htm . This is strong evidence a binary "EPS raised" rule would miss growth mix effects.
- **WMT Nov16**: August and November FY24 EPS adjusted midpoint $6.41 ->6.44 (+0.468%); constant-currency sales growth midpoint4.25% ->5.25% (+1pp); Q3 adjusted EPS1.53 vs Aug prior Q3 guidance midpoint1.475 (+3.73%). Declared normal-margin metrics not severe negative, therefore mechanical **INTACT_VERIFIED** but underlying consumer spending warnings led to -8% market day and our D1+20 simulation TIMEOUT -2.19%, proving positive management FY guidance insufficient. Original https://stock.walmart.com/sec-filings/all-sec-filings/content/0000104169-23-000088/earningsreleasefy24q2.htm and https://stock.walmart.com/sec-filings/all-sec-filings/content/0000104169-23-000124/earningsreleasefy24q3.htm ; contemporary Reuters https://www.investing.com/news/stock-market-news/walmart-lifts-targets-as-shoppers-pick-lowpriced-groceries-for-the-holiday-3236293 .
Other dated causes with UNKNOWN source class:
- CRWD Jan05 analyst target cuts https://www.fool.com/investing/2023/01/05/why-shopify-palantir-and-crowdstrike-stocks-slumpe/ ; DDOG same-day and SNOW Feb03 did not have verified issuer guidance observations (no absence claim).
- ADBE Feb24 federal antitrust potential Adobe-Figma DOJ report prior evening https://news.bloomberglaw.com/tech-and-telecom-law/doj-preparing-suit-to-block-adobes-20-billion-deal-for-figma .
- C/WFC Mar13 SVB/Signature contagion, genuine financial-system risk https://www.kitco.com/news/off-the-wire/2023-03-13/us-stocks-sliding-bank-shares-drag-wall-street-choppy-trade ; SLB Mar15 oil/counterparty panic https://www.investing.com/news/commodities-news/oil-prices-bounce-back-helped-by-stronger-opec-outlook-for-china-3030661 .
- PANW Jul12 Microsoft competing network access products https://stockstory.org/us/stocks/nasdaq/panw/news/why-up-down/why-palo-alto-networks-panw-stock-is-trading-lower-today/ ; ANET Oct26 customer META capex reduction https://www.boursorama.com/bourse/actualites/arista-networks-et-pure-storage-en-baisse-apres-que-meta-a-revu-a-la-baisse-ses-previsions-d-investissements-5664f170f603e4b6a795195f6e4e5116 .
All source links cited as original issuer or contemporaneous reporting as appropriate. Original sources verified for 4/13 with FY price-relevant quantified issuer guidance; not 13/13. Timing of after-market source versus T+1 entry is supported for FTNT, other publishers day-dated; no detailed NBBO quote chronology.

## Historical crosscheck — already outcome-exposed 164 earnings selloffs (DO NOT add to independent sample)
Prior integrated study at `research/earnings_recovery/quality164_asof_expectations_sector_integrated_findings_2026-10-11.md` reviewed 164 source prices but comparable historical FY guidance classifications only 27 of earlier 72 audit. 23 stable/up outlook labels had just 8 D4 stock +3 before -5 target-first, net -1.782% (20bps) and 11 eventual full-price recoveries by 60d. Three guidance DOWN labels had 2 target and mean +0.515%, all failed full-price recovery by D60. Outcomes seen before source coding, groups tiny/nonrandom. Six exact prior-quarter actual-company-guidance comparisons among previously selected winning/losing examples also mixed: AMAT EPS/margin beats winners, LEN Dec24 new orders -11.8% failure, FTNT Nov2025 EPS FY guide increased +7.2% but D4 stop. True historical same-period Street EPS consensus revision 0/164. Therefore FY profit guidance alone not usable to greenlight short-dated calls.

## Core result and next rigorous falsification
2023 high-volume one-day selloff can produce short-lived +3% intraday recoveries, but two -5% stops clustered same macro shock and date-cluster CI crosses zero. Source labels insufficient, so **NO validated fundamental-vs-liquidity reversal classifier** and no options edge.
Best next operation: prospectively freeze a larger fresh, untouched universe/calendar, source-code **all** initial event information via dated filings and analyst EPS revision snapshots before exposing returns; importantly code customer capex, competitive threats, product and backlog as known **quantitative** company news. Alternative is testing unchanged 2023 sharp-selling PRICE rule in fresh dates only, but that is a distinct strategy and must have its own untouched predeclared universe, cost and benchmark, and not pretend to validate fundamentals. Never label absent data 'intact'; don't optimize 2023 13 or old 164/106/45. No paid source or scanner/trade change.
