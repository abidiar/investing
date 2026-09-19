# Investing OS — Options Positioning Research Status

Updated: 2026-09-19
Status: **CANONICAL TOPIC INDEX**

Detailed prior-work reviews, frozen protocols, code, and machine-readable results remain in `research/`, `research/prior_work/`, and `research/results/`. Governance is controlled by `research/RESEARCH_GOVERNANCE.md`.

## Current production posture
Options-positioning research remains **context-only / research-only** unless a particular decision rule passes its preregistered production gate. No tested OI/gamma feature may independently create direction, add STRENGTH/RUNWAY, manufacture R:R, authorize BUY/SELL/CALL/PUT/HOLD, or authorize overnight carry. **Price gets final vote.**

Every new hypothesis requires a prior-work review under `research/PRIOR_WORK_REVIEW_STANDARD.md` before the outcome protocol is frozen.

## Pass history

### Pass 1 — Dealer/GEX regime
Verdict: **PROVISIONAL / RESEARCH-ONLY**.
Signed/modelled dealer gamma may characterize amplification/damping after independent price confirmation. Raw GEX direction, exact wall/flip precision, and wall proximity alone are not promoted.

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
A strong 2026 QQQ gap-follow-through association appeared but failed the frozen incremental-utility gate.

### Pass 7 — SPY 2025 independent replication
Verdict: **FAILED REPLICATION**.
The QQQ directional gap-gamma relationship did not generalize to SPY.

### Pass 8 — QQQ 2025 time-shift replication
Verdict: **FAILED REPLICATION**.
The 2026 QQQ directional relationship did not reproduce in QQQ 2025. Treat the original directional effect as regime/source-specific, not durable.

### Pass 9 — Multi-year unsigned near-spot gamma compression
Files: `research/multiyear_near_spot_gamma_compression_v1.md` and matching results.
Verdict: **REPLICATED ASSOCIATION / RESEARCH-ONLY**.
Across 2,221 SPY/QQQ/IWM observations in 2023–2025, higher near-spot unsigned gamma associated with smaller next-session RTH range/excursion. Price-volatility state captured most practical forecast value.

### Pass 10 — Untouched 2020–2022 incremental-value holdout
Files: `research/near_spot_gamma_incremental_value_v1.md` and matching results.
Verdict: **CONDITIONAL ASSOCIATION / RESEARCH-ONLY**.
Across 2,262 untouched observations, the compression relationship survived seven price-volatility controls, instrument/year checks, and non-OPEX robustness. Adding gamma improved walk-forward MAE by 1.26% for next RTH range and 1.33% for max excursion, below the frozen 2% promotion gate.

### Pass 11 — Decision-level chase/veto falsification
Files:
- `research/gamma_chase_decision_v1.md`
- `research/results/gamma_chase_decision_v1_results.md`

Verdict: **FAILED DECISION-LEVEL OVERLAY**.
Untouched holdout: 1,195 SPY/QQQ/IWM candidates in 2017–2019, trained on 2014–2016. A gamma veto improved T1 precision from 69.39% to 73.97% (+4.58 pp), but retained only 79.41% of baseline winners and improved Brier only 0.38%. **Unsigned gamma must not be used as a hard entry/chase veto.**

### Pass 12 — Target-calibration decision falsification
Files:
- `research/gamma_target_calibration_v1.md`
- `research/results/gamma_target_calibration_v1_results.md`

Verdict: **FAILED DECISION-LEVEL TARGET OVERLAY**.
Untouched holdout: 799 SPY/QQQ/IWM candidates in 2012–2013 with a 2011 seed. Price-only and price+gamma produced identical 0.21% mean captured target distance, identical 40.55% hit rates, and no target changes on any event. Adding gamma worsened average Brier performance by 0.82%. **Unsigned gamma must not be used as a production target-sizing rule.**

### Pass 13 — Modelled dealer-GEX gap follow-through
Prior work and data audit:
- `research/prior_work/dealer_gex_amplification_damping_prior_work_2026-09-19.md`
- `research/prior_work/dealer_gex_data_method_audit_2026-09-19.md`

Files:
- `research/modelled_dealer_gex_gap_followthrough_v1.md`
- `research/results/modelled_dealer_gex_gap_followthrough_v1_results.md`

Verdict: **MECHANISM-CONSISTENT / INCREMENTAL UTILITY NOT SUPPORTED**.

The broad signed-gamma mechanism was already supported by prior academic work, so this test focused on incremental Investing OS utility. Direct participant-class dealer/customer data were not available, so the test used a published **MODELLED DEALER-GEX PROXY**: call gamma positive, put gamma negative, normalized by trailing-20 underlying dollar volume. This is an inventory assumption, not observed market-maker positioning.

Untouched sample: 741 SPY/IWM opening-gap candidates in 2009–2010, using 2008 as seed.

Mechanism-consistent findings:
- signed GEX/ADV vs gap-direction open-to-close follow-through: **rho=-0.0759, p=0.0389**;
- signed GEX/ADV vs excursion efficiency: **rho=-0.0758, p=0.0391**;
- both expected signs persisted in **4/4** prespecified instrument/year subgroups;
- negative-proxy sessions had **51.37%** gap-direction continuation vs **44.33%** for positive-proxy sessions;
- negative-proxy sessions had larger RTH ranges (**2.31% vs 1.76%**), consistent with an amplification regime.

But incremental predictive value was weak:
- continuation Brier improvement: **0.61%** vs frozen 2% gate;
- follow-through MAE improvement: **0.15%** vs frozen 2% gate;
- excursion-efficiency MAE worsened slightly by **0.11%**.

Conclusion: the easy/public call-minus-put OI proxy broadly matches the economic mechanism but **does not add enough decision value beyond price, volatility, and liquidity** for Investing OS. It receives no production authority.

## Current best interpretation
- Raw OI is not directional.
- Delta-OI persistence is not useful enough for next-session movement/continuation.
- Large gamma walls are not automatic magnets; exact wall/flip levels are not penny-precise trade levels.
- The unsigned-gamma directional gap-continuation idea failed two independent replications.
- Unsigned near-spot gamma has a replicated non-directional amplitude/compression association but failed two practical decision-level uses.
- The published **OI-sign dealer-GEX proxy** is mechanism-consistent but fails our material incremental-utility standard.
- Stronger dealer-side data remain potentially useful because participant capacity / signed-flow information solves the central measurement problem that OI cannot.

## Data/source conclusion for signed dealer GEX
The strongest historical sources we identified are not currently in the Investing OS tool stack:
- Cboe trade-by-trade participant capacity + buy/sell + open/close;
- Cboe Open-Close participant summaries;
- OptionMetrics Signed Volume / TradeFlow or equivalent signed-flow data.

The open Dubach ETF archive provides excellent OI/Greeks history but cannot identify dealer inventory. Therefore further OI-based sign tuning is low priority.

## Rejected / not production-eligible
- Raw OI as bullish/bearish direction.
- Call-vs-put OI buildup as direction.
- Delta-OI/volume persistence as a next-day movement/continuation edge.
- Large gamma wall as an automatic magnet.
- Exact gamma wall/flip as penny-precise trade levels.
- High unsigned gamma as a directional signal.
- High unsigned gamma as a hard entry/chase veto.
- High unsigned gamma as a production target-sizing rule.
- The QQQ 2026 gap-gamma continuation effect as a general market rule.
- Call-positive / put-negative modelled dealer-GEX as a production continuation/reversal overlay.

## Do Not Re-Test Unless
- Do not resurrect the failed QQQ gap-continuation rule by changing gap threshold, DTE, moneyness, near-gamma band, IV filter, or OPEX exclusions.
- Do not tune 2020–2025 unsigned-gamma thresholds to force the 2% forecasting gate.
- Do not soften the failed Pass-11 veto using the same 2017–2019 outcomes and call it validation.
- Do not lower the Pass-12 target threshold or change its ladder using the same 2012–2013 outcomes.
- Do not treat public open interest as observed dealer inventory.
- Do not tune Pass-13 sign convention, gap threshold, liquidity normalization, or 2009–2010 outcomes to force promotion.
- Do not make exact wall/pinning behavior the next priority without materially stronger data/evidence.

## Next clean research priority
Pause further **OI-based** dealer-GEX proxy work.

If stronger participant-class or signed-flow data become available, use a modern multi-year SPX/SPXW sample with intraday bars and test whether observed/stronger dealer positioning improves 30/60/120-minute continuation/reversal and MFE/MAE beyond a price/volatility/liquidity baseline.

Otherwise shift Investing OS research to another hypothesis family rather than continuing to optimize public OI-based GEX.
