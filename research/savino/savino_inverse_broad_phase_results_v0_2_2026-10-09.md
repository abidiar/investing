# Savino inverse broad-phase / turning-window test v0.2 — October 8, 2026

Completed: 2026-10-09. Status **EXPLORATORY RETROSPECTIVE RE-SCORING**.
Protocol: `research/savino/savino_inverse_broad_phase_test_v0_2_exploratory_2026-10-09.md`
Immutable prior study: `research/savino/savino_inverse_combined_poc_results_2026-10-09.md` (30-minute original 6/12).
Reproduction: `research/run_savino_inverse_broad_phase_v0_2.py`
Full 88 derived window rows: `research/results/savino_inverse_broad_phase_v0_2_windows.csv`
Original 12 underlying 30-minute data rows: `research/results/savino_inverse_poc_2026-10-08_intervals.csv`

**Verdict:** GENERAL BROAD PHASE MATCH ON THIS SELECTED DAY (90m and 120m), HIGH MEASUREMENT HORIZON/ANCHOR SENSITIVITY. PREDICTIVE EDGE AND COMBINED TRADE INCREMENTAL VALUE **UNPROVEN**. NO PRODUCTION PROMOTION.

## Fixed-grid directional matches
All grids use the SAME ORIGINAL premarket red-curve pixel points and Webull SPY 5-minute-derived closes. No time shifting or endpoint selection based on outcomes. Forecast UP if original-red-line y drop >12 pixels, DOWN if rise >12; actual UP if SPY end-start >=$0.15, DOWN <=-$0.15; otherwise FLAT. Every grid covers 10:00–16:00 when anchored at 10:00.

| Horizon | 10:00 anchored correctly matched | Always UP baseline | Always DOWN baseline | Meaning |
|---|---:|---:|---:|---|
| 30 minutes (original frozen POC) | 6/12 = 50.0% | 6/12 | 6/12 | no gain |
| 60 minutes | 2/6 = 33.3% | 2/6 | 3/6 | poorer than simple down baseline |
| 90 minutes | **4/4 = 100%** | 2/4 | 2/4 | broad direction and turnaround matched, N=4 overlapping in information |
| 120 minutes | **3/3 = 100%** | 1/3 | 2/3 | broad down-down-up matched, N=3 |

### Exact 90-minute sequence
- 10:00–11:30: forecast DOWN, SPY 775.3187 → 774.66 = **−0.6587** (match).
- 11:30–13:00: forecast DOWN, SPY 774.66 → 773.14 = **−1.5200** (match).
- 13:00–14:30: forecast UP, SPY 773.14 → 773.35 = **+0.2100** (match). This is only ~0.027% upside and would become NEUTRAL if actual-threshold were >$0.21; fragile match.
- 14:30–16:00: forecast UP, SPY 773.35 → 773.93 = **+0.5800** (match).

### Exact 120-minute sequence
- 10:00–12:00: forecast DOWN, SPY −0.9087 (match).
- 12:00–14:00: forecast DOWN, SPY −2.4900 (match).
- 14:00–16:00: forecast UP, SPY +2.0100 (match).

## Window-alignment and overlap diagnostics
Overlapping 30m-stepped windows are CORRELATED, and cannot be described as additional independent forecast successes.

| Horizon | Rolling sliding windows | Always-UP | Always-DOWN | Alternate non-overlap starting 10:30 |
|---|---:|---:|---:|---:|
| 60 minutes | 5/11 | 4/11 | 5/11 | 3/5 |
| 90 minutes | 9/10 | 4/10 | 5/10 | **3/3** |
| 120 minutes | 7/9 | 2/9 | **7/9** | **1/2** |

The 90-minute macro-phase match is less dependent on starting exactly at 10:00 (3/3 at 10:30 anchor and 9/10 overlapping windows). The 120-minute 3/3 is LESS robust: 1/2 alternate offset, and rolling 7/9 merely equals always-DOWN 7/9. **Do not select 90 minutes as optimal trading horizon after seeing this day.**

## Main low / reversal timing (only ONE trough per chart)
Using forecast-original-premarket red-pixel points:
- Approx forecast broad trough: **13:00 ET** (trough estimated nearer ~13:03 ET by original graphic-axis linear interpolation).
- Connected Webull SPY RTH M5 session low: **13:25 ET bar**, low **$770.435**.
- Clock error ~25 minutes (or ~22 if using graphic interpolation), within ±30 and ±60-minute bands. The M5 bar start time does not tell us the precise tick-by-tick low.
- Shape: forecast 10:00→13:00 DOWN, 13:00→16:00 UP; actual SPY changes **−$2.1787** and **+$0.7900** respectively (net directions agree).
- These are one selected low and two broad directions, not calibrated predictive probabilities. The often-cited 7730 is posted SPX support, NOT a precise forecast price read from the tiny 08:58 red chart. The pre- and post-screenshots use different Y axes.

## Savino structural-level interaction / Investing OS
- Oct 8 Savino preposted SPX levels: 7836 / 7813 / 7786 / 7762 / 7734. They can describe nearby maps, but no exact SPX intraday M5 level-response dataset available for this POC; SPY is a proxy, not SPX/10.
- The one prior independent OR+VWAP signal for Oct 8: LONG at ~10:10 SPY 775.81, stop ~775.09; Savino next upper target ~778.34 SPY proxy (3.51R) not reached before stop. The original inverse short-horizon phase then was DOWN and would have disagreed with the entry.
- Yet actual 10:00–10:30 SPY was UP (~+$1.12), so inverse was WRONG in that immediate window. Broad 90-minute DOWN confirmation cannot be backfilled into the 10:10 executable trade without changing the precommitted decision horizon. No proof of an advantageous Savino-filtered trade.
- Do NOT conflate four-arm research with proven four-arm trading performance. The user-requested phase accuracy is a different outcome target from entry, invalidation, option P&L and target-first net costs.

## Next disciplined operation
- Before viewing any *new* session, predefine either 90-minute phase accuracy or a multi-resolution predeclared score with no after-the-fact horizon picking; include trivial always-UP, always-DOWN, time-of-day, opening-trend, and same-day comparable SPY autocorrelation baselines and never conflate correlated windows with N.
- Obtain 30–50+ timestamped untouched paired Savino inverse forecasts and posted level maps as published before open (plus edits), exact SPX M5 (current Massive entitlement cannot access it). If unavailable, use dated SPY proxy with clear basis metadata.
- First validate qualitative broad-phase repeatability. Only if promising, test same independently qualified trade entries for destination/invalidation improvements and false-exclusion opportunity cost. Maintain frozen A+ v1.0.
