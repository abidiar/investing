# Savino as destinations / invalidation — exploratory test v0.1 (FROZEN BEFORE CALCULATING OUTCOMES)

Freeze date: 2026-10-09.
Status: exploratory retrospective pilot, NOT an out-of-sample edge test. Do not modify A+ DAY DETECTOR v1.0 or the 11:00 late-state-change experiment. No live-trade probability inference.

## Preset sample
Exactly six days with level sets already archived from user-supplied premarket posts: 2026-09-25, 09-28, 09-29, 09-30, 10-02, 10-08. Do not add/remove days after observing results.

Levels (SPX) by date:
- 09-25: 7774, 7749, 7726, 7700, 7676, 7648.
- 09-28: 7765, 7739, 7716, 7689, 7663, 7634.
- 09-29: 7729, 7705, 7679, 7649.
- 09-30: 7719, 7695, 7668, 7641.
- 10-02: 7750, 7725, 7699, 7672, 7642, 7611.
- 10-08: 7836, 7813, 7786, 7762, 7734.

## Data
- Primary execution path: Webull **SPY** RTH completed M5 OHLCV candles, 09:30–16:00 ET; no fabricated bars.
- Exact contemporaneous SPX 5m candles presently NOT entitled through Massive. Therefore this is explicitly a **SPY proxy test**, not a validation of exact SPX level crossings.
- SPX→SPY translation uses only previous RTH closes known before entry: ratio r = previous SPX close / previous SPY close. SPY proxy for SPX level L = L/r.
- SPX daily close from dated Yahoo historical data; SPY prior RTH close via Webull. Calibrate once per day using PRIOR close only; no same-day close or post-entry SPX levels used.
- Reject date if fewer than 78 valid RTH bars, missing prior closes, or duplicate/non-monotonic timestamps. No silent interpolation.
- If there is intrabar ambiguity (same 5m bar touches both stop and target), score **stop first**, a conservative convention.

## Independent entry signal (Savino never drives entry)
- Opening range (OR) = high/low of first SIX completed SPY RTH M5 bars, 09:30–09:55 (range known at 10:00).
- Calculate cumulative session VWAP from typical-price HLC3 weighted by per-bar volume using completed bars only.
- Scan bars timestamped 10:00 through 14:30 ET, inclusive, in chronological order. Use the FIRST bar meeting either:
  * LONG: completed 5m bar close > OR high, and bar close > cumulative VWAP.
  * SHORT: completed 5m bar close < OR low, and bar close < cumulative VWAP.
- If both are possible on different bars, use whichever fires first in time; at most ONE independent signal per session. No post-hoc alternate entry.
- Signal becomes executable at OPEN of NEXT M5 bar; record exact time and entry price. Exclude signal if no next bar.
- Structural stop: LONG -> min(low of signal bar, low of previous bar) minus $0.05; SHORT -> max(high of signal bar, high of previous bar) plus $0.05. Exclude invalid zero/negative risk.
- Stop is fixed from entry. No option spread/IV modeling: outcomes on SPY underlying proxy, not options P&L.

## Savino destination and controls
- Savino target T1 = closest strictly higher posted Savino level proxy for LONG, closest strictly lower for SHORT, relative to entry (minimum $0.05 gap). If no level in direction, mark NO TARGET, not a win.
- Level spacing control = steps of 25 SPX index points from PREVIOUS SPX close, projected to SPY using prior close ratio. First grid line strictly beyond entry in trade direction. Offsets predetermined [0, 5, 10, 15, 20] SPX points; five fixed, paired controls per same trade. No optimizing offset after results. For each grid, use nearest qualifying line.
- Prior-day H/L control: for LONG use prior RTH SPY high; SHORT use prior RTH SPY low, only if beyond entry; otherwise NO TARGET.
- Evaluate Savino and controls on IDENTICAL entries/stops; target hit only if price first touches respective target strictly before stop before RTH 16:00. If target/stop both touched in the same candle, count stop first.
- Report target distance, entry-risk ratio, 2:1-eligible fraction, target-first fraction over ALL eligible first signals (including no-target as not achieved), and median target-distance; keep targets with R:R below 2 separately rather than asserting executable A+.
- Also record favorable and adverse underlying SPY excursion to close and final close return for each first signal; do not confuse descriptive MFE with authorized A+.
- No statistical significance or predictive-edge claims from six selected dates; compare to controls, do not assume touching posted levels gives an edge.

## Limitations / next phase
SPY vs SPX mapping can be off intraday due to ETF/index tracking basis; require exact SPX M5 for final validation. Sample selected by screenshots has survivorship/selection risk. Opening-range signal is newly invented research control, not a previously used live A+ setup. Only declare 'interesting' vs 'not supported'; replication requires 30–50+ untouched **timestamp-archived** days and a matched-level null.

Archive untouched level screenshots and market raw data separately where licensing allows.
