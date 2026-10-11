# Investing OS Research — Master Status

Updated: 2026-09-21
Status: **CANONICAL CROSS-TOPIC INDEX**

This file is the concise cross-chat research state. Detailed prior-work reviews, frozen protocols, code, and results remain in their topic files. Governance is defined in `research/RESEARCH_GOVERNANCE.md`.

## Current production posture
- **Price gets final vote.**
- No research-only options-positioning feature may independently create direction, add STRENGTH/RUNWAY, manufacture R:R, or authorize BUY/SELL/CALL/PUT/HOLD/overnight carry.
- Quarterly expiration/rebalance risk is a standing scanner gate and must be surfaced prominently.
- A finding enters production only after its preregistered promotion standard passes.
- **Every new hypothesis requires a prior-work review before protocol freezing.** See `research/PRIOR_WORK_REVIEW_STANDARD.md`.

## SPY quarterly-expiration late-close → next-open research
Files:
- `research/spy_quarterly_expiration_frozen_event_panel_v1.md`
- `research/results/spy_quarterly_expiration_late_close_next_open_discovery_2026-09-21.md`
- `research/results/spy_quarterly_expiration_backward_falsification_v1_results.md`

Status: **PRIMARY HYPOTHESIS FAILED LONG-HISTORY STABILITY / RECENT-REGIME CLUSTER ONLY**.

The event panel was frozen before backward outcomes were exposed: 79 quarterly-expiration sessions from 2007-03 through 2026-09, with holiday-adjusted expirations preserved. Existing Webull M5 history supplied 64 valid frozen events from 2010-12-17 through 2026-09-18; the first 15 frozen events remained missing. Massive was checked for the missing old intraday history but the current plan was not entitled, and Alpaca returned no old records.

Frozen primary result:
- 33 / 64 directional matches = **51.56%**
- 95% Wilson CI: **39.58%–63.37%**
- exact two-sided binomial p vs 50%: **0.901**
- return-level Pearson correlation: approximately **-0.009**
- Spearman correlation: approximately **+0.044**

Therefore the 3:30 PM ET → expiration-close direction does **not** provide a durable long-history directional edge for the next-session opening gap.

Era behavior was unstable: 2010-2014 = 41.18%, 2015-2019 = 50.00%, 2020-2023 = 43.75%, 2024-2026 = 81.82%. The recent observation remains notable: **2024-09-20 through 2026-09-18 is 9/9**, including 2026-09-18 (+0.108% late move) → 2026-09-21 (+0.617% opening gap). But the pre-streak sample was only 24/55 = 43.64%.

Magnitude filters did not rescue the rule. This recent 9/9 run is preserved as a **descriptive recent-regime cluster**, not a live probability, scanner score, or production rule.

**Research verdict: do not promote the directional rule.** The existing quarterly-expiration/rebalance distortion gate remains unchanged because late-day expiration flows can still be mechanically distorted; that is a risk-management conclusion, not a directional forecast.

## Options-positioning / gamma research status

### Pass 1 — Dealer/GEX regime
Verdict: **PROVISIONAL / RESEARCH-ONLY**.
Signed/modelled dealer-gamma regime may be useful for amplification/damping conditional on independent price confirmation. Raw GEX direction, exact wall/flip precision, and wall proximity alone are not promoted.

### Pass 2 — QQQ settled OI persistence
Verdict: **NOT SUPPORTED**.
Delta-OI/volume persistence did not predict larger next-session movement or improve continuation. Call-vs-put buildup imbalance had essentially zero directional value.

### Pass 3 — QQQ gamma concentration / pinning
Verdict: **RESEARCH-ONLY**.
Near-spot unsigned gamma associated with smaller next-session RTH range. Dominant-strike pinning failed and walk-forward improvement was insufficient.

### Pass 4 — Overnight vs RTH decomposition
Verdict: **RESEARCH-ONLY**.
Near-spot gamma related more clearly to RTH range compression than overnight-gap magnitude, but predictive improvement remained insufficient.

### Pass 5 — QQQ path efficiency
Verdict: **BROAD HYPOTHESIS FAILED STABILITY**.
Generic high-gamma cleaner-path behavior was unstable across time and bar resolution.

### Pass 6 — QQQ gap-conditioned continuation
Verdict: **RESEARCH-ONLY DISCOVERY**.
A strong 2026 QQQ gap-follow-through association appeared, but it was not promoted because walk-forward incremental utility failed.

### Pass 7 — SPY 2025 independent replication
Verdict: **FAILED REPLICATION**.
The QQQ directional gap-continuation relationship did not generalize to SPY.

### Pass 8 — QQQ 2025 time-shift replication
Verdict: **FAILED REPLICATION**.
The QQQ 2026 directional gap-gamma result did not replicate in QQQ 2025. Treat the original directional effect as regime/source-specific, not durable.

### Pass 9 — Multi-year unsigned near-spot gamma compression
Verdict: **REPLICATED ASSOCIATION / RESEARCH-ONLY**.
Across 2,221 SPY/QQQ/IWM observations in 2023–2025, higher near-spot unsigned gamma associated with smaller next-session RTH range and excursion. The raw association was broad and stable, but price-volatility variables captured most practical forecasting value.

### Pass 10 — Untouched 2020–2022 incremental-value holdout
Verdict: **CONDITIONAL ASSOCIATION / RESEARCH-ONLY**.
Across 2,262 untouched observations, the compression relationship survived seven price-volatility controls, instrument/year checks, and non-OPEX robustness. Gamma improved walk-forward MAE only 1.26% for next RTH range and 1.33% for max excursion, below the frozen 2% promotion gate. Conclusion: gamma contains a small real additive amplitude signal, but not enough for production authority.

### Pass 11 — Decision-level chase/veto falsification
Files:
- `research/gamma_chase_decision_v1.md`
- `research/results/gamma_chase_decision_v1_results.md`

Verdict: **FAILED DECISION-LEVEL OVERLAY**.
Untouched holdout: 1,195 SPY/QQQ/IWM candidates in 2017–2019, trained on 2014–2016. A gamma compression veto improved T1 precision from 69.39% to 73.97% (+4.58 pp), but retained only 79.41% of baseline winners versus the frozen >=85% requirement, while Brier improvement was only 0.38% versus the frozen >=2% requirement. **Unsigned gamma must not be used as a hard entry/chase veto.**

### Pass 12 — Target-calibration decision falsification
Files:
- `research/gamma_target_calibration_v1.md`
- `research/results/gamma_target_calibration_v1_results.md`

Verdict: **FAILED DECISION-LEVEL TARGET OVERLAY**.
Untouched holdout: 799 SPY/QQQ/IWM candidates in 2012–2013 with a 2011 seed. Price-only and price+gamma both produced 0.21% mean captured target distance, 40.55% hit rate, and identical targets on all 799 candidates. Adding gamma worsened average Brier performance across T1/T2/T3 by 0.82%. **Unsigned gamma must not be used as a production target-sizing rule.**

### Pass 13 — Modelled dealer-GEX gap follow-through
Prior work / audit:
- `research/prior_work/dealer_gex_amplification_damping_prior_work_2026-09-19.md`
- `research/prior_work/dealer_gex_data_method_audit_2026-09-19.md`

Files:
- `research/modelled_dealer_gex_gap_followthrough_v1.md`
- `research/results/modelled_dealer_gex_gap_followthrough_v1_results.md`

Verdict: **MECHANISM-CONSISTENT / INCREMENTAL UTILITY NOT SUPPORTED**.

This was the first signed-GEX branch test after the mandatory prior-work and data-method audit. Because direct dealer/customer participant data were unavailable in the current tool stack, the experiment used the published **MODELLED DEALER-GEX PROXY** convention: call gamma positive, put gamma negative, normalized by trailing-20 underlying dollar volume. It is explicitly **not observed dealer inventory**.

Untouched holdout: **741 SPY/IWM opening-gap candidates in 2009–2010**, with 2008 as the seed year. The descriptive mechanism matched prior literature:
- signed GEX/ADV vs gap-direction open-to-close follow-through: **rho=-0.0759, p=0.0389**;
- signed GEX/ADV vs excursion efficiency: **rho=-0.0758, p=0.0391**;
- both expected signs held in **4/4** prespecified instrument/year subgroups;
- negative-proxy sessions continued in the gap direction **51.37%** vs **44.33%** for positive-proxy sessions and had larger RTH ranges (**2.31% vs 1.76%**).

But incremental prediction was far below the frozen materiality gates:
- continuation Brier improvement: **0.61%** vs required 2%;
- follow-through MAE improvement: **0.15%** vs required 2%;
- excursion-efficiency MAE slightly worsened by **0.11%**.

Conclusion: the public OI-based sign proxy is **mechanism-consistent but not decision-useful enough for Investing OS**. It must not receive production authority and should not be tuned on the same data.

## What is rejected / not production-eligible
- Raw OI as bullish/bearish direction.
- Call-vs-put OI buildup as direction.
- Delta-OI/volume persistence as a next-day movement/continuation edge.
- Large gamma wall as an automatic magnet.
- Exact gamma-wall/flip levels as penny-precise trade levels.
- High unsigned gamma as a directional signal.
- High unsigned gamma as a hard chase/entry veto.
- High unsigned gamma as a production target-sizing rule.
- The QQQ 2026 gap-gamma continuation effect as a general market rule.
- The call-positive / put-negative **modelled dealer-GEX proxy** as a production continuation/reversal overlay.

## What remains alive
- **Direct or stronger dealer-side positioning data** — participant-class inventory/open-close data, signed flow, or a validated inventory proxy — as a potentially distinct amplification/damping mechanism.
- Unsigned near-spot gamma as a small non-directional next-session amplitude/compression association, **research/context-only** after failing two practical decision-level overlays.
- SPY quarterly-expiration recent 9/9 sign-match streak as a **descriptive recent-regime cluster only** after the long-history primary rule failed.

## Prior-work and data-source conclusion — signed dealer-GEX branch
The broad mechanism is already well studied: negative/short dealer gamma can amplify price moves and positive/long dealer gamma can dampen them, especially relative to available liquidity. The remaining Investing OS question is **incremental decision value**, not whether the mechanism can exist.

The data-method audit found that the strongest sources are commercial/proprietary:
- Cboe participant-class open/close or trade-by-trade execution data;
- OptionMetrics Signed Volume / TradeFlow;
- comparable direct dealer/customer position data.

Our open ETF archive is sufficient only for an OI-sign proxy. Pass 13 shows that this easy/public proxy is too weak to justify scanner use even though its descriptive signs match the literature.

## Do Not Re-Test Unless
- Do not resurrect the failed QQQ gap-continuation rule by changing gap threshold, DTE, moneyness, near-gamma band, IV filter, or OPEX exclusions.
- Do not tune the 2020–2025 unsigned-gamma thresholds to force the 2% forecast gate.
- Do not soften the failed Pass-11 veto using the same 2017–2019 outcomes and call it validation.
- Do not lower the Pass-12 0.60 target threshold, change the target ladder, or tune on the same 2012–2013 outcomes to create target changes.
- Do not treat public open interest as observed dealer inventory.
- Do not tune the Pass-13 call-minus-put proxy, gap threshold, liquidity normalization, or 2009–2010 sample to force the 2% incremental gates.
- Do not make exact gamma-wall pinning the next research priority without materially stronger evidence/data.
- Do not change the SPY quarterly-expiration primary 3:30→close / next-open definition after exposing backward-test outcomes; alternate start times and near-zero filters remain robustness checks only.

## Next clean research priority
**Do not optimize the failed SPY quarterly-expiration primary rule.**

If the expiration branch is continued, the next defensible question is whether the recent 2024-09→2026-09 9/9 cluster corresponds to a **pre-specified observable regime difference known before the next open** (for example closing-auction imbalance type, expiration/rebalance coincidence, volatility regime, breadth, or dealer-hedging environment). Any such branch requires the mandatory prior-work review and a frozen regime definition before outcomes are exposed.

OI-based GEX proxy work remains paused unless stronger dealer-side data become available.

If we later obtain participant-class or signed-flow data, the next clean GEX experiment should use a modern multi-year SPX/SPXW sample with intraday underlying bars and ask:

> Given an independently confirmed price impulse, does **observed or substantially stronger dealer positioning** improve 30/60/120-minute continuation/reversal, MFE/MAE, and realized excursion beyond price, volatility, and liquidity?

Until then, do not further tune public OI-based GEX.

## Key locations
- Governance: `research/RESEARCH_GOVERNANCE.md`
- Prior-work standard: `research/PRIOR_WORK_REVIEW_STANDARD.md`
- Start-here bootstrap: `INVESTING_OS_RESEARCH_START_HERE.md`
- Detailed options status: `research/options_positioning_research_status.md`
- Prior-work reviews: `research/prior_work/`
- Frozen protocols/code/results: `research/` and `research/results/`
- Google Doc human-readable ledger: **Investing OS Research Ledger — Canonical**, document ID `1MxHv5HPlr1Ab9A8cb3diPUtBJv6fWgNZwhhrw72zAus`
- Live Investing OS Sheet: spreadsheet ID `14lTnD-on91I4F5E5FAQ8-39zTRv2GzBjyd1b4_uCzjc`

## Savino SPX destination/invalidation reference — 2026-10-09
Verdict: **RESEARCH-ONLY / NO DEMONSTRATED DECISION EDGE**; optional non-directional display is permitted, but NO live production promotion or automatic scanner logic change.

Records:
- `research/savino_preliminary_pattern_audit_2026-10-09.md`
- `research/savino_destination_invalidation_test_v0_1_frozen_2026-10-09.md`
- `research/savino_destination_invalidation_results_v0_1_2026-10-09.md`
- `research/savino/savino_structural_reference_overlay_v0_1_2026-10-09.md`

Six screenshot-selected retrospective dates; first independent OR+VWAP M5 entry each day (Webull SPY proxy). Nearest Savino translated next level won the target-before-structural-stop race 3/6, but each target-first outcome offered under 0.5R at entry. One of six setups offered >=2R to the nearest level, and it stopped first. Plain offset fixed-distance level grids had 2–4/6 target-first outcomes; no demonstrated Savino edge. No exact SPX intraday entitlement; provider/basis and selection risks remain.

**Use:** timestamp/source-verified SPX major-level map as a separate optional reference showing potential next destination, intervening friction and possible failure/reclaim zone AFTER direction, independent trigger, stop, destination and viable R:R have been established. No Savino-derived entries, no Strength/Runway credit, no auto-veto/auto-target/auto-stop, and no A+ reclassification. When unposted/unverified, omit map rather than backfill. Do not modify frozen A+ v1.0 or 11:00 late-state-change experiment.

Do Not Re-Test Unless: exact SPX M5 and materially more complete timestamped premarket archive available, a documented prior-work review is completed, and a new distance-matched v0.2 test is frozen before its untouched outcomes. Separate invalidation-stop test must account for stop widths, false exits and net options execution quality.

Google Doc ledger must match this posture; operational prompts may print optional research context but live service/scanner logic remains unchanged.

## Savino inverse timing + SPX level combined proof of concept — 2026-10-09
Verdict: **MEASUREMENT PIPELINE FEASIBLE / INCREMENTAL EDGE NOT DEMONSTRATED / RESEARCH-ONLY**.
- Prior work: `research/prior_work/savino_inverse_timing_combined_poc_prior_work_2026-10-09.md`
- Precommitted exploratory measurement method (AFTER the session outcome was known): `research/savino/savino_inverse_combined_poc_protocol_v0_1_2026-10-09.md`
- Detailed results: `research/savino/savino_inverse_combined_poc_results_2026-10-09.md`
- Reproducible scorer/data: `research/run_savino_inverse_poc_v0_1.py` and `research/results/savino_inverse_poc_2026-10-08_intervals.csv`

One screenshot-selected matched October 8 inverse curve scored from ORIGINAL PREMARKET red path against connected Webull SPY M5 30-minute signs: **6 of 12** direction matches; always-UP and always-DOWN same-day baselines also **6 of 12**. Afternoon forecast trough ~13:03 ET versus actual Webull SPY low in 13:25 M5 bar (~22m early, approximate chart x calibration). **Major scale warning:** morning red chart left axis ~7795–7807 SPX; post-close results chart left axis ~7730–7805. The premarket chart cannot legitimately be credited with accurately calling 7730. The independent Oct 8 OR+VWAP 10:10 LONG contradicts the inverse DOWN phase (and later stops), but the actual first half-hour direction was UP; hypothetical after-the-fact filtering is NOT evidence of an advantageous live filter.

Conclusion: do not add inverse as timing gate, Direction/Strength/Runway input, veto, A+ promoter, trade or stop authority. Savino levels remain optional structural reference only, frozen A+ unchanged. Before any future promotion collect 30–50+ timestamp-archived untouched matched intraday inverse+levels sessions, resolve axis and SPX M5 data quality, and compare price-only vs inverse-only vs levels-only vs combined under matched entries/stops and opportunity cost.

## Savino broad inverse phase exploratory re-score — 2026-10-09
Status: **RETROSPECTIVE SELECTED-DAY PHASE ALIGNMENT; PREDICTIVE/TRADE EDGE NOT DEMONSTRATED**. Additional researcher-chosen metrics AFTER outcome are NOT prospective validation.
- Protocol: `research/savino/savino_inverse_broad_phase_test_v0_2_exploratory_2026-10-09.md`
- Results: `research/savino/savino_inverse_broad_phase_results_v0_2_2026-10-09.md`
- Reproducible source: `research/run_savino_inverse_broad_phase_v0_2.py`, `research/results/savino_inverse_broad_phase_v0_2_windows.csv`.
- Source is original premarket Oct 8 red curve digitization, not post-event result image; Webull SPY RTH M5 proxy; one selected day only; SPX chart scales differ markedly between morning and after-close.

Same-day matching: 30m 6/12; 60m 2/6; **90m 4/4**; **120m 3/3** with fixed 10:00 anchored windows. Robustness: 90m rolling 9/10, starting 10:30 3/3; 120m rolling 7/9 (equal to always-DOWN baseline 7/9), starting 10:30 only 1/2. Broad forecast trough 13:00–13:03 vs actual SPY five-minute low bar 13:25 (~22–25min early). Morning image Y axis ~7795–7807 vs later ~7730–7805, so do not claim precisely predicted 7730 SPX. No independent trade improvement or Savino invalidation advantage established.

**Strict boundary:** horizontal levels = optional unvalidated map; inverse = optional unvalidated broad timing hypothesis; neither generates trades/Strength/Runway, creates or vetoes A+ state, hard-stops, or options entries. Do not optimize/trust 90m on this observed day. Next test only on untouched timestamp-archived curves with predeclared horizon and naive/price-only benchmarks; frozen A+ v1.0 unchanged.

## Savino October monthly dual-path update — captured 2026-10-09 AM
**SOURCE CAPTURED / NOT YET OUTCOME-SCORED; NO DIRECTIONAL TRADE CALL.**
User-supplied screenshots from 08:22–08:23 ET on Oct 9 display a post labeled ~1d old containing an October 2026 SPX monthly forecast AND its inverse. Author expressly warns charts **not scaled for price** and **direction uncertain**, with "some sort of spike" around Oct 9 of unspecified sign. Primary green chart descends into ~Oct 17–19 then rebounds ~Oct 23–25; inverse is approximately mirrored. Oct 17–18 is weekend; exact trading-session mapping awaits prespecified protocol. These are **one unresolved binary scenario**, not two separately creditable directional predictions. Vertical scale is NOT an SPX price target. Never backfill winning direction after moves occur.

Source archive with screenshot SHA-256 fingerprints, captured-time/provenance limitations, and pre-event candidate windows: `research/savino/savino_spx_october_2026_monthly_primary_inverse_update_captured_2026-10-09.md`.

This is a MONTHLY chart and must not be conflated with the single-day Oct 08 intraday inverse 90-minute pilot. Capture is descriptive only; no A+ gate, options signal, event veto, Savino level target/stop, Strength or Runway promotion. Before prospective timing accuracy verdict freeze outcome definition/date tolerance and matched base-rate/volatility benchmark; do not claim a directional success when both directions were originally supplied.

## CROM volatility cluster alert × Savino timing overlap — 2026-10-09
Verdict: **BROAD OCT 08 TEMPORAL COINCIDENCE ONLY; UNVALIDATED ALIGNMENT AND NO SCANNER PROMOTION**.
Source observation and audit: `research/savino/crom_savino_volatility_alignment_capture_2026-10-09.md`. User screenshots preserve Crom Oct 05/06 SPY "new cluster" with horizons 2.62/4.61 trading days; Oct 08 05:00 AM and 1:30 PM app "volatility >1.0" threshold detections; Oct 09 05:00 AM new cluster with 2.63 trading days. **Critical clock conflicts:** Oct 05 3 PM ~2.62 trading days displayed as Oct 06 11:03; Oct 09 5 AM ~2.63 trading days displayed as Oct 10 01:05 (Saturday). Do not use raw displayed prediction times as validated expiry; cluster duplicates cannot be identified without IDs. App forecast-volatility threshold is not directly validated option IV.
Webull SPY Oct 08 RTH range 0.859% (Oct 05 0.906%, Oct 06 0.470%, Oct 07 0.708%); max 5m candle range Oct 08 0.319% at 12:15 vs Oct 06 0.099%, Oct 07 0.224%. Savino Oct 08 originally posted intraday chart had afternoon trough estimated 13:00–13:03, actual SPY low in 13:25 five-minute candle. The overlap concerns *time/volatility* only, not directional agreement or statistical validation. Savino Oct 09 "spike" direction unspecified; Crom Oct 09 forecasts a future cluster with incoherent timestamp; no Oct 09 completed session outcome at morning capture.
No standalone trade, no A+ changes; future test requires deduplicated timestamps/horizon units and precommitted objectively measured volatility event/baselines on untouched sessions.

### Crom ~trading-day interpretation clarified — 2026-10-09 08:34 ET
The "~2.62/~2.63 trading days" texts are **approximate forecast horizons**, not exact event datetimes. Earlier strict treatment of Oct 05 alerts as unusable due to mismatched displayed clock timestamps was too dismissive: Oct 05 afternoon ~2.62 TRADING DAYS can plausibly correspond broadly to the Oct 07–08 period, making the Oct 08 volatility expansion **a relevant temporal consistency candidate** (unscored due to unknown "~" width and proprietary volatility metric). Oct 09 Fri 05:00 AM ~2.63 trading-day cluster means approximately early the following market week (roughly Tue Oct 13 on full-session counting), **not** literal Sat Oct 10; Mon Oct 12 is next equity trading day but not ~2.63 full sessions later. Printed app absolute calendar times and printed trading-day horizons are still internally mismatched; preserve both raw fields and seek vendor explanation. "Approximately 2.63 trading days away" is NOT logically identical to "anytime before 2.63 days"; freeze allowable tolerance BEFORE new observations. Source clarification appended in `research/savino/crom_savino_volatility_alignment_capture_2026-10-09.md`. No verified forecast hit nor production promotion from this reinterpretation.

Illustrative conditional arithmetic (NOT provider-verified): interpreting a Crom 'trading day' as **6.5 elapsed RTH hours** and skipping overnight/weekends, Oct 05 3 PM +2.62 days maps ~**Oct 08 12:32 PM ET** (Webull Oct 08 largest five-minute high-low at 12:15; day low in 1:25 candle); Oct 09 Fri 5 AM +2.63 days maps ~**Tue Oct 13 1:36 PM ET** (Oct 12 equity market OPEN despite bond-market holiday). These are reverse-engineered clock examples, not ex-ante validated Crom timestamps, and Oct 05 app absolute timestamp still conflicts. Source audit appended and preserved as unscored exploratory alignment.


## Earnings-selloff rebound options execution sensitivity — 2026-10-10
**Verdict: RESEARCH-ONLY / NOT A VERIFIED OPTIONS BACKTEST / NO A+ CALL RULE.**
The earlier 164 quality-qualified event stock-price study (92 original and 72 different-company events) was extended with a frozen 14/30/45/60/90-calendar-day synthetic ATM call premium sensitivity. Four existing fixed entry signals, three starting implied vols (25/40/60%), and three post-entry IV paths (−10/0/+10 points over 10 days) yielded 25,920 modeled position-scenarios. Underlying +5% target / −5% stop, 20-session maximum, before-expiry forced close, 2% combined assumed spread and $0.65 per side contract fee. European Black–Scholes with 4% rate, zero dividends. This is *not* options-market history; the entry sample was already outcome-observed.
Primary IV40/−10-point scenario: 45D call mean modeled return original vs holdout was next-open −22.8/−22.4%, day3 −15.7/−28.7%, SMA crossover −12.0/−31.4%, three-rising-lows −23.8/−19.0%. Higher nominal DTE generally reduced worst interim premium damage in this model but did not produce robust positive means and has substantially higher contract debit. Alternative IV-change scenarios often reverse the profitability verdict, demonstrating that true quotes and contemporaneous IV are mandatory. Same-event timing advantages did not repeat across the two cohorts. No DTE/entry method promoted.
Connected Massive returned historical option CONTRACT TRADE bars for an AAPL 2025 expired call, but historical actual NBBO quotes were NOT_ENTITLED. The frozen four-earnings-event tradebar pilot hit RATE_LIMIT and was not completed, no data purchased. Next: real option bar pilot if limit permits, then executable bid/ask prospective shadow log with fixed affordable contract selection; else hypothesis-only budget-sensitive OTM simulations and fresh validation. Do NOT conflate modeled IV paths, real trade prints, and realizable option fills.
Files: `research/prior_work/earnings_rebound_call_entry_options_prior_work_2026-10-10.md`, `research/earnings_recovery/options_execution_model_protocol_2026-10-10.md`, `research/earnings_recovery/options_execution_model_findings_2026-10-10.md`, `research/earnings_recovery/options_execution_model_results_2026-10-10.json`, `research/earnings_recovery/run_options_execution_model_2026-10-10.cjs`.


## Four-company affordable OTM earnings-call historical pilot — 2026-10-10
**Verdict: PARTIAL DATA-COLLECTION / RESEARCH-ONLY / NO EXECUTABLE EDGE.** New frozen extension: `research/earnings_recovery/affordable_otm_tradebar_pilot_protocol_2026-10-10.md`; results: `research/earnings_recovery/affordable_otm_tradebar_pilot_results_2026-10-10.md`; source observations: `research/earnings_recovery/affordable_otm_tradebar_pilot_observations_2026-10-10.json`.
Exactly 4 original earnings-selloff cases (DELL/QCOM/PYPL/AMAT) with 8 pre-existing day3/three-rising-lows entries, 30/60 day target expirations, call premium debit <=$50 including $0.65 entry fee, entry day option volume >=10. Massive's as-of historical contract listing found options in 8 of 8 thirty-day windows and 2 of 8 STRICT 60–67 calendar-day expiry windows. Thirty-six single-contract history probes (some without entry bars) yielded six entry-cost-and-volume-pass contract observations across QCOM day3/rising and PYPL day3/rising; closest strike not fully certified for all rows.
Examples from genuine option TRADE OHLC, NOT executable quotes: QCOM Sep 5 $175 call bought at Aug 5 first print $0.14 and marked at Aug 13 last print $0.25 = +66.2% after $0.65 fee/side; PYPL Mar 21 $90 call Feb 18 first print $0.40 and Feb 24 last print $0.15 = −64.7%. PayPal Mar 14 $89 call met $50 entry/10-volume floor but had NO print on stock exit date; no fill/return assumed. DELL and AMAT had NO verified eligible candidates in probed strikes, not exhaustive proof of no option availability. QCOM rising September 12 $170 call was an additional historically qualifying affordability/volume probe: Aug 13 first trade $0.43 with 16 daily contracts, Sep 5 last trade $0.16 with 107 contracts = day-end proxy −64.8% after illustrative $0.65 fee each way. But Sep 5 option low/high were $0.11/$0.48, a wide price range relative to the same day's intraday stock target; option fill at trigger time cannot be inferred. Nearby QCOM rising strikes were too expensive or thinly traded in probed data; full strike scan not completed. Historical calls remained not executable-quote-verified. The first-print option series is not a synchronous option chain, and multiple cells were rate-limited. Historical option NBBO access NOT_ENTITLED; user funds not spent.
Do not treat isolated trade-print proxy results as actual option ROI, do not promote $50 OTM call buying. Next clean research requires completing remaining explicitly frozen probes at no cost when accessible and separately, more importantly, a prospective bid/ask shadow log of new earnings-selloff events with actual affordable contract selection, point-in-time IV and liquidity.

## Alternative existing 2025 options data-source audit — 2026-10-10
**Research branch ongoing; NO HISTORICAL QUOTE-VERIFIED FOUR-EVENT P&L YET.** Source review saved at `research/prior_work/earnings_recovery_historical_option_data_audit_2026-10-10.md`. OnclickMedia free historical options backtester advertises 2013–2026 EOD actual bid/ask, but its separate free quote API appears to limit older histories. We created and actually executed an Investing OS public GitHub Actions no-cost access audit, `research/earnings_recovery/onclickmedia_four_event_feasibility_2026-10-10.json`: all DELL/QCOM/PYPL/AMAT historical availability GET calls returned HTTP 502 origin errors, ZERO 2025 chain/quotes retrieved. Repro script/workflow committed. Alpaca free Basic users may access actual historical OPRA option bars/trades from Feb 2024 more than 15 minutes old, per Alpaca market-data specialist, but the connected Alpaca tools do not expose option historical methods and Alpaca docs DO NOT expose historical options NBBO quote time series; its indicative quotes are modified and unsuitable as actual fills. Already connected Massive successfully returns 2025 option trade OHLC subject to rate limit, NOT actual historical bid/ask. MarketData.app free/trials limit to latest 1 year and Alpha Vantage historical option chain is premium; SPY/QQQ/IWM public archived options chains do not cover these four names. We will keep research historical rather than replace it with a shadow test; no data purchased, no scanner changes or expectancy claims.


## Four-company truly FREE historical EOD bid/ask + five-minute option print reconstruction — 2026-10-10
**Status: HISTORICAL FREE-DATA RECONSTRUCTION COMPLETED FOR SELECT CASES; ONLY EXPLORATORY, NO EXECUTABLE P&L OR A+ RULE.**
Free, unauthenticated DoltHub `post-no-preference/options/master` SQL returned 2025 dated **EOD option bid/ask, strike/expiry, IV and delta** on ALL 8 frozen entry dates and corresponding stock exits for DELL/QCOM/PYPL/AMAT (16 spot-filtered symbol/date queries, 351 quote rows including overlap). Complete raw quoted chain responses: `research/earnings_recovery/dolthub_four_event_eod_chain_2026-10-10.json`, reproducible script `research/earnings_recovery/run_dolthub_four_event_2026-10-10.py`; chain is sampled 3 expiries/date, lacks volume/OI; field `vol` is IMPLIED VOLATILITY, not traded contract volume, so EOD ask-only matches cannot satisfy the frozen entry-volume rule and EOD quotes are not next-OPEN quotes.
One fixed 30-day affordable matched entry/exit EOD bid/ask available: PYPL rising Feb18 March21 $90C bought EOD ask $0.39, exited Feb24 bid $0.15 => −63.8% with illustrative $0.65/side. IV increased from 34.21% to 39.50% (didn't rescue option). Historical QCOM day3 Sep05 $175C had bid $0.02, ask $0.23 entry EOD, an unusually 91.3%-of-ask spread; its historical first trade $0.14 that morning is not proof one could buy it for $0.14. No claims of quote-based P&L for contracts omitted from next snapshot.
**Also accessed historical Massive FIVE-MINUTE stock and option TRADE OHLC at no extra cost**, and located FIRST stock target/stop 5-minute bars using unadjusted stock OPEN and +5%/−5% thresholds. QCOM day3 Aug13 11:10 ET stock target; QCOM $175 Sep05 call first traded after signal at 11:45 ET $0.24 versus Aug05 first buy-day print $0.14 => +59.4% proxy but 35-minute missing quote gap. QCOM rising Sep05 9:40 ET stock target; QCOM $170 Sep12 call first post-signal traded at 9:50 ET $0.28 versus Aug13 first buy-day print $0.43 => −37.3% proxy; only ONE option contract printed in that bar. PYPL rising Feb24 10:05 ET stock stop; Mar21 $90C first printed after stock-stop bar 10:10 ET $0.15 vs Feb18 first print $0.40 => −64.7% proxy. **Critical corrective audit:** PYPL day3 Feb21 stock stop was 13:20 ET, established only after fetching a second 5m STOCK page; Mar14 $90C on that date traded at 09:50 and 10:10 ET only, both BEFORE stock stop, so the previous unsynchronized '−67.1% exit' is NOT an observed sale at stop. Actual primary $89C had no exit-date trades at all. Never claim those as fills.
Detailed audit `research/earnings_recovery/four_event_free_historical_bidask_intraday_audit_2026-10-10.md`; full time/price observations `research/earnings_recovery/four_event_free_5min_timestamped_option_prints_2026-10-10.json`. Free alternative sources found; the earlier 104-stock public CDN was offline since 2026 and supplied NO data, while OnclickMedia probe was 502 for 4 names. Historical analysis can continue without shadow test or paying. No verified full-option NBBO at trigger, no demonstrated positive expectancy, no live scanner change.


## Free historical 100-event earnings recovery OTM options study — 2026-10-10
**Completed an expanded RETROSPECTIVE EOD bid/ask sensitivity study; remains RESEARCH-ONLY and NOT a strict executable options backtest or A+ CALL edge.**
Canonical result: `research/earnings_recovery/free_100event_2024_2025_otm_options_results_2026-10-10.md`. Pre-frozen source cohorts: ALL 45 previously qualified 2024 selloff events (29 original /16 separate-company) and 55 2025 events (29/26), not fresh OOS. Same pre-frozen day3 and first three-rising-lows stock next-open entries, +5% target/-5% stop or 20 sessions, same $50 call debit and 30/60-day expiry bucket with 7-day grace. Corrected historical post-event stock split conversion; excluded unresolvable scale/deliverable periods.
Free DoltHub historical OPTION END-OF-DAY quotes (not first-trade-open or target-time NBBO), 331/331 historical quote queries returned successfully; results and compressed raw source caches permanently committed under `free_2024_eod_otm_45event_*` and `free_2025_eod_otm_55event_*`, with reproducible Python and workflows. 100 events x two stock signal methods = 200 possible entry setups, times 2 expiries =400 cells; 169 eligible setups had quote date read, 52 affordable EOD-ASK option candidates, **only 20 same-contract EOD bid/ask exit observations (5% of possible cells)**, representing 17 distinct events and 13 symbols. Missing quote not loss. Source has NO contract daily trading volume; `vol` means IV; source samples only about three expirations per trading date, not full listed history, and entry/exit are EOD snapshots rather than actual frozen stock OPEN and first intraday threshold touch. Real frozen first-option-trade >=10 volume rule therefore remains UNVERIFIED for broad cohort. Cannot compare day3 vs rising on same event and same DTE from any matching EOD pairs.
Conditional 2024 **6/10 positive**, mean +87.4%, median +27.0%; 2025 **2/10 positive**, mean −40.4%, median −54.1%. Combined **8/20 positive, mean +23.5% but median −39.0%**, large 2024 outliers TGT +309.8%, CPRT +380.5% and +131.4% on the same event in different expiries, PYPL +304.2%. This is NOT an unbiased return or win-rate estimate; severe expiry/exit selection, timing, and spread biases and strong cross-year conflict. Some stocks touched +5% while their quoted calls still lost >30%.
Completed additional DELL/AMAT original fixed pilot strike-tail screening: DELL March06 day3 2025-Apr11 $116 first print $0.50 (with $0.65 fee exceeds budget; 3 contracts); DELL March13 rising 2025-Apr17 $115 $0.48 with 6 contracts, below 10 volume; AMAT Feb20 day3 2025-Mar28 $210 $0.50 and 3 contracts; AMAT Feb21 rising $220 $0.15 but 1 contract. No verified instrument meeting both $50 and 10-entry-day-trading-volume rules from observed history. This is **NOT** proof no theoretically possible contract existed in unqueried strikes. Further selected strikes and expiries archived in complete report.
Other 2024 Massive historical trade bars sometimes NOT_ENTITLED while PYPL Nov2024 option daily bars were observed; user not charged. No live scanner changes; valid next operation would require free historical full-chain or timestamped NBBO fillability that resolves sparse coverage before interpreting profitability. Do NOT substitute paid feed or forward shadow test by default.


## Historical option volume/quote bottleneck audit + stock-adjustment corrections — 2026-10-10
**RESEARCH-ONLY; PARTIAL HISTORICAL COVERAGE; NO A+ option-entry validation.**
Full audit: `research/earnings_recovery/free_historical_quote_volume_and_raw_stock_exit_bottleneck_findings_2026-10-10.md`. Pre-enumerated the complete 52 previously affordable EOD-selected contract opportunities `frozen_100event_52_eod_affordable_contracts_for_volume_repair_2026-10-10.json` BEFORE new independent price/volume checks. 32 lacked matched Dolt EOD exit bid: 32/32 SQL queries by exact option contract date, expiration, strike without spot filter succeeded but returned zero rows; missing is truly due to Dolt sampled/archive omissions, NOT a guaranteed zero option price. Public 104-symbol option parquet archive was ACTUALLY checked on independent Github runner: QCOM/PYPL/TGT/TXN/ADBE/SPY HEAD and QCOM/PYPL range GET all returned 404. No source data from defunct archive. Full source-test JSON `historical_options_missing_contract_source_probe_2026-10-10.json`.
Massive free historical option daily actual TRADE OHLC (v=contract volume, n=number of trades) repaired some Dolt gaps. Saved 13 targeted contract-query observations in `volume_repair_massive_historical_trade_probes_phase1_2026-10-10.json` and `phase2_2026-10-10.json`: nine returned trade data, three rate limited, one empty. These were targeted probes, NOT random sample. Affordable sampled contracts that met frozen first reported trade debit <=$50 WITH entry fee and >=10 entry-day traded contracts include **UPS Mar7 2025 $121C** (Feb4 first print $0.29, volume 27) and **CMCSA Mar7 $35C** (Feb4 first print $0.23, volume 63); NOT YET verified to be the nearest eligible listed strike. Other EOD candidates were excluded on price or traded volume: DOW Mar7 $41C entry contracts 7, FIS Apr17 $77.5C 1, HPE Apr11 $16C 1, TXN Aug29 $215C 1, QCOM Sep05 $170C 1; HPE May16 $17C traded 30 but first print $0.52 = $52.65 with fee (too expensive), invalidating its EOD +47% illustration as a strict budget trade; TPR Sep19 $115C had no entry-day trade though exit print available. Incomplete coverage persists; never divide by 52 as a win probability.
SEPARATELY pre-froze actual RAW vs dividend-adjusted stock target diagnostic for 200 frozen 2024/25 method setups. Raw Yahoo source audit `raw_stock_price_dividend_exit_audit_100events_2026-10-10.json` successfully compared 178 eligible-entry setups; **171 same exit day, 7 different**. 26 had a dividend during hold and 6 of 7 exit-date differences had such ex-dividend event. Includes UPS day3 Feb4 entry where original adjusted-stock +5% marked Feb18 2025 despite raw stock high that day below +5%; actual RAW +5% target first Feb24. Official UPS dividend $1.64 ex Feb18. Also NOC, LEN, UPS rising, HON, TXN, NFLX exhibited raw/adjusted differences. Among the 20 previously price-matched EOD call bid/ask results, all **18 distinct matched setup** exit dates agree with raw equity price audit; their quoted EOD outcomes still do not equal executable stock-threshold-time fills.
Time-aligned original stock RAW +5% and first NEXT option trade examples, `repair_exit_timestamp_raw_stock_CMCSA_UPS_2026-10-10.json`: **CMCSA** Feb6 12:25 ET target, Mar7 $35C first option trade after trigger at 12:35 ET $0.55 vs Feb4 first trade $0.23, after $0.65 side fees +129.81% first-print proxy. **UPS** corrected raw Feb24 09:50 ET stock target, Mar7 $121C first next option trade at 09:55 ET $0.52 vs entry day first print $0.29, after fees +73.19% first-print proxy. Original prior UPS Feb18 end-of-day first-print mark −17.88% was associated with an incorrect adjusted-stock target EXIT DATE; do NOT cite as a strategy loss. Trade prints not executable bid/ask, and strike nearest-eligible eligibility across full historical chain unconfirmed. These examples do not establish expectancy; 100-event EOD source remains heavily missing exit quotes, and true-time NBBO is unavailable. No paid data, no changes to live scanner; continue historical only.


## Complete historical free option volume-source bottleneck audit — 2026-10-10
**Status: FINISHED ALL 52 FROZEN CANDIDATE SOURCE CHECKS. RESEARCH-ONLY. No validated option execution or A+ strategy.** Canonical study and precise tabulated discrepancies: `research/earnings_recovery/frozen_52_contract_volume_and_time_eligibility_findings_2026-10-10.md`. Exact 52 source rows and tests `research/earnings_recovery/frozen_52_contract_volume_reconciliation_2026-10-10.json`; source data and reproducible offline reconciler committed.
2024 EOD-ask-affordable candidate rows 21, 2025 31. Actual historical option TRADE OHLCV provider queries attempted all **52**: **37** returned option price/volume records, **10** older-contract requests NOT_ENTITLED, **3** empty, **2** rate/error. Of 37 with records, **17** had first traded call debit <=$50 including $0.65 entry fee and >=10 option contracts traded over entry DAY (5 in 2024 and 12 in 2025); **11** failed volume, **2** failed entry-price budget, **7** had NO ENTRY-DATE OPTION TRADE observed. Of 17, **15** had exact-contract final trade observed on stock's CORRECT raw-stock exit date: 2024 **3 positive/2 negative** five first/last print proxies, 2025 **2 positive/8 negative** ten first/last proxies. Combined 5 positive, 10 negative; illustrative median **−64.7%**, arithmetic mean **+5.4%** heavily influenced by >+300% late-2024 PYPL/TGT winners. NOT a population trade/win-rate estimate, and no executable contemporaneous NBBO. UPS 2025 corrected raw stock target date Feb24 vs original dividend-adjusted Feb18: time-aligned next-option-trade price gave +73.2% illustrative print return, separately from the 15 day-last pairs. Many affordable/liquid candidates had −60% to −98% premium declines on option trade marks.
**NEW CRITICAL EXECUTION RULE LIMITATION:** the frozen 'first entry-DATE option trade price' and '>=10 options contracts traded by END OF ENTRY DATE' uses FUTURE information relative to the frozen next-open stock entry. Real opening option ask and daily volume at open were not established. Thus the 52-contract volume audit is a feasibility stress screen, NOT non-lookahead tradable call selection. Closest affordable as-of-entry strike across full listed chain remains unverified. A scientifically clean future historical experiment should freeze *previous-day volume or strictly before-trade cumulative option volume / contemporaneous bid-ask* and recompute using raw equity stock barriers and actual listed option strikes, without buying data or silently claiming fills. No scanner promotion.


## FIXED INFORMATION TIMING / NO-LOOKAHEAD 2025 RECOVERY OPTIONS ENTRY TEST — 2026-10-10
**Completed frozen historic alternative entry protocol, 55 2025 selloffs / 110 stock setup opportunities; NO VERIFYABLE OPTION PRINT ENTRY in selected 10am entry window. Not a 0% options win rate. NO A+ CALL EDGE, no scanner promotion.**
Frozen BEFORE new previous-close option data inspected: `research/earnings_recovery/frozen_nonlookahead_prior_close_1000am_historical_option_protocol_2026-10-10.md`. Fixes past LOOKAHEAD: old strike selection from stock-entry SAME-DAY EOD option ask, and treating entry-DAY total volume/first reported trade as available at stock NEXT-OPEN 09:30. New rule chooses nearest qualifying strike using only PRIOR TRADING DAY 4pm EOD option bid/ask and UNADJUSTED underlying previous close; expiries 30–37 or 60–67 DTE, one standard OTM call, prior ask×100+$0.65<=50, prior spread<=35% of ask. Then 10am ET after >=10 actual option contracts traded 09:30–09:59 and first observed option trade 10:00–10:30 priced <=$50; new raw stock barrier price starts AFTER option trade entry, never at earlier 9:30 stock opening.
Executed reproducible prior-close selection across all 55 saved 2025 quality earnings-selloff events (original 29, separate company holdout 26), 110 potential stock entry method setups, 101 actual stock signals and 9 skipped, **101/101 historic DoltHub previous-day chain SQL requests succeeded**. Only **9 independently prior-close preselected options** (6 nominal ~30D, 3 ~60D, 9 distinct events) among 101 stock signals; 92 no observed prior-close affordable <=35%-spread option in archive (not necessarily absent at exchange). 9 exact preselected contract entry day historical Massive five-minute option trade checks completed. DOW (5), AMAT (7), CSCO (0), CPRT (0) option contracts traded before 10am => **4 FAILED** >=10 pre-10am volume rule. QCOM 20 before 10am but **NO recorded options trade between 10 and 10:30** => 1 failed printed entry. 4 preselected HPE, FTNT May, FIS, FTNT Aug contracts had NO retrievable intraday 5min option trade bars => **4 UNKNOWN quote/execution accessibility**, NOT proof no executable ask. Thus **0/9 actual transaction-based historical entries verified**, no option P&L can be computed and no win/loss inference. Actual bid/ask at 10am still unavailable, prints cannot establish execution.
Independent timing diagnostic on eight older EOD-preselected contract examples: only PYPL Feb18 March21 $90C passed pre10 volume(74) and post10 trade($0.31). Other seven failed one or both. But old list was EOD hindsight sampled; never present it as valid strategy returns.
Detailed full test and accurate negative feasibility result: `research/earnings_recovery/nonlookahead_2025_55event_entry_time_findings_2026-10-10.md`. Raw prior-close chain and frozen selections: `nonlookahead_priorclose_2025_55events_selections_2026-10-10.json` and `nonlookahead_priorclose_2025_55events_rawchains_2026-10-10.json`; selected-candidate time-gate records `nonlookahead_55event_2025_entry_time_results_2026-10-10.json`; 3 exact option history probe phase datasets and the GitHub Actions script/workflow saved. No paid data or shadow test. Do NOT optimize 35%/10-contract gate on already-inspected 2025 data and call new profit edge; use independent cohort before rule relaxation, and seek historical as-of time-stamped options NBBO, prior-day contract OI and full listed chains for remaining research bottleneck.
