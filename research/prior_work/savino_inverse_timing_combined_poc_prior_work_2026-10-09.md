# Savino inverse-chart / SPX-level alignment — prior-work review for retrospective proof of concept
Date: 2026-10-09. Scope: methodology audit, NOT a new efficacy claim.

## Question
Can a posted intraday time-path forecast add incremental timing information to independently confirmed SPY/SPX signals and separately posted structural SPX levels, beyond conventional price-only controls?

## Sources and what they establish
1. Bailey and López de Prado (2021), "How Backtest Overfitting in Finance Leads to False Discoveries," Significance, https://academic.oup.com/jrssig/article/18/6/22/7038278. Different trial definitions, selected examples, and optimizing after seeing outcomes cause spurious financial backtest edges. Implication: sample must be preposted and complete; exploratory POC not OOS.
2. Bailey et al. (2015), "The Probability of Backtest Overfitting," https://escholarship.org/uc/item/4w1110bb. Many tested variants on small sample produce false discoveries. Implication: one fixed timing metric, report baseline and no post-hoc threshold tuning.
3. Gilleland et al. (2015), forecast accuracy using dynamic time warping, https://rmets.onlinelibrary.wiley.com/doi/10.1002/met.1485. Time-warped scoring can capture timing shifts but adds methodological choices; exact-time scoring preferred for initial tradability because changing time to fit forecast defeats timing utility.
4. Waghmare and Ziegel (2026), "Proper Scoring Rules for Estimation and Forecast Evaluation," https://www.annualreviews.org/content/journals/10.1146/annurev-statistics-042424-050626. Proper probabilistic scoring is useful for probabilistic forecasts, but Savino's chart provides no explicit probabilities. Do NOT describe a qualitative path's correlation as calibrated confidence.
5. Investing OS own 6-session Savino destination v0.1, research/savino_destination_invalidation_results_v0_1_2026-10-09.md. Independent OR+VWAP entries: target-first only 3/6 and all three <0.5R; no demonstrated edge vs simple grids. Overlay must not create A+ signals.

## Data integrity priority
Available contemporaneous user screenshot at 08:58 ET of chart posted ~10 min prior on 2026-10-08, plus following-day screenshot of results overlay. **The premarket chart shows a left price scale around ~7795–7807, whereas the later result screenshot is displayed with a much wider ~7730–7805 left scale.** This could be dynamic plot scaling, transformation, or separate chart iterations; without exact source mapping it prohibits a legitimate "predicted price 7730" claim. Only *shape and time ordering* are eligible for illustrative assessment.
The actual chart's result graphic was produced after outcome and cannot serve as a predictor. Digitize ONLY the earlier chart to define the prediction path.

## Known limitations
We have one matched intraday inverse example, selected after noticing an apparent pattern. Chart exact x-axis timezone/scale is not certified and premarket screenshot is a small inset of a screen capture. Webull SPY M5 is price proxy, not actual SPX 5m. No bid-ask/options fills, and external source's methodology is unavailable. Six Savino level days do not imply six inverse-chart days.

## What remains open
Pre-specify chart timestamp-to-x calibration; obtain raw original-size chart or numeric curve coordinates and exact SPX 5m; archive 30–50 untouched paired premarket inverse+levels before outcomes; run same independently generated entries as price-only, inverse, levels and both, with same stops and conservative intrabar ordering; compare inverse timing against clock/no-forecast baselines.
