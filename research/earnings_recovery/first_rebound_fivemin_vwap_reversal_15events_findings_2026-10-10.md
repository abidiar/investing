# Can a 5-minute VWAP/higher-low signal catch the *beginning* of an earnings-selloff rebound?
Historical intraday stock-only test, October 10 2026 — **completed and not validated.**

## Honest bottom line
This exact early intraday signal **failed** in the complete 15-event pre-frozen July–September 2026 earnings-selloff cohort. Waiting for the 5-minute VWAP reclaim, three prior closes below VWAP, rising 5-minute lows, and close above the prior high selected 12 trades; only **2/12** reached an additional +1.5% underlying before −1.0% within three entry-inclusive trading sessions, while **10/12** hit the stock stop first. Across all 15 events, the model gained +1.5% first only 2/15 times; gross per-event stock mean −0.4915% (no-trade as zero), or −0.6515% per event with illustrative 20bp costs per entered stock trade. Both straightforward first following session 10:00 and third following session 10:00 entries returned 5 targets/15 events, 10 stops, and worse than breakeven gross means (−0.2371% and −0.2558% respectively). All are hypothetical stock OHLC trades, **not actual options fills, returns, or an actual 2x ETF backtest**.

## Pre-frozen rules and chronology
- Frozen full event list from 61 preexisting historically quality-pass companies: 15 reaction-close −5% or more earnings selloffs Jul17–Sep02 2026. Entire company/event list committed BEFORE this new 5m collection and prior daily result, six issuer reaction histories unavailable.
- Frozen 5-minute test definitions committed BEFORE collecting 5m bars (one ISRG 5m data coverage probe seen beforehand, no outcome); protocol `frozen_2026_intraday_early_rebound_vwap_test_2026-10-10.md`.
- 5-minute RTH source: connected Webull historical stock candlestick tool, 15/15 tickers, all 78 scheduled 09:30–15:55 bars on each historical session, serialized into NINE GitHub JSON event-date grouped files `early_reversal_2026_intraday_webull_{jul17,jul21,jul23,jul28,jul29,jul31,aug05,aug13,sep02}_2026-10-10.json`. All 15 event day 5m closing values exactly matched separately archived Yahoo as-traded daily closes: 0.0% close discrepancies. This is evidence of coherence, not independent exchanges. Historical cash-dividend adjustment must remain unadjusted; no corporate splits observed requiring exclusion.
- Intraday event eligibility only after selloff day CLOSE (so no lookahead by entering before known −5% event close). Search FIRST five sessions following close for five-minute bar at 10:00–13:00 close: preceding 3 completed closes below THEIR OWN as-of-session cumulative 5m typical-price-volume VWAP proxy; current close above its own VWAP AND prior bar high; lows at k−2,k−1,k nondecreasing; at signal close <=+1.5% from today's trough so far; buy following 5m OPEN unless >+1.5% from known trough. Stop at −1% stock, +1.5% profit from entry, first touch wins within 3 entry-inclusive RTH sessions (conservative same-candle stop first, overnight gaps at next open). Fees excluded except 20bp illustrative sensitivity.
- Comparators on exact same 15 events: 10:00 ET first following regular session, and 10:00 third following regular session, same stop target time; both entered all 15.

## Performance and signal quality

| Method | Trades | +1.5% before −1% | Stock stops | No signal | Win% per all 15 events | Gross return per all events |
|---|---:|---:|---:|---:|---:|---:|
| First daily-session 10:00 | 15 | 5 | 10 | 0 | 33.3% | −0.2371% |
| Third daily-session 10:00 | 15 | 5 | 10 | 0 | 33.3% | −0.2558% |
| **First VWAP higher-low reclaim** | **12** | **2** | **10** | **3** | **13.3%** | **−0.4915%** |

In early signal 12 entered, the +1.5% stock target happened GLW Aug04 and PANW Sep08. Stops hit in ISRG, NFLX, CMCSA, GOOG, UPS, AMD, CVS, EOG (gap), CSCO (gap), TPR. HAL, KLAC and COIN never triggered; not unsuccessful purchases. Among 12 triggered, 2/12=16.67% target first, 10 stops (2 overnight gap stops). All resolved. This filter underperforms both simple 10am baselines with identical risk rules. Four prespecified promotion gates: minimum >=10 entries yes, >=+10pp success advantage no, positive mean after 20bp roundtrip stock costs no, at least half entries within 0.75% of session low no. **Do not deploy, promote A+, use as a trade recommendation, or optimize option DTE using this rule**.

## Is it already late by a VWAP reclaim?
- **Median entry 1.1278% ABOVE the lowest trade price already observed in that session** (as-of-entry trough). **10 of 12** entries already more than **0.75% above the session trough**, 7 of 12 >1% above.
- Signals arrived on session 1 after event for only THREE events, session 2 for one, session 3 for four, and session 5 for four. Thus this daily 5m reclaim definition often arrived several sessions after the earnings dislocation, not at first selling exhaustion.
- This supports that requiring multiple confirmations **can** introduce lag; it does NOT prove entering at the trough is possible or profitable. In fact both cases with <=0.75% distance from trough (CVS and EOG) failed to hit target under the studied entry and stop, so 'enter sooner' alone is not enough.
- The VWAP used is the running weighted average of completed **five-minute HLC3×volume**, not transaction-level exact VWAP; a trading platform's exact VWAP may differ. Even genuine as-of VWAP doesn't establish buys on the option ASK.

## What factors need attention without indicator fishing
A successful early reversal requires three separate things: (i) an as-of-knowable dislocation, (ii) **selling actually exhausted** rather than a brief bear-market bounce, and (iii) enough demand/new catalyst to push through nearby supply while a call's premium/delta/time remain favorable. Our observed five-minute VWAP reclaim + higher-low rule verified (some) price stabilization but did not establish (ii) or (iii); only GLW and PANW won among 12.
Next **single** research possibility on a *different untouched period* would replace late VWAP as entry filter with an **early exhaustion / buyers taking control** test: declining sell-volume into second intraday low and first expanding buy-volume breakout, with measured market/sector context and trade taken before distant VWAP reclaim, while retaining a fixed risk budget. Define as-of observable candles, use next 5m open, and NEVER optimize entry distance threshold on these same 15 events. Evidence here does not license a CALL edge, and historical option asks, deltas, spreads and OI still unavailable for our exact timestamps.
This test deliberately did not look at the user's actual META 0DTE July 2026 call, which may have been a different overnight momentum regime. Don't conflate it with these selloff-close anchored three-session stock proxies.

## Reproduce
- Source event list: `frozen_jul_sep2026_earnings_selloff_discovery_2026-10-10.json`.
- Pre-frozen intraday signal protocol: `frozen_2026_intraday_early_rebound_vwap_test_2026-10-10.md`.
- Exact complete outcomes per event, entry/stop/times: `early_2026_frozen_fivemin_vwap_rebound_actual_results_2026-10-10.json`.
- 9 Webull archived real historical 5m OHLCV sources as above.
- `run_frozen_2026_early_intraday_vwap_rebound_research.py`, GitHub Actions `.github/workflows/earnings-intraday-first-rebound-vwap-2026.yml`.
