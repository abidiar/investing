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
