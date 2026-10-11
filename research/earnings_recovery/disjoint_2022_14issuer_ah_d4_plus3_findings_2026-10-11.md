# NEW-ISSUER 2022 replication: after-hours early secondary low, day-four +3% rebound
Dated 2026-10-11. **VERDICT: INCONCLUSIVE / DIRECTIONAL FAILURE on only 7 eligible opportunities, does NOT validate the early +3% trading edge.** All precommitted 54 after-hours announcements, 14 new issuer symbols with no intersection with previously studied 61-company 2023–26 universe. Date/time checked from SEC 8-K-linked Quant500. The full date roster and fixed rules were COMMITTED BEFORE Webull OHLC for these events was read.

Protocol: `frozen_2022_disjoint_14issuer_ah_early_dip_d4_plus3_v1_2026-10-11.md`.
Original exact results: `disjoint_2022_14issuer_ah_d4_plus3_replication_result_2026-10-11.json`.
Source Webull data windows: `disjoint_2022_14issuer_ah_earnings_rth_source_windows_2026-10-11.json`.
Runner: `run_2022_disjoint_AH_D4_plus3_replication.mjs`.

## Procedure
After each fixed 2022 AH release: first closing selloff >=5% versus earnings-day close on either next (R1) or second (R2) trading session defines D0. Require a further observed LOW below D0 low on at least one D1–D3, known by the completion of D3. Market-enter D4 OPEN. Target +3% underlying stock high versus stop −5% underlying low from the purchase price; 20 entry-inclusive trading-day window, conservative stop-first same-bar and opening gap fill at open, 20bp illustrative roundtrip stock cost. No outcome of these 2022 stocks was used to revise the thresholds from the original 2023–2026 discovery result. Broker source daily bars are (adjusted) and stock-only. The companies' point-in-time QUALITY screens were NOT reverified and are not interchangeable with older quality cohort.

## Frozen result
- **54 AH earnings reports** (14 different issuers), 14/14 historic Webull stock series accessible with 1200 daily OHLC bars each, ending 2026-10-09 and spanning back to Dec 2021.
- **13/54** first- or second-session >=5% closing selloffs; other 41 didn't enter this post-reaction strategy population.
- **7/13** made secondary fresh low by D3; D4 open buy -> **4 +3% target first, 3 −5% stop first**, zero timeouts. Gross mean **−0.42857%**, illustrative net mean **−0.62857%** per entered trade.
- D6 open on same seven: three targets, four stops, net mean **−1.77143%**. Paired D4 minus D6 gross **+1.14286 percentage points**: waiting to D6 was worse here, but choosing D4 did not produce positive expectancy.
- D4 open in other six >=5% selloffs with NO extra lower low D1–D3: **1 +3% target vs 5 stops**, net mean **−4.0530%**; buying ALL 13 qualified afterhours shocks on D4: 5 targets /8 stops, net mean −2.2091%. This suggests the dip filter may have distinguished relative outcomes IN THIS SMALL PANEL but still didn't earn money with +3/-5 stock barriers.
- Early-dip selected H1 2022 **4/5 targets, net +1.2%**; H2 2022 **0/2 targets, net −5.2%**; small and unstable.
- Qualifying initial selloff identities: ALGN 2022-04-27 and 2022-10-26; CDNS 2022-10-24; DECK 2022-02-03; EBAY 2022-05-04 and 2022-08-03; EXPE 2022-05-02; LYV 2022-05-05 and 2022-11-03; MU 2022-03-29; ORCL 2022-09-12; TTWO 2022-11-07; WDAY 2022-05-26. Include all cases, not only hits.

## Judgment
In the earlier 2023–26 quality-qualified AH cohort, D4 +3/-5 after a secondary lower low worked 38/54 and produced +0.368% hypothetical after-stock-cost mean. In this 2022 issuer-and-time-disjoint sample, only four of seven targets were hit; net was -0.629%. The predeclared minimum sample 8 failed, so classify **INCONCLUSIVE / unfavorable point estimate**, not a formal FAILED REPLICATION nor a successful validation. It is strong enough to prevent promoting the simplistic D4 rule to the call radar. Even +3% stock trade targets can lose due to 5% losses and the narrow gross advantage, and are not comparable to option marks.

## Next scientific operation (NO MORE THRESHOLD MINING)
To distinguish temporary overshoot from continuing earnings drift, obtain **at least 30 additional objective AH secondary-low events in an independently predefined multi-year broad issuer panel with point-in-time accounting quality**, and compare fixed D4/D6 +3/-5 stock first-passage net outcomes, against sector/SPY-relative controls if historical bars permit. If and only if stock expectation is stable, obtain option-tradeable historical matched ask/bid for cheap, actually listed calls. An independent price-only result in one relatively bearish year cannot settle the quality-conditional claim. No paid data, no A+ scanner change, no DTE instruction.
