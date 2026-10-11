# FROZEN v1 before NEW matching or financial-outcome computations: 164-event recovery case-control
Frozen UTC calendar date: 2026-10-11. **Discovery-only, retrospectively previously price-outcome-exposed, not blind holdout.** The scientific record of the frozen 2023–Jun2026 164 quality screen and past D4 exercise cannot become unseen by making fresh comparisons.
Prior review: `research/prior_work/earnings_164_matched_fundamental_winner_failure_prior_review_2026-10-11.md`.

## Questions/labels (kept DISTINCT)
On all 164 archived point-in-time-screened quality PASS first- or second-reaction-session >=5% EARNINGS SELLOFF events:
A. D4 OPEN stock entry with **+3% target before -5% stop** over 20 entry-inclusive full RTH sessions; stop-first ambiguous daily OHLC; later opening gap exit at actual open, timeout final bar close, 20bp fixed illustrative trade costs. Every event gets D4 trade result, whether or not fresh low occurred by D3.
B. Full recovery within 60 post-D0 sessions: a subsequent DAILY CLOSE >= RTH earnings-pre-announcement stock close (D0 may be 2nd reaction session). Use `quality_164_long_horizon_recovery_2026-10-10.csv` `h60_fullclose`, all 164 must have `h60_eligible`; do not mislabel intraday partial +5% touch or future option gains as full recovery.
C. As-of-D3 further lower low (D1/D2/D3 min intraday LOW below D0 LOW) is a predeclared STRATIFIER, not a tuned rule. Focus A for the subset if numeric count sufficient, otherwise state underpowered.
Describe A,B,C jointly for original92 vs company-disjoint72, AH vs BMO, years, sample totals, not only winners. If archival D4 and recovered definitions cannot be reconciled, label unavailable and stop rather than invent.

## Continuous historical fundamentals, available 72 of 164 only
For exactly 72 PASS events in `holdout_final_136events_2026-10-10.csv`, inner-join by TICKER+EARNINGS DATE+SELLOFF DATE into `holdout_quality_batch_0_2026-10-10.json`.. `holdout_quality_batch_8_2026-10-10.json`.
Three predeclared **pre-earnings** factor features only, WITHOUT outcome-informed cutoffs:
1. `yoy_growth_pct`: latest published quarter revenue year-over-year percentage.
2. `debt_equity`: latest pre-earnings published total debt/equity, positive denominator.
3. `cash_conversion` = trailing four quarter FREE CASH FLOW / trailing four quarter NET INCOME (both strictly positive under existing screen), only finite ratios; report medians, NOT assume cash conversion greater than one is always good across bank/nonbank sectors. No scaling with current stock market prices.
Narrate publication-date quality from original archived calculation, but original92 numerical values were NOT archived: mark all three as MISSING (not zero and not quantified). `ttm_income` and `ttm_fcf` raw values are used only to derive ratio; absolute size-biased monetary totals are not used for predictive results.
No historical analyst consensus EPS revisions or recently updated management EPS guidance relabelled as known historical inputs. The prior 27/72 guidance proxy already FAILED separately.

## Exact matched-pair design for each label A and B within numeric subset
Case = A TARGET_FIRST vs control A STOP_OR_TIMEOUT; separately B FULL_RECOVERY vs control NO_FULL_RECOVERY. Work on 72 PASS events, no inferred results for missing Original92 fundamentals.
Exact calendar SELLOFF YEAR and after-hours vs BMO release session to reduce major confounding. Sort cases by ABS(SELLOFF PCT) ascending, then ticker, then selloff date. For each case select unused control **of DIFFERENT TICKER** with smallest ABS difference in ABS(SELLOFF PCT), max permitted distance **5 percentage points**. Break ties lexicographically ticker, then selloff date. If none in same year/session and within ±5 percentage points, case remains UNMATCHED. No control reuse. Matching DOES NOT balance industry, company risk, or market regime within a year, so not causal; report unmatched.
For each of 3 fundamentals, compute paired difference = CASE − matched CONTROL and median/mean paired differences, count pairs with case > control, case < control, tied, and TWO-SIDED exact sign test ignoring ties for DESCRIPTIVE uncertainty; NO cutoff/p-value mining.
Also report cohort-wide successful vs failure numeric median/mean for all 72 including unmatched and by AH/BMO if sizes allow.
For A D3-further-low selected subgroup, perform **same exact matching rule** independently, but label exploratory underpowered if <10 pairs. Does not change existing overall pair assignments.
Safety/calibration: compare any sign indication across A vs B and AH vs BMO, and matched vs unpaired. No claims of incremental predictive utility without independent validation.
All 164 = population-level descriptive A/B outcomes; 72 = only continuous FUNDAMENTAL matched analysis.

## Audit/reproducibility/verdicts
Source archived daily OHLC JSONs 92 and 72, RTH bar indexed `event_index`, event metadata all CSVs, long-horizon audit 164 csv, quality row JSON batch_0..8.
D4 model: D0 first qualifying earnings selloff close; enter opening 4th following full RTH session; high target +3% / low stop -5%; even entry day ambiguous stop-first; later gaps at observed open; timeout final session CLOSE, full 20 sessions data required. Earnings release next quarterly announcement during 20 sessions is NOT systematically excluded; do not attribute subsequent news to initial release.
Reconciliation: require 92+72 original company cohorts =164 unique source rows, 72 detailed numeric matches with quality PASS, h60 eligibility 164; count BMO/AH; cross-check D4 AH and early-low subset earlier n54 with 38 target/16 stop exactly.
Predeclare no threshold search/ML model fit on these previously outcome-observed events. Explicit verdict **NOT SUPPORTED / INCONCLUSIVE / HYPOTHESIS-GENERATING** unless signs agree across outcomes/cohorts and at least 15 matches and sign-test p<0.05 after acknowledging 3-factor comparisons; even then strictly RESEARCH-ONLY and never scanner production. A fundamental "edge" cannot be proven by retrospective matching or by a p value alone. Missing historical same-period consensus revision needs separate acquisition.
Save machine-readable all 164 event rows and matched control pairs + an auditable script, record result summary and update master/GDocs. No paid data, trading or scanner modifications.
