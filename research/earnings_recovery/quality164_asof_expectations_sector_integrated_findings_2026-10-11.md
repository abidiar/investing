# 164-event expectations-versus-sector audit, source coverage and winner/failure comparisons
Date: 2026-10-11. VERDICT: RESEARCH-ONLY / NO VALIDATED EARLY REBOUND OR OPTIONS EDGE.

## Scope and immutable prior studies
Existing frozen design: research/earnings_recovery/frozen_catalyst_mechanism_matched_study_v1_2026-10-11.md .
Prior work: research/earnings_recovery/forward_guidance_proxy_results_2026-10-10.md and research/earnings_recovery/ah_original_release_vs_continuation_six_pair_test_findings_2026-10-11.md .
Integrated machine rows 164/164: research/earnings_recovery/quality164_asof_expectations_sector_integrated_coverage_2026-10-11.json .
Runner: research/earnings_recovery/run_quality164_asof_expectations_sector_coverage_v1.mjs .
Original quantitative prior/current source checks: research/earnings_recovery/ah_12_original_release_quant_management_surprises_inputs_2026-10-11.json .
All stock event outcomes already known when the source coding began, none of this is an independent trading experiment. No paid data.

## Coverage
- All 164 stock event and D4 +3-before-5, 20 session managed stock outcome, D60 closing full recovery, archived as-of-D3 SPY and mapped ETF source histories: 164/164.
- Older 72-event manual guidance audit: 72 reviewed but only 27 publicly comparable full-FY issuer EPS/revenue guidance changes (45 UNKNOWN). The original92 had no such audit. These 27 form an exposed nonrandom subset.
- Earlier original company earnings-release narratives for preselected six AH D4 matched pairs: 12/164 (six winners / six failures), plus 3 Dell = 15/164 total exact original release narratives. The 27 previously coded and 15 original-source groups do not overlap in exact event membership, so at most 42/164 have at least one sourced fundamental feature, NOT necessarily same full-year comparable numerical forecast.
- New same-quarter issuer forecast midpoint vs reported ACTUAL numerics: 6/12 in preselected release matched cases (3 D4 winners, 3 nonwinners); 6 unmeasured remain UNKNOWN.
- SAME FY numeric management EPS changes: 3/164 (Dell Nov2024 and Aug2025, Fortinet Nov2025), all of which D4 stopped but two full D60 recovered. Dell Feb2025 first FY26 guide $9.30 cannot be compared to any previously issued FY26 guidance, so not a FY26 revision.
- Genuine pre/post earnings same-fiscal-period Street consensus FY1 EPS snapshots: 0/164. Pre-earnings Street gross-margin consensus surprise: only Dell Aug25 1/164. Do not treat absences as zeros.

## A. Full 164 EVENT versus sector repricing (re-used earlier results, not a new independent effect)
| Median as-of D3 feature | FULL closing-price recovery by D60 (n86) | DID NOT fully recover D60 (n78) |
|---|---:|---:|
| Initial Dell/stock reaction minus sector ETF on reaction day | -6.632pp | -8.372pp |
| Stock return D0-to-D3 minus sector contemporaneous return | +0.752pp | -1.671pp |
| Sector ETF D0-to-D3 | +0.511% | +0.519% |
| LATER sector ETF D0-to-D60: FUTURE LOOKAHEAD, not an early trading signal | +9.255% | +0.657% |

The early sector ETF return itself is essentially equal in eventual winners/failures. Stock-specific early shock differs somewhat, but prior same-sector matched sector test direction failed replication across separate companies and 2026. Future sector returns often coincide with rebounds but CANNOT be known at D3 or assigned causal direction.
For the 99 D4 short stock +3 before -5 targets versus the 65 D4 losses/timeouts, the initial stock minus sector median shock is -7.04 vs -7.69pp and D0-to-D3 stock-relative-to-sector -0.68 vs -0.96pp; insufficiently separative and mean all164 hypothetical D4 net -0.312%.

## B. SAME FY issuer full-year guidance measured in old 72 subgroup, NOW joined to frozen D4 outcomes
DO NOT mistake the earlier study's D3-entry +5/-5 outcome for the new combined D4-entry +3/-5 result below. All numbers from same 27 previously reviewed source outcomes, exploratory cross-file join.

| Prior management FY guidance label | N classified | D4 +3 target before -5 stop | Hyp D4 net mean (20bp roundtrip modeled stock cost) | 60d FIRST FULL price recovery |
|---|---:|---:|---:|---:|
| STABLE_OR_UP EPS/revenue | 23 | 8 | -1.782% | 11 |
| DOWN | 3 | 2 | +0.515% | 0 |
| MIXED | 1 | 1 | +2.800% | 0 |

EPS-only direction in the 27: EPS UP n9, D4 target4, modeled net -0.980%, full D60 recovery5. EPS STABLE n14, D4 target4, net -2.298%, full D60 recovery6. EPS DOWN n4, D4 target3, net +1.086%, full D60 recovery ZERO. The DOWN n4 is far too small and issuer/market dependent to assert negative guidance helps early trades. It does demonstrate decisively why improving FY earnings expectations is not SUFFICIENT for an early managed D4 rebound.

By label EPS UP versus STABLE versus DOWN, median initial stock shock minus sector was -8.13 / -7.10 / -11.49pp respectively. Strong negative firm-specific shock in DOWN can coexist with several small later bounces that first hit +3 before -5; that does not make calls profitable.

## C. NEW quantitative prior same-quarter management-guidance midpoint vs actual: 6 of 12 selected matched earnings releases
These 12 were frozen as six AH D4 winners vs 6 AH nonwinners matched YEAR and initial selloff, NOT matched by same sector or exact date; comparing technology, housing, energy, mining and industrials is confounded. 6/12 have verified historical numerics; equal 3 winner / 3 nonwinner.

| Dated earnings and D4 outcome | Prior SAME QUARTER management forecast vs newly reported earnings-day ACTUAL |
|---|---|
| AMAT May15 2025, WIN | Q2 revenue $7.10B vs $7.10B, zero surprise; nonGAAP EPS $2.30 vs $2.39 +3.91%; nonGAAP gross margin 48.4% vs 49.2%, +0.8pp |
| AMAT Aug14 2025, WIN | Q3 revenue $7.20B vs $7.30B, +1.39%; nonGAAP EPS $2.35 vs $2.48, +5.53%; nonGAAP gross margin 48.3% vs 48.9%, +0.6pp; separate Q4 sales forecast showed sequential weakness |
| LEN Jun16 2025, WIN | New orders midpoint 23,000 vs 22,601, -1.73% but within 22,500–23,500 stated guidance; deliveries 20,000 vs 20,131 +0.66%; adjusted homebuilding gross margin about 18% and 18% in line |
| LEN Dec18 2024, FAIL | New orders midpoint 19,150 vs 16,895 -11.78%, and -11.08% BELOW previously forecast minimum 19,000; homebuilding gross margin previously expected flat with Q3 22.5%, actual 22.1%, -0.4pp |
| MPWR Oct30 2025, FAIL | Q3 revenue guidance midpoint $720M, actual $737.2M +2.39%; GAAP gross margin 55.2% guidance midpoint vs 55.1% actual -0.1pp; nonGAAP gross margin 55.5% vs 55.5% in line; Q4 guidance flattening forward demand |
| FTNT Nov05 2025, FAIL | Q3 revenue midpoint $1.70B vs $1.72B +1.18%; billings midpoint $1.80B vs $1.81B +0.56%; nonGAAP operating margin midpoint 33.0% vs 36.9% +3.9pp; FY25 nonGAAP EPS company outlook raised $2.50 to $2.68, +7.2%. Despite positive surprises, D4 first hit STOP, although D60 full closing price recovery was YES |

Original source pairs: AMAT first prior Feb13 SEC https://www.sec.gov/Archives/edgar/data/6951/000000695125000005/exhibit991q12025earningsre.htm with May15 https://www.sec.gov/Archives/edgar/data/6951/000000695125000017/exhibit991q22025earningsre.htm ; next AMAT May15 -> Aug14 https://www.sec.gov/Archives/edgar/data/6951/000000695125000032/exhibit991q32025earningsre.htm .
LEN Sept19 2024 original https://investors.lennar.com/press-releases/2024/09-19-2024-213050023 vs Dec18 https://investors.lennar.com/press-releases/2024/12-18-2024-213041323 ; LEN March20 2025 https://investors.lennar.com/press-releases/2025/03-20-2025-210025354 vs June16 https://investors.lennar.com/press-releases/2025/06-16-2025-224524472 .
MPWR prior July31 https://www.globenewswire.com/news-release/2025/07/31/3125370/0/en/monolithic-power-systems-provides-earnings-commentary-for-the-quarter-ended-june-30-2025.html vs Oct30 https://www.sec.gov/Archives/edgar/data/1280452/000143774925032411/ex_854756.htm .
FTNT Aug06 https://investor.fortinet.com/news-releases/news-release-details/fortinet-reports-second-quarter-2025-financial-results/ vs Nov05 https://fortinet.gcs-web.com/news-releases/news-release-details/fortinet-reports-third-quarter-2025-financial-results/ .

The 6 nonnumeric events are OKE 2, CPRT 3, NEM 1; annual non-EPS or maintained outlook exists but truly comparable prior-quarter figures for target metric not newly verified here. REMAIN UNKNOWN.
The observations are objective but HETEROGENEOUS (EPS, gross margin, revenue, new orders, billings). They cannot be collapsed into a one-variable statistical win rate, and outcome labels were all seen before coding. Prior company guidance is NOT prior analyst consensus or post-report FY1 EPS forecast change. Margin YoY is not a surprise. No naked claim of causal buy motivation.

## D. What survived and what failed
Positive quarterly margin/EPS surprises can coexist with early D4 winners (AMAT twice) or failures (FTNT and MPWR). Strongly negative order surprise plus negative margin surprise coincided with LEN Dec24 early and long failure. LEN June25 had softer homebuilding orders yet won D4 and full D60: company order strength not just sign. Previous management guidance FY EPS up did not fix D4 entries (9 raised EPS n4 target; modeled negative mean). A FY forecast rise can be less than analyst consensus, and expense/margin deterioration or CEO comments can shift valuation down.
More than half of 164 events had some full recovery, future sector rally may contribute to risk-premium repricing, but not preknown. No verified institutional/passive flows, option ask/bid, or historical FY1 actual analyst revised forecasts.
No production changes and no subscription spend.

## NEXT predefined falsification / records
Source-code original earnings releases and PRIOR same-period margin/EPS/orders guidance for the remainder of 164, paying attention to 91 AH and same issuer winners/failures. Archive published timestamp by D3; if historical street forecasts unavailable mark UNKNOWN. Preserve all 164 events and match by year, release time, sector, event selloff magnitude and repeat issuer; no new threshold optimization and no claim a new independent 2023-26 holdout. A truly NEW issuer/quarter blinded validation with >=30 adequate events, and subsequent actual option NBBO ask-to-bid costs, is necessary to promote. Prior unvalidated studies not reset.
