# SPY Quarterly Expiration — Auction-Footprint Proxy Test v1

Frozen: 2026-09-21
Status: **FROZEN BEFORE OUTCOME EXPOSURE**

## Purpose
Test whether observable SPY M5 price/volume behavior is mechanically consistent with the independently documented 2024 change in U.S. closing-auction price discovery, without claiming that SPY OHLCV measures the actual auction imbalance.

## External prior
NYSE independently reports that effective 2024-08-12 Closing D-Orders were incorporated into NYSE Closing Auction imbalance information beginning at 3:50 PM ET rather than 3:55 PM. NYSE reports faster paired-notional accumulation, more gradual imbalance offsetting after 3:50, and reduced variability previously concentrated at 3:55. This is an NYSE-listed-constituent mechanism; SPY itself is NYSE Arca-listed, so SPY M5 data are treated only as a market-level footprint proxy.

## Frozen breakpoint
- PRE: observations through 2024-08-09.
- POST: observations beginning 2024-08-12.
- Quarterly-expiration comparison therefore has 2024-06-21 as the last PRE event and 2024-09-20 as the first POST event.
- Do not move the breakpoint based on SPY outcomes.

## Frozen primary footprint metrics
Computed from SPY RTH M5 bars:
1. `r_1530_1550`: return from 15:30 bar open to 15:50 bar open.
2. `r_1550_1555`: return from 15:50 bar open to 15:55 bar open.
3. `r_1555_close`: return from 15:55 bar open to 15:55 bar close (4:00 close proxy).
4. `late_share_after_1550`: absolute 15:50→close displacement / absolute 15:30→close displacement; report undefined when denominator is effectively zero.
5. `final5_share`: absolute 15:55→close displacement / absolute 15:30→close displacement.
6. `continuation_1550`: sign(15:30→15:50) equals sign(15:50→close), excluding exact-zero legs.
7. `continuation_1555`: sign(15:30→15:55) equals sign(15:55→close), excluding exact-zero legs.
8. `late_path_efficiency`: absolute 15:30→close displacement divided by sum of absolute M5 close-to-close changes from 15:30 through close. Higher means smoother/more directional.
9. `final_bar_volume_share`: 15:55 M5 volume / total RTH volume.
10. `final_bar_volume_vs_prior_30m`: 15:55 M5 volume / mean M5 volume from 15:25 through 15:50.

## Samples
### A. Quarterly-expiration sample
Use the already-frozen quarterly-expiration event list. Primary footprint comparison uses all events with complete M5 bars around the close.

### B. Ordinary-Friday control
For each quarterly expiration, use the immediately preceding ordinary Friday that is a full RTH session and is not itself a major scheduled quarterly index-reconstitution/rebalance date when identifiable from the calendar. Selection is calendar-based only; do not inspect returns when choosing controls.

If a selected Friday is a market holiday or shortened session, step back one Friday. Record substitutions.

## Primary questions
1. Did the POST period show less incremental SPY displacement/variability in the final 5 minutes relative to the 15:50→close window, consistent with earlier price discovery?
2. Did late-path efficiency increase POST?
3. Did final-bar volume concentration materially change POST?
4. Are any changes stronger on quarterly-expiration sessions than on ordinary-Friday controls?

## Analysis
- Report medians and means PRE vs POST.
- Report effect sizes and bootstrap confidence intervals where sample size permits.
- Do not optimize thresholds.
- Do not use next-open outcomes in the primary footprint comparison.
- The known recent 9/9 next-open streak remains quarantined from metric definition.

## Interpretation rules
- If predicted footprint changes are absent in SPY, downgrade the auction-mechanics explanation for the 9/9 streak.
- If predicted footprint changes appear in both expiration and ordinary-Friday controls similarly, classify as a general closing-regime footprint, not a triple-witching-specific mechanism.
- If predicted changes are materially stronger on expiration sessions, classify as **consistent with** an expiration-sensitive auction mechanism, not causal proof.
- SPY M5 OHLCV can never be described as direct auction-imbalance or paired-quantity evidence.

## Production rule
No scanner or live-probability change may result directly from this proxy test.