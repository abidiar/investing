# Opening-aware multi-session support undercut/reclaim — frozen 2025 historical pilot
Run: October 13, 2026 · Protocol commit `c08dc4ce983455232c4212df55596072f32734d2` **before** 2025 Webull outcome pulls.
**Verdict: no demonstrated long-stock trading edge and no cheap-call edge; do not update scanners or trade these rules.**

## Research question
Can the **second genuine undercut** of support (vs a near-touch), and the combination of **shallower second penetration plus weaker volume relative to the SAME 5min time of day**, predict an early, tradable +2% move before −1%? A previous June–October 2026 pilot yielded 1/6 targets and could not measure the pressure condition due incomplete opening-bar reference. New dates May 1–September 30 **2025**, 60 different prespecified stock symbols, with preformed support dated prior to first/second tests. The raw 5-minute bar data are Webull RTH as-traded, not daily adjusted bars.

## Sample and frozen outcomes
One preset ticker, **FI**, caused Webull `INVALID_SYMBOL` for whole batch, excluded without replacement (first error archived); 59 others obtained. 30 backward pages of stock M5 history (10 each for 20/19/20 ticker groups) with 706,907 timestamp-unique bars. Fetch end Oct 1 2025 and at least Mar 10 2025 lookback. Entries at next opening five-minute bar after reclaim by noon. Bar-by-bar through end of next complete RTH session: +2% target first or −1% stop first, if both STOP first; gap at open price; timeouts at last D+1 5-minute close. Roundtrip stock costs **50bp** (hypothetical, not actual quotes); no option prices/IV/bid-ask spreads.

| Predeclared cohort | Trades | +2 FIRST | −1 FIRST | Timeouts | Target-first% | Average gross stock% | Average net stock% @50bps |
|---|---:|---:|---:|---:|---:|---:|---:|
| ALL second undercut/reclaims | 25 | 4 | 11 | 10 | **16.00** | +0.0866 | **−0.4134** |
| 2nd depth >=20% shallower and improvement >=0.10 percentage points | 9 | 1 | 5 | 3 | 11.11 | −0.1389 | −0.6389 |
| Probe M5 relative volume second <=80% of first | 9 | 1 | 5 | 3 | 11.11 | −0.1849 | −0.6849 |
| BOTH depth and lower relative volume | 5 | 0 | 4 | 1 | **0.00** | −0.5958 | **−1.0958** |
| Neither combined condition (19 measured) | 19 | 3 | 7 | 9 | 15.79 | +0.1655 | −0.3345 |
| Probe candle close in top 35% of candle range | 14 | 3 | 6 | 5 | 21.43 | +0.2002 | −0.2998 |
| Entry **10:30–12:00 ET** | 4 | 1 | 0 | 3 | 25.00 | +1.1136 | +0.6136 |
| All pre-10:30 | 21 | 3 | 11 | 7 | 14.29 | −0.1090 | −0.6090 |

All stats denominator is completed, qualifying entries, not all opportunities. Exactly one of 25 baseline trades lacked a full time-matched 20-session pre-retest volume measure; it remains in baseline and is excluded from complete-pressure comparisons. All other 24 have volume features. The 10:30–noon subset's +0.61% net is **only 4 entries**, three timeouts and one target; selecting that as a new edge would be unjustified. There are **17 issuers** in the 25 entries; AMGN contributes four and multiple names have repeated trades, so observations are dependent. Wilson 95% target-rate interval for baseline [6.40%,34.65%] is a simple binomial approximation (does not adjust for ticker correlation). Ticker-cluster bootstrap mean net 95% interval (12k deterministic draws) **[−0.8242%, +0.0061%]**; includes zero at top and does not certify true expectancy. In particular the strategy is nowhere close to demonstrating 80% target-first.

## Outcome distribution / date audit
2025 May 4 events 0 target; June 4 events 0; July 1 target/1 event; **August zero qualifying events**; September 16 events/3 target. Heavy September skew limits external validity.

The conservative `full-session` check required >=75 bars, opening 09:30 bar and closing 15:55 bar, for **every** session D-35..D+1. This excludes historical 2025-07-03 half-day and many other days with missing 5m source bars; over the 59 names only 3,672 issuer-date opportunities reached this full-coverage gate before any support/probe rules. Outcome sample is therefore NOT representative of all May–Sep 2025 days. Group1 provider bars had markedly more isolated incomplete sessions than groups2–3. Nine candidate days in group3 were excluded under predeclared >25% session-open gap split/source-continuity gate. No excluded dates were called stopped trades. No point-in-time, full-company corporate action/ex-dividend certification was completed.

### Audit correction: full 20-day volume denominator
Initial generated results calculated 5-minute time-of-day median from preceding **20 chronological sessions**, which could include incomplete sessions. The preregistered definition requires preceding **20 FULL sessions**. We retrieved the 17 qualifying issuers' complete histories AGAIN and recalculated every first and second probe ratio from the 20 preceding complete RTH days; saved all dates/volumes. **The fixed correction changed ZERO binary lower-volume or BOTH classifications**, and thus all tabulated outcome counts and means above are unchanged. The post-correction full-row source is the authoritative version; prior first-pass group files remain separately as transparency.
Probe relative volume is NOT signed net-selling pressure; a lower five-minute volume value can mean less activity from both buyers and sellers. Candle close location is price-action proxy, not measured aggressive buy orders.

## Operational interpretation
The opening-aware design solved the original opening-bar proxy coverage problem (24/25 measured) but **did NOT improve stock-target hit frequency** or yield positive mean net stock expectancy under these exact frozen rules. Much of the apparent 'higher low and declining probe activity' pattern can precede a failed rebound. The narrow ~4-event preferred entry subgroup does not justify changing scan hours or CALL rules. This is retrospective and partially issuer/period-outcome overlapping with other investing research; new distinct sample and legitimate level-vs-shifted-level controls are mandatory before strong causal claims. No $50 option-chain tradability, quotes/IV, bid/ask or slippage certification; no A+ scanner upgrade. Do not retune cutoffs after exposure.

**Next genuinely discriminating test:** predeclare *genuine historically established levels* vs matched shifted/fake support levels, holding sector/volatility and every entry/exit rule fixed, and use a **fresh issuer-year** and complete source quality. This addresses Adam Grimes's level authenticity question rather than piling on filters that failed. Require statistical and costs robustness before promotion.

## Files / reproducibility
- [Frozen protocol](frozen_opening_aware_support_retest_2025_60stock_2026_10_13.md)
- [Authoritative corrected per-event 20-full-session baseline and group outcomes](data/opening_aware_2025_corrected_20fullsession_volume_2026_10_13.json)
- [First pass multi-stock aggregate, including issuer-date and bootstrap summaries](data/opening_aware_2025_59stock_aggregate_2026_10_13.json)
- [Group 1 source QA / event measures](data/opening_aware_2025_group01_2026_10_13.json)
- [Group 2 valid19 source QA / event measures](data/opening_aware_2025_group02_valid19_2026_10_13.json)
- [Group 2 FI invalid-symbol first attempt](data/opening_aware_2025_group02_2026_10_13.json)
- [Group 3 source QA / event measures](data/opening_aware_2025_group03_2026_10_13.json)

Each event trace stores support formation lows, test dates, probe prices, volume reference values, and modeled entry/exit prices. Full ~707k raw OHLCV bar corpus was retrieved and calculated but **not persisted verbatim** to GitHub; re-running from Webull is needed to regenerate every 5-minute path. Outcome algorithm was executed directly during analysis; no claim that an independently tested executable script exists.
