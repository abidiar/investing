# Frozen intraday EARLY rebound onset audit — 2026-10-10
**Status:** defined BEFORE fetching the 15-event test's complete post-selloff five-minute bars. An ISRG 2026-07-17 to 07-21 feasibility source probe has been inspected to confirm connected Webull and Massive return historical five-minute bars. No entry/outcome of that event was calculated before the freeze. This is an exploratory analysis, not pristine blind validation.

## Event panel and nonlookahead
Take EXACTLY the 15 frozen Jul-02 Sep-04 2026 one-day >=-5% earnings selloffs in `frozen_jul_sep2026_earnings_selloff_discovery_2026-10-10.json`. No issuer additions, ticker performance filtering or date substitution. Six potential historical issuer source reaction table gaps remain unavailable (AMAT/HON/HPE/REGN/WAB/ZBH): preserve missing coverage in interpretation.
The earnings event qualifies ONLY after the event day's CLOSE. Earliest permitted entry is first subsequent regular-session open. A signal during the selloff event day is **not** tested because it would rely on knowing the event's final close reaction from the future. Test intraday historical 5-minute Webull RTH bars (America/New_York) over the **first five following market sessions**, plus two further trade-exit sessions. Use volume-weighted typical-price VWAP proxy per day, calculated cumulatively from *completed bar HLC3* times bar volume / cumulative bar volume; this is an estimate, not exact tick-based VWAP. Reset VWAP at regular-session 09:30 each day. Do NOT use full-session volume, closing high/low, whole-day VWAP or next-bar close for selection.

## Early-reversal entry — ONE fixed signal
Within the first 5 regular sessions AFTER selloff event day, scan 5m bars with bar START timestamps 10:00-13:00 ET in chronological order.
At completion of 5m bar k, require:
1. THREE immediately preceding *completed* 5m bar closes at k-3,k-2,k-1 each strictly **below its own as-of-bar session running VWAP**.
2. Current k close **above** current cumulative as-of VWAP and strictly **above high of previous bar** (demand reclaim plus short resistance breach).
3. Lower lows have stopped: **low(k-2) <= low(k-1) <= low(k)** (three nondecreasing successive 5m bar lows; as-of known at k close).
4. Signal close no more than **1.5% above the minimum intraday LOW observed from today's 09:30 session open through bar k** (don't chase overextended rebound).
Take only FIRST fully qualifying signal per event; if next bar unavailable, invalid; don't rescan after failure.
**Buy stock reference at OPEN of NEXT 5m bar k+1**, requiring both bars to be within the SAME regular trading day and entry no later than 13:05 ET. If this entry open exceeds +1.5% above session low as of signal k, mark TOO_EXTENDED_SKIP (no later entry or price substitution). Report elapsed sessions after event, time ET, entry level, session observed low, remaining percentage to PRE-event price for descriptive diagnostic.
Price VWAP/volume unavailable or incomplete RTH session => MISSING_SOURCE, not an inferred entry.

## One exit (no option P&L)
Underlying fixed +1.5% target **OR −1.0% stop**, first touched, within **three entry-inclusive regular-market trading sessions** after entry, checking EVERY subsequent 5m OHLC bar. First entry bar starts at the entry open. If both hit in same 5m bar, conservative STOP-FIRST. Overnight next-session gaps checked at next open before intrabar; fill gap at first open. If neither, exit at closing price of third entry-inclusive trading session. Missing/incomplete follow-up => RIGHT_CENSORED, not a win or loss. Exclude or separately label splits. Returns from as-traded unadjusted OHLC; no commissions, fees, liquidity or after-hour holds.

## Comparators
A: fixed buy at 10:00 ET of FIRST session following selloff close; exactly SAME +1.5%/-1.0% 3-session intraday stop/target.
B: buy at 10:00 ET of THIRD session following selloff close; same exit. Distinct from prior day3 09:30 open but only a context benchmark. Require actual corresponding 5m bar.
For each comparator, one trade per event, no additional momentum restrictions. Count strategy target-wins, stop-first, timeouts, avg gross return among entries and **per all 15 frozen event opportunities** with no-trigger as 0. Report relative delta, but sample n=15 underpowered and new exact intraday rules are post-hypothesis-generated on prior results (outcome aware by research history).

## Minimum go / no-go
Demand (i) at least TEN actual early entries, (ii) >=+10 percentage-point advantage in wins **per all frozen events** vs first-day 10:00 benchmark, and (iii) positive average gross stock return per ALL events after a conservative 0.20% round-trip illustrative transaction cost, and (iv) at least half of candidate signals entering <=+0.75% above the contemporaneously observed intraday trough to establish earliness. Small 15-event exploratory series CANNOT on its own promote any strategy as a validated edge even if these gates pass. No option ROI or claim about user's META 0DTE style; five-minute RTH data, VWAP approximation and lack of exact fills limit inference.

Do not tune the 1.5%, VWAP, 3-bar, opening time or targets on these 15 results. Log all 15 event outcomes, missed signals, source prices, mismatch versus frozen daily raw OHLC, and any source price adjustments. Subsequent truly independent period or distinct companies required for validation.
