# Investing OS — Options Positioning Research Status

Updated: 2026-09-19

## Current production posture
Options-positioning research remains **context-only / research-only**. No tested options-positioning feature may independently create direction, add STRENGTH/RUNWAY, manufacture R:R, or authorize BUY/SELL/CALL/PUT/HOLD/overnight carry. Price gets final vote.

## Pass 1 — Dealer/GEX regime
File: `research/options_positioning_dealer_structure_v1.md`

Provisional finding: signed/modelled dealer-gamma regime appears more useful for expected move behavior than direction. Negative gamma may amplify an independently confirmed move; positive gamma may dampen it. Small sample; not promoted to action gate.

Rejected/not promoted: raw GEX direction, exact wall/flip precision, wall proximity alone.

## Pass 2 — QQQ settled OI persistence
Files:
- `research/qqq_oi_persistence_v1.md`
- `research/results/qqq_oi_persistence_v1_results.md`

Verdict: **NOT SUPPORTED**.

Across 162 sequential sessions, delta-OI/volume persistence did not predict larger next-session movement and did not improve continuation after a meaningful Day-T move. Call-vs-put buildup imbalance had essentially zero directional relationship with next-session return. Do not promote raw delta OI, persistence, or call/put buildup direction.

## Pass 3 — QQQ gamma concentration / pinning
Files:
- `research/qqq_gamma_concentration_v1.md`
- `research/results/qqq_gamma_concentration_v1_results.md`

Verdict: **RESEARCH-ONLY**.

Near-spot unsigned gamma concentration was associated with smaller next-session RTH high-low range, with expected-sign stability and stronger evidence in the second half. However, it did not materially reduce absolute close-to-close movement, pinning to a dominant strike failed, and the extended walk-forward model did not satisfy the frozen promotion gate.

## Pass 4 — Overnight vs RTH decomposition
Files:
- `research/qqq_gamma_rth_decomposition_v1.md`
- `research/results/qqq_gamma_rth_decomposition_v1_results.md`

Verdict: **RESEARCH-ONLY**.

Near-spot gamma concentration was more clearly associated with RTH range compression than overnight-gap magnitude. Full-sample rho for near-spot gamma vs RTH range was -0.220 (p=0.0045) versus -0.061 for absolute overnight gap. Walk-forward improvement was insufficient for promotion.

## Pass 5 — QQQ gamma path efficiency
Files:
- `research/qqq_gamma_path_efficiency_v1.md`
- `research/results/qqq_gamma_path_efficiency_v1_results.md`

Verdict: **RESEARCH-ONLY / BROAD PATH-EFFICIENCY HYPOTHESIS FAILED STABILITY**.

The apparent relationship between higher near-spot gamma and cleaner RTH path was concentrated in the first half and disappeared in the second half and recent 5-minute robustness sample. Walk-forward prediction worsened. A narrower secondary gap-conditioned signal remained interesting but required a dedicated test.

## Pass 6 — QQQ gap-conditioned gamma continuation
Files:
- `research/qqq_gap_gamma_continuation_v1.md`
- `research/results/qqq_gap_gamma_continuation_v1_results.md`

Verdict: **RESEARCH-ONLY**.

On 119 QQQ sessions with abs(overnight gap) >=0.25%, higher prior-day near-spot gamma was associated with better same-direction follow-through (rho=+0.277, p=0.0023), better excursion efficiency (rho=+0.286, p=0.0016), and lower adverse excursion (rho=-0.355, p=0.0001). The expected sign persisted across chronological halves for the two primary relationships and outside OPEX. However, the extended walk-forward model failed the frozen incremental-usefulness gate, so no promotion was allowed.

## Pass 7 — SPY 2025 independent replication
Files:
- `research/spy_gap_gamma_replication_v1.md`
- `research/results/spy_gap_gamma_replication_v1_results.md`

Verdict: **FAILED REPLICATION**.

This replication used SPY rather than QQQ and calendar-2025 options snapshots, with no 2026 QQQ observations. There were 129 qualifying abs(gap)>=0.25% sessions and the same frozen gamma construction/thresholds.

The primary QQQ relationship did **not** generalize:
- near gamma -> gap follow-through: rho=+0.054, p=0.547 full sample; second half rho=-0.172
- near gamma -> excursion efficiency: rho=-0.036, p=0.690 full sample; second half rho=-0.202
- near gamma -> MFE was significantly negative rather than positive (rho=-0.308, p=0.0004)

A lower-adverse-excursion relationship survived in the full SPY sample (near gamma -> MAE rho=-0.248, p=0.0045) and non-OPEX sample, but it failed chronological stability because the second-half sign turned slightly positive. Descriptively, higher-gamma SPY gaps continued 53.1% vs 46.2% for lower gamma, far smaller than the prior QQQ 61.0% vs 36.7% separation.

Walk-forward performance materially worsened when gamma features were added: follow-through MAE -18.4% improvement (worse), excursion-efficiency MAE -2.8% (worse), and MAE-from-open prediction -21.7% (worse). Therefore the QQQ gap-gamma effect must be treated as sample/instrument-specific until proven otherwise, not as a general scanner edge.

## Pass 8 — QQQ 2025 time-shift replication
Files:
- `research/qqq_gap_gamma_2025_replication_v1.md`
- `research/results/qqq_gap_gamma_2025_replication_v1_results.md`

Verdict: **FAILED REPLICATION**.

This is the same underlying as the original discovery but a non-overlapping calendar year and an independent historical options archive. It contained 151 qualifying abs(gap)>=0.25% sessions.

The original 2026 QQQ relationship did not replicate:
- near gamma -> gap follow-through: rho=-0.030, p=0.718
- near gamma -> excursion efficiency: rho=-0.144, p=0.078, opposite the frozen expected sign
- near gamma -> MFE: rho=-0.328, p<0.001, strongly opposite the original favorable-excursion hypothesis
- near gamma -> MAE: rho=-0.085, p=0.297, directionally favorable but weak

Chronological stability also failed. In the second half, near gamma vs follow-through was rho=-0.189 and near gamma vs excursion efficiency was rho=-0.237 (p=0.039), both opposite the expected continuation relationship. Non-OPEX follow-through became mildly positive (rho=+0.129) but excursion efficiency remained essentially zero (rho=-0.006).

Descriptively, above-median near-gamma sessions continued only 45.3% versus 46.1% below median, with lower average MFE (0.51% vs 0.91%) and lower excursion efficiency (42.4% vs 48.4%).

Walk-forward performance worsened materially when gamma features were added: follow-through MAE -7.0% improvement (worse), excursion-efficiency MAE -1.43% (worse), and adverse-excursion MAE -14.27% (worse).

Because both SPY 2025 and QQQ 2025 failed, the original QQQ 2026 gap-conditioned gamma continuation result is now best treated as **2026-regime/source-specific discovery rather than a durable cross-regime scanner edge**.

## Pass 9 — Multi-year near-spot unsigned gamma compression
Files:
- `research/multiyear_near_spot_gamma_compression_v1.md`
- `research/results/multiyear_near_spot_gamma_compression_v1_results.md`

Verdict: **REPLICATED ASSOCIATION / RESEARCH-ONLY**.

This preregistered test used **2,221** SPY/QQQ/IWM Day-T observations across **2023, 2024, 2025** and asked a non-directional question: does greater unsigned theoretical gamma concentration within ±0.50% of spot predict a smaller next-session RTH range/excursion?

The raw association replicated strongly:
- pooled near gamma -> next RTH range: rho=-0.456, p<0.001
- pooled near gamma -> next max excursion: rho=-0.382, p<0.001
- non-OPEX near gamma -> RTH range: rho=-0.452, p<0.001
- SPY: rho=-0.459; QQQ: rho=-0.305; IWM: rho=-0.090 for next RTH range, all negative and IWM still p=0.014
- 2023: rho=-0.407; 2024: rho=-0.463; 2025: rho=-0.488 for next RTH range, all p<0.001

Using each instrument-year's own median to avoid simple scale pooling, HIGH near-gamma sessions averaged **1.228%** next-day RTH range versus **1.507%** for LOW near-gamma sessions, and **0.999%** versus **1.187%** maximum open-centered excursion.

However, the normalized `NEXT_RANGE_VS_20D` relationship was much weaker (pooled rho=-0.084), and the price-only walk-forward baseline already captured nearly all of the practical information. Adding gamma improved MAE only **0.19%** for next RTH range and **0.24%** for max excursion, far below the frozen 2% promotion threshold. This strongly suggests near-spot gamma concentration is a **robust marker of the prevailing compression/volatility regime, but not yet an independent forecasting edge beyond price-based volatility state**.

## Pass 10 — Untouched 2020–2022 incremental-value holdout
Files:
- `research/near_spot_gamma_incremental_value_v1.md`
- `research/results/near_spot_gamma_incremental_value_v1_results.md`

Verdict: **CONDITIONAL ASSOCIATION / RESEARCH-ONLY**.

This preregistered holdout used **2,262** SPY/QQQ/IWM Day-T observations across **2020, 2021, 2022**, with no 2023–2026 observations in the verdict. It directly tested whether near-spot unsigned gamma retained information after controlling for seven Day-T volatility/range variables: absolute O/C move, RTH range, RV5, RV20, trailing-20 median range, ATR20, and current-range/trailing-median ratio, with instrument/year fixed effects and HC3 errors.

The controlled association **survived strongly**:
- pooled near gamma -> log(next RTH range): coefficient **-0.722**, HC3 p<0.001
- pooled near gamma -> log(next max excursion): coefficient **-0.747**, HC3 p<0.001
- range coefficient was negative in **SPY (-1.191, p<0.001), QQQ (-0.560, p=0.015), and IWM (-0.374, p=0.031)**
- range coefficient was negative in **2020 (-0.477, p=0.023), 2021 (-1.210, p<0.001), and 2022 (-0.490, p=0.013)**
- non-OPEX coefficients remained strongly negative for both primary outcomes.

Residual tests told the same story after removing the volatility-only fitted component:
- near gamma vs unexpected next RTH range residual: rho **-0.090**, p=0.00002
- near gamma vs unexpected max-excursion residual: rho **-0.072**, p=0.00057
- both remained negative/significant outside OPEX.

However, the practical incremental forecast improvement was still modest rather than large. Adding the frozen gamma features to the richer price-volatility baseline improved walk-forward MAE by **1.26%** for next RTH range and **1.33%** for max excursion, below the frozen **2%** promotion threshold; absolute O/C improved only 0.64%.

Interpretation: near-spot unsigned gamma is **not merely a simple volatility proxy**. It contains a small but statistically robust amount of independent information about next-session amplitude after controlling for observable price volatility. But the incremental forecasting gain remains too small under our predeclared standard to influence scanner action states, Strength/Runway, or option selection.

## Current best interpretation
- Raw OI: not directional.
- Delta-OI persistence: not useful enough for next-session movement/continuation.
- Large gamma wall: not automatically a magnet.
- The directional gap-continuation interpretation of near-spot unsigned gamma **failed two independent replications** and is not usable.
- A narrower, non-directional compression relationship has now survived both a 2023–2025 broad replication and a separate 2020–2022 controlled holdout.
- High near-spot unsigned gamma appears to be a **real, small additive signal about expected RTH amplitude/compression**, not just a restatement of price volatility, but current walk-forward value is below the frozen promotion threshold.
- Signed/modelled dealer GEX remains economically distinct and still requires larger independent validation.

## Do Not Re-Test Unless
Do not re-optimize or resurrect the failed QQQ gap-conditioned continuation rule by changing the gap threshold, DTE, moneyness, near-gamma band, IV filter, or OPEX exclusions.

For unsigned gamma compression, do not tune thresholds on the 2020–2025 results to force the 2% gate. The core relationship is now sufficiently replicated; additional work should focus on either (a) a genuinely new data source/mechanism, such as signed dealer positioning, or (b) whether the small additive amplitude signal improves a specific already-frozen Investing OS decision problem such as chase avoidance, target sizing, or option-structure choice without granting directional authority.

## Next clean falsification
If continuing unsigned-gamma work, the most useful next experiment is **decision-level utility**, not another correlation test. Freeze one concrete use case—for example, whether adding a high-gamma compression flag to otherwise-qualified breakout setups reduces false breakout/chase losses or improves target calibration—then test it out of sample without changing entry direction or Strength/Runway rules. Alternatively, shift research effort to signed/modelled dealer-GEX amplification/damping, which remains a distinct and potentially more actionable mechanism.
