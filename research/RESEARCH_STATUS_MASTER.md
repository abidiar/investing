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
