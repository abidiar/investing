# Dell 3 earnings-selloff case audit: dated catalysts, buyer evidence, and as-of limitations
Date: 2026-10-11
VERDICT: RETROSPECTIVE MECHANISM DISCOVERY / NO CAUSALLY VERIFIED BUYER OR OPTIONS ENTRY EDGE.
Preceding source review: research/prior_work/dell_catalysts_buyer_mechanisms_prior_review_2026-10-11.md .
Future systematic frozen design (NOT YET EXECUTED): research/earnings_recovery/frozen_catalyst_mechanism_matched_study_v1_2026-10-11.md .
This descriptive forensic review occurred AFTER event outcomes exposed. It is NOT an outcome-blinded or new statistical backtest.

## Data lineage and convention
Source: existing archived 164 events JSON matched_quality164_fundamentals_v1_all_events_pairs_2026-10-11.json (DELL three rows), stock bars actionable_bounce_price_windows_92events_2026-10-10.json (same archive), sector matching quality164_asofD3_sector_market_factors_fullmatched_results_2026-10-11.json. No new bars or options data reconstructed.
D0 is saved first >=5% qualifying reaction-day CLOSE. Crucial Feb 2025: after Feb27 AH report, actual first next session is Feb28 but original archive's D0 qualifying shock is Mar03, not Feb28. D4 is four trading sessions after archived D0. 'Full recovery' first CLOSE >= close ON THE ACTUAL earnings-release session (not necessarily the day preceding D0). 'D60' 60 sessions after archived D0. Price values adjusted/as provided historical archive, not executable options.
D4: +3% price before -5% stop through 20 sessions, historical hypothetical 20bps roundtrip cost; stock-only. Existing model picks stop first where same bar touches both; gaps modeled at open.

## Three complete outcomes
| Earnings AH | Archived reaction D0 | initial % | D3 public-knowledge cutoff 16:00 ET | D4 model | First full closing rec | D60 vs preearn close | SPY D0->D60 | XLK D0->D60 |
|---|---|---:|---|---|---|---:|---:|---:|
| 2024-11-26 | 2024-11-27 | -12.25% | 2024-12-03 | 2024-12-04 entry $121.897, STOP 2024-12-10, -5.20% hypothetical after stock costs | None by D60 | -23.62% | -1.97% | -3.72% |
| 2025-02-27 | 2025-03-03 | -11.38% | 2025-03-06 | 2025-03-07 entry $89.618, TARGET 2025-03-12 +3.01% hypothetical after stock costs | 2025-05-13 (D50) | +6.19% | +0.98% | +5.93% |
| 2025-08-28 | 2025-08-29 | -8.88% | 2025-09-04 | 2025-09-05 entry $125.649, GAP STOP 2025-09-09 -5.21% hypothetical after stock costs | 2025-09-22 (D15) | -4.76% | +3.96% | +6.71% |

February 2025 has long path not a smooth or sustained recovery: low on 2025-04-07 $64.730 (approx -38.56% from $105.364 earnings day close); 2025-05-13 first full recovered close; stock D4 +3% exit March12 precedes both trough and later tariff truce. August first closing full recovery 2025-09-22 but by D60 2025-11-24 -4.76% again. November first D60 not restored. DELL after 2025 August D4 stop and fullD60 recovery illustrates wrong horizon for early call.

## Nov 2024 (FAIL): known before D4 vs hindsight
- Nov26 original SEC 8K https://www.sec.gov/Archives/edgar/data/1571996/000157199624000130/dell-20241126.htm : Q3 revenue +10% to $24.4b and nonGAAP EPS $2.15, but below consensus on revenue; legacy PC consumer demand and weaker-than-expected subsequent quarterly revenue guidance. Analysts discussed delayed AI server deployments ahead of NVIDIA Blackwell ramp. Published before Nov27 and Dec04 D4.
- Nov27 date-stamped analyst revisions both signs: Melius price target $140->$155 and Barclays $106->$115; Citi $160->$156, Mizuho $155->$150; https://www.benzinga.com/24/11/42221770/these-analysts-revise-their-forecasts-on-dell-after-q3-results . Existing ratings/revised price targets did NOT deliver D60 recovery.
- Jan21 2025 Stargate $500b prospective AI buildout announcement https://openai.com/index/announcing-the-stargate-project/ ; Dell NOT among named initial funding/equity participants nor initial tech partners, broad tech sentiment, LATER THAN D4 AND still failure D60.
- SEC 10-K published Mar25 2025 https://investors.delltechnologies.com/sec-filings/all-sec-filings/content/0001571996-25-000034/dell-20250131.htm retrospectively reveals 2.2 million repurchased Nov30-Dec27, 3.2m Dec28-Jan31, notwithstanding decline. These realized figures NOT public at Dec03 cutoff and not a preregistered early signal. It is concrete counterexample to buybacks-guarantee-recovery.
- D0–D60 XLK -3.72%, SPY -1.97% RETROSPECTIVE sector/macro context; could be contributory but cannot be known at D3.

## Feb 2025 (RECOVER): multiple mechanisms on DIFFERENT dates
- Feb27 original report https://www.sec.gov/Archives/edgar/data/1571996/000157199625000014/exhibit991earnings8kq4fy25.htm : FY25 revenue $95.6b up8%, FY26 annual revenue guidance growth 8%, nonGAAP diluted EPS guidance +14%; dividend +18%, new $10b share repurchase AUTHORIZATION, FY AI server narrative and prior backlog. All known pre D4. Contradictory near-term margin pressure (projected lower gross margin rate) and AI infrastructure competition; forecasts and guidance not same as historical analyst EPS revisions.
- Mar12 earlier modeled +3% stock target exits BEFORE new March18 GTC news, and before tariff truce. Therefore those future announcements cannot explain D4 March07->12 modeled stock win.
- Mar18 Dell NVIDIA AI Factory new products and adoption http https://www.dell.com/en-us/dt/corporate/newsroom/announcements/detailpage.press-releases~usa~2025~03~corp.htm ; context for medium-term customer demand but no verified incremental forward margin expansion.
- April 2 tariff shock and Apr07 low, subsequent market repricing with May12 USA–China tariffs truce (Reuters https://www.reuters.com/world/china/us-stock-futures-jump-us-china-trade-stand-off-thaws-2025-05-12/ ), Dell first preearn close regain May13. Macro timing strong association, not company-specific causal proof; May12 NEVER day3 information.
- SEC June10 2025 10Q https://investors.delltechnologies.com/sec-filings/all-sec-filings/content/0001571996-25-000063/dell-20250502.htm : actual 6.3m share buybacks March01-28, 12.7m March29-May02, 22.1m during Feb01-May02. Disclosure AFTER pre D4 and May13 recovery, cannot use purchases quantity ex ante; demonstrates issuer buying in failing early drawdown and late rebound.

## Aug 2025 (RECOVER FULL D15, early D4 STOP):
- Aug28 Dell original https://investors.delltechnologies.com/news-releases/news-release-details/dell-technologies-delivers-second-quarter-fiscal-2026-financial : revenue $29.8b +19%, server/networking +69%, $8.2b Q2 AI shipments, $5.6b Q2 new AI orders, backlog ~$11.7b, FY26 AI shipments raised $15b->$20b; Q2 cash flow from operations $2.5b, Q2 shareholder return repurchases+dividend $1.3b. All disclosed earnings day, known before D4. NOTE $20b updated guidance already priced/known by D4, not new Sep post-D4 catalyst.
- Aug29 Reuters morning https://www.reuters.com/business/dell-slides-after-weak-margins-eclipse-upbeat-full-year-forecast-2025-08-29/ adjusted gross margins 18.7% vs expected 19.6%, Q3 EPS guidance $2.45 vs $2.55 est and costs, competition, weak profit conversion.
- Aug29 10:37 ET https://www.schaeffersresearch.com/content/news/2025/08/29/dell-stock-struggles-as-ai-push-weighs-on-outlook at least nine sellside price target INCREASES despite −10% share fall and 15/20 buy ratings pre-event. Mixed management outlook, analyst target optimism both known by Sep04 D3. These DID NOT prevent Sep09 D4 stop. Analyst PRICE TARGETS are NOT same fiscal-period FY1 EPS consensus revisions, which remain UNKNOWN historically.
- Sep22 2025 original OpenAI/NVIDIA partnership (letter of intent, future NVIDIA data centers and up-to $100b NVIDIA investment) https://openai.com/index/openai-nvidia-systems-partnership/ coincides Dell first full closing-price recovery; market AI-risk-on is plausible, no new DELL contract named, publication day only not intraday event study. Source not public by Sep04 D3; must NOT be an early entry feature.
- SEC Dec9 2025 https://investors.delltechnologies.com/sec-filings/all-sec-filings/content/0001571996-25-000127/dell-20251031.htm retrospectively showed Dell 2.8m shares repurchased Aug30-Sep26 avg ~$129.53, including period of 09/22 full recovery; LATE public evidence, NOT known D4 and purchases dates cannot be localized inside period. This is concrete buyback participation but causal fraction unidentifiable.
- Sector XLK +6.71% and SPY +3.96% over later 60 sessions (future, never ex-ante).

## Trump's role explicitly checked
- 2024-25 3 earnings windows: NO VERIFIED Trump post/direct public endorsement of Dell on an identified timestamp that can be tied causally to stock recovery. The May12 2025 Trump-admin China tariff reprieve is important *macro*, near Feb25 eventual May13 recovery, far later than D4. Jan21 2025 AI Stargate White House-linked program did NOT name Dell partner and could not rescue Nov24 60d.
- 2026 DIFFERENT PERIOD: Fortune dated July07 2026 https://fortune.com/2026/07/07/presidents-cannot-pick-winners-white-house-ethics-lawyer-trump-dell/ gives public Trump praise/endorsements Feb19, May08, July06 2026; also May27 2026 Department of Defense up-to-$9.7b five-year licensing contract (ceiling NOT guaranteed revenue). Not relevant to past 2024–25 events. Claims from secondary journalism require original remarks/doc and timestamp if conducting 2026 new separate event study; same-day price move isn't attribution.
- Prospective Trump/post catalyst class remains a *hypothesis* requiring a specific named statement, actual public time, peers and counterfactual. Do not conflate 2026 political Trump Accounts fundraising with 2025 earnings rebounds.

## Observed buyers / known vs unknown
- VERIFIED issuer repurchases occurred across winners and failure. Authorization size first known Feb27 2025; exact retrospective future quarter buyback amounts only SEC date. No 5m issuer tape labeled 'buyback buyer', no causal proof.
- AMBIGUOUS institutional: 13F delayed quarterly positions are not fresh buys and changes may reflect rebalances/valuation; no transaction-level historical accumulating fund verified for 2024-25 three windows. High ownership and 401k contributions do NOT certify Dell-specific inflows. Passive index creations/rebalancing need dated constituent weights, index flow, vehicle subscriptions, derivative hedges, cross trades; unmeasured.
- Insider open-market BUY evidence not verified at Form4 accepted by the respective D3 cutoffs; unknown, not zero.
- Price/volume OHLC and raw five-minute total candle volume are NOT signed trade imbalance and cannot establish buyer identity.

## Retrospective Dell within-issuer sector comparison
| Event | initial stock shock minus XLK D0 (pp) KNOWN | stock minus XLK D0->D3 (pp) KNOWN | future XLK D0->D60 (RETRO only) |
|Nov2024| -10.893 | -1.305 | -3.725%|
|Feb2025| -9.618 | -1.172 | +5.934%|
|Aug2025| -7.343 | +3.628 | +6.713%|
The direction coincides with recovery: less issuer-specific initial damage, then much stronger FUTURE tech-sector gains. N=3 already selected, observational and same-market exposures; not independent validation. December 2024 preD4 XLK was strong +2.25% D0-D3 even though Dell still failed: immediate sector bounce by itself is not sufficient. Negative initial sector-shock signals had inconsistent disjoint-cohort and 2026 signs in previous full 164 study.

## Verdict and next concrete test
1. SUPPORTED facts: new vs old earnings outlook can conflict; Dell actual repurchases existed during winners AND failure; positive sellside targets existed during winners AND failure; systemic macro regime and technology demand later differed. No proof any flow CAUSED price reversal. Side note full-recovery definition marks first touch, not durable profit.
2. RESEARCH-ONLY mechanism most plausible: transient issuer earnings repricing of lower projected current-quarter profit against fairly durable AI demand; large systematic TECH/discount-rate changes; capital-return buying may add marginal demand but cannot prevent a decline.
3. Most valuable NEXT *not previously proven*: original earnings surprise measured relative to PRE-EARNINGS SAME PERIOD expectation and actual recent gross margin/operating profit trend, corroborated by date-stamped NEW firm orders and only AS-OF analyst forecast revision if truly accessible. Distinguish margin dilution temporary fulfillment costs from permanent impaired margins, using matched unsuccessful cases.
4. Second: quantify same-issuer winner-failure XLK/SPY idiosyncratic D0 shock and PRE-D4 macro context already archived, without future sector as predictor; no threshold tuning on exposed 164.
5. Repurchases disclosure: as-of authorization + stated capital-return policy vs NONPREDICTIVE hindsight actual amounts; inspect buyback influence only if daily legal publication date can be sourced. Passive and pensions low priority without historical issuer-specific flow.
6. See separately frozen pre-registration; NO quantitative outcome test of all 164 newly run here, no trading change, no options recommendation, no subscription or paid feeds.
