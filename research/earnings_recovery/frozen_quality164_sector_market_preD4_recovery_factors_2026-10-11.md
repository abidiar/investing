# FROZEN v1 164-company-earnings-sector context vs recovery, BEFORE GETTING ETF RETURNS OR ASSOCIATIONS
Date 2026-10-11; prior-review `research/prior_work/earnings_recovery_causal_mechanisms_sector_spy_residual_literature_2026-10-11.md`. **Previously EXPOSED price outcomes; new sector factor study is descriptive/exploratory, not an independent validation or causal mechanism identification.**

## Sample, outcomes, historical time cutoff
164 previously financially-qualified >=5% initial earnings-event RTH selloff closes, 92 original +72 company-disjoint, 61 companies, 91 AH +73 BMO. D0=first qualifying >=5% *close* earnings selloff within 2 reaction RTH sessions. D1/D2/D3 = following three RTH sessions; observer knows all candidate signal features only BY D3 close; buy enters D4 OPEN. **Outcome A** eventual full CLOSE recovery of ORIGINAL pre-announcement closing price within 60 RTH sessions after D0 = original `quality_164_long_horizon_recovery_2026-10-10.csv` h60_fullclose for 164 with sufficient follow-up, 86 yes/78 no. **Outcome B** D4 open +3% target before -5% stop/20 sessions, gap executed at actual open, stop first if same-day both high/low, 0.20% assumed stock roundtrip cost and timeout day20 close = original completed 164 research; 99 target/65 stop or timeout. Note 60-day full recovery NOT tradability and option P&L unknown.

## Frozen sector ETF proxy assignments
These are coarse **sector proxy categories based on current broad GICS-style business classification**, NOT verified historical GICS membership, not individual stock pre-announcement total-return peers. ETFs have individual issuer holdings and changing weight; including the stock in its ETF causes mechanical dependence. Nevertheless, price and dated market ETF data are independent of 164 future outcomes and suitable exploratory benchmarking. Do not reassign after viewing result:
```json
{
  "XLK": [
    "ADBE",
    "AMAT",
    "AMD",
    "ANET",
    "CRM",
    "CRWD",
    "CSCO",
    "DELL",
    "FSLR",
    "FTNT",
    "GLW",
    "HPE",
    "IBM",
    "KLAC",
    "MPWR",
    "NOW",
    "PANW",
    "QCOM",
    "TXN"
  ],
  "XLC": [
    "CMCSA",
    "DIS",
    "GOOG",
    "NFLX"
  ],
  "XLY": [
    "ABNB",
    "LEN",
    "LOW",
    "SBUX",
    "TPR"
  ],
  "XLP": [
    "DG",
    "DLTR",
    "HSY",
    "KDP",
    "KR",
    "TGT"
  ],
  "XLE": [
    "COP",
    "EOG",
    "HAL",
    "OKE"
  ],
  "XLF": [
    "COIN",
    "FIS",
    "GPN",
    "PYPL"
  ],
  "XLV": [
    "CVS",
    "EW",
    "GILD",
    "ISRG",
    "REGN",
    "TMO",
    "ZBH"
  ],
  "XLI": [
    "ADP",
    "CPRT",
    "DAL",
    "FDX",
    "GE",
    "HON",
    "JCI",
    "NOC",
    "UPS",
    "WAB"
  ],
  "XLB": [
    "DOW",
    "NEM"
  ]
}
```
Assert exactly one ETF per 61 tickers (XLC,XLY,XLP,XLE,XLF,XLV,XLI,XLK,XLB). SPY additional overall market benchmark. No historical membership / sector reclassification adjustment in first pass. Daily closes from connected Webull US_ETF RTH count 1200 ending 2026-10-09; store exact raw fetched 10 ETFs (within provider limits) and date coverage; any unavailable session = MISSING, exclude only that feature and report count; never fill future or use interpolated close across holidays. Use provider session dates sorted.

## Predeclared candidate features (all measurable BY D3 CLOSE)
1. `preSector20Pct`: twenty **trading-session** SPDR sector-ETF close-to-close returns from ETF session `index(D0)-21` to `index(D0)-1` (prior day, 20 return intervals), exposure to prior sector sentiment. Market control `preSPY20Pct` analogous. Note no company pre-20 total price available for all 164 from saved windows, so won't pretend full pre-announcement stock trend.
2. `sectorD0ToD3Pct`: matching sector ETF close at D3 vs D0 close return 100*(C3/C0-1). `spyD0ToD3Pct` same; `sectorMinusSPYD0D3Pp` = sector minus SPY.
3. `stockMinusSectorD0D3Pp` = stock (D0 close to D3 close) pct return MINUS ETF D0 to D3 percentage; not liquidity/flow or future EPS, is stock relative early behavior already partly tested vs SPY on 91 AH.
4. `shockMinusSectorD0Pp`: stock earnings D0 close from actual RTH pre-announcement close (AH earnings date close; BMO previous full trading day's close) percentage minus ETF D0 close / same pre-announcement daily session close, if exact dates available. This is initial price reaction idiosyncrasy, not fundamental residual due to unavailable EPS revisions.
5. `sectorD0ToD60Pct`: ETF D0 to D60 close return, future *DESCRIPTIVE* covariate only (NOT known at D3), to describe sector tailwinds accompanying recovery; same-period SPY D60 also for context. NEVER include in any D4 predictor, classifier, recommendation.

## Tests, matching, and audit
- For ALL164 and AH91 and separately original92/disjoint72, compare outcome winners vs failures on six preD3 sector inputs (1-4 above, pre-SPY market includes seventh) via group medians/means; no fitting or thresholds. Also report D60 future sector tailwind conditional on outcomes clearly separated.
- **Case/control matching** separately outcome A D60 close recovery and outcome B D4 +3 firsthit, using EXACT event year AND earnings release session AH/BMO AND sector ETF proxy, unmatched control DIFFERENT TICKER and absolute magnitude of D0 earnings drop within <=5 percentage points, deterministic order: sort winners by absolute selloff magnitude then ticker/date and greedily match closest unused control (break ties ticker/date). Report pair coverage, medians of case-minus-control, sign directions and sign-test exact TWO-SIDED exploratory p values. No minimum n => no conclusions if <10 pairs; no choosing another tolerance after result. 
- Also report stratification separately AH with additional LOW by D3 (n54), but don't fit composite or optimize threshold; may not have enough per-sector controls.
- Distinguish stock-vs-sector relative vs SPY to correct conflation of market vs company price. Need avoid conditional-on-success future SPY or sector as an early signal.
- Cross-check static historic numeric financial quality 72 previous factor report: higher historic revenue growth, lower debt, cash conversion previously NOT stable in matched data; don't re-test them to rescue sector interpretation.
- No current "analyst EPS consensus forward revision" or measured manager sentiment Q&A; those source families remain MISSING. Do not treat a generic negative word, current EPS revision, stock relative strength, or unexplained residual as a proof that institutional investors changed minds or liquidity reversal. Don't infer WHY without direct news/flow.
- No p-values authorizing production on 164 previously observed outcomes. No scanner, no $50 call DTE selection, no automated tasks. Save ETF raw snapshot, frozen runner, event and pair data, readable verdict. No data purchase.
