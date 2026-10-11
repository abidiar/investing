# Research reset: stop asking "does it bounce?" and test EX-ANTE selective trade edge
Date: 2026-10-11. This is an AUDIT of already outcome-exposed 283-event 2024–25 fixed issuer-disjoint cohort, NOT a new OOS trading edge.

## Core empirical observations (all reproducible from existing Webull D archives)
Original preregistered v3 next-regular-session-open +3% target before -5% stop through 20 full sessions @50bp modeled trading friction: 160/283 first target=56.54%, 123 stops, average net -1.11284% (ticker 95% CI [-1.6607,-0.5743], event-day 95% [-2.0331,-0.1054]).
Observed winner average +2.6247% after fees, loser average -5.9747% after fees; empirical hit rate needed 69.48% to break even given that average magnitude. Stops with overnight gaps 18 had mean -8.744% net. Neither 56.5% hits nor +3 targets ever guarantee cheap call premiums profit.

**Different endpoint** on SAME 283 trades (not a new strategy): ignoring any stop/drawdown, 216/283 = 76.33% touched +3% (based on next-day open) by 20 full days. 48 of the stop-first cases reached +3 strictly on a LATER daily bar, 8 cases' order of both target & stop touched same day is unknowable from daily OHLC, plus 67 never touched +3 after a STOP-first classification. Endpoint "eventually +3%" is a price EXCURSION measured with hindsight and not tradable without entry, finite capital, option mark and drawdown/time risk. Among 283, 131 closed D+20 >=+3% above entry and mean D+20 closing return +2.37% (no stop, stock, descriptive only, not options). For comparison, only 74/283 reclaimed the PRE-SELLOFF CLOSE in that interval, different and harder milestone.

**MOST IMPORTANT BASE-RATE CHECK (done retrospectively after outcomes exposed):** On each selloff DATE, select single other stock from the SAME 7-group sector roster NOT itself down >=7% that day and nearest PAST 20-session avg daily true range / prior close. 275/283 had a same-sector eligible comparator; all 8 missing were semis on April 3, 2025 broad sector event (no nonselloff semi comparator), don't replace/cherry-pick.
- Paired signals: **208/275=75.64%** ever +3% in 20 sessions.
- Matched same-sector past-volatility non-severe-selloff controls: **222/275=80.73%** ever +3% in 20 sessions.
- Paired difference signal minus control **-5.09 pp**, ticker-cluster bootstrap 86 tickers CI [-11.40,+1.00]pp, event date-cluster 139 dates CI [-13.30,+1.53] pp; zero included, cannot say severe shocks categorically worse, but **no established improvement relative to volatile sector peers**.
- First +3 before -5 daily-bar comparison in matched 275: signal 158/275 vs peer 171/275, also no demonstrated improvement in signal.
- Paired 2024 signals 86/120 vs peers 95/120 ever+3; paired 2025 signals 122/155 vs peers127/155. All thresholds and matching diagnostic, not preregistered, control universe itself survivorship-biased, company historical OHLC future-adjusted, daily within-bar order ambiguous. No causality proven.

Supporting archive in `research/swing_two_session/data/disjoint92_283event_plus3_excursion_vs_matched_peer_2026_10_11.json` commit fdf6581.

## What the extensive experiments actually rule out
- Generic buy-after -7% plus 1.2 RVOL at next open +3/-5 over20 sessions has negative simulated edge on fresh issuer-disjoint 283.
- 40-session support false break + next-day two VWAP closes across 49 issuer-disjoint 2024–26 source diagnostic has negative simulated edge on 103.
- Generic company profit quality/unchanged management FY guide not a reliable quick-buy filter in previous 164 earnings with only 27 comparable FY categories and new 50 source-priority 2024 with just n4 intact, n3 worse. Most actual fundamental source labels MISSING/UNKNOWN. No actual point-in-time street before-vs-after FY EPS consensus over 164 to test main causal story.
- 80% **eventual touching a level** is not an A+ entry or edge because base rate may already be >=80% even for peer nonselloffs. Hit rate must be for executable after-cost specified trade outcomes conditional on ex-ante gating and risk/reward.

## Proposed next single scientifically meaningful question
**Can a source-timed, buyer-driven TURN OF STATE plus market/sector regime and a non-deterioration fundamental NEWS check predict that an ENTRY AVAILABLE BEFORE THE RECOVERY is followed by favorable OPTIONS-AFFORDABLE trade PnL, at an 80% TARGET SUCCESS RATE while abstaining on most signals, OUTPERFORMING same-date ATR and sector matched peer opportunities after costs?**
Do NOT frame "did stock eventually hit x" as trade result.
Freeze one decision time per candidate (e.g. first eligible 10:30am-12pm ET), measurable sellers exhausted state (failed new-low plus higher low and aggressive participation relative to peer/sector) not just repeat old VWAP filter; known-public catalysts as of decision point with UNKNOWN not healthy; regime (broad market and sector relative strength); one or two feasible option expirations and actual historical quote availability, contract ask/mark/bid/spread plus trading budget; not rely on free M5 OHLC to pretend options prices exist. Define target stop and after-cost round-trip options PnL upfront. Train only on dev cohort; freeze classifier before brand-new year/issuer holdout. Require meaningful A+ count and independent ticker/day clusters, report abstention frequency and matched-peer base rate. If no real options quote source is available free, start with independent stock/ETF underlying PnL gate and live forward paper option quotes and label OPTIONS_UNVALIDATED.

Why plausible conditional edges can exist: Da/Liu/Schaumburg (Management Science 2014, https://www.newyorkfed.org/research/staff_reports/sr513.html) isolated nonfundamental reversal residual using ANALYST FORECAST REVISIONS, not mere stock-sector relative down days. Chordia/Goyal/Sadka/Shivakumar (Financial Analysts J 2009, https://business.columbia.edu/faculty/research/liquidity-and-post-earnings-announcement-drift) found institutional drift concentrated in illiquid stocks, trading costs consume much of academic paper returns. Published effects do not establish 80% short-dated options wins.

Research remains OPEN for narrow circumstances; there is NO evidence that *no edge exists*. Never re-use now-exposed 283 or 63/106/45/164 as pristine OOS. No paid feeds, real orders, scanner/automation changes.
