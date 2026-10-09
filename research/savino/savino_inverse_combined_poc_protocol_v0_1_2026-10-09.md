# Savino inverse time-path + posted levels: OCT-08 retrospective POC protocol v0.1
Frozen for implementation: 2026-10-09 (the Oct-08 result is ALREADY KNOWN, so this cannot count as ex-ante validation regardless of freeze timestamp).
Verdict category: pipeline/measurement feasibility only. No production changes.

## Raw evidence available before vs after
PRE: User-supplied screenshot of Savino's "Also posting the intra-day inverse here" from Oct 08 screenshot at 08:58 ET, post ~10m old, with small SPX 5m chart. User-supplied levels post ~1h old: **7836 / 7813 / 7786 / 7762 / 7734**.
POST: separate user-supplied screenshot ~Oct 09 07:30 ET "Here's the result of today's inverse chart of Price & Time analysis" with forecast-overlaid candles.
NEVER digitize *forecast* from POST image for timing validation; only use PRE picture to reconstruct forecast path.
The Y-axis ranges differ PRE (~7795..7807 SPX) and POST (~7730..7805 SPX); do NOT infer that PRE forecast predicted precise POST trough price ~7730. The two images might rescale/transforms; magnitude accuracy is unscorable.

## Data
PRE chart crop from earlier screenshot: native pixel region x205..810, y940..1400, scaled 1.6x for visibility, yielding 968x736 reference image. User screenshot filenames/provenance preserved in conversation.
M5 actual: connected Webull SPY RTH 78 5m bars 2026-10-08; returns/candle time on SPY are a PROXY for SPX dynamics, not exact index.
SPX posted levels as separate static contextual locations; direct touches need exact SPX data, not proxy/10.

## Fixed chart/time alignment
In the upscale chart PRE crop: horizontal x=255 at 10:00 ET, x=485 at 12:00, x=715 at 14:00, x=945 at 16:00. Treat as **approximate manually read chart axis**. Linear x = 255 + (minutes_since_10:00)*230/120, no time shifting to improve fit.
Predicted forecast red trace y(x): identify red-ish line only for x>=215 on upscale PRE chart; a priori segmentation threshold R>=115, R-G>=20 and R-B>=20; sample median/redline per column; fill tiny gaps using linear interpolation. y coordinate inverted: decreasing y => upward forecast phase.
Potential ambiguity: curve/axes low-res, any 30m forecast differences within +/-12 pixel are labeled NEUTRAL; otherwise UP or DOWN.
Actual 30-min returns: 5m RTH close from candle END at each 10:00, 10:30 ...16:00. If 16:00 no candle timestamp, 15:55 bar close. Actual UP if delta >=+$0.15 SPY, DOWN if <=-$0.15, else NEUTRAL. These arbitrary tolerances are engineering sensitivity, not optimized on results.

## Fixed evaluation
- 12 non-overlapping time intervals: 10:00–10:30 through 15:30–16:00 ET.
- Count 3-class agreement forecast UP/DOWN/NEUTRAL with SPY changes, and coverage of forecast non-neutral windows; separately include naive all-DOWN and all-UP baselines on same hours (descriptive 1-day).
- Do NOT flip forecast "inverse" direction, shift its times, or re-scale magnitudes to maximize agreement after seeing outcomes. "Inverse" is Savino's term; red path is interpreted visually as the predicted market price direction depicted in his charts.
- Report forecast broad trough time from smallest y? red curve low in price = maximum pixel y for 11:00..14:30; actual SPY low bar time in matching window; error shown as approx due axis and image resolution.
- Compare already frozen independent OR+VWAP October 8 first entry (10:10 LONG @ 775.81, structural stop 775.09) to the **as-posted forecast phase** at 10:00–10:30 and available nearest Savino target, but NO simulated trading outcome changes or post-hoc signal permission. A hindsight appealing gate remains HYPOTHESIS ONLY.
- Mark visual resemblance of forecast timing and actual shape separately from target/stop decision-usefulness.
- Run time-anchor sensitivity +/-15 minutes as DIAGNOSTIC ONLY not as optimized fit.
- No Monte Carlo significance or live directional hit probability from one day; no tweak without new v0.2 and untouched days.

## Required outputs
1. Forecast pre-source time + integrity/axis caveat.
2. Tabulated 12 30m PRE-red slope and Webull SPY realized signs / baseline.
3. Estimated forecast midday trough vs actual SPY trough ET error.
4. Interaction with Oct 8 independent entry and Savino levels, with no classification modification.
5. Reproducible code and machine-readable compact data saved under research/results/ if permitted; store screenshot hash but no third-party chart image bytes.
6. Verdict PIPELINE WORKS/DOES NOT WORK; PREDICTIVE EDGE UNDETERMINED; next untouched prospective data plan.
