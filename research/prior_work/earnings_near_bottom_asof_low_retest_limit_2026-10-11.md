# Prior-work review — as-of secondary-low reference buys after earnings selloffs
2026-10-11; NEW hypothesis after comparing original 164-event research and academic evidence.

## Question before protocol freeze
A rebound from an ultimate trough is arithmetically profitable *if bought near that trough*, but can a trader place a known-price order near an **already observed** post-earnings lower low, rather than wait for late candle confirmations and chase? Crucial neglected axes: fill coverage, bottom proximity, partial +3% bounce rather than full pre-earnings reclaim, and downside-before-upside. Buying a historical lowest low in hindsight is not executable.

## Existing internal evidence — do not re-test as though unknown
- `research/earnings_recovery/after_hours_delayed_dip_recovery_diagnostic_2026-10-11.md`: 62/91 AH selloffs made a fresh lower low within D1–D5; 42 subsequently hit +5% vs initial selloff close D6–D60. This is descriptive and selection-biased; a future ultimate low is not known by entry.
- `research/earnings_recovery/ah_delayed_secondary_dip_oneday_stabilization_v0_1_findings_2026-10-11.md`: single subsequent higher-low + higher-close trigger filled 28/91 AH events with -0.146% mean gross stock return, and underperformed fixed day six by -1.159 pp on paired 28 events. Late confirmation + >4% chase cap left 63/91 without executed entries.
- `research/earnings_recovery/actionable_bounce_results_164events_2026-10-10.md`: broad unqualified next-open, day3, SMA5, 3 rising lows cannot establish stable advantage; the fixed day6 all-event mean flipped sign by company-disjoint groups.
- `research/earnings_recovery/affordable_otm_tradebar_pilot_results_2026-10-10.md` and `free_100event_2024_2025_otm_options_results_2026-10-10.md`: low-cost OTM options are possible in isolated examples but quote coverage and as-of bid/ask timing severely deficient; an underlying +5% bounce can still result in option losses, so no call ROI assumption permitted.
- `research/earnings_recovery/forward_guidance_proxy_results_2026-10-10.md`: 72-event guidance classification too incomplete to demonstrate entry edge; no valid historical FY1 sellside revisions. Don't re-test with guessed revisions.

## External prior work and measurement issues
- Lehalle and Mounjid (2017), *Limit Order Strategic Placement with Adverse Selection Risk and the Role of Latency* (Market Microstructure and Liquidity). https://doi.org/10.1142/S2382626617500095; limit buyers face a higher probability of a fill exactly when sellers possess reason to send price further down. Improve execution price vs market order only at the expense of skipped upside and adverse selection. Thus explicitly preserve fill/non-fill and all-event expectancy.
- Chordia et al. (2009), *Liquidity and the Post-Earnings-Announcement Drift* (Financial Analysts Journal) https://rpc.cfainstitute.org/research/financial-analysts-journal/2009/liquidity-and-the-post-earnings-announcement-drift; execution costs absorb much published PEAD paper returns in illiquid segments. Daily low touches do not prove real limit order queue fill; negative result can't be made positive by ignoring fees.
- Fink (2021), *A Review of the Post-Earnings-Announcement Drift* https://doi.org/10.1016/j.jbef.2020.100446; drift can continue in direction of negative fundamental surprise. Extra selling may be rational revaluation, not panic overshoot.
- Options Industry Council (October 2026) https://www.optionseducation.org/news/september-office-hours-faqs-volatility-crush%2C-assignment-risk-and-vertical-spreads ; IV crush may offset directional call gains. The present test is explicitly underlying-only.

## Gap and proposed single new test
After a verified AH >=5% initial selloff, a *second* lower low observed within first THREE full postreaction RTH days sets a real-time reference. On D3 close, a single GTC-style BUY limit within +1% of the already observed D1–D3 low during D4–D6 can buy a retest rather than paying for late confirmation. Exact one configuration vs D4/D6 same-event opening baselines; profit target +3% and stop -5%, 20 entry-inclusive days, with cautious intraday ambiguity. All source data already outcome-exposed, so exploratory only, no new A+ call recommendations. This is a test of **entry method and fill selection**, not a duplicate of prior candle or volume screens.

## Contradictions/limitations
- Low risk-reward of +3% vs -5% needs >62.5% target-first rate without timeouts and costs. Mere event hit rate without sequence is insufficient.
- Concomitant future earnings/market movements, adjusted OHLC vs raw exchange quote, dividend/split effects, current-stock-universe survivorship bias, AH event timestamp verification, bid/ask and passive order priority uncertainty.
- Only supported as exploratory inference even if positive. If this fails, do NOT tweak fill tolerance/holding target on the same known cases; instead test genuinely new issuer/quarter events with option data.
