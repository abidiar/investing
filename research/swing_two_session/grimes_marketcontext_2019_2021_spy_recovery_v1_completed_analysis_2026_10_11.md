# Frozen SPY-as-of-entry market recovery diagnostic — 2019–2021

**Completed 2026-10-11. Verdict: the prespecified SPY-above-morning-open condition FAILED to improve the existing stock failed-breakdown rule.** It selected the worse subset in this sample. This is an explicit **negative result on one specific market context gate**, not a refutation of market exhaustion studies or of Adam Grimes's original discretionary setup.

## Protocol and audit

- Preregistered complete rules `frozen_grimes_market_recovery_2019_2021_v1_2026_10_11.md` at commit `ba13fdd32df497425148a467fa89854b900f9fcd` BEFORE the 2019–21 daily histories were retrieved.
- Frozen exact 90 ticker universe carried from earlier 2022 study (future-selection/survivorship limitations). Historical daily pre-outcome archives in five `data/grimes_marketcontext_2019_2021_daily_preoutcome_batch_0*.json`.
- **198** daily support candidates across 2019–2021; roster and as-of D0 double-swing-pivot support committed at `b4cb144e9708cd46b0601d230b7a16884e79c44d` BEFORE D1/D2 M5 events were accessed.
- **174** complete 78+78+78 five-minute stock RTH bars, **24 UNKNOWN/incomplete** (not failures, winners or zeros). Vendor originals preserved in 14 `data/grimes_marketcontext_2019_2021_m5_source_batch_*.json` files.
- **28** filled mechanical failed-breakdown stock entries; initial stock price-only decisions written in `data/grimes_marketcontext_2019_2021_stock_entries_pre_spy_gate_2026_10_11.json` BEFORE accessing SPY M5 D1 data. All **25 entry dates** had complete 78-bar SPY D1 M5 histories; sources in two `data/grimes_marketcontext_2019_2021_spy_d1_source_batch_*.json` files.
- Only market condition changed: at already-determined stock entry open, prior fully completed SPY five-minute close is **strictly ABOVE** the initial SPY 09:30 open. No future SPY bars or later entry conditions. Same stock fill, structural stop (penetration low −0.10%), +2.00% target, D2 close timeout, conservative gap/ambiguous fills, 0.50% stock-equivalent roundtrip costs. No historical options quotes.

## Result

| Frozen variant | Filled | Target-first | Stop-first | Target-first / filled | Avg net / filled stock trade |
| --- | ---: | ---: | ---: | ---: | ---: |
| Price-only failure, no market filter | 28 | 9 | 19 | 32.143% | -0.396% |
| **SPY above morning open at stock entry** (pre-specified selection) | **10** | **1** | **9** | **10.000%** | **-1.120%** |
| SPY at or below morning open at stock entry (DESCRIPTIVE, NOT an independently frozen buy filter) | 18 | 8 | 10 | 44.444% | 0.006% |

- Contrasts among **executed fills**: SPY-above-open minus SPY-at/below-open mean net **-1.126 percentage points**. Estimated 95% ticker-cluster bootstrap interval **[-1.985, -0.171] pp** with 10,000 resamples. Date-cluster 95% interval **[-1.952, -0.182] pp**. This is conditional, observational, small-sample, multi-year; NOT a causal treatment effect or robust independent winner.
- **Per evaluable daily candidate** including skips as 0: ungated price-only **-0.064%**, SPY-above-open-gated **-0.064%**, unconditional D1 next-open +2/-2 baseline **-0.680%**. Gated minus ungated **-0.001 pp** (essentially unchanged and negative). 95% ticker-cluster interval gated minus ungated **[-0.063, 0.062] pp** spanning zero.
- Year detail: 2019 SPY-above-open n=0 (no inference); 2020 n=4, 0 targets / 4 stops and −1.346% net; 2021 n=6, 1 target / 5 stops and −0.969% net. These are descriptive, not extra selection gates.
- **Predeclared 10:30–noon ET subset** (entry index >=12, same rules): 14 total fills, 5 targets; above-open SPY **4 entries, 0 targets, -1.273% net / fill**; at/below-open SPY **10 entries, 5 targets, 0.251% net / fill**. Too few for a high-probability strategy claim.

## Why this does NOT contradict Hanna or Grimes

- **Rob Hanna** measures **extreme capitulation breadth** among large-cap stocks, with CBI exit tied to breadth normalization. He explicitly acknowledges the indicator is early sometimes, and that price may decline before the rebound. SPY's previous 5m close relative to the same day's opening price is NOT his CBI or NYSE closing-TICK oscillator, nor a measure of breadth or exhaustion.
  - [Hanna, original Capitulative Breadth Indicator (2008)](https://quantifiableedges.com/my-capitulative-breadth-indicator/)
- **Adam Grimes** describes an actual prior **pivot or support/resistance zone**, then a brief break and quick recovery, but writes that valid failure tests can lose, and highlights context (trading ranges or countertrend extremes) and risk control. This experiment approximates prior support with mechanical double-pivot rules and tests only very specific fixed stock exits; it is not his full trading program.
  - [Grimes, The Failure Test (2014)](https://www.adamhgrimes.com/failure-test-2/)
- SPY being below its morning OPEN includes **both stocks in falling markets and those in markets already climbing back from the morning low**. This particular binary does not actually detect a reversal in SPY, much less true market-wide capitulation.
- No option bid-ask spread, DTE, delta, theta, IV/crush, contract liquidity, or $50 premium affordability were measured. Modeled stock profits do not imply executable positive call-option expectancy.

## Data limitations and decision

- Incompleteness concentrated partly in the 2020 crash period and 2019; strict 78 M5 per session requirement excludes some severe volatility regimes. 198 candidate events, 174 complete, only 28 fills. Stock universe was selected from later-available 2023 stock data, and the entire general failure-test idea was exposed in prior tests. Calendar disjointness is narrower than truly independent validation of all research choices.
- 10 up/18 down SPY comparison is insufficient to claim any new 80% probability edge, and a near-zero mean among 18 down-SPY trades is not option-profitable once options spreads/time decay are considered. Do not pivot to an SPY-red-only scanner based on this result.
- **Do not change scanners or automated tasks**. Reject "SPY currently above the open" as a reliable positive confirmation for this exact failed-breakdown setup.
- A new genuinely differentiated test must match a creator's original claim: either (i) **Grimes trading range / uptrend pullback and genuine swing pivot**, or (ii) **Hanna broad selloff exhaustion (breadth, TICK) with longer, prespecified exit timing**. Predefine exactly one, freeze a genuinely unused cohort, and evaluate its own declared risk and holding period, with affordable option execution separately. Do not optimize new threshold based on 2019–2021 trade outcomes.

Machine-readable event records: [Full per-stock entry, SPY classification, trade outcomes and clustered bootstraps](data/grimes_marketcontext_2019_2021_spy_recovery_v1_results_2026_10_11.json).
