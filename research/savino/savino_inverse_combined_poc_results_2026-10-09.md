# Savino inverse forecast + horizontal levels: October 8 retrospective proof of concept
Completed: 2026-10-09
Prior work: research/prior_work/savino_inverse_timing_combined_poc_prior_work_2026-10-09.md
Method (frozen before numeric scoring BUT AFTER known outcomes): research/savino/savino_inverse_combined_poc_protocol_v0_1_2026-10-09.md
Inputs/score rows: research/results/savino_inverse_poc_2026-10-08_intervals.csv
Re-score script: research/run_savino_inverse_poc_v0_1.py
Verdict: **MEASUREMENT PIPELINE FEASIBLE / NO DEMONSTRATED PREDICTIVE EDGE / NOT PRODUCTION-ELIGIBLE**.

## Provenance & integrity
- ORIGINAL OCT 8 PREMARKET Savino post screenshot provided by user (screenshot time 08:58 ET, post ~10 minutes old). Source image SHA-256: `c6f0e58c5b5bb2e2710c477d1b885fc9e4bd611f86613d96522f2c5130d726e9`. Red curve digitized ONLY from the premarket image, not the later results screenshot.
- POST screenshot "Here's the result of today's inverse chart" SHA-256: `35e8be730ffbc8f9e8c361701f4b93030b3bc1642e5fc238266a257aa04f31bc`. This was visually checked for source consistency only.
- Original premarket red chart LEFT axis spans about **7795–7807 SPX**, whereas later results screenshot LEFT axis spans about **7730–7805 SPX**. This is a major rescaling/representation difference. **Do not assert morning red curve precisely predicted the 7730 low.** It cannot be treated as an exact forecast of SPX price magnitudes.
- Chart time-axis x calibration manually estimated from 10:00/12:00/14:00/16:00 tick labels, not independently verified. Approx x=255 at 10am and +230 pixels per two hours in a 968px enlarged crop. Small screenshot extraction and time-zone interpretation have uncertainty.
- Observed price proxy = connected Webull SPY October 8 RTH M5, exactly 78 bars originally retrieved; 13 half-hour endpoint closes are saved in results CSV. SPY candles are NOT exact SPX.
- Research sample is ONE retrospectively noticed / user-provided, eye-catching inverse forecast day. Forecast was posted before session, but THIS RESEARCH TEST was designed with outcome already known.

## Primary fixed 30-minute directional metric
- 12 NON-OVERLAPPING windows 10:00–16:00 ET.
- Forecast sign from original red-line slope over same window: screen y falls >12px => UP, rises >12px => DOWN, else FLAT.
- Actual sign from 30-minute Webull SPY change: >= +$0.15 => UP, <= -$0.15 => DOWN, else FLAT.
- **Matches: 6/12 = 50.0%**.
- Same-day **always-UP = 6/12**; **always-DOWN = 6/12**. This is NOT evidence that a time-forecast provides improved phase direction.

| Window ET | Morning inverse | Webull SPY change | Actual | Correct? |
|---|---|---:|---|---|
| 10:00–10:30 | DOWN | +1.1213 | UP | NO |
| 10:30–11:00 | DOWN | -1.0900 | DOWN | YES |
| 11:00–11:30 | UP | -0.6900 | DOWN | NO |
| 11:30–12:00 | DOWN | -0.2500 | DOWN | YES |
| 12:00–12:30 | DOWN | +1.0300 | UP | NO |
| 12:30–13:00 | DOWN | -2.3000 | DOWN | YES |
| 13:00–13:30 | UP | -2.0600 | DOWN | NO |
| 13:30–14:00 | UP | +0.8400 | UP | YES |
| 14:00–14:30 | UP | +1.4300 | UP | YES |
| 14:30–15:00 | UP | -0.4700 | DOWN | NO |
| 15:00–15:30 | UP | +0.5100 | UP | YES |
| 15:30–16:00 | DOWN | +0.5400 | UP | NO |

The path visually captured an afternoon selloff followed by recovery, but the forecast predicted DOWN 10:00–10:30 while SPY gained ~1.12 points, and predicted a reversal around 13:03, while the SPY session low came inside the five-minute bar starting **13:25 ET**, approx **22 minutes later**. The trough clock error is approximate given chart x-axis and 5-min bar resolution. +/-15m time-axis diagnostic produced 6–7 matches of 12 with possible edge clamping; do not optimize timing shift.

## Combined first-entry check — IMPORTANT: HYPOTHESIS, NOT EXECUTED STRATEGY
From independently frozen Savino destination v0.1 on this date:
- First opening-range+VWAP signal **LONG**, confirmation 10:05 ET, simulated next-bar 10:10 SPY entry ~775.810; structural stop ~775.090.
- Next higher Savino posted SPX level 7813 translated with prior-close SPX/SPY basis to ~SPY 778.339; nominal target/risk ~3.51R.
- Original chart inverse phase over 10:00–10:30 was DOWN, contradicting that entry. A hypothetical combined phase-concordance filter would have flagged it as not aligned, and the baseline long eventually stopped before hitting that target.
- HOWEVER, SPY actually moved UP during 10:00–10:30, so inverse timing's immediate 30m direction was WRONG; vetoing a later losing trade would be a cherry-picked ex-post observation from one trial. **No claim of avoided loss, accuracy improvement, or live veto is justified.**
- The levels 7786/7762/7734 are descriptive later-price landmarks and could function as future non-directional map annotations. The post-forecast extreme near 7734 does NOT prove the original inverse predicted that magnitude.

## Four-arm architecture: status after this POC
1. Price-only independent entry: one Oct-8 baseline signal, studied.
2. Price + Savino-level destination: one Oct-8 baseline signal, target-first failed.
3. Price + original inverse phase: timestamped possible disagreement identified; NOT tested as authorized signal/veto.
4. Price + Savino levels + inverse: same hypothetical disagreement; **sample N=1**, no comparative statistical or economic performance test possible.
No A+ v1.0 changes, promotions, backfills or repricing by hindsight.

## Next untouched evaluation prerequisite
- Acquire and preserve COMPLETE daily premarket source forecasts with actual curve timestamps and time-zone metadata, posted levels, revision history, and independent SPX M5 bars for 30–50+ days. Require a usable raw chart source/numeric forecast curve.
- Establish stable precision of chart axes across pre/post screenshots. Do not presume red line's dynamic visual magnitude predicts SPX target prices.
- After mandatory prior-work and pre-spec v0.2, compare the same independently qualified trades and stops under price-only, price+levels, price+inverse and combined overlays with risk, distance-matched controls and net option execution economics; hold an untouched sample and measure opportunity cost of filtered winners.
- Until then, Savino inverse remains **VISUAL RESEARCH CONTEXT ONLY**, not a trading timing gate; Savino major levels also remain optional unvalidated reference context. Keep frozen Investing OS A+ v1.0 / late-state-change v0 unchanged.
