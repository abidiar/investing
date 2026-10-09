# Crom + Savino incremental timing test v0.1 — feasibility and frozen next-step specification
Date 2026-10-09. Status: FEASIBILITY COMPLETED; PROSPECTIVE COMBINED PERFORMANCE NOT YET ESTIMABLE.

## Question and prior-work context
Does the intersection of a timestamped Crom volatility window and an independently preposted Savino time-of-day pivot improve forecasting of SPY 30–90-minute absolute moves/reversal quality versus Crom-only, Savino-only and price/time-only baselines? Prior internal work: `research/savino/crom_savino_volatility_alignment_capture_2026-10-09.md`, `research/savino/savino_inverse_broad_phase_results_v0_2_2026-10-09.md`, and `research/savino/crom_savino_oct12_prospective_test_frozen_2026-10-09.md`. External literature review is outstanding; per `research/PRIOR_WORK_REVIEW_STANDARD.md`, this document is NOT a new validated frozen outcome trial and should not be promoted as such.

## Four-arm comparison design
- **Price/time baseline**: compare SPY 5m candle ranges and future 30/60/90m absolute return and max favorable/adverse excursion from same-clock windows on preceding 20 completed sessions; no model alert information.
- **Crom only**: blue Spike Watch, deduplicate same-day repeated bar IDs, use ET ±4 elapsed hours and RTH intersection, with each alert cluster counted once. Yellow ~trading-day clusters are a separate experimental arm, not conflated with blue.
- **Savino only**: preposted intraday curve pivots timestamped before the outcome. Primary/inverse monthly paths are opposite directions; score nondirectional pivots only unless sign was selected ex ante. No inference of a pivot from horizontal price levels.
- **Intersection**: a preposted Savino pivot point falls in the already-frozen Crom blue RTH window. Score same outcome only for intersections, and separately quantify lost opportunities/false exclusions versus union and individual arms. Do not treat two models' broad discussion of volatility as independent confirmations.
- **Outcome**: for prospective new events use the Oct 12 protocol's precommitted 80th percentile of historical matched-window daily maximum five-minute range as PRIMARY Crom volatility outcome. Savino 30/60/90m phase direction and reversal tolerance require a separate untouched precommitment and independent dates. No options return claim until executable timestamp, option chain, spread, stop and slippage are available.

## Executed feasibility/overlap audit from existing frozen source records
| Date | Crom blue preposted RTH window | Savino preposted intraday pivot | Strict intersection? | Market observations | Verdict |
| Oct 08 | 13:30–16:00 ET, assuming center 17:30 and ±4 elapsed hourly bars | Approx 13:00–13:03 ET premarket | **NO** (pivot 27–30m before window) | Actual SPY low inside 13:25 M5 bar; 13:45 bar largest inside Crom window 0.172158%; Oct 08 afternoon matched 20-day mean range 0.080832% vs 0.062991%; 20-day 80th percentile of daily-window maximum 0.190314%, so max fails strict strong spike criterion | Broad same-day coincidence only; NOT a strict joint hit |
| Oct 12 | 11:30–16:00 ET union, blue centers 15:30/17:30 | No independently archived specific Oct 12 pivot yet | **NOT EVALUABLE** | Future session, do not use outcome | Crom-only forecast until preposted Savino timing arrives |
| Oct 17–19 | No blue alert in current screenshots | Broad monthly primary/inverse turning region | **NOT EVALUABLE** | Future | Savino-only watch |

## Decision and next required data
**Observed number of qualifying strict combined events: 0.** Thus no denominator for combined win rate, no incremental precision/recall, no statistically supported improvement, and no trade filter to deploy. Do not turn 0 observations into a zero percent win rate. The Oct 08 strict joint event is a NO, not a negative outcome of an eligible joint signal. Oct 12 remains untouched and frozen under its original separate protocol.
To proceed: archive preposted Savino intraday curve(s) with timestamps and time-axis before Crom windows begin, capture all Crom alerts (including misses and repeats), obtain at least 20–30 independent qualifying/nonqualifying sessions, score 4 arms against matched historical controls and actual transaction costs. No production/A+ change.
