# Pre-analysis spec: Can a post-earnings bounce be captured without entering too early?
Protocol frozen 2026-10-10 before NEW path/entry comparisons. Two OLD and previously outcome-observed qualified cohorts: 92-company-discovery events and 72-company-disjoint historical holdout events. This analysis is EXPLORATORY, not an untouched-outcome trial: signals are new but the broad datasets were already examined for prior strategies. Keep results disaggregated. Re-read historical daily RTH OHLC from connected Webull, no payments.

## Observable event anchor and risk path
- Event is already qualified by *original* published quality-screen criteria and initial earnings selloff close <= -5% relative to prior earnings close.
- Anchor = **qualifying selloff day's CLOSE**, known at end of event date. No hindsight bottom. Over NEXT 20, 40, 60 trading sessions compute first intraday +5% from anchor versus first intraday -5% or -10% from anchor, stop-first when both touched on same bar. Gaps handled as adverse-first/target-first according to opening gap; if open breaches both impossibly, evaluate stop first. Also time to first +5%, time to low, min excursion during window, time to full pre-earnings close if available (not in focus). These path statistics do not imply investability from next-open.
- Report rebound touch irrespective of whether stop came first **and** first-hit ordering to quantify 'eventually rebounds but options die first'.

## Objective entry candidates (use only information known at time)
A) next_open: buy first session OPEN AFTER selloff close.
B) day3: buy third session OPEN AFTER selloff close (previous frozen baseline).
C) 5DMA_reclaim: scan *post-selloff* sessions 5 to 20 inclusive for earliest close above its 5-day SMA (including that closing bar), prior close at or below its own 5-day SMA, AND closing price above immediately prior session HIGH; enter NEXT regular-session OPEN. If no trigger by 20, skip. Entry may include gaps.
D) three_rising_lows_break: scan post-selloff sessions 3 to 20 inclusive for earliest three consecutive daily lows nondecreasing (l[k-2]<=l[k-1]<=l[k]) and close above MAX of HIGH[k-1],HIGH[k-2]; enter next regular-session OPEN. No trigger => skip.
- For C and D: 'don't chase' restriction: if that very first signal's next opening price exceeds +8% above original selloff close, SKIP event outright; don't search subsequent triggers. Also count how often restriction causes skip, and how many events had already touched +5% from anchor before entry. For A/B no cap so clean baseline.
- No future daily values used to enter. No option market series used.

## Underlying (not option) exits
- From entry OPEN, profit target +5%. Stops -5% (current baseline) OR -10% to permit ordinary post-selloff volatility. Each managed for 20 entry-inclusive sessions, separately 40 entry-inclusive sessions. Within each bar: check opening gap breaches first, then if both high target and low stop touch assume STOP first (conservative OHLC). Timeout exit at last window close. Report trigger coverage, target/stop/timeout counts, gross stock return on triggered trades AND per *all qualifying events* (skips = 0) so rare signals cannot look better by dropping losers. Model no commissions, spread, slippage, overnight option IV or premium. Do NOT rank calls.
- Calendar DTE proxy: 14, 30, 45, 60 calendar days from each next-open entry; evaluate whether a +5% underlying target was reached before the -10% underlying stop in window, plus held-only expiration underlying return and time to target. This is NOT an options P&L and calendar cutoffs are NOT real option listings.
- Cross-check events with frozen source entry values / first 5-session outcome, inspect unexpected discrepancies. Explicitly report minimum coverage and missing price series (if any), and year/ticker clustering. Do not change thresholds after outcomes. No A+ or deployment if results not robust in BOTH 92/72 cohorts. Future truly unseen test required.

## Caveats and next phase
The 92-event cohort was preselected from 50 current stocks; 72-event was screened from 65 current companies, not a historical index; survivorship, time/revision, sector, event-label biases. Overlapping market regime across events. Four candidate methods and two stops induce multiple-testing. A realized 5% underlying bounce can occur after large loss in an option; future test must use actual historically executable options bids/asks & IV or transparently stated Greeks stress scenarios and options expiry.
