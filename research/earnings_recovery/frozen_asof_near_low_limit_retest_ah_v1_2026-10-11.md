# FROZEN before outcome evaluation — AH secondary-low near-trough limit v1
Date 2026-10-11. Prior work: `research/prior_work/earnings_near_bottom_asof_low_retest_limit_2026-10-11.md`.
HISTORICAL RETROSPECTIVE EXPLORATION ONLY, source outcomes previously exposed; commit this protocol before calculating new v1 test.

**Research question:** Can paying close to a formerly *observed*, not hindsight-future, post-earnings low create an actionable +3% partial-rebound edge and outperform a calendar-market buy, despite adverse-selection risk? Not a promise of catching the ultimate bottom.

## Frozen roster
Join 92+72 existing quality-qualified earnings selloffs with session metadata at ticker+selloffDate; only after-hours AH cohort, exactly 91 events. Base set is all 91. Eligible subcohort: post-reaction D1, D2 OR D3 daily low below original D0 low (no requirement of a certain percent). This subcohort can be identified at D3 CLOSE, BEFORE submitting orders. Keep ineligible and no-fill as SKIP (zero P&L for full-91 opportunity denominator). D0 is first qualifying >=5% closing price decline vs preceding earnings close, may follow the immediate day.
Archived input: `actionable_bounce_price_windows_92events_2026-10-10.json`, `actionable_bounce_price_windows_72events_2026-10-10.json`, `earnings_selloff_recovery_92events_2026-10-10.csv`, `holdout_final_136events_2026-10-10.csv`.

## Single limit rule; no tuning
At END D3, if eligible, calculate known as-of observed LOW L = min(RTH lows of D1–D3). Place BUY LIMIT at **1.01 x L** starting D4 opening auction; keep through END D6 if unfilled; cancel at D6 close if not filled.
- On D4/D5/D6: if OPEN <= limit, fill at OPEN (limit marketable on open); otherwise if low <= limit, assume fill at LIMIT. This optimistic low-touch fill ASSUMPTION overstates certainty when queues, spreads, and overnight discontinuities cause slippage; flag even if positive.
- If bar's daily low == limit rather than strictly below, assume **no fill** (conservative require LOW < limit), except actual opening <= limit counts as filled at open.
- If entry during bar via low-touch limit fill, same-day stock stop may hit if daily low <= stop, but SAME-DAY target high cannot be credited (may have occurred BEFORE fill). If entry at OPEN, conventional same-day stock high/low first-hit ambiguity resolves STOP FIRST.
- Once filled, first +3% HIGH above **actual filled stock entry price** before -5% low stops; 20 ENTRY-INCLUSIVE completed RTH days max; gap opening beyond stop/target exits at gap open; ambiguous stop-before-target, held-to-day20 closes as timeout. Missing 20 bars is INCOMPLETE not loss; do not substitute unknown.
- Roundtrip hypothetical STOCK cost 0.20% deducted from every filled trade. No options/IV/fee execution approximations as real.

## Baselines
A. Buy at D4 OPEN for every **same D3-eligible event**; stock +3%/-5%/20 sessions.
B. Buy at D6 OPEN for every **same D3-eligible event**, identical stock model.
C. Paired D4/D6 baseline on ONLY exact events where the retest limit fills.
D. Report market D6 ALL 91 AH for background but **never** compare conditional per-traded winner rate with all-event returns to make an edge claim.
Population mean defined as sum of trade net stock P&L / 91 initial AH events, skipped = zero. Conditional mean per filled entry additionally. No option P&L.

## Primary outcome and gates
Primary: paired (limit minus D6) mean gross % across events on which BOTH can buy (every limit fill), alongside net per all D3-eligible episodes and per original 91. Target-first count, stop-first count, timeouts, limit fills/nonfills. D4 as another baseline.
Breakdown: original65 AH versus separate-company26 AH; no post-hoc subsets or target changes. Median lag & as-of low distance, median worst interim adverse move, time to +3%, and fill fraction. No hypothetical portfolio leverage; option risk cannot be computed.
Predeclared interpretation gate for further independent test: limit fills >=25, paired limit-D6 mean >+0.75pp overall and positive in BOTH groups, cost-adjusted per-all-91 net >0, and no wider than 2pp issuer-cluster interval crossing zero for paired advantage. For actual scanner options promotion still need unseen chronological cohort, point-in-time selection, actual <=$50 liquid option asks/bids, + realistic IV/DTE/cost & drawdown. If gate fails => v1 NOT SUPPORTED and no threshold mining on 91 old events.

## Anti-lookahead and restrictions
This is NOT hindsight lowest 20- or 60-day price, and must include stopped-out falling knives and unfilled orders. No rule revisions after result inspection. Volatility/guidance/market context not added without independent preregistration. Historical daily bars cannot reveal queue position, actual touch sequence or executable call premiums. No automated trading/scanner change.
