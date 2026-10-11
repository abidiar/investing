# First failed new-low + shrinking seller volume + expanding buyer volume: 45-event earnings-reaction-day audit
Completed 2026-10-10. **NO TRADEABLE SIGNAL FOUND UNDER THE FROZEN RULE; NO 0% WIN RATE CLAIM.**

## What was actually tested
Source universe was **all 45 unambiguous BMO/AH** July 1–Sept 4, 2026 earnings announcements in frozen 61-company historical quality research list (the other seven have missing/uncertain release timing or during-session release: AMAT/HON/HPE/HSY/REGN/WAB/ZBH). The earlier 15-event study *selected by closing >=5% selloffs*, thus missed stocks with >=5% intraday selloff that had rebounded by close. In this study eligibility is strictly as-of: on the earnings reaction session only, the first COMPLETE 5-minute bar whose low <=95% of the PRE-earnings previous regular-session close, no later than 11:30am ET. For BMO, release same session, for AH release next session. Source dates sourced from earlier frozen Quant500 SEC-linked event list and archived as `frozen_all45_jul_sep2026_earnings_announcements_pre_5min.json`, committed BEFORE this broad historical intraday outcome retrieval.

The signal rules in `frozen_intraday_first_failed_low_volume_takeover_45events_2026-10-10.md` were committed before broad OHLC inspection: first -5% candle i's low L0 and volume V0, retest from i+2 to i+12 within L0 ×[0.998,1.003] without ANY prior intervening candle breaking materially below 0.998×L0; retest bar volume <=80% of original V0; next 1–3 completed 5m bars first green candle close above both retest and preceding bar highs, volume >=120% of preceding three bars' average; buy NEXT 5m bar's opening (not the prior candle) within 1.5% of L0 and by 13:05; no later rescans or threshold optimization. Stock barrier +1.5% target/−1% stop first, 3 entry-inclusive trading sessions, stop-first ambiguous same five-minute bar and gap execution at next session open. **Stock only, no option quotes or premium.** Baseline is first next five-minute bar OPEN after the initial -5% dislocation fully printed, same risk and window.

### IMPORTANT transparent historical adjustment repair
First exploratory pass had erroneously mixed Webull historically *corporate-action-adjusted daily* bars with genuine as-traded/unadjusted five-minute OHLC. 18 of 45 issuers had >0.2% difference between D and M5 on the same date, with CMCSA, FIS, UPS >1% initially excluded. This can corrupt raw stock trigger prices. Before rerunning, documented a **data-only source basis change**: calculate previous session as-of-close from previous trading session's LAST RTH 15:55 five-minute bar CLOSE (known before announcement), and use daily series ONLY to check corporate action adjustment ratio consistency before/after reaction. The adjustment ratios were consistent so no price exclusions in repaired run. No trade entry criteria or threshold was changed. Both versions were historical, not an untouched blind experiment. Corrected code and workflow committed; source files preserved.

## Actual complete repaired outcomes
- **45/45** scheduled issuer earnings reaction sessions with complete date-specific archived RTH five-minute Webull bars (nine date-grouped raw JSON files, exactly 78 bars per full session). Previous daily closes stored in three raw JSON parts, but stock threshold uses 5m historical actual as-of close.
- **24** did not touch −5% intraday at all on that reaction day; **2** first touched −5% only AFTER 11:30 ET (CMCSA at 14:45, GE at 12:05); **19** first touched −5% by 11:30.
- **5 of these 19** recovered enough by the 4pm regular close that they did NOT finish the session down at least 5%: **DLTR (−3.92%), FIS (−1.16%), NOC (−2.23%), QCOM (−2.62%), TXN (−3.13%)**. Thus an end-of-day −5% filter would literally exclude 5 genuine intraday dislocations, including **two successful next-bar +1.5-before−1 stock rebounds (DLTR and NOC)**.
- Among 19 first-5% as-of eligible episodes, frozen seller exhaustion setup produced **0 actual entries**: **11** had no lighter-volume retest at the original low, **5** had a further material breach of original low (invalidates a FAILED lower-low story), **3** had an eligible low/volume retest but not a confirmed expanding-volume buyer breakout. **Zero** passed the full sequence; outcome profitability for filtered trades **undefined**, NOT 0% win rate.
- Unfiltered immediate-next-five-minute-opening-stock entry after the initial -5% complete candle produced **19 actual entries**, **7 +1.5% target wins**, **12 first -1% stops**, zero timeouts. Target-first rate **36.84% of trades**, arithmetic average **−0.0789% gross STOCK** per entry, or **−0.2789% after a purely hypothetical 0.20% trading roundtrip**. The seven target winners were **CSCO, CVS, DLTR, ISRG, NOC, TPR, UPS**, ALL reached target on reaction day itself. THIS IS NOT OPTIONS P&L. Its profit target 1.5x stop and conservative stop-first allows positive arithmetic edge at win rates under 50% in principle, but observed gross actually negative and fees widen losses.
- All **seven immediate-buy target winners failed to exhibit the specifically required weaker-volume retest of their FIRST low** before getting underway. This is the central mechanical mismatch: a same-day earnings gap-down and sharp rebound may never revisit the extreme of the first 09:30 five-minute price candle, and waiting to see that retest rules out the move instead of detecting it. This does not imply buying the low would have been possible or profitable.

| Historical broad events | Count |
|---|---:|
| Earnings reaction announcements with BMO/AH | 45 |
| No -5% intraday within day | 24 |
| -5% first breached only after 11:30am | 2 |
| As-of early -5% dislocations | 19 |
| Initial low later broken >0.2% | 5 |
| No initial low retest on <=80% initial selling bar volume | 11 |
| Good retest, but not buyer volume breakout | 3 |
| Full conservative retest/volume BUY entries | **0** |
| Simple post-breach next-bar stock BUY entries | **19** |
| Simple post-breach +1.5 before -1 success | **7/19 (36.84%)** |
| Correctly captured mid-session intraday -5%-breach -> not down5 by close | **5** |

### Verdict without overinterpretation
**Reject this exact FIRST-LOW-RETEST buyer take-over scanner condition.** It failed to fire in 19 dislocations despite genuine seven early +1.5% stock winners; it did NOT test whether all forms of authentic selling exhaustion are useless or whether the user's profitable META options represent a broader edge. A raw 5m volume reduction compares total prints, not signed aggressive sell order flow; a green high-volume candle is at best a BUY-INITIATIVE proxy. First 09:30 high-volume dislocation bar is not always meaningful support to retest. A stock might reverse immediately, form a higher low at a **higher price level**, or take days to stabilize. Strict same-low retest selects a particular morphology that may be rarer than broad recovery and will certainly skip many strong immediate moves.

An information-valid next candidate **if justified in a DIFFERENT untouched quarter/company cohort** would allow first 5m candle after -5% breach and seek next 1–4 bars of sustained buyer initiative (higher closes / lower wicks / expanding green candle volume) **without demanding the initial 09:30 low be retested**, and cap entry distance from first observed trough. Predefine clean thresholds once; do NOT tune +/− stop widths, 80%/120% volume and 5m windows on these 45 observed outcomes and claim victory. To prove the user's cheap-call trading mechanism, historical contemporaneous option ask/bid, delta, DTE, and all wins/losses would still be needed. Never promote results to A+ scanner from this dataset or treat first print as executable option ASK.

## Reproducibility
- `frozen_all45_jul_sep2026_earnings_announcements_pre_5min.json` — all 45 and seven excluded announcement timestamps fixed before 5m retrieval.
- `frozen_intraday_first_failed_low_volume_takeover_45events_2026-10-10.md` — frozen rule plus transparent post-first-pass data-basis repair amendment.
- `first_failed_low_volume_buyer_takeover_45events_results_2026-10-10.json` — exact event-by-event event-day first threshold, volume-stage failure, baseline stock return and source adjustment ratios, including no events dropped.
- `first_failed_low_2026_all45_intraday_week2026-*.json` — nine Webull actual historical M5 RTH price/volume source files.
- `first_failed_low_2026_all45_daily_priorclose_part*.json` — three historically ADJUSTED daily comparison source files, do not use for as-traded threshold.
- `run_first_failed_low_volume_buyer_takeover_all45_2026.py` and `.github/workflows/earnings-first-failed-low-45event-2026.yml` — executable reproducible code with entire same universal roster.
