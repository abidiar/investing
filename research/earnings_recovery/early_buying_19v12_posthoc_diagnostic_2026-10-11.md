# Early buyer-pressure vs immediate earnings-shock rebound: retrospective 19-vs-12 diagnostic (Oct 11, 2026)

**Status: DESCRIPTIVE / POST-HOC / NO PRODUCTION RULE.** This is a retrospective audit of already outcome-exposed price bars, NOT a new frozen hypothesis test and not an options-price backtest. Never describe its selected features or cutoffs as validated.

## Existing pre-frozen experiments this audit reads, does NOT replace
- 2026 full 45 reaction-announcement cohort, 19 first >=5% RTH intraday shocks by 11:30: `first_failed_low_volume_buyer_takeover_45events_results_2026-10-10.json`, `first_failed_low_2026_all45_intraday_week*.json` and findings.
- Independent calendar-year 2025 cohort, 40 preselected announcements, 39 source-covered, nine early >=5% shocks: `early_buyer_initiative_no_retest_2025_40events_actual_2026-10-10.json`, `buyer_initiative_2025_week*_M5_webull_2026-10-10.json` and findings. BK used Massive in saved main experiment, but not among these nine early shock events.
- 2026 original frozen initial-low retest / shrinking seller volume / expanding bullish volume setup: **0 of 19 entries** (not a zero percent win rate).
- 2025 separately pre-frozen two-adjacent-green + breakout + volume + <=2% away from low WITHOUT retest: **0 of nine entries**, two potential price/volume confirmations were too far from low; not a zero percent win rate.

## Outcomes: immediate baseline underlying stock, same +1.5% profit before -1% stop, 3 entry-inclusive sessions
- 2026: 7/19 target-first and 12/19 stop-first; simple entry at the next 5m open following the first completed -5% shock candle. All seven stock profit targets reached the SAME reaction session: five in the **entry** five-minute bar (09:35) and the other two in the following bar (09:40). Thirteen of the 19 total trades (five winners, eight losers) resolved in their entry bar. Thus requiring even one completed *post-entry* candle cannot identify those five outcomes before they happen; two consecutive post-shock confirmations arrive too late to capture any of the seven +1.5% wins at original prices.
- 2025: 3/9 target-first, 6/9 stop-first with same underlying rules. Combined descriptive baseline across two cohorts: 10/28 target wins, 18/28 stops, gross return [(10*1.5)+(18*-1)]/28 = -0.1071% per underlying trade, hypothetical 20bp round trip = -0.3071% per trade. **Not actual options results.**

## Exploratory, as-of candle-only cross-group comparisons
A feature is computed at the CLOSE of the first completed 5m shock bar, before the immediate comparator NEXT 5-minute OPEN. The feature is based only on existing Webull as-traded RTH OHLCV; no future signal bar is used.

- `green = close>open`
- `close_location = (close - low)/(high-low)`; `lower_half = close_location<0.5`
- `relative_volume = first shock bar total traded volume / mean of up to 5 available earlier sessions' 5m traded volumes at the SAME clock time` (all 19+9 cases had five such controls). This is not signed/aggressive BUY volume. 09:30 bars vs 11:25 may have different market microstructure, but matching by clock helps.

| Diagnostic | 2026 TARGET 7 | 2026 STOP 12 | 2025 TARGET 3 | 2025 STOP 6 |
|---|---:|---:|---:|---:|
| First shock candle green | 2/7 | 6/12 | 1/3 | 3/6 |
| First shock candle closes BELOW halfway in bar range | 5/7 | 5/12 | 3/3 | 3/6 |
| Median close location in first shock bar | 0.301 | 0.551 | 0.242 | approx 0.468 |
| Median relative shock-candle volume vs prior five matched bars | 11.52x | 4.95x | 11.46x | 15.47x |

*2025 loser close-location median is the mean of the central two values approx (0.3904+0.5456)/2=0.468; 2025 winner 0.2419.*

**Implications**:
1. A strong **bullish green shock candle did NOT distinguish wins**; green happened in 3/10 eventual winners versus 9/18 eventual losers over the pooled 28, so blindly favoring a green first shock candle is not supported.
2. Relative shock-volume appeared larger for winners in 2026 but **REVERSED** in 2025; volume surge alone is not a robust separator across these two years.
3. A first completed shock candle closing in its LOWER half descriptively selected 10/19 2026 shocks (5 winners, 5 losers), and 6/9 2025 shocks (3 winners, 3 losers). Pooled selected 16/28, of which 8/16 were targets and 8/16 were stops, compared with immediate all-28 10/28 target wins. It missed two of ten known targets and avoided ten of eighteen stops. **This threshold was investigated only AFTER viewing both sets of outcomes**: training/discovery evidence, NOT a held-out win rate. Fisher exact two-sided p approximately 0.114 for pooled 8W/8L below-half vs 2W/10L above-half. Small samples, multiple inspected candidate features, nonrandom issuers, and no actual spread/ASK make this inconclusive. Gross underlying among 16 selected trades: (8*1.5-8*1)/16 = +0.25% per entry. After *hypothetical* 0.20% round trip: +0.05% per entry; across all 28 qualified shock opportunities zero-skips: +0.0286%. These are extremely small gross/net-sensitivity figures and are retrospective/optimistic because the feature was selected post hoc.
4. Five of seven 2026 winners hit target DURING first postshock entry bar; waiting to establish *sustained* postshock pressure cannot capture the specified early trade without target move already occurring. A later entry has a different denominator, stock payoff and options price; do not transplant original outcomes to later triggers.

## Research verdict
**Early, sustained buying pressure has NOT been shown to separate the seven target-first rebounds from twelve stop-first failures with an executable, early-as-of rule.** Two independent pre-frozen but different price/volume confirmations each produced zero candidate entries, so their win rate is undefined. Initial green candle and normalized total-volume intensity do not replicate as winning separators. The lower-half opening shock bar pattern is a *possible capitulation/repricing clue*, but requires genuine prospective/untouched out-of-sample freeze/replication and executable option ASK/BID/IV/DTE/cost before any trade recommendation. This audit must not be used to rescue or tune the frozen prior rule, change the A+ scanner, or claim actual bullish buyer initiated volume.

## High-value next research question
Rather than demanding two postshock buying bars when most targets already printed, use a fundamentally different, predeclared target: **can the entry-time 09:30 shock candle and observable prior-session baseline select an actual immediately executable 09:35 STOCK reaction, with enough option premium movement AFTER its actual ask?** Evaluate once on a larger unseen quarter after freezing a single rule, keeping all announcements in denominator and risk timing exact; do not refit threshold to these 28. Separately reconstruct actual cheap CALL entries, DTE, strike, option ask/bid, IV and exits to see if option scalp winners require the underlying +1.5% at all.

Primary sources:
- [2026 45-event report](first_failed_low_45event_selling_exhaustion_buyer_initiative_findings_2026-10-10.md)
- [2025 40-event report](first_buyer_initiative_without_retest_2025_40events_findings_2026-10-10.md)
