# Diagnostic completed: Price-only failed LOW after 2023 shock, original-Grimes-inspired but NOT full pivot strategy
Date 2026-10-11. Retrospective check after 2023 57-stock M5 outcomes had ALREADY BEEN EXPOSED in prior study; **not independent validation**. The prior M5 data source was archived already, so no new downloads/option quotes or trading required.

### Chain
- Frozen the new derived-test algorithm FIRST commit `fcab1cb3b4032ab54964af149120d3d8f38b1f45` in `frozen_grimes_priceonly_prior_session_low_2023_exploratory_2026_10_11.md`.
- All 57 original source signal events reused unaltered from `data/heldout2023_v4_preoutcome_candidate_manifest_2026_10_11.json`; 3 incomplete M5 known source exceptions retained as UNKNOWN and excluded, no favorable imputations. Therefore 54 complete three-session 78 bar sessions.
- Reference = as-of D0 previous completed RTH day's LOW, which is a **ONE-DAY low proxy rather than a published multi-day support/pivot**. D1 M5 candle between 9:30 and 11:50 ET sweeps below D0 low by >0.1%; closes back above in SAME candle or NEXT (Grimes original price-only quick reversal). Buy following 5min open by noon, enter not >2% above pivot; stop breached low-.10%, require stop distance 0.35–2%, target +2% of entry; stop/target pessimistic within M5 bar; first barrier through D1+D2 complete; 50bps stock roundtrip modeled. NO VWAP, volume/higher-low filter, 80% claim, news/sector gates, true aggressor flow or options.
- Saved every eligible skipped/entered row with source counts in `data/grimes_priceonly_2023_57m5_prior_day_low_failure_exploratory_2026_10_11.json` commit `d5c917daa38b60a18522863f6d600aed0ea517e4`.

### Actual results
| Measure | Count / result |
|--|--:|
| Frozen daily selloff events |57|
| Full 3×78 M5 evaluable |54|
| Entered price-only failure test |**20**|
| No failed D0 low within 12pm entry |30|
| Price extended too far or structural stop invalid |4|
| Price-only TARGET before STOP (+2% fixed) |**6 / 20 =30%**|
| Structural stops |13/20|
| D2 close timeout |1/20|
| Average net per ENTERED stock @50bps |**-0.6053%**|
| Average net per eligible DAILY source event, SKIPs zero @50bps |**-0.2242%**|
| Same cohort buy-next-open (old +2/-2 stop) benchmark @50bps |**-1.1168%**|
| Paired per-event model improvement over opening-buy (NOT same stop/risk!) |**+0.8927 percentage points**|

Unlike high-frequency next-open buy-all, the price-only event entry reduced losses and avoided 34 of 54 events; however, it **did NOT produce profits or 80% hit rate**. Paired +0.893pp performance improvement is mechanically partly a result of SKIP counting zero and DIFFERENT structural vs fixed stop; do not attribute causally to confirmation. Research diagnostic, outcomes all previously known. Strict ticker and date bootstraps:
- ticker 95% net eligible [-0.46846512851705174,0.01581623483762173]%; date95% [-0.5076983601352074,0.043671081281501004]%.
- ticker95% paired advantage [0.4095754087775885,1.4019497056154773] pp; date95% [0.38626661839166704,1.4172815415626898] pp.
- per entered ticker clustered CI [-1.2297743854649705,0.037579826170772906]%.
- Four historical quarters each had 2/6,2/7,1/5,1/2 TARGET FIRST (respectively), and all 4 mean per-fill NET negative @50bps.
- Earlier M5 `v4` combined failed-low/higher-low/signed candle volume proxy gave 11 fills, 4 winners (36.36%), mean net per eligible event -0.1896%, per fill -0.9308%; not directly matched because stop, target and trigger rules are different.
- Across 57, 3 missing M5: HUBS Feb3 D2 74, CMG Jul27 D2 73, AEO Nov21 holiday D2 42; missing > not assumed losers/winners.

### What remains unsolved
This is not Adam Grimes's full proposed public setup with meaningful multi-session previously observed pivotal support/range; D0 low proxy can be a random downside bar within a strong downtrend. Genuine test should first freeze 20+ days PRE-signal support from public prior daily and M5 bars, wait for swift failed break then assess same/next bar reclaim, make entry with stop at failure extreme, and compare to contemporaneous valid ordinary support touches. Include historical option NBBO only if available for user premium around $50, otherwise stock research only. True independent OOS issuer/time and >=20 filled trades required to talk about an edge.
