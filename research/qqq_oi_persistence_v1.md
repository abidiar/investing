# Investing OS Research — QQQ OI Persistence v1.0

Status: COMPLETED — NOT PROMOTED
Frozen: 2026-09-19
Completed: 2026-09-19

## Question
Does settled contract-level QQQ open-interest change, especially relative to same-contract trading volume, add next-session information beyond price alone?

## Data discipline
- Instrument: QQQ options and QQQ underlying price.
- Snapshot Day T may predict only the next trading session T+1.
- Never treat settled OI as intraday/same-day information.
- Only compare sequential snapshots when the prior snapshot is the immediately preceding available trading-session snapshot; missing-session gaps are excluded from persistence-ratio tests.
- Raw OI, delta OI, and put/call labels are not assumed to reveal buyer/seller direction.

## Frozen contract universe
- Expiration DTE: 1–30 calendar days from snapshot date.
- Moneyness: strike within +/-3.0% of Day-T QQQ close.
- Calls and puts retained separately and combined.
- Exclude rows with missing OI; treat missing/blank volume as zero only for descriptive raw counts, but exclude zero-total-volume aggregates from persistence-ratio calculations.

## Frozen features
For each matched contract between T-1 and T:
- delta_OI = OI_T - OI_T-1
- OI_BUILD = max(delta_OI, 0)
- OI_UNWIND = max(-delta_OI, 0)

Aggregate by session and side:
- CALL_BUILD, PUT_BUILD, TOTAL_BUILD
- CALL_UNWIND, PUT_UNWIND, TOTAL_UNWIND
- CALL_VOLUME, PUT_VOLUME, TOTAL_VOLUME
- CALL_PERSISTENCE = CALL_BUILD / CALL_VOLUME
- PUT_PERSISTENCE = PUT_BUILD / PUT_VOLUME
- TOTAL_PERSISTENCE = TOTAL_BUILD / TOTAL_VOLUME
- BUILD_IMBALANCE = (CALL_BUILD - PUT_BUILD) / (CALL_BUILD + PUT_BUILD), when denominator > 0

No ratio clipping or outcome-driven winsorization in this pass. Obvious source-data impossibilities are reported rather than silently repaired.

## Frozen price baseline
- Day-T price direction = sign of QQQ open-to-close return.
- Meaningful Day-T move = |open-to-close| >= 0.25%, retained from Dealer Structure v1.0 for consistency.

## Primary hypotheses
H1 — Persistence / movement, non-directional:
Higher TOTAL_PERSISTENCE is associated with larger next-session absolute close-to-close movement and/or larger high-low range. Primary statistic: Spearman rank correlation.

H2 — Raw option-side buildup is not reliably directional:
BUILD_IMBALANCE should not be promoted unless it shows stable association with next-session signed return and survives basic robustness checks.

H3 — Price-conditioned continuation:
Among sessions with |Day-T open-to-close| >= 0.25%, test whether TOTAL_PERSISTENCE improves the probability/magnitude of next-session continuation in the already-established Day-T price direction.

## Secondary descriptive cuts — exploratory only
- 1–7 DTE vs 8–30 DTE
- calls vs puts
- ordinary sessions vs monthly/quarterly OPEX where sample size permits
- persistence above/below the eligible-sample median for readable continuation tables; median split is descriptive and is not a scanner threshold.

## Outcomes
- T+1 close-to-close return
- absolute T+1 close-to-close return
- T+1 high-low range / Day-T close
- T+1 opening gap
- T+1 open-to-close return
- same-direction T+1 continuation after a meaningful Day-T move

## Data
Daily QQQ chain snapshots from `oceanyang2024/qqq-option`, with strike, type, daily volume, settled open interest and IV. Underlying outcomes use independent QQQ daily bars.

Eligible sample:
- 162 sequential-snapshot sessions
- 2026-01-21 through 2026-09-15
- median 612 matched 1–30DTE near-spot contracts per session
- no TOTAL_PERSISTENCE observations above 1.0, so no clipping/data repair was needed

## Results
### H1 — persistence did NOT predict larger next-session moves
1–30DTE TOTAL_PERSISTENCE:
- vs next absolute close-to-close move: Spearman rho = -0.060, p = 0.446, n = 162
- vs next high-low range: rho = -0.084, p = 0.289, n = 162

The result remained weak/negative in both frozen DTE sub-buckets:
- 1–7D: rho = -0.110 for absolute move; -0.099 for range
- 8–30D: rho = -0.009 for absolute move; -0.087 for range

Above-median persistence sessions had average next absolute move 1.01% vs 1.07% at/below median. There was no amplification edge.

### H2 — call-vs-put buildup imbalance had essentially zero directional information
- BUILD_IMBALANCE vs next signed close-to-close return: rho = 0.006, p = 0.944, n = 162
- 1–7D and 8–30D results were likewise approximately zero.

This strongly supports the rule that raw call/put OI buildup must not be interpreted as bullish/bearish without buyer/seller identity and price confirmation.

### H3 — persistence did NOT improve continuation after an already meaningful price move
Among Day-T moves of at least 0.25%:
- above-median persistence: n=63, continuation 53.97%, average next absolute move 1.01%
- at/below-median persistence: n=64, continuation 57.81%, average next absolute move 1.08%

The higher-persistence group was not better.

### Exploratory side result
Call persistence showed a small inverse relationship with subsequent movement:
- call persistence vs next absolute move: rho = -0.168, p = 0.032
- call persistence vs next range: rho = -0.151, p = 0.055
Put persistence was effectively zero on both metrics.

This was not a primary predeclared hypothesis, so it is NOT promoted. It may motivate a separate frozen falsification if desired.

### OPEX descriptive cut
- ordinary sessions: n=127, average next absolute move 1.07%, range 1.52%
- monthly-OPEX-week sessions: n=35, average next absolute move 0.95%, range 1.40%
- mean persistence was virtually identical (0.107 vs 0.106)

## Verdict
NOT SUPPORTED / NOT PROMOTED.

The Reddit-style idea that a larger share of same-day option volume surviving as net new OI should, by itself, predict a larger next-day move did not survive this frozen 162-session test. Call-vs-put OI buildup imbalance also supplied no directional edge.

## Scanner impact
Do NOT add TOTAL_PERSISTENCE, CALL/PUT BUILD_IMBALANCE, or raw delta-OI as Strength, Runway, R:R, directional, or continuation inputs.

They may remain visible for research/context, but they receive no action authority.

Dealer-gamma regime from the separate Pass-1 study remains the more promising options-structure concept because it addresses hedging behavior rather than treating OI buildup as directional intent.

## Reproducibility
- Runner: `research/run_qqq_oi_persistence.py`
- Workflow: `.github/workflows/qqq-oi-persistence.yml`
- Full results: `research/results/qqq_oi_persistence_v1_results.md`
- Session panel: `research/results/qqq_oi_persistence_v1_session_panel.csv`
- Statistical tests: `research/results/qqq_oi_persistence_v1_tests.csv`

## Do Not Re-Test Unless
- a materially different data source supplies buyer/seller or dealer-side identity;
- a genuinely new frozen construction is proposed (for example gamma-weighted concentration rather than raw OI persistence);
- an untouched out-of-sample period is added for replication of a separately frozen hypothesis.
