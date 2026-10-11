# After-hours earnings selloff: additional 1–5-day dip, then recovery (October 11, 2026)

**Status: DESCRIPTIVE, POST-HOC, RESEARCH-ONLY.** This diagnostic corrects a mismatch in prior research framing: the user describes a multi-day post-earnings secondary selloff followed by an eventual multi-day recovery, **not** an immediate 09:35 earnings-day reversal. No entry rule was preregistered or validated in this exercise; no options quotes/premiums were examined, and no Investing OS scanner change is authorized.

## Sources (previously archived, no new stock-price acquisition)
- `actionable_bounce_price_windows_92events_2026-10-10.json` (92 original quality-qualified earnings selloff events)
- `actionable_bounce_price_windows_72events_2026-10-10.json` (72 distinct-company quality-qualified holdout)
- `earnings_selloff_recovery_92events_2026-10-10.csv` (ticker/date/event release session)
- `holdout_final_136events_2026-10-10.csv` (filter/join the selected 72 by ticker + selloff_date, including actual AH vs BMO release session)
- `long_horizon_recovery_findings_2026-10-10.md`
- `actionable_bounce_results_164events_2026-10-10.md`
- Prior-work context: Fink (2021), *A review of the Post-Earnings-Announcement Drift* https://doi.org/10.1016/j.jbef.2020.100446 ; Chordia et al. (2009), *Liquidity and the Post-Earnings-Announcement Drift* https://business.columbia.edu/faculty/research/liquidity-and-post-earnings-announcement-drift . Literature documents negative as well as positive continuation after an earnings surprise, not a guaranteed rebound.

## Methodology
Start at the **first qualifying daily closing selloff of >=5%**, which can occur in the first or second reaction session. This is an already-qualified retrospective quality-company event sample, NOT a study of all after-hours reporters. Use adjusted, vendor archived daily regular-session OHLC at as-of corporate action price basis; event-day last close C0, event-day intraday low L0, and subsequent full trading session days D1, D2 etc. In the 164 saved events, 91 have an **after-hours (AH)** earnings release (65 original plus 26 holdout); 73 have before-market-open (BMO) releases. Join sessions by ticker + selloff date. 'New low' is any subsequent DAILY LOW below L0; 'additional downside' is measured from C0 as the minimum intraday low in following N sessions. 'Partial rebound' = subsequent DAILY HIGH >= 1.05*C0, not full price recovery, not option profit. Conservative temporal sequence to represent a 1–5-day dip THEN a later rebound: new lower low during D1–D5 plus subsequent high >=1.05*C0 during **D6–D60**. D6+ requirement makes the order unambiguous but misses cases that rebound before the sixth session.

### All 164 quality-selected events, AH and BMO together
- 81/164 made a lower low than qualifying event-day intraday low on D1.
- 95/164 (57.9%) made a new lower low within D1–D2.
- 114/164 (69.5%) made a new lower low within D1–D5; 125/164 by D10.
- Median of the worst future lows as a % of qualifying event **close** was -1.96% through D2; -2.85% through D5; -3.90% through D10. These figures are based on intraday low values and can look materially more negative than future closing prices.
- 94/164 subsequently touched +5% from C0 by D20, and 113/164 (68.9%) by D60. Median first +5%-touch day = D9 among the 113 successes. The saved long-horizon benchmark for full **pre-earnings CLOSE** recovery by 60 sessions is 86/164; avoid substituting 'partial bounce' for 'full reclaim'.

### Specifically after-hours reported events: N=91
- D1–D2 new lower low: **49/91 (53.8%)**.
- D1–D5 new lower low: **62/91 (68.1%)**.
- D1–D10 new lower low: **67/91 (73.6%)**.
- Median worst low within D1–D5 is **-2.72% from C0**, beyond the initial >=5% earnings selloff.
- Subsequent +5%-from-C0 intraday high: **57/91** by D20, **65/91 (71.4%)** by D60; median D8 to first +5% high among winners by D60.
- **Exact ordered delayed-dip-THEN-rebound morphology:** **42/91 (46.2%)** made a new low below initial qualifying selloff day's low in D1–D5 and subsequently reached +5% above C0 in D6–D60. Conditional on being in the early-new-low group: **42/62 (67.7%)**. This does NOT mean an as-of buyer could have purchased at the later five-day lowest low; it was selected with hindsight.
- Early dip isn't itself a positive predictor: among AH events with a lower low in first 2 sessions, **31/49 (63.3%)** reached +5% above C0 by D60; among those WITHOUT that first-two-day lower low, **34/42 (81.0%)** reached +5%. This contrast is retrospective and depends on conditioning on initial -5% event; it cannot be promoted.
- Company-disjoint holdout AH n=26: 17/26 new lower low in D1–D5; 12/17 then reached +5% above C0 in D6–D60. Original AH n=65: 45/65 lower low D1–D5; 30/45 then rebound D6–D60. This directional delayed-dip morphology appears in both groups but is **not** a trading-strategy proof.

## Corrected research interpretation
A later dip followed by a meaningful partial rebound is a frequent descriptive path after an after-hours earnings shock. Our 45-event intraday 09:35 call proxy and 2025 two-green candle 'buyer initiative' experiments tackled a different same-day opportunity and should not be cited as disproving the user's delayed, days-to-weeks recovery observation.

However, **the additional dip does not by itself select more successful recovery trades**. The actual entry remains unresolved: a trader must know *as of entry* that sellers are fading without relying on a hindsight bottom. Reaching +5% above the previous selloff CLOSE at any time in 60 sessions is not necessarily profitable at a price paid on day 3/6/10, and bears no direct relationship to a cheap call bought at the ask with theta, IV repricing, spread and fixed expiration.

A focused **new** frozen test (on genuinely fresh/unseen releases) should begin with AH releases, >=5% initial selloff, delay of 2-5 trading sessions, then distinguish bottom formation from continuing negative post-earnings drift. Compare an observable stabilization entry vs same-opportunity fixed-day entries (day3/day6) using stock 5% target before 3%/5% stop and 20/40-session windows. Preserve ALL initially eligible AH releases (including no-signals) and issuer/period split, use point-in-time earnings guidance/estimate revisions if available, and only then test 30/45/60-day affordable calls with actual entry asks/exit bids/IV. Do not optimize thresholds on the 164 already exposed results, do not purchase data, do not alter the live scanner.

**Practical next question:** Which day-2-to-day-10 information-valid change—stopped making new lows, reclaimed a prior-day high, stabilized analyst forward expectations, or changed selling volume—is observable *before* enough of the rebound has occurred to erase the call's upside?
