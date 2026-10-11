# Frozen v0.1: After-hours earnings secondary dip → first one-day price stabilization

Frozen/committed: October 11, 2026. **Exploratory retrospective candidate only**; all underlying 2023–June2026 price data has been available and partially outcome-observed in previous research. FREEZE IS PRIOR TO THE v0.1 ENTRY OUTCOME CALCULATION but does NOT confer unseen/out-of-sample status.

Prior review: `research/prior_work/after_hours_delayed_selling_stabilization_prior_work_2026-10-11.md`.

## Primary question
Among AFTER-HOURS earnings announcements with an already quality-qualified first >=5% RTH daily CLOSE selloff, can a single-day buyer-response *after a further observed daily low* provide a more actionable long STOCK entry than a fixed day-three or fixed day-six purchase? Target is days-to-weeks recovery, **not** the previously studied same-day earnings-gap reflex bounce.

## Fixed roster / complete data source
Exactly the 164 existing qualified earnings selloff events saved in
- `actionable_bounce_price_windows_92events_2026-10-10.json`
- `actionable_bounce_price_windows_72events_2026-10-10.json`.
Join earnings session by `ticker|selloff_date` from `earnings_selloff_recovery_92events_2026-10-10.csv` and `holdout_final_136events_2026-10-10.csv`. Only AH gets primary-scored, retain other BMO in count only. NO dropping by future outcome or trigger. The prior saved AH count is 91, 65 original and 26 distinct-company. D0=first objectively qualified selloff DAY CLOSE (occasionally second postearnings trading session); D1=following regular session, etc. Daily adjusted OHLC price arrays; no volume/option data. Fully report coverage/missing event frames.

## One frozen one-day signal; no alternate threshold tries
Scan sessions D2 through D10 in ascending order. The first session t whose CLOSE is available AND:
1. A further low below **D0's intraday LOW** has already been observed on an earlier D1..Dmin(t−1,5) candle, so early further downside is known by signal close.
2. D_t LOW >= D_(t−1) LOW. (First failure to print yet another lower low.)
3. D_t CLOSE > D_t OPEN **and** D_t CLOSE > D_(t−1) CLOSE. (One-day buyer response measured as price, not signed order flow.)
As soon as first signal t completes, propose buy at **D_(t+1) OPEN**, which is the first executable simulation price AFTER full signal evidence.
4. Anti-chase: D_(t+1) OPEN <= 1.04 × minimum intraday LOW already seen across D0..Dt. If violated, mark SKIP/EXTENDED and do NOT rescan at another signal. All close and high/low information is as-of, no future trough.
No signal by D10 → NO TRADE. No volume, SMA, VWAP, SPY strength, analyst revision, extra confirmation day, or parameters to tune. This is earlier/simpler than previously rejected three rising lows, but not yet proven superior.

## Comparators on identical source events
A. Fixed D3 OPEN for all AH initial opportunities (buy regardless of additional downside).
B. Fixed D6 OPEN for all AH initial opportunities (buy regardless of secondary downside).
C. Fixed D6 OPEN **only among events that had lower low below D0 low in D1–D5** (observable by D5 close; skipped otherwise), a condition-matched baseline.
D. Paired fixed D3 and fixed D6 for those EXACT events where v0.1 actually enters; compare mean gross/net and first target rates. Don't mistake selective per-entered-trade improvement for higher all-event profitability.
The v0.1 filter and all comparator outcomes are reported against full AH opportunity denominator (skip = 0) and by individual entered trade.

## One primary risk/output model
Underlying STOCK, NOT a call options P&L. Buy at actual next-session OPEN, profit target +5% vs stop -5% from that ENTRY OPEN, hold at most 20 **entry-inclusive RTH sessions**. At start of later sessions handle opening price crossing target/stop at ACTUAL OPEN (gap slippage captured). Within daily candle, if both high>=target and low<=stop, assume STOP FIRST (conservative). Other touches exit at their price barrier; no-touch exit at last 20th close. If final 20 bars missing, label incomplete (not an automatic loss or timeout). Separate illustrative total 20-basis-point roundtrip cost for every entered trade.
Report entries, no secondary low, no signal, extended skips, signal day index / entry day, % already bounced above observed trough, target first, stop first, timeout, mean stock gross & hypothetical net per traded, per ALL AH, and paired deltas.

## Secondary/robustness (no rule changes)
- Original65 AH vs separate-company26 AH outcome slices; list per-ticker counts, note issuer clustering.
- Alternate -3% stop with +5% target and same 20 sessions; and +5/-5 for 40 sessions if source has fully-observable horizon (mark missing otherwise).
- Day3 and day6 baselines held to same entry-relative 20 sessions, same event roster.
- Anti-chase skip count and winners lost vs unconditional day6 must be disclosed.
- Point-in-time quality and adjusted raw prices from old case screens are not perfect. No quantitative claim about option premiums or an A+ hit rate; cash dividends can distort adjusted relative stock prices.

## Non-negotiable decision and promotion boundary
This dataset has been repeatedly studied. **Even if v0.1 beats comparators on these 91 AH events, that is exploratory only, NOT eligible for production promotion.**
A future genuinely unseen AH event cohort must be frozen before collection; prespecified gates for considering the rule useful: >=30 signal entries overall, positive mean stock return net hypothetical 20bp in the full opportunity population, >=+10pp target-first *per all early-secondary-low eligible events* versus condition-matched day6 comparator with at least three extra target wins, positive paired average net-entry advantage versus D6 among jointly traded events, and consistent direction in time/company-separated groups. Company cluster resampling intervals should not straddle zero for the main net difference. Options A+ promotion additionally requires affordable actually listed strikes (<= $50 debit contract plus fees if that remains the user budget), contemporaneous executable ask/bid, IV, DTE, spread and expiration tests. If any material requirement fails, stop; don't soften.
No modifications to current A+ or recovery scanner, automation, CALL/POT authorization, option expiry or stop rules from this protocol.

## Data leakage and governance
Everything about this retrospective cohort is outcome-exposed from earlier work. This freeze is to prevent additional **within-test** threshold changes and create an exact reproducer; it is not a blind external replication. Any mismatch between AH confirmation dates and source bars must be reported without trying alternate labels after viewing winners. Prior existing event lists have survivorship bias; future samples need an up-front broad issuer calendar and quality-at-event check.

Status upon freeze: **AWAITING EXPLORATORY v0.1 RUN**. Source records in repo. Do not claim an outcome until saved alongside code/results.
