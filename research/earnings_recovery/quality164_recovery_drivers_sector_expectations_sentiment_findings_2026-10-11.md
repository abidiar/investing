# What makes quality companies rebound after earnings? 164-case pre-D4 sector/sentiment proxy audit
Date: 2026-10-11. **VERDICT: ONE EXPLORATORY COMPANY-VS-SECTOR SHOCK DISCRIMINATOR; NO VERIFIED D4 OPTIONS STRATEGY OR CAUSAL BUYER-MOTIVATION RESULT.**
This is the first broad ETF sector proxy test of **all 164** saved quality-screened earnings reactions, frozen definition before ETF data fetched or comparisons computed (see `frozen_quality164_sector_market_preD4_recovery_factors_2026-10-11.md`). The stock outcomes themselves were historically seen on several occasions and the same issuers repeat, so results are NOT independent discovery.

## Why stocks recover — published mechanisms
The core economic split is **(A) future cash-flow expectations being less impaired/improving, (B) reduced discount rate/risk premium including stock/sector market tailwinds and (C) temporary liquidity-driven selling/behavioral sentiment pressure unwinding**. These overlap. Da, Liu and Schaumburg's peer-reviewed *A Closer Look at the Short-Term Return Reversal*, *Management Science* (2014) https://doi.org/10.1287/mnsc.2013.1766 is especially relevant: price changes NOT linked to earnings forecast revisions or industry/fundamental exposures were more likely to reverse, consistent with long-side LIQUIDITY selling pressure; much closer to the user's causal question than RSI/day4 candles, but not D4 earnings + $50 call validation. Federal Reserve Bank of NY report https://www.newyorkfed.org/research/staff_reports/sr513.html.
Noh & Zhou 2022 *Executives' blaming external factors...*, *Journal of Banking & Finance* https://www.sciencedirect.com/science/article/pii/S0378426621003095 finds negative management blame language predicts NEGATIVE nonreversing return and analyst downgrades. Price et al 2012 JBF conference call textual tone https://www.sciencedirect.com/science/article/pii/S0378426611002901 predicts subsequent returns, especially unscripted Q&A. Analyst revisions vs price fundamental expectation data do exist in research but remain unavailable AS-OF for these 2023–26 cases through current no-fee connections (Webull latest-only, Quartr requires Pro).

## New auditable matching
Universe 164 dated quality PASSED selloff events 2023–June2026 (61 current companies, original92+separate72, AH91+BMO73). All 164 mapped to ONE coarse frozen sector ETF (XLK/XLC/XLY/XLP/XLE/XLF/XLV/XLI/XLB), plus SPY. Webull US ETF daily RTH 1200 bars from 2021-12-29 through 2026-10-09 archived with original date-closes at `frozen_source_spdr_sector_etf_daily_1200_2026-10-11.json`. ZERO missing ETF observations. **Historical sector ETF proxies are not perfect sector peer groups** (company classifications can change, ETF weights include issuer, broad sector is not subindustry, no separate PE/beta changes). Historical company daily OHLC from archive. Only earliest D0→D3 close and 20 sessions PRIOR ETF returns are features known before entry D4. Sector D0→D60 is AFTER THE FACT ONLY, not signal.

Outcomes:
(1) Full preearnings-price closing recovery at any close within D60: 86/164 recovered, 78 did not;
(2) Buying stock D4 open, +3% before -5% stop within 20 RTH bars at 20bp hypothetical cost: 99/164 targets, 65 stops/timeouts, hypothetical all164 net -0.312% per trade. These are not option returns. 
PreD4 explanatory inputs: sector ETF prior20 return, SPY prior20 return, sector ETF and SPY return D0→D3, sector-SPY D0→D3, STOCK-sector D0→D3, and INITIAL stock earnings shock relative to sector ETF shock over exact same pre-announcement-close→D0-close window. No RSI/MA/residual estimates requiring actual analyst revisions. Long run sector D60 returns observational only.

## What separated recoverers from nonrecoverers? (ALL 164, unpaired)
| Pre-D4 observable, median | FullD60 yes (n86) | FullD60 no (n78) |
| Sector performance in prior 20 RTH sessions | +2.05% | +2.24% |
| Sector return D0→D3 | +0.51% | +0.52% |
| Sector return minus SPY D0→D3 | -0.05pp | -0.19pp |
| Stock minus same-sector return D0→D3 | **+0.75pp** | **-1.67pp** |
| ORIGINAL earnings stock shock MINUS same sector shock, pre-earnings→D0 | **-6.63pp** | **-8.37pp** |

This suggests successful recoveries tended to endure LESS uniquely issuer-specific damage relative to their sector, while initial sector trend strength alone looks near-identical. Do NOT infer investors bought because of this difference; the dataset records prices, not actual investor motives.

**AH91 ONLY**, D60 recovered 51/nonrecovered40:
- median initial stock shock minus sector shock **-6.98pp vs -8.73pp**, respectively;
- D0→D3 stock minus sector **+0.71pp vs -1.68pp**;
- D0→D3 sector performance itself +0.625% vs +0.641% (essentially indistinguishable);
- pre20 sector trend +1.78% vs +2.87% (no 'must be rising sector' indication).
The D4 short-stock target outcome after AH91 was 58 target vs 33 stopped/timedout; winning D4 trades' median initial shock-minus-sector -6.86pp vs losers -8.52pp, BUT their D0→D3 stock-minus-sector median -1.19pp vs +0.15pp, OPPOSITE of the long-horizon recovery signal. **What predicts full recovery is not necessarily what optimizes D4 entry timing.**

## Matched winner failure results controlling event year + AH/BMO + same sector + comparable initial decline (<=5pp), different ticker, one control per pair
- FULL D60 recovery matched 34 pairs (20 AH): median winner-minus-failure ORIGINAL stock shock relative sector **+2.51 percentage points**, less idiosyncratic negative reaction in **26/34** pairs, exploratory two-sided paired sign p=0.00294 uncorrected. In AH-only 20 pairs: 16/20 same direction, median difference +3.10pp, uncorrected p=.0118. However **17/20 AH full-recovery pairs are XLK technology**, so not representative of all sectors.
- This is *NOT* independent proof: Original issuer group 19/23 full-recovery pairs show this direction but different-company group only 7/11 (p~0.55), not consistent in genuinely separate issuer control group. By YEAR median shock difference corresponding to recoverers vs failures goes in correct direction in 2023, 2024, 2025 but **REVERSES in 2026** (-7.28pp recoverers vs -5.74pp failures). Multiple comparisons and repeated ticker/event clustering add false positives.
- D4 +3% before -5% 20-session STOCK trade: matched 43 pairs (25 AH), winners had initial shock less negative vs same sector in 30/43, median +1.19pp (raw sign p=.0137); AH 18/25, median +1.63pp (raw p=.0433). BUT D3 sector momentum and D3 stock-relative-to-sector did NOT distinguish D4 outcomes after exact matching (AH stock minus sector winner>loser only 12/25). Long-run first-hit win is still NEGATIVE mean net unconditionally. Do not promote.
- Other PRE-D4 sector tailwind and momentum matched differences not consistent; exact tests over many related factor × outcome definitions are multiple-tested and not independent causal identification.

## What changed DURING the actual recovery? (FUTURE, NOT DAY3 INFORMATION)
- Earlier SPY decomposition: among 86 fully recovered events, 76/86 SPY rose by first recovery, median SPY +3.02%, median stock+8.76%, 80/86 stock outperformed SPY at that *selected* recovery date, about 10/86 recovered with SPY down/flat. Market tailwind common but not necessary.
- Sector ETF D0→D60 **median +9.25%** for those that EVENTUALLY fully recovered vs **+0.66%** among unrecovered, within all 164. For AH D60 recoveries, sector ETF median **+11.37%**, unrecovered **+4.22%**. That is large evidence of a **coincident future sector rally** that may contribute to repricing but is NOT at all usable to choose a D4 call (sector returns through day60 are not known on day3). Sector ETF and stock holdings correlate; the fullD60 outcome is selected on subsequent stock gains. Cannot infer specific buyer motivation.
- Prior market/SPY results held in `quality164_recovery_market_attribution_exploratory_2026-10-11.json` (164 exact matched; no missing).

## Evidence grading by requested factor
| Factor family | What we have | Status |
| Published-pre-earnings QUALITY, revenue YoY, debt/equity, TTM FCF/net income | Exact historic numeric only 72; matched 25/27 pairs previous experiment, effects weak/opposite or not replicated | NOT supported as stable discriminator |
| Dated FY1 analyst EPS consensus REVISION S0→D3 | unavailable historical free from Webull; explicitly unknown; no re-use current EPS as past | HIGHEST causal value / NOT TESTED |
| Change in investor/manager *tone* vs prior call Q&A | prior call and current historical transcripts inaccessible on Quartr without paid pro | Not measured; published academic association |
| Sector prior20 and D0→D3 strength/tailwind | All164 connected ETFs; indistinguishable pre-D4 | Not a robust early discriminator |
| Degree of INITIAL issuer-specific SELLING vs sector index | All164, matched 34/43, AH 20/25, weakly rep by year/holdout | MOST INTERESTING exploratory price-only clue; not verified |
| Stock *relative strength* vs sector D0→D3 | All164 full D60 recoveries show some separation; 20 AH matched pairs only 12 favorable; AH D4 matched 12/25 | Cannot be a validated entry criterion |
| Future MARKET and sector recovery | all164, sector large positive for future recoverers, 76/86 SPY up by recovery | Accompanies recovery, not known by D3 |
| Insider buying, institutions, order imbalance, forced flows | SEC Form4 possible timestamped, actual historical order flows missing | Not measured and cannot be assumed |
| Contract ask/bid IV theta/expiry D4 | old small partial option datasets, no comprehensive executable contracts | No evidence options trade works |

## New decision model we SHOULD eventually test (NOT a rule today)
"Bad initial STOCK print *relative to its industry* with nonpersistent/unchanged expected future PROFITS and evidence selling pressure is dissipating" might be the actual premium rebound hypothesis. But our current study found **less issuer-specific initial downside**, not necessarily the **most severe residual** being best—a contrary caution against blindly selecting the most oversold relative to sector. If the sector also sold off materially, some absolute company decline could be sector-driven and later unwind. A downward initial price minus sector is NOT necessarily nonfundamental, as EPS shock not measured.
Next scientifically strongest event test is updated analyst estimates as-of SAME future fiscal period or strict original outlook execution vs prior expectations, *plus* same-industry year matched controls and time-stamped sentiment / filings for early selling pressure; sample all newly unseen historical companies or prospective events. The printed feature must improve D4 stock firsthit after fees vs full existing baseline AND prospective stock/option ask-to-bid, issuer cluster, years. Do not optimize sector initial-shock -7pp thresholds on these 164 seen outcomes; NO new live scanner or alerts.
## Reproducibility
- Prior lit `research/prior_work/earnings_recovery_causal_mechanisms_sector_spy_residual_literature_2026-10-11.md`.
- Frozen v1 `research/earnings_recovery/frozen_quality164_sector_market_preD4_recovery_factors_2026-10-11.md`.
- Exact source 1200 bars × 10 ETF `research/earnings_recovery/frozen_source_spdr_sector_etf_daily_1200_2026-10-11.json`.
- Deterministic original issuer+ETF row script `research/earnings_recovery/run_quality164_asofD3_sector_market_v1.mjs`.
- All 164 prices / features and exact matched pairs `research/earnings_recovery/quality164_asofD3_sector_market_factors_fullmatched_results_2026-10-11.json`.
- AH/issuer/year sensitivity `research/earnings_recovery/quality164_sector_match_ah_cohort_sensitivity_2026-10-11.json`.
- This document `research/earnings_recovery/quality164_recovery_drivers_sector_expectations_sentiment_findings_2026-10-11.md`.
