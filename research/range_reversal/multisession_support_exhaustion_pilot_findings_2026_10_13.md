# Cross-session established-support retests — frozen pilot outcomes (2026-10-13)

## Bottom line
**INCONCLUSIVE for the seller-exhaustion volume hypothesis, and negative for the broad near-support re-test baseline in this tiny pilot. Do not promote scanner or trade calls.** Frozen protocol was committed as d3aeb67564d2a67a8655010c518b36e83e045f16 **before** fetching bulk Webull M5 data or outcome scoring. Results and per-event source archive committed as b62dc1ce5cfc02c5fc997d32aaff8df5084a3189.

## Data
Webull RTH raw/as-traded M5, 20 prespecified US stocks, 6 backward 1200-bar slices per stock, exactly 144,000 timestamp-unique five-minute bars, 92 complete RTH sessions (>=75 five-minute bars) per ticker between 2026-06-03 and 2026-10-13; 35 complete sessions of point-in-time support warmup. No paid data. No Webull API failure. No adjusted DAILY bars mixed into the support calculation. A separate dividend/price continuity audit was NOT carried out; detected no price gap >25% under preset guard in the six passing cases. Intraday bars only; no actual options chains or spreads.

## Method
Pre-established morning support from 20 sessions D-35..D-16, >=2 separated proximity touches; last two distinct-session support re-tests in prior15 sessions, next-bar opening entry after M5 close that reclaimed support by noon. Re-test touch allowed within +1% support, without mandatory strict UNDERCUT; label this a **near-support re-test** rather than a guaranteed breakdown. De-dup within five sessions. Target first +2% before stop −1%, ambiguous M5 bars stop first, gap executed at opening, through end of next full session. Net means subtract hypothetical 0.50% roundtrip stock execution cost. **IMPORTANT** no results show options profit, and selected 20 issuers/time overlap past research: not independent confirmation.

## All events
| Name | Previous test | Second test | Entry ET | Higher second low >=0.20% of support? | Outcome +2/-1/timeout | Net stock model |
|---|---|---|---|---|---|---:|
| AMZN | Oct01 | Oct02 | 09:35 | YES | STOP | -1.500% |
| COST | Aug20 | Sep03 | 09:35 | NO | TIMEOUT | -1.073% |
| GOOGL | Sep11 | Sep23 | 10:20 | YES | STOP (gap adverse) | -1.610% |
| JPM | Sep17 | Sep21 | 09:35 | YES | STOP | -1.500% |
| NVDA | Jul29 | Jul30 | 09:40 | NO | TARGET | +1.500% |
| ORCL | Sep24 | Sep25 | 09:35 | YES | STOP | -1.500% |

Baseline SIX events / six distinct stocks: 1 TARGET, 4 STOP, 1 TIMEOUT. Target-first **16.7%** (95% Wilson CI ~3.0%–56.4%). Average NET **−0.9472%** per entered stock trade with 0.5% costs. Four higher-second-low events, zero target, all 4 stops, mean net −1.5275%. A 4-event filter result proves nothing reliably. No target-first sample with a valid decreased-pressure pair.

## Why volume-gate comparison is UNTESTED
Across all SIX baseline events, **each has at least one pressure measurement NULL** due to frozen requirement >=4 available bars and >=2 red-body bars in last six ending at probe low, plus 20 comparable time-of-day observations. Five of six prior support tests reclaimed in the opening 09:30–09:35 time span; only NVDA prior first test reclaimed at 10:10. Four of six current reclaims occurred 09:30, one 09:35, GOOGL 10:15. Exactly zero pass declining-pressure alone; zero pass BOTH, reflecting unavailable proxy measurement, **not evidence no exhaustion occurs**. First test event timestamps: AMZN09:30/COST09:30/GOOGL09:30/JPM09:30/NVDA10:10/ORCL09:35. All entries <10:30; zero 10:30-noon cases. Do not call this a successful test of the user's preferred timing.

## Research judgment / next clean design
This pilot was **too restrictive / misaligned**: support tests often happen at opening; requiring >=4 completed bars to quantify selloff excludes nearly all otherwise-valid support tests, while allowing a test to merely get within 1% support can confuse a failed undercut with routine drift. Do NOT loosen these thresholds and rescore the same six as an out-of-sample result. Next hypothesis should preregister a separate **company-disjoint or earlier-period** panel and a fully defined opening-aware proxy using the probe candle's LOW-to-CLOSE rejection, absolute penetration relative to support/ATR, and probe-bar volume divided by median previous-20 comparable 5-minute-slot volumes (can work even in the 09:30 bar), with actual below-support probes distinguished from just near-level visits. Again evaluate fixed +2%/-1% underlying bar-by-bar and 10:30-noon coverage as a separate predeclared subgroup. Require dozens of independent cases before scanner or $50 call promotion; separately measure option IV, spreads and slippage.

Primary protocol: [Frozen pilot](frozen_multisession_seller_exhaustion_pilot_2026_10_13.md). Machine audit: [Row-level results](data/multisession_support_exhaustion_pilot_results_2026_10_13.json).
