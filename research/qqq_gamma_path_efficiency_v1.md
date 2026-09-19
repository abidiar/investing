# Investing OS Research — QQQ Gamma Path Efficiency v1.0

Status: **FROZEN BEFORE RESULTS**
Frozen: 2026-09-19

## Question
Does near-spot gamma concentration predict a cleaner, less-whipsaw regular-session price path on the following QQQ session, even when it does not materially reduce close-to-close movement?

This is a mechanism follow-up to the already-frozen gamma-concentration and overnight-vs-RTH decomposition work. It is not independent OOS proof.

## Information hierarchy
1. Price remains primary; price gets final vote.
2. Gamma structure is tested only as a path-quality / behavior overlay.
3. No feature may create bullish/bearish direction, STRENGTH, RUNWAY, R:R, or action-state authority.

## Source panel
Use `research/results/qqq_gamma_concentration_v1_session_panel.csv` exactly as previously generated. Gamma features are Day-T information and are matched only to Day T+1 RTH behavior.

Primary gamma features, unchanged:
- `near_gamma_share_0_5`
- `front_near_gamma_share`
- `weighted_abs_distance`

## Intraday data
QQQ regular-session bars only, America/New_York, 09:30–16:00.

Two resolutions are frozen:
- **Primary coverage:** 60-minute bars across the full available 2026 panel.
- **High-resolution robustness:** 5-minute bars over the most recent Yahoo-supported period available on run date. This secondary sample is reported separately and is not allowed to overwrite the primary result.

No premarket or after-hours bars.

## Frozen path metrics
For each T+1 RTH session:

### 1. Path efficiency
`PATH_EFFICIENCY = abs(session_close - session_open) / GROSS_PATH`

where `GROSS_PATH = abs(first_close - session_open) + sum(abs(close_i - close_{i-1}))` across RTH bars.

Range: 0–1. Higher = cleaner net travel per unit of bar-to-bar movement.

### 2. Whipsaw ratio
`WHIPSAW_RATIO = 1 - PATH_EFFICIENCY`.

Higher = more back-and-forth movement relative to net travel.

### 3. Bar-direction persistence
For sessions with non-zero RTH open-to-close direction, compute the fraction of non-flat bars whose close-open sign matches the session's final open-to-close sign.

Higher = more bars aligned with final session direction.

### 4. Reversal count
Count sign changes between consecutive non-flat bar close-open returns.

Higher = more intraday directional flipping.

### 5. Directional adverse excursion
For sessions with abs(RTH open-to-close) >= 0.25%:
- Up day: adverse excursion = max(0, session_open - session_low) / session_open.
- Down day: adverse excursion = max(0, session_high - session_open) / session_open.

`ADVERSE_TO_NET = adverse_excursion / abs(RTH open-to-close return)`.

Lower = cleaner path with less excursion against the eventual direction.

## Frozen hypotheses
### H1 — Near gamma improves path efficiency
Higher `near_gamma_share_0_5` and `front_near_gamma_share` should correlate **positively** with `PATH_EFFICIENCY`, and **negatively** with `WHIPSAW_RATIO` and `REVERSAL_COUNT`.

### H2 — Farther/diffuse gamma worsens path efficiency
Higher `weighted_abs_distance` should correlate **negatively** with `PATH_EFFICIENCY` and **positively** with whipsaw/reversals.

### H3 — Near gamma reduces adverse excursion on meaningful RTH moves
Conditional on abs(T+1 RTH open-to-close) >= 0.25%, higher near gamma should correlate **negatively** with `ADVERSE_TO_NET`.

### H4 — Gap-direction path efficiency, secondary
Conditional on abs(T+1 opening gap) >= 0.25%, define:
`GAP_ALIGNED_EFFICIENCY = PATH_EFFICIENCY` if RTH close finishes in the gap direction from the open, otherwise `-PATH_EFFICIENCY`.

Higher near gamma should correlate positively with this metric if the prior gap-follow-through result reflects a cleaner directional grind rather than simple range suppression.

H4 is secondary and cannot promote the module by itself.

## Primary statistics
Spearman rank correlations. Report full 60m sample plus chronological first/second halves. For 5m robustness, report the available recent sample separately.

Also report above/below-median near-gamma descriptive splits for efficiency, whipsaw, bar persistence, reversal count, and adverse-to-net. The median split is descriptive only and may not become a scanner threshold from this test.

## Incremental walk-forward test
Minimum training window: 60 primary sessions.

Targets:
- PATH_EFFICIENCY
- WHIPSAW_RATIO

Price-only baseline features from Day T:
- `day_abs_oc`
- `day_range`
- `rv5`

Extended model adds exactly:
- `near_gamma_share_0_5`
- `front_near_gamma_share`
- `weighted_abs_distance`

Use one-step-ahead expanding-window ordinary least squares, no hyperparameter tuning or feature selection. Compare MAE.

## Promotion standard
A compact scanner context tag may be considered only if all are true:
1. At least one primary near-gamma relationship has the expected sign in the full 60m sample and both chronological halves, with full-sample p < 0.10 on PATH_EFFICIENCY or WHIPSAW_RATIO; and
2. The same relationship has the same sign in the available 5m robustness sample; and
3. Above-median near gamma improves mean path efficiency or reduces mean whipsaw by at least 10% relative to below-median; and
4. The extended walk-forward model improves MAE by at least 2% on PATH_EFFICIENCY or WHIPSAW_RATIO without worsening the other by more than 1%.

If any gate fails, verdict = **RESEARCH-ONLY**.

Even if promoted later, maximum impact is a contextual field such as `RTH PATH STRUCTURE: CLEANER / WHIPSAW-RISK / NEUTRAL`. It may not create a trade or override price/event/expiration rules.

## Do Not Re-Test Unless
- materially larger or independent gamma sample becomes available;
- signed/intraday dealer positioning is available without lookahead;
- a different intraday resolution or path metric is defined and frozen in advance.

## Results
PENDING — rules above were frozen before calculation.
