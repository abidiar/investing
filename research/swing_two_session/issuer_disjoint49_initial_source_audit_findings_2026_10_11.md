# Frozen range-VWAP replication v2 — source feasibility, 49-issuer daily screen, 18-case price/volume audit
Date: 2026-10-11
Verdict: **SOURCE ACQUISITION + ADJUSTMENT DIAGNOSTIC COMPLETED; INDEPENDENT TRADING OUTCOME TEST NOT YET EXECUTED. NO PROVEN STOCK OR OPTIONS EDGE.**

## Governance and evidence sequence
- Mandatory governance research/RESEARCH_GOVERNANCE.md and canonical Google ledger checked before this run.
- Prior-work review completed and **committed FIRST**: research/prior_work/range_failed_support_vwap_replication_prior_review_2026-10-11.md. Institutional FRBNY Osler 2000/2001, 2010 JF intraday liquidity, 2021 SR persistence arXiv and transaction cost regime-dependent studies support mechanism but don't validate this exact trade.
- Protocol **committed BEFORE new price retrieval/outcome study**: research/swing_two_session/frozen_issuer_disjoint_range_vwap_replication_v2_2026_10_11.md . Preserves 40-day support/break/reclaim + 1.2x volume, below VWAP then two completed M5 closes above, next-bar open <=noon, +2% before -2% two-session stock exits; opening baseline, skip zero, explicit fees, issuer clustering. 49 fixed ISSUER-DISJOINT tickers, 2024-Jan2 to 2026-Sep30.
- No outcome data (post-signal future VWAP entries or target/stop) downloaded/scored under v2. Do not present new candidate hits as profits.

## NEW frozen daily source / signal panel
Connected Webull original get_stock_bars D RTH ending 2026-Oct01, exactly 1000 recent daily candles EACH for **49/49 preselected issuer-disjoint stocks**, no paid data. Raw provider OHLCV preserved losslessly as five CSV files:
research/swing_two_session/data/disjoint49_daily_webull_batch_01_2026-10-11.csv through batch_05_2026-10-11.csv .
Exact ALL-49 preliminary 40-session screen and 106 signal-day previous40 input windows saved:
research/swing_two_session/data/disjoint49_daily_screen_preliminary_2026_10_11.json .
**106 preliminary events across 41 tickers**, 2024 n40 / 2025 n39 / 2026 through Sep30 n27. This is eligible **daily source signals**, NOT 106 executions. Other 8 issuer stocks yielded no qualifying source-D candidate in the fixed interval. No performance stats and no excluded failure based on future outcome.
Disjoint original 20: META ORCL DELL AMZN AAPL AMD MSFT GOOG CRM QCOM JPM CAT HD COST XOM BAC LLY INTC UBER PYPL. v2 universe different but PRESENT-DAY curated 2026 constituents; survivorship bias remains.

## NEW independent input source reconciliation — frozen 18 event audit (6/year)
Audit subset frozen BEFORE requesting the audited M5 historical data: first three and last three distinct ticker events by chronological order within EACH 2024,2025,2026, see research/swing_two_session/data/frozen_18case_price_basis_audit_sample_2026_10_11.json .
Requested up to four full historical M5 RTH histories per case, required all previous 40 stock sessions + original signal session. All **18/18** had 41 session calendar dates reconstructed, but almost every event prior40 included intermittent 77-of-78 candle days and standard 42-bar market half-days (occasionally 41); so not ALL 41 sessions have exactly 78 complete bars. No future-bar returns retrieved or evaluated.
Archived **per-day** original Webull D adjusted O/H/L/C and summed M5 RTH as-traded OHLCV for every case, six frozen three-case files:
research/swing_two_session/data/frozen18_m5_daily_audit_part01_2026_10_11.json ... part06_2026_10_11.json .
Machine reconciliation research/swing_two_session/data/frozen18_adjusted_vs_m5_price_volume_reconciliation_2026_10_11.json and deterministic reducer research/swing_two_session/run_frozen18_price_volume_reconciliation_2026_10_11.mjs .

### Step A: naive raw RTH price vs adjusted daily
Only **11/18** previous40+event M5 unadjusted raw PRICE+M5 RTH VOLUME reconstructed signals qualified, versus 18/18 adjusted daily source signals. Exactly 7 initially discordant. NEVER imply 7 profitable backtest signals were proved fake: difference may reflect legitimate ex-dividend actions within preceding40 window and different daily/M5 volume coverage.

### Step B: confirm actual CASH dividend exdates in the frozen windows, all known by original SIGNAL date
**SEVEN** audited basis-sensitive examples have issuer/company data independently verifying an ex-dividend within the prior40 **or on event day**, and price adjustment ratio change matches the dividend percentage order of magnitude:
- FDX Dec23 2024 signal: $1.38 cash ex-date 2024-Dec09, D/M5 adjustment ratio drift 0.494%. Issuer original https://investors.fedex.com/stock-information/dividends/default.aspx .
- SBUX Dec16 2024: $0.61 cash, 2024-Nov15 date of record/ex-date under T+1; D/M5 ratio drift 0.619%. Original https://investor.starbucks.com/stock-info-and-resources/dividend-and-stock-split-history/2024/default.aspx .
- UPS Dec04 2024: $1.63 cash exdate 2024-Nov18, ratio change 1.231%, https://investors.ups.com/quarterly-earnings-and-financials/dividends .
- TGT Feb12 2025: $1.12 cash exdate on Feb12, ratio 0.868%, original https://corporate.target.com/press/release/2025/01/target-corporation-declares-regular-quarterly-dividend ; press release dated Jan15 BEFORE signal.
- ABBV Jan16 2026: $1.73 cash exdate Jan16, ratio 0.805%, prior declaration 2025-Oct31 https://investors.abbvie.com/stock-information/stock-quote .
- UNH Sep18 2026: $2.32 cash exdate Sep14, ratio 0.616%, 2026-Aug12 prior issuer release https://www.unitedhealthgroup.com/newsroom/2026/2026-08-12-uhg-authorizes-payment-quarterly-dividend.html .
- GS Sep15 2026: $5 cash exdate Sep01, ratio 0.490%, issuer/SEC 2026 July predeclared https://www.sec.gov/Archives/edgar/data/886982/000088698226000294/a2q26gsearningsresults.htm .
**IMPORTANT:** Using an adjusted time series is not intrinsically lookahead for dimensionless 40-session relative thresholds: later ex-dates *AFTER* signal day generally multiply all earlier 40 prices by a COMMON factor and cancel in low/close/support ratios. Ex-dates *WITHIN* the preceding40 must instead be applied to history point-in-time (all such cash dividends already known by candidate day). Thus the naive raw-versus adjusted 11/18 apparent invalidation was misleading and does not demonstrate that original v1 profits were fictitious.

### Step C: rescale each same-day RTH M5 price onto DAILY historical adjusted basis
For independent source-QA ONLY, take provider DAILY_CLOSE / M5_RTH_LAST_CLOSE on each of 41 sessions as diagnostic proportional adjustment factor, rescale reconstructed M5 OHLC and recompute EXACT 40-session price predicates (original RTH M5 volumes preserved separately). Result: **17 of 18** sampled daily signals persist; one **UNH Sep18 2026** differs on RTH-M5 volume ONLY (Webull D 20d RVOL 1.815 vs M5 RTH 20d RVOL 0.756). Original DAILY total event volume 8,616,225 shares vs summed RTH M5 volume 2,279,502 shares (daily/RTH 3.78x!). CRWD Jan16 2026 also daily/RTH M5 event volume 4.47x though its M5 RTH RVOL still passed. This is not a basis-proof for rest106 events or verified publisher split/dividend factor; it **is** strong evidence that DAILY and 5-minute RTH feeds have materially different volume inclusion. Do NOT silently replace daily volume or adjust 1.2x rule after seeing wins/losses.
Across cases, rescaled M5 price highs/lows can differ ~0.2%–0.7% from original adjusted D OHLC, and 77 of expected78 M5 candles common. Remaining 17 passing 40d price/volume diagnostic DO NOT satisfy full original source-quality gate across 49 issuers.

### Why new trial trade P&L was withheld
v2 preregistered requirement was **consistent point-in-time as-traded/source-certified 49-stock complete historical coverage**, not a lucky subset of 18 QA cases. Full 106 source-positive signals may change membership after source checks; 49-stock daily all-date scan must be reconciled and M5 missing bars explained or precisely handled before P&L sample can be labelled independently replicated. Since source requirement not fully fulfilled today, **v2 independent OUTCOME test NOT EXECUTED**; no 106-event profitable claim, no 18-case win-rate sampling, no user call contract hypothesis promotion.
Exact archived v1 +0.574%/signal 63 known-outcome result remains RESEARCH ONLY, not rejected on this basis audit. At 1% assumed friction earlier v1 only +0.092%/signal. Original top-three tickers AMZN/QCOM/XOM contributed 60.4% of simulated gains, none of these is included in v2.

## Next necessary clean operation
1. Reconcile **DAILY volume** vs M5 RTH universe: verify whether difference reflects off-hours, venue consolidated prints, missed 5min bars and any special split. Preserve original v1 daily >1.2x threshold without redefining it.
2. Verify corporate-action history through signal-date exdate, exdiv known at time, same-day D price ratio and corporate action adjusted single-consistent series for ALL 106 prelim signals, including missing candidates caused by basis decisions in ALL49 histories; no outcome-based removal.
3. Source needed after verification: M5 RTH of **day AFTER signal plus next trading session** for all correctly qualified events; compute as-of VWAP closes and fixed +2/-2 within two sessions, same calendar + benchmark open all signals, stop-first/cost sensitivity and ticker clustered bootstrap. Until then outcome status NONE, NO EXECUTION or $50 options case.
4. Only after full stock edge verified, vintage option ASK entry / BID exit / spread+fees / IV DTE / 1-contract<=50 prior-time selection.
Do not spend on provider credits, alter scanner/automation or issue a trade instruction from this exploratory work. Frozen v2 unchanged.
