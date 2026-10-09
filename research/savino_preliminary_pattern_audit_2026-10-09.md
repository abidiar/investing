# Savino SPX levels — preliminary pattern audit (2026-10-09)

Status: exploratory, retrospective and NOT validated. Independent from frozen A+ DAY DETECTOR v1.0 and frozen 11:00 late-state-change experiment. No historical rate here is a live probability.

## Inputs and provenance
Six dates with user-supplied, reportedly preposted Savino SPX level sets preserved in conversation/September archive:
- September 25, 28, 29, 30; October 2 and 8, 2026.
- Repo source for September: research/savino_spx_levels_forecast_archive_2026-09.md
- User-provided October 2 and October 8 Savino screenshots in conversation.
- Historical SPX daily RTH high/low (in points), taken from https://www.investing.com/indices/us-spx-500-historical-data (viewed 2026-10-09). Oct 2 also supported by https://ycharts.com/indices/%5ESPX/level and intraday https://www.statmuse.com/money/ask/s-and-p-500-close-october-2 .
- Source caveat: ChartExchange displays a conflicting October 2 range. Confirm discrepancy with canonical index data before a formal backtest.
- NOT a complete audited post archive; no claim that all Savino levels/days were captured.

## Daily range-intersection audit (not a trading-system win rate)
A "touched" level is defined strictly as an integer posted SPX level lying inside the day's reported high-low interval. This proves only that the index range included the price; it does NOT prove reaction, order, clean acceptance, tradability, or predictive power.

| Date | Preposted levels descending | SPX low-high | Exactly touched levels | Touch count |
|---|---|---|---|---:|
| 2026-09-25 | 7774 / 7749 / 7726 / 7700 / 7676 / 7648 | 7693.08–7752.07 | 7749, 7726, 7700 | 3 of 6 |
| 2026-09-28 | 7765 / 7739 / 7716 / 7689 / 7663 / 7634 | 7666.60–7724.15 | 7716, 7689 | 2 of 6 |
| 2026-09-29 | 7729 / 7705 / 7679 / 7649 | 7653.55–7699.60 | 7679 | 1 of 4 |
| 2026-09-30 | 7719 / 7695 / 7668 / 7641 | 7651.54–7722.88 | 7719, 7695, 7668 | 3 of 4 |
| 2026-10-02 | 7750 / 7725 / 7699 / 7672 / 7642 / 7611 | 7700.51–7754.67 | 7750, 7725 | 2 of 6 |
| 2026-10-08 | 7836 / 7813 / 7786 / 7762 / 7734 | 7731.26–7797.79 | 7786, 7762, 7734 | 3 of 5 |

Totals: 14 of 31 listed levels were inside reported daily ranges; at least one on 6 of 6 days; two or more on 5 of 6 days. These counts are descriptive only. Continuous prices mechanically cross any intervening levels. Density, positioning, daily volatility, and selective screenshot coverage can make touch counts unremarkable versus a naive null.

IMPORTANT CORRECTION: On October 2 the daily low 7700.51 was 1.51 SPX points above the posted 7699 level. It counts as a near approach (within two points), NOT an exact touch. Never label it an exact 7699 hit.

## Observational patterns to test (unproven)
1. Accepted break/rejection/reclaim at one major level might increase same-session probability of reaching the next adjacent level before invalidation.
2. After breaking through, a prior support level may turn into resistance and vice versa (role reversal).
3. Adjacent major levels may supply objective T1 destinations if a *separate* execution signal exists and fresh >=2:1 R:R remains.
4. Approximate subdivisions may act as useful intermediate checkpoints. Evidence is chart-derived and less certain than posted exact major levels.
5. Inverse/time projection must be evaluated independently; visually aligned shape/timing on a selected result post does not validate forecast skill.

## Measurement guardrails for next phase
- Collect exact level post timestamp and screenshots BEFORE 09:30 each day; preserve original untouched source artifacts.
- Acquire authoritative **SPX five-minute** OHLC timestamps (not SPY/10, which ignores the changing SPX-SPY basis). An attempt on 2026-10-09 to query Massive I:SPX M5 failed with NOT_ENTITLED; Webull SPY M5 is available but only a proxy.
- Score pre-specified first qualifying rejection / acceptance / reclaim; no retroactive best signal.
- Lock price/timestamp/tolerance and invalidation rules before applying to out-of-sample days.
- At each first signal track nearest adjacent level before invalidation and within time cutoff, MAE, MFE, elapsed time, 09:50/10:20/11:00 alignment, and R:R after range consumption.
- Compare against random levels matched for count, spacing and location, prior-day high/low, opening range, VWAP and conventional pivots. **Level touch count alone is not evidence of edge.**
- Separately test intraday inverse projected turning points against simple baseline like random/no-change/previous day pattern, using exact timestamped premarket forecast.
- Freeze prospective/OOS rules as a new research specification after data access and exact definitions are confirmed; do not change A+ v1.0.

## Data caveat
Some earlier narrative summaries may have misstated historical extremes, including Oct 2 7699 as a touch. This audit gives primacy to the independently published daily high/low for range membership. For temporal *sequence* a primary SPX M5 source is still required.
