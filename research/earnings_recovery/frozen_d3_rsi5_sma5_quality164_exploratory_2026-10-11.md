# FROZEN 2026-10-11: EARLY stock indicator audit on 164 quality post-earnings selloffs (exploratory only)
Premise: do short D3 momentum/exhaustion gauges ADD information about later share-price recovery and D4 tradable partial rebound? This is a different timing rule from failed post-D5..20 SMA5 repair confirmation. **No RSI14, VWAP, MACD, or volume could be correctly calculated from the saved 77 daily OHLC per-event windows (6 before D0), so do NOT label them tested**.

## Prespecified sample and outcomes
All exact 164 archived quality-screened earnings initial >=5% price drop events D0, 2023–mid2026, 92 original vs 72 different issuers; AH91 and BMO73, with D3=3 sessions AFTER qualifying D0. No filters to count as eligible besides existing base. Two preexisting known outcomes (not independent):
A. **D4 stock open** buy, +3% target before -5% stop over 20 full RTH bars and 0.20% illustrative roundtrip stock cost, precomputed `matched_quality164_fundamentals_v1_all_events_pairs_2026-10-11.json`, 99 TARGET vs 65 STOP/TIMEOUT. This is NOT historical options P&L.
B. First full preannouncement stock closing price recovery by any daily CLOSE within D60: 86 yes, 78 no; do not use outcome to filter input.
C. report AH subgroup, original92 vs separate72, observed second D1–D3 lower low subgroup (54 AH) without tuning.

## Exact numeric as-of D3 features, ONLY frozen 77-bar saved event OHLC
All source stock prices are close-only derived from `actionable_bounce_price_windows_92events_2026-10-10.json` and `actionable_bounce_price_windows_72events_2026-10-10.json`.
- **Cutler RSI5 at D3**, n=5 close-to-close arithmetic absolute price differences, using intervals D3−4→D3−3 through D3−1→D3, with exactly five daily changes. Definition 100*sum(max(delta,0))/sum(abs(delta)). If all five deltas 0, neutral 50 (but mark). Do not confuse with Wilder RSI14.
- RSI5 CHANGE from D1 to D3 = RSI5(D3) − RSI5(D1), requires six prior stock daily bars; event first D0 index>=6.
- SMA5 DISTANCE at D3 in PERCENT =100*(C_D3/mean(C_D3−4…C_D3)−1).
- SMA5 SLOPE from D2 to D3 in PERCENT =100*(MA5_D3/MA5_D2−1); no upcross signal requirement.
- No timing leakage: no D4/forward bars in any predictor, everything measurable after D3 close (different task from intraday earlier D4 entry).
- 5-day RSI may be distorted by earnings gap in five-day lookback; assess descriptively, no ad hoc RSI20/30 threshold or mean reversion edge.

## Analysis, no overfit
- Across all164, AH91, original92, separate72 and AH early second low n54, calculate feature medians, means and counts for outcome A winner vs failure and B full60 recovery vs none.
- EXACT same-year, AH/BMO and **sector ETF** and similar initial fall within <=5 percentage points, different ticker, no control reused case/control matchers pre-frozen in `quality164_asofD3_sector_market_factors_fullmatched_results_2026-10-11.json`: 43 D4 and 34 recovery matched (AH25 / AH20). Reuse identical pair IDs without reoptimization. Report median case−control factor difference and favorable sign count, simple exact two-sided sign p only descriptive, note multiple comparisons across 4 factors × 2 outcomes.
- No new 5d RSI/MA thresholds, optimization, machine learning, or all 4-feature 'A+' combo. If matched statistics not directionally consistent in AH, original and separate-issuer cohorts => **RESEARCH-ONLY NEGATIVE/INCONCLUSIVE**. Even apparently 'significant' after 8 comparisons not valid deployment unless fully independent new issuer-year test and options execution validated.
- VWAP and true intraday momentum + RELATIVE volume require event-time 1m or 5m OHLCV; daily archives have NO volume, historical intraday insufficient for ALL164, so not part of this test. No claim that MA/RSI reveals investor fundamental reasons or proof of buying pressure.
- Save original event feature and paired result JSON, reproducible Node script, readable verdict, update GitHub master + Google Doc. No scanner changes/trading automation/paid data.
