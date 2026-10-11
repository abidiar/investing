# Completed frozen matched fundamental study — 164 quality earnings selloffs (2023–June2026)
Date: 2026-10-11. **VERDICT: NO ROBUST FUNDAMENTAL EDGE IDENTIFIED / EXPLORATORY ONLY.** Frozen protocol committed before new pair-level associations: `frozen_164_match_fundamental_winners_losers_v1_2026-10-11.md`; prior review `research/prior_work/earnings_164_matched_fundamental_winner_failure_prior_review_2026-10-11.md`.

## What we genuinely measured
- **All 164** prior quality-PASS earnings selloffs across **61 unique current stocks**, 92 original (32 issuers) and 72 company-disjoint (29 issuers), 91 AH + 73 BMO, first or second earnings-reaction session >=5% closing price decline, 2023–Jun2026. Future market prices and 60-session price recoveries already previously studied, so no blind/forward validation.
- Every case assigned an objective D4 regular-session OPEN BUY, +3% gain before −5% stock stop over 20 entry-inclusive RTH sessions, stop-first same bar/gap open exits/otherwise closing timeout; 20 basis points hypothetical stock roundtrip cost. This is not $50-call option P&L.
- Separate long-term label: any **daily close >= pre-earnings closing price within 60 trading sessions**. This is not a trade and need not occur before any earlier stock stop or option expiry.
- Third label: as-of-D3 additional intraday lower low below initial qualifying D0 intraday low.
- Importantly, **original 92 historical continuous financial ratios were NOT preserved**. They had a historical published-before-announcement PASS quality screen, but NOT recoverable quantitative `yoy_growth_pct`, `debt_equity`, `ttm_fcf` and `ttm_income` values in canonical records. Numeric fundamental comparison therefore legitimately covers only **72 PASS disjoint-company events** whose exact historical data ARE archived (`holdout_quality_batch_0..8`), not fictitious ratios for all 164.

## Full 164 actual stock-price and recovery outcomes
| Cohort | Cases | D4 +3% TARGET first | D4 -5% STOP first | Timeout | D4 gross mean % | Hypothetical D4 net mean % | Full price recovery by 60 sessions |
|---|---:|---:|---:|---:|---:|---:|---:|
| All |164|99|58|7|-0.112|-0.312|86/164 (52.4%)|
| Original |92|62|28|2|+0.482|+0.282|48/92 (52.2%)|
| Different company |72|37|30|5|-0.872|-1.072|38/72 (52.8%)|
| Specifically AH |91|58|31|2|+0.009|-0.191|51/91 (56.0%)|
| BMO |73|41|27|5|-0.263|-0.463|35/73 (47.9%)|
| All observed SECOND new lows by D3 |101|64|32|5|+0.283|+0.083|49/101 (48.5%)|
| AH observed second low by D3 |54|38|16|0|+0.568|+0.368|29/54 (53.7%)|
- All 164 joint labels: 65 achieved BOTH D4 target and eventually full60 price recovery; **21 fully recovered within D60 WITHOUT a D4+3%-before-5% target**; **34 D4 target winners did NOT achieve full price recovery by D60**; 44 neither. Recovery and fast options-aligned stock profit are different objectives. (D4 non-winner includes stop or timeout.)
- Historical year D4 hypothetical net: 2023 -0.903%, 2024 -0.227%, 2025 +0.089%, 2026 -0.461%, showing no year-stable average D4 stock edge.

## Exact matched fundamentals: only the 72 with archived numeric prerelease data
Three predeclared factors, NO post-earnings leaked financial statements, NO forward consensus invention: latest published quarterly revenue YoY growth %, historical published debt/equity ratio, and positive TTM free cash flow / positive TTM net income (trailing cash-conversion measure).

Two mutually exclusive outcome comparisons were independently matched. Within the 72, exact calendar year and AH/BMO release session, closest initial earnings selloff absolute magnitude within **5 percentage points**, different ticker, no reusing controls. Greedy deterministic, unmatched retained in global denominators but excluded from PAIRED statistics.

### A. D4 TARGET FIRST vs STOP-or-timeout
- 37 eligible winning events, 35 nonwinning events, **25 matched pairs** (12 cases unmatched). Matched pairs had only **6 AH** and 19 BMO.
- Unmatched-inclusive feature MEDIANS winners vs nonwinners:
  - historical preearnings revenue growth: **5.49% vs 10.00%**;
  - debt/equity: **0.630 vs 0.483**;
  - TTM cash conversion: **0.886 vs 0.962**.
- Paired **winner−failure** differences: revenue-growth median **−3.355 percentage points** (case lower in 18/25 pairs, exact uncorrected sign p=0.0433); debt/equity median **+0.136** (case higher 13/25; p=1.0); cash conversion median **−0.159** (case lower 16/25; p=0.2295). NOT evidence that low-growth or more-debt is causally favorable; growth sectors/release mix and year confounding remain.
- At D3 observed early-lower-low stage only: 42/72, 23 D4 winners and 19 nonwinners; **12 matched pairs** (only **1 AH pair**). Revenue-growth lower in 11/12 pairs with median paired −5.626pp, uncorrected p=0.00635, but underpowered, multiply tested, overwhelmingly BMO and not directly transferable to AH strategy.

### B. FULL recovery to preearnings closing price within 60 sessions
- 38 events recovered, 34 did not; **27 matched pairs** (11 cases unmatched), **7 AH** +20 BMO.
- Unmatched-inclusive feature MEDIANS recovered vs unrecovered:
  - revenue growth **7.47% vs 7.69%**;
  - debt/equity **0.648 vs 0.502**;
  - cash conversion **0.871 vs 0.980**.
- Pair recovered−not recovered median differences: revenue YoY **−0.433pp** (case lower 15/27; uncorrected sign p=0.701); debt/equity **+0.136** (case higher 15 vs 11; one tie, p=0.557); cash conversion **−0.277** (case lower 21/27, exact uncorrected sign p=0.00592). CAUTION: this seemingly counterintuitive cash conversion result does NOT replicate a general 'weak FCF is good' idea. The ratio is business-model sensitive, 72 panel includes retail/airlines/payments etc, one GPN cash conversion ratio ~14.6 skewed means; paired case mean delta +0.385 despite median −0.277, illustrating substantial asymmetry.
- Multiple comparisons: 3 factors × 3 outcome specifications = 9 sign tests, so simple Bonferroni p_adj for D4 growth = **0.3896**; D60 cash conversion **0.0533**; early-dip growth **0.0571**. NONE pass 0.05 familywise, even before issuer clustering (matched pairs reuse company exposures) or history-exposed exploratory design. This adjustment is illustrative and not an exoneration of selection issues.
- Internal AH-only 26 numeric cases: D4 winner/failure n13/13, median historical revenue growth 7.80% vs 14.03% and cash conversion .881 vs .915, but AH paired matches only 6 (D4) and 7 (D60), and 1 among AH observed extra D1–D3 low. Cannot infer a AH trading signal.
- Per-event files contain all matched controls, features, dates, trade exit outcomes, h60 status, and missingness, not just winning cases.

## What these results mean
**The hypothesis 'historically better financial quality (higher past growth, lower leverage, better cash conversion) selects early recovery trades' is NOT SUPPORTED by our data.** Indeed some discovery differences have the opposite direction. This is not a claim low-growth, leveraged or weak-cash businesses are preferable: all 164 were already positively filtered quality (range restriction), and industry/sector composition, regime, news revisions, risk, multiple testing, real execution and small N are uncontrolled.
In the user-relevant AH cases, true matched sample is too small to claim any fundamental predictive edge. Both cohorts' long-run full recovery rates are about 52%, whereas D4 trade mean results diverge in sign: **a recovered stock is often not a profitable early CALL trade**.
Static before-earnings quality may be less useful than **what changed in forward earnings power at announcement**. Relevant literature: Shivakumar (2006), *Accruals, Cash Flows and PEAD* https://doi.org/10.1111/j.1468-5957.2006.01425.x, examines UNEXPECTED cash flows versus accruals, **not** the TTM quality ratio measured here; Fink PEAD 2021 review https://doi.org/10.1016/j.jbef.2020.100446; Chordia et al. 2009 liquidity/implementation https://business.columbia.edu/faculty/research/liquidity-and-post-earnings-announcement-drift. Our unchanged guidance proxy was previously tested with failures and true historical forward analyst EPS revision data is unavailable in current connected free feeds.

## Verdict and next *single* research priority
**VERDICT: RETROSPECTIVE NON-SUPPORT / HYPOTHESIS-GENERATING, not a validated edge and never a screen promotion.**
Don't try to optimize fundamental thresholds on the 72 known outcomes or re-label CASH conversion as investor surprise. Prioritize a POINT-IN-TIME earnings information CHANGE audit: what was **newly disclosed** in the earnings release versus expectations (forward EPS estimates if genuinely date-stamped, or explicitly comparable management outlook in original release; negative profit/margin or demand revisions), distinguish CONTINUING FUNDAMENTAL REPRICING vs temporary overshoot. Need event *failures* as controls, year/issuer/industry market conditions and at least ~30 newly independent AH lower-low opportunities, with trade target-first as the actual primary and option quotes as further gate. No spend on data or changes to scanner or scheduled alerts without explicit authorization.

## Reproduce
- Frozen design `frozen_164_match_fundamental_winners_losers_v1_2026-10-11.md`.
- Exact reader / D4 trade + matching script `run_matched_quality164_fundamentals_v1.mjs`.
- Full 164 outcomes + 72 financial observations + 25/27/12 matched pairs `matched_quality164_fundamentals_v1_all_events_pairs_2026-10-11.json`.
- Prior work `research/prior_work/earnings_164_matched_fundamental_winner_failure_prior_review_2026-10-11.md`.
- Source historic financial rows `holdout_quality_batch_0..8_2026-10-10.json` and original92/batch72 bars; all required raw historical data previously saved.
