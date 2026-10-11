# 2022 established double-pivot support failure: frozen calendar-separated test

**Run completed:** 2026-10-11. **Verdict: no demonstrated positive net stock trading edge and no evidence of an 80% target-first setup.** The 2022 cohort was identified after freezing a new algorithmic *established support* definition, not chosen from the 2022 intraday outcomes.

## Audit and sequencing

1. Prior 2023 diagnostic preserved: `grimes_priceonly_prior_session_low_2023_exploratory_analysis_2026_10_11.md` (20 filled; 6 targets first, -0.605% net / entry; hindsight-exposed exploratory cohort).
2. New freeze: `frozen_grimes_2022_established_pivot_support_v1_2026_10_11.md` commit `da412ee1494350d403e4d858a5133dedae022a3d`; exact 90-symbol universe commit `a3c3460088ababcd4c093cf43709cc228c9ce252`.
3. Daily 2021-06 through 2022-10 source stored in five `data/grimes_2022_daily_history_preoutcome_batch_0*.json` files; **no next-day M5 outcomes used for candidate construction**.
4. All **45** event identities and support pivots frozen in `data/grimes_2022_established_pivot_preoutcome_manifest_frozen_2026_10_11.json`, commit **`e80ab395610c3fb7fa76cdc8d04a713f82424af6`**, BEFORE accessing D1/D2 M5 bars. 37 issuers, 34 dates, severe-selloff (<= -7%) subgroup n=6. This makes this a clean calendar-separated 2022 historical test for the **newly stated rule**, although not free of the 2023-derived issuer-universe survivorship bias.
5. Three source batches `data/grimes_2022_double_pivot_m5_three_session_source_batch_0{1,2,3}_2026_10_11.json` were then fetched and stored. Subsequent source and outcomes remain auditable. No thresholds were optimized after forward outcomes.

## Primary outcome after 50bp modeled stock roundtrip cost

| Frozen rule | Evaluated | Filled | Skipped | +2% target first | Structural/fixed stop first | Timeouts | Target / filled | Avg net / filled | Avg net / evaluated event |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| 2 historical low pivots + intraday failure, structural stop | 40 | 13 | 27 | 6 | 7 | 0 | 46.154% | -0.102% | -0.033% |
| Descriptive fixed -2% stop on same signal | 40 | 13 | 27 | 7 | 4 | 2 | 53.846% | -0.127% | -0.041% |
| Descriptive near-support touch without earlier intraday break | 40 | 2 | 38 | 0 | 2 | 0 | 0.000% | -1.608% | -0.080% |
| Next-day-open buy +2%/-2% benchmark | 40 | 40 | 0 | 19 | 19 | 2 | 47.500% | -0.486% | -0.486% |

The primary strategy entered 13 trades out of 40 evaluable events: **6 targets first, 7 stops first**. Its net expectancy was **-0.102% per trade** and **-0.033% per candidate** counting 27 skips as 0. It did not meet the profit or 80% target-first objective. Primary skip counts: `SKIP_EXTENDED`=1, `SKIP_NO_PATTERN`=26.

It reduced adverse exposure compared with the unconditional next-day open buy, an average paired gain of **0.453 percentage points per evaluable signal**. However the primary average remains marginally negative and clustered bootstrap intervals for improvement span zero. Not evidence that primary beats alternative controls in a larger, truly independent sample.

## Sample quality and statistical uncertainty

- Full history received for **40 of 45** frozen ticker/date events; **5 are UNKNOWN** due to missing D0/D1/D2 five-minute bars. Exclude UNKNOWN from the evaluable denominator, not 0, not failures, not winners. They are URI 2022-01-05, DPZ 2022-01-07, ALGM 2022-04-06, ROK 2022-04-26, CMG 2022-06-13.
- The available 40 cases pass the 78-per-session M5 continuity and adjusted daily-to-intraday OHLC factor QA; no OHLC basis mismatches >3%.
- 10,000 deterministic ticker-cluster bootstrap samples across 33 issuers: 95% mean net **per trade** interval [-0.963%, 0.747%]; 95% net **per candidate** interval [-0.305%, 0.234%]. Paired excess per candidate relative to next-open [-0.153, 1.027] percentage points. The D0 signal-date clustered result is also in the event-results JSON.
- Outcomes vary sharply across quarters, exploratory **not actionable filters**: Q1 3/3 targets, Q2 1/6, Q3 1/3, Q4 1/1. No post hoc quarter selection. This single 2022 bear-market period does not demonstrate cross-regime robustness.
- Entries **10:30–noon ET** (descriptive only; frozen protocol allowed 09:35-noon): **5 filled, 2 targets first / 3 stops first, -0.120% mean net per fill**. The 5 were LHX 2022-01-31 (+1.500%), FAST 2022-05-05 (-1.376%), PH 2022-05-05 (-1.253%), SYF 2022-09-13 (+1.680%), and DRI 2022-09-22 (-1.152%). The sample is too small to conclude the user-preferred window does or does not have an edge.
- No verified historical option chain/quotes, DTE, NBBO spread, implied vol, slippage, expiration, or sub-$50 contract cost. A stock-bar proxy does not show options viability.
- The 90 issuer list derives from a later 2023 sample; it is **not survivorship-free** or broad-market representative. Historical adjusted prices and data availability may create further selection differences. Original Grimes pivot selection was discretionary; these are precisely defined *algorithmic* historical swing support approximations, not Adam Grimes's original full trade criteria.
- The 2022 period was chosen and frozen *after* other reversal studies; don't claim clean pre-registration of the general idea. This is stronger temporal separation than retrospectively changing the 2023 sample, not forward-live validation.

## Decision

**Reject promoting the exact double-pivot + price-only failure rule as a profitable scanner entry.** It improved selective loss avoidance versus buying every candidate but did not generate positive expected modeled net returns and did not attain a high target-first rate. Preserve the previously implemented scanner's *observational* failure-test flag without upgrading it to an automatic A+ entry or an 80% strategy.

Next meaningful unresolved hypothesis: a failed breakdown may depend on **market-wide conditions** (e.g., broad-market pressure and reversal) rather than isolated support geometry. To test, freeze a completely new *calendar* and as-of market/breadth context BEFORE revealing future returns, and require a genuinely broader contemporaneous/security universe if free historical access permits. Do not choose Q1 winners, sector, early/late entry window, pivot-count, or stop distance based on this exposed result. Alternatively prospectively record upcoming setups under frozen rules and score them with real execution quotes, including affordable options.

**Machine-readable source and event-level results:** `data/grimes_2022_established_pivot_v1_event_results_2026_10_11.json`.
