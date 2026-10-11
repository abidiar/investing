# Completed AH earnings NEW-disclosure vs rebound pilot & independent published research
Date: 2026-10-11. **VERDICT: RELEASE-ONLY PROXY NOT SUPPORTED; PRE/POST EXPECTATION REVISIONS + MANAGEMENT CALL TONE CHANGE CANNOT BE TESTED WITH PRESENT FREE HISTORICAL DATA.** No scanner or options alert change.

## User's specific decision hypothesis
Can a trader on/around fourth trading day after a **quality company** drops >=5% following AFTER-HOURS earnings, buy a profitable CALL because the stock's decline was EXCESSIVE RELATIVE TO newly disclosed negative future outlook, whereas bleak manager tone or genuinely lowered FY/next-quarter earnings expectations predicts continuing declines? 
This requires SAME future fiscal period point-in-time analyst revisions, prior quarter same firm call-transcript baseline, accounting forecasts, market/sector neutral price reaction, historical option asks/bids/IV and stop-first stock/contract outcome. Broadly plausible, but not equivalent to testing release positive/negative wording.

## Published research — others HAVE tested specific parts
- **Liu & Ziebart (1999), J Empirical Finance**, https://www.sciencedirect.com/science/article/pii/S0927539899000122 : most bad annual management forecast price reaction was reversed within 60 days; unfavorable QUARTERLY forecast rebound could occur around the NEXT quarterly earnings announcement. Big mismatch to profitable D4 calls.
- **Das, Kim & Patro (2012), J Business Finance & Accounting**, https://doi.org/10.1111/j.1468-5957.2012.02298.x : abnormal UPWARD subsequent drift following bad AND good quarterly management forecasts, initial negative-price-reaction inversely linked to later drift for bad forecasts; estimated-cost-aware profits. Closest underlying overreaction mechanism, not AH 5% screened+second dip+D4 stock stop/option.
- **Druz, Petzev, Wagner & Zeckhauser (2020), Financial Analysts Journal**, https://rpc.cfainstitute.org/research/financial-analysts-journal/2020/0015198x-2019-1707592 : BLEAK change in call tone versus own prior quarter predicts lower earnings, higher uncertainty, future negative price drift after other news. CFA summary 100,000 calls 2003–16; next quarter consensus average declines 1.85% per SD managerial presentation bleakness; subsequent negative drift vs matched stocks; monthly long-short risk-adjusted returns, NOT early reversal calls.
- **Livnat & Mendenhall (2006), J Accounting Research**, https://doi.org/10.1111/j.1475-679X.2006.00196.x : drift stronger with surprise against ANALYST expectations than modeled time-series, reinforcing *relative surprise* need.
- Review: `research/prior_work/precise_ah_earnings_negative_news_rebound_versus_continuation_literature_2026-10-11.md` updated with primary published verified sources; NO research located jointly establishes the user's full cheap D4 call method.

## Our completed frozen test (N=12 issuer releases, 6 matched AH event pairs)
Source `ah_6matched_pairs_12_original_release_news_coding_v1_2026-10-11.json` used original company-issued original earnings releases/SEC 8-K dated to announcement. Records PREVIOUSLY reviewed and outcomes EXPOSED. Matched winner/control roster fixed earlier in `matched_quality164_fundamentals_v1_all_events_pairs_2026-10-11.json`, company-different, same release session AH and event year, >=5% initial decline within 5 percentage point magnitude tolerance. Six simulated +3%-before−5% D4 opening STOCK target winner vs 5 -5% stops + one timeout. Not options data. 
Frozen simple binary comparisons BEFORE computing exact paired tables, `frozen_ah_original_release_6pair_forward_impairment_contrast_v1_2026-10-11.md`; executable `run_ah_6pair_original_release_disclosure_contrast_v1.mjs`; event/pair result `ah_6pair_frozen_release_disclosure_contrast_results_2026-10-11.json`.

| Precommitted press-release flag | D4 winners n6 | D4 nonwinners n6 | Discordant matched pairs | Favored no-impairment hypothesis | Two-sided exact p |
|---|---:|---:|---:|---:|---:|
| Explicit negative customer demand | 2 | 1 | 3 | only 1 / 3 | 1.0 |
| Specific material external operating constraint | 2 | 1 | 3 | only 1 / 3 | 1.0 |
| Same-FY financial guidance reaffirmed (negative control) | 1 | 1 | 2 | no difference | 1.0 |
| One-time transaction/charge | 2 | 2 | 4 | no difference | 1.0 |

Because only 3 or 4 discordant pairs vs predeclared >=5 needed, **NO confirmed directional effect and NO matched trade strategy support**. Release 'absent' means ABSENT IN REVIEWED ORIGINAL RELEASE, NOT absent from fuller call Q&A. 
Real failure examples from published original sources:
- **FTNT Nov5 2025 (STOP)** reported +14% revenue, +14% billings and record GAAP/adjusted margins. https://fortinet.gcs-web.com/news-releases/news-release-details/fortinet-reports-third-quarter-2025-financial-results/
- **CPRT May22 2025 (STOP)** +7.5% sales, +7.7% EPS YoY https://www.sec.gov/Archives/edgar/data/900075/000162828025027262/cprt4302025ex99-1.htm
- **MPWR Oct30 2025 (STOP)** Q3 revenue $737.2m versus original July31 quarter guide $710-730m (+0.99% above upper), while Q4 future guide 730-750m flatish to Q3; modest actual guidance beat cannot rescue short D4 entry. https://www.sec.gov/Archives/edgar/data/1280452/000143774925032411/ex_854756.htm and previous original quarter https://www.sec.gov/Archives/edgar/data/1280452/000143774925024185/ex_815329.htm
- **LEN Dec18 2024 (STOP)** NEW home orders 16,895 versus previous guidance floor 19,000 (-11.08%), management newly admitted miss and margin contraction https://investors.lennar.com/press-releases/2024/12-18-2024-213041323.
Counterexamples:
- **AMAT Aug14 2025 (TARGET)** explicit NEW warning of sequential Q4 revenue decline and near-term China weakness, yet achieved early +3% stock target https://investors.appliedmaterials.com/news-releases/news-release-details/applied-materials-announces-third-quarter-2025-results/
- **LEN June16 2025 (TARGET)** clear mortgage/demand concerns but reports quarterly new orders within previous guidance; trade won https://investors.lennar.com/press-releases/2025/06-16-2025-224524472
- ONEOK April29 (TARGET) and Aug4 2025 (STOP) BOTH affirm FY guidance: additional negative control that full-year maintenance on its own not enough. Primary SEC earnings exhibits in JSON.
**Initial committed result BUG**: incorrectly accessed snake_case keys, all flag totals zero. The result JSON and deterministic Node runner have been corrected against camelCase source fields; no thresholds, roster, outcomes or original codes changed. Erratum explicitly preserved.

## What this test DOES NOT measure
- Original published negative news was not normalized against contemporaneous market EXPECTATIONS; reported +14% YoY is not necessarily a POSITIVE EPS surprise.
- Historical original call-to-call managerial tone change from Q&A not measured: Quartr Pro subscription required (confirmed for all seven relevant issuer queries); no cheaper connected full archived transcript feed confirmed.
- Same-period PRE AH analyst forward consensus vs as-of end D3 EPS snapshots unavailable from Webull current estimates and rate-limited TipRanks; only two retrospective *partial* numeric prior guidance vs actual comparisons among 12 reliable (MPWR surprise BEAT +0.99% upper, LEN surprise MISS -11.1% lower), insufficient to infer distribution.
- 12 cases / 6 pairs already outcome inspected; industry mismatch and calendar-month differences, no statistical power, and historical stock price surrogate not executable options.
- Existing 72 panel management binary guidance study already found no profitable D3 +5/-5 benefit with only 27 classifiable; DON'T run same proxy again or count UNKNOWN as maintained.

## Research judgment and next single priority
**Release-only binary features failed this exploratory matched-pair falsification.** The genuinely novel deeper hypothesis remains TESTABILITY BLOCKED, not refuted: measure *change in manager's call tone versus its own prior call* and *forward analyst future EPS expectation revision prior release → D3*, plus negative price reaction sector-adjusted. We should not keep mining six cases for new adjectives until something 'works'. Given historical free feed limitations and prior outcome exposure, genuinely **prospective as-of earnings archive** is scientifically efficient: store issuer release, BEFORE/AH same-period guidance baseline, call transcript if available free, estimated FY/next-quarter EPS before and after if free, SPY/sector, D4 trade and actual option quotes in a chronological freeze; no after-the-fact exclusions. Until sufficient coverage, emphasize actual quantitative SAME-PERIOD management operational guidance miss/beat as *coverage pilot*, not validated factor. Broaden to >=30 matched independent AH issuer/quarter cases; note may take many earnings quarters. No paid subscriptions without user approval.
No scanner, automatic $50 calls, or new user task on this evidence.
