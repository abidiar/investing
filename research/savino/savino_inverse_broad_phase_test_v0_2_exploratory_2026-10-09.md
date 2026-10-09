# Savino inverse broad-phase test v0.2 — exploratory re-scoring
Created 2026-10-09 (AFTER October 8 outcome AND after original 30-minute evaluation).
Status: RETROSPECTIVE ENGINEERING / NOT OUT-OF-SAMPLE. Analysis windows are motivated by user preference for broad directional correctness. This must not be represented as frozen ex-ante predictive validation.

## Prior work and immutable sources
Read research/prior_work/savino_inverse_timing_combined_poc_prior_work_2026-10-09.md and research/savino/savino_inverse_combined_poc_protocol_v0_1_2026-10-09.md, then use ONLY the already-archived v0.1 derived half-hour endpoint series:
research/results/savino_inverse_poc_2026-10-08_intervals.csv. Forecast pixels are from Oct 8 ORIGINAL PREMARKET screenshot, not subsequent 'results' screenshot. Actual SPY half-hour endpoint closes derive from Webull RTH M5. This premarket chart has different Y scale from later results chart: ONLY directional/turning-time analysis is viable.

## Research goal
Does the original forecast match broad 60/90/120-minute directional phases more usefully than the strict 30-minute pilot, and how sensitive is such 'general correctness' to choice of time-window size/alignment? Account for ordinary price-only baselines and whether the combined context would have materially affected a precommitted independent entry.

## Fixed phase definitions (set before calculating this re-scoring)
- 13 time endpoints, 10:00 through 16:00 ET, every 30m. Forecast = original pre-market chart y-pixels per half-hour. Y decreases when forecast predicts increase.
- Predicted UP if initial forecast y minus ending forecast y > 12 px; DOWN if < -12 px; otherwise FLAT. Equivalent to original 30m threshold, NOT changed for wider windows.
- Actual UP if SPY closing price at end of interval minus start >= $0.15; DOWN if <= -$0.15; otherwise FLAT. No hindsight epsilon adjustment.
- Primary *user-centered broad correctness* view: fixed non-overlapping windows anchored at 10:00, durations 60, 90, 120m, covering 10:00–16:00 without gaps, respectively 6, 4, 3 windows. 30m (12) historical v0.1 benchmark unchanged.
- IMPORTANT SENSITIVITY: calculate overlapping windows sliding in 30m increments for each of 60/90/120m, and identify difference from the nonoverlap reported headline. Sliding windows are correlated, NOT independent evidence.
- Compare at EACH horizon to always-UP and always-DOWN baselines (and majority-class count); also compare same-day prior-window trend persistence where defined without peeking forward. Do NOT choose best horizon, lag, threshold, or window anchor as trade policy.
- For robustness, additionally calculate an alternate grid anchored 10:30 ET, including only complete windows before 16:00. Report if strong nonoverlap result disappears.
- Broad V pattern check: predicted SPY direction into forecast main low around 13:00 (10:00→13:00) and from it until 16:00 (13:00→16:00), and actual realized signs. Explicit note that actual session trough could occur later.
- Turning-time: forecast primary trough = global maximum forecast pixel y in endpoint interval 11:00–14:30, using first maximum tie; actual RTH primary low = lowest actual 5m low in 11:00–14:30 ET (from already recorded Webull source if accessible), with exact bar start time. Hit within ±30m and ±60m; only ONE selected turn, not every wiggle. From existing v0.1 documentation actual 13:25 5m bar is expected, but verify against Webull before scoring.
- Do not credit forecast exact price target at 7730: early chart scale ~7795–7807, result chart rescaled ~7730–7805.
- Do NOT claim independent four-arm trade improvement: Oct 8 only 1 independently signaled entry (10:10 long) and inverse phase at that instant conflicted; one retrospective veto would be cherry picking.

## Outcome schema
Nonoverlap 30/60/90/120: n, matches, baseline always-UP, baseline always-DOWN, forecast category distribution, actual category distribution, confusion on mismatches. Sliding 60/90/120: n, matches, baselines. Alternate anchored 10:30: n, matches, baselines. Core down-to-trough/up-after-trough true/false; minute error; ±30/±60 hit. All outputs include 'ONE SELECTED DAY / NO VALIDATED EDGE'.
- Verdict distinct for (a) general qualitative phase alignment; (b) stable incremental decision advantage. No production change or new A+ rules under any result.

## Production and scientific boundary
This is revised exploratory descriptive scoring prompted AFTER observing first 30m accuracy and desired tolerances. It **does not rescue** the original 6/12 result. It cannot validate Savino levels, authorize new entries/exits, override A+ gates, or justify live vetoes. Future test requires pristine complete premarket inverse+levels archive, exact SPX M5, preregistered broad-horizon metric with baseline and an untouched set of 30–50+ days.
