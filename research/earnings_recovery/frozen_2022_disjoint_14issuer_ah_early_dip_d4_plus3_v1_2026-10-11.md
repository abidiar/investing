# FROZEN BEFORE PRICE-OUTCOME READ: 2022 New-Issuer AH Early Second Low / Day-Four +3% Study
**Date:** 2026-10-11. **Type:** historical time-and-issuer disjoint replication pilot, sources/roster selected before retrieving any 2022 D0 or trade outcome OHLC for the specified cohort.

## Prior work and rationale
Reviewed research/RESEARCH_GOVERNANCE.md and research/PRIOR_WORK_REVIEW_STANDARD.md. Existing prior work in research/prior_work/earnings_near_bottom_asof_low_retest_limit_2026-10-11.md and research/prior_work/after_hours_delayed_selling_stabilization_prior_work_2026-10-11.md; prior research outcomes: research/earnings_recovery/asof_near_low_limit_ah_v1_findings_2026-10-11.md. Unconfirmed retrospective 2023–2026 hypothesis: a further lower low by D3 following the first >=5% earnings-reaction close may predict a quick +3% target before -5% stop if stock bought D4 open (38/54 target, gross mean +0.568%, post-hypothetical-20bp +0.368%). Prior 54 early-dip opportunities across 28 distinct tickers were outcome-inspected and should not be re-used as unseen validation. This new test uses 2022 reports in **14 completely different issuers** from the earlier 61-company panel, with exact release dates and after-close times sourced BEFORE price outcomes. The S&P 500 current-member (2026) universe and issuer selection biases remain.

## Event roster (FROZEN)
- A: 2022-02-22, 2022-05-24, 2022-08-16, 2022-11-21 (https://quant500.com/earnings-date/A)
- ALGN: 2022-02-02, 2022-04-27, 2022-07-27, 2022-10-26 (https://quant500.com/earnings-date/ALGN)
- AVGO: 2022-03-03, 2022-09-01, 2022-12-08 (https://quant500.com/earnings-date/AVGO)
- CDNS: 2022-02-22, 2022-04-25, 2022-07-25, 2022-10-24 (https://quant500.com/earnings-date/CDNS)
- DECK: 2022-02-03, 2022-05-19, 2022-07-28, 2022-10-27 (https://quant500.com/earnings-date/DECK)
- EBAY: 2022-02-23, 2022-05-04, 2022-08-03, 2022-11-02 (https://quant500.com/earnings-date/EBAY)
- EXPE: 2022-05-02, 2022-08-04, 2022-11-03 (https://quant500.com/earnings-date/EXPE)
- FICO: 2022-01-27, 2022-04-27, 2022-08-03, 2022-11-09 (https://quant500.com/earnings-date/FICO)
- JBHT: 2022-01-18, 2022-04-18, 2022-07-19, 2022-10-18 (https://quant500.com/earnings-date/JBHT)
- LYV: 2022-02-23, 2022-05-05, 2022-08-04, 2022-11-03 (https://quant500.com/earnings-date/LYV)
- MU: 2022-03-29, 2022-06-30, 2022-09-29, 2022-12-21 (https://quant500.com/earnings-date/MU)
- ORCL: 2022-03-10, 2022-06-13, 2022-09-12, 2022-12-12 (https://quant500.com/earnings-date/ORCL)
- TTWO: 2022-02-07, 2022-05-16, 2022-08-08, 2022-11-07 (https://quant500.com/earnings-date/TTWO)
- WDAY: 2022-02-28, 2022-05-26, 2022-08-25, 2022-11-29 (https://quant500.com/earnings-date/WDAY)

**Total 54 AH announcements**, all from 2022 as shown on Quant500's SEC Form 8-K linked calendar, after-close release sessions. AVGO 2022-05-26 was BMO, excluded before outcomes. No posthoc addition/removal of tickers or dates. Quant500 8-K acceptance stamps can lag actual issuer release; in this cohort after-close classification is verified per historical row; raw timestamps stored in source URL rather than fabricated precise moment of press release.

## Price-event definitions and planned data
From connected Webull free historical daily RTH **adjusted OHLC** with 1,200 bars per ticker ending 2026-10-09, and SPY if accessible; split/dividend considerations recorded. For each AH announcement date E:
- Let P0 be RTH closing price ON earnings-announcement date (before after-hours release).
- Let reaction sessions R1 and R2 be next 1st and 2nd RTH sessions.
- If R1 CLOSE <=0.95*P0, set event reaction D0=R1. Else if R2 CLOSE <=0.95*P0, set D0=R2. Else **NOT QUALIFIED**; keep in full `54` announcement count but exclude from conditioned trade results. No intraday-only -5% substitution or using more days for D0; do not infer earnings causality.
- Initial after-hours -5% selloff population includes both market/industry-associated declines, as in prior cohort, but no added selection by future event path.
- D1...D3 are 3 TRADING sessions after qualifying D0. Known early dip if min LOW(D1..D3) < LOW(D0), objectively knowable at D3 CLOSE.
- If early dip: Buy D4 OPEN unconditionally, including gaps, and calculate +3% profit-target / -5% stop for next 20 entry-inclusive RTH stock sessions. Opening gap stop/target goes at actual OPEN; ambiguous simultaneous touches within same OHLC bar count STOP before target. If no touch, close day20. Hypothetical fixed 20 basis points ROUNDTRIP cost deducted from trade P&L. Every eligible event has a resulting filled stock market order (unless price feed missing). No favorable intraday minimum assumed as an actual fill.
- Secondary D6 OPEN after early dip, same risk/holding rules (fair paired comparison); universal D4 OPEN for all >=5% events, compare early dip vs no dip and all-event per-qualified-opportunity P&L (skips=0). NO change to +3, -5, 20 or entry day after outcomes.
- Report first subsequent fresh low below original D0 intraday LOW (D1..D10), day of lowest LOW among D1..D5 (hindsight descriptive only), number of D0 at R1/R2, first low day after announcement, whether day-four has already exceeded selloff reference.
- SPY market benchmark: if SPY OHLC actually retrieved, compute SPY same-entry D4 as 20-session return (holding timeline aligned); *no* custom beta or optimizing relative strength. Do not use SPY for filtering trade entries.

## Predeclared evaluation and verdicts
Primary two margins: entry target-first fraction on early-secondary-low cases; COST-ADJUSTED mean stock return per early-secondary-low entry. Baseline exact risk model D6 after dip on same events. Compare to initial previously seen 54-event result and different-issuer/2022 subcohort: note regime differences and sector/membership survivorship.
- If >=12 qualifying >=5% selloffs AND >=8 objective D1–D3 secondary low events, classify result **DIRECTIONALLY CONSISTENT** only if new 2022 stock gross/net mean >0 and D4 >D6 on matched early-low events; otherwise **FAILED REPLICATION** if clear inconsistent point estimates, or INCONCLUSIVE if too few.
- Even directional consistency is not formal deployment evidence: >=30 newly disjoint eligible cases and ticker-resampled uncertainty excluding zero are needed for stronger validation; actual options asks/bids required for trading signal endorsement.
- Save all `54` events, including unqualified, no early low, and failures. Never tweak before leaving repo result. No paid data, no options P&L assumed, no A+ or scanner modifications.

**Source and known limitation:** this fixed 14-issuer source is a new historical sample, but contemporaneous accounting quality is NOT revalidated point-in-time. The earlier 91 AH cohort was selected by historical quality screen, and this new cohort is NOT quality-matched; interpret any disagreement as either sample difference or invalidated generality, not a definitive falsification of the conditional quality hypothesis. Historical Webull adjusted values are source convention and split/cash corporate actions may affect exact OHLC comparability.
