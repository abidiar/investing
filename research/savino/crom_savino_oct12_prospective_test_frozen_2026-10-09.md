# Crom × Savino — Oct 12 2026 prospective volatility test v1.0 (FROZEN BEFORE OUTCOME)

**Frozen 2026-10-09 before Oct 12 RTH.** Status: PENDING. No Oct 12 data used. This is a prospective research hypothesis, NOT an A+ signal or trading instruction.

## Source alerts, preserved unchanged
Crom Discord blue **Spike Watch** cards issued Oct 05 15:00 ET (as displayed in screenshots): SPY, TF 60, projected Oct 12 **15:30** (expected bars 43216, 43219) and **17:30** (bars 43222, 43225), window ±4 bars, typical spike range 6.01% (metric undefined). Two center times, duplicated IDs; treat as **ONE OCT 12 ALERT CLUSTER**, not four independent forecasts. Original screenshots supplied in conversation Oct 09 08:38. Crom yellow Oct 09 05:00 cluster ~2.63 trading days is a **separate forecast family**, conditional time near Tue Oct 13 under 6.5-RTH-hour assumption; do not conflate.

## Frozen clock assumptions
User authorized: consecutive **60-minute elapsed clock-hour bars**, ET/EDT, ±4 hours around each center, boundaries inclusive. Thus centers and windows:
- Center 15:30 -> **11:30–19:30 ET**; RTH 11:30–16:00.
- Center 17:30 -> **13:30–21:30 ET**; RTH 13:30–16:00.
- Unique union **11:30–21:30 ET**, RTH **11:30–16:00**. Count one event cluster. Analyze each center's window descriptively; **PRIMARY** use the **RTH union** so overlapping alerts cannot inflate sample size.
- NYSE/Nasdaq open Oct 12 despite Columbus Day/Indigenous Peoples Day; **U.S. bond market closed**, potentially changes cross-asset information; flag as event/calendar condition. NYSE source https://www.nyse.com/trade/hours-calendars ; https://www.investopedia.com/is-the-stock-market-open-for-columbus-day-here-s-the-fall-and-winter-trading-holiday-schedule-12159740 .
- Outside RTH: no primary score without verified extended-hours bars. The model's timezone, exact meaning of ±4 bars and 6.01% are unverified; this is an explicitly conditional test.

## Frozen realized-volatility outcome and comparison
- Instrument SPY, Webull RTH five-minute OHLC, full bars only. Candle range % = 100×(high-low)/open. Compare Oct 12 **11:30–15:55** ET 5m bars with the same exact 11:30–15:55 clock-time bars on **the 20 completed trading sessions immediately before Oct 12** (as of freeze Oct 09 is not completed; last session must be Oct 09 after its close, then baseline sessions Sep 14–Oct 09, excluding weekends). No Oct 12 bars enter threshold. If Oct 09 incomplete at fetch, defer threshold finalization until completed Oct 09 RTH, then freeze before Oct 12 open; do not substitute a different date range silently.
- **PRIMARY spike criterion**: Oct 12's maximum individual 5m range % within 11:30–16:00 RTH union **strictly exceeds the nearest-rank 80th percentile of the 20 historical daily maximum 5m ranges in that exact 11:30–16:00 RTH window**. Nearest-rank index ceil(0.8×20)=16 in ascending list. Ties do not count. A PASS means elevated peak relative to historical window, not that Crom's proprietary implied-vol metric was confirmed.
- Secondary: mean of all 5m candle ranges within same window versus historical mean; per-center 11:30–16:00 and 13:30–16:00 peak/mean; count of five-minute bars above pooled matched-window historical 80th percentile (NOT independent trials); where the day's overall RTH peak occurs (inside vs outside union); session range and event timing. Report empirical base rate and false alarms, not just hits. Report out-of-window extremes.
- **Control**: historical 20 daily window maxima, not pooled five-minute bar maxima, to avoid a nearly-always-hit event definition. Oct 08 retrospective descriptive baseline not an OOS hit-rate estimate. Do not revise thresholds, union, clock rules or event definition after Oct 12 outcome.

## Savino independent overlap (frozen before outcome)
- Source archive `research/savino/savino_spx_october_2026_monthly_primary_inverse_update_captured_2026-10-09.md`: monthly primary/inverse are opposite-direction scenarios, not scaled for price; Oct 09 possible spike direction uncertain; major turn Oct 17–19; **NO specific preposted Savino Oct 12 intraday pivot currently documented**.
- If a Savino **preposted and timestamp-verifiable Oct 12** intraday curve is supplied before relevant window begins, archive raw time-axis forecast BEFORE reading Oct 12 subsequent outcomes, then compare its predeclared pivot window to Crom's 11:30–16:00 RTH union. Do not select primary vs inverse post hoc or count both opposite directions as success. If no independently frozen Oct 12 Savino forecast, report combined overlap **NOT EVALUABLE**, not success.
- Savino daily horizontal levels are price destinations/invalidations, not timing signals, and cannot qualify a Crom volatility overlap by themselves.

## Result record (must remain blank until post-close)
Date/time run: PENDING. Completed Oct 09 baseline count: PENDING. Historical daily max 80th percentile: PENDING. Oct 12 max and time: PENDING. Primary pass/fail: PENDING. Mean volatility comparison: PENDING. Outside-window largest bar: PENDING. Savino independent preposted pivot: NOT CURRENTLY AVAILABLE. Combined timing overlap: NOT EVALUABLE. Frozen A+ detector effect: NONE.

Related source audit `research/savino/crom_savino_volatility_alignment_capture_2026-10-09.md`.
