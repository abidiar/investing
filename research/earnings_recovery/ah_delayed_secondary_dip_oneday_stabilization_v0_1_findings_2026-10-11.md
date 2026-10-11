# First prioritized AH delayed earnings recovery test: one-day stabilization v0.1
Run date: 2026-10-11. **Verdict: FAILED / RESEARCH-ONLY; no entry improvement over a fixed day-six opening buy.** Precommitted new diagnostic after academic/prior-work review; the historical 2023–June2026 164-event source panel has prior outcome exposure and must NOT be presented as prospective OOS validation.

## The exact decision
An AH earnings release with first observed >=5% daily close selloff (D0) was followed for a SECOND lower daily low D1–D5. From D2–D10, the first completed green session closing above prior day's close and holding at least the prior day's LOW triggers a following-open purchase, unless that open is >4% above the minimum observed trough as-of signal. A single signal only, no rescanning. This is intentionally *one* higher low/close, earlier than old triple-rising-lows. Stock +5% target vs -5% stop within 20 entry-inclusive sessions, stop-first on same daily bar, gaps at next open, hypothetical 20bp total cost. Frozen protocol: `frozen_ah_delayed_secondary_dip_oneday_stabilization_v0_1_2026-10-11.md`.

## Retrospective OHLC result on all 91 AH events (65 original / 26 disjoint-company)
- 62/91 formed a lower low by D5.
- First one-day price stabilization pattern was found in 58/91 (including patterns that were **too extended**) ; **28/91 entered**, **30/91 skipped as >+4% from known trough**, and **33/91 found no pattern** by D10.
- Among 28 actual simulated stock entries: **12 target first, 13 stop first, 3 timeouts**. Gross underlying mean **-0.146% per entered trade**; after hypothetical 20bp cost **-0.346% per entered trade**. Per ALL 91 AH opportunities counting no-entry as 0: **-0.1064% cost-adjusted**.
- Simple **D3 opening entry** on ALL 91: 47 targets / 38 stops / 6 timeouts; +0.4487% gross, +0.2487% after hypothetical 20bp each.
- Simple **D6 opening entry** on ALL 91: 46 targets / 36 stops / 9 timeouts; +0.4704% gross, +0.2704% after hypothetical cost.
- D6 opening ONLY for the 62 with an observed extra low in D1–D5: **34 targets, 23 stops, 5 timeouts**, +0.898% gross per trade, +0.476% after-cost per ALL 91 AH events with skips zero. This baseline has its own selection effect, not automatic option profits.
- **Fair paired comparison on SAME 28 events where stabilization entered:** its gross mean **-0.1458%** against their own D6 gross mean **+1.0132%**, a **-1.1590 percentage point underperformance**; stabilized trade target 12/28 versus D6 target 15/28.
- Split outcomes: original 65 → 21 stabilization entries, 9 targets, 10 stops, 2 timeouts, -0.475% after-cost per entered; disjoint 26 → seven stabilization entries, three targets, three stops, one timeout, +0.0415% after-cost per entered. The 7-case opposite sign is far too weak to rescue pooled/paired failure; paired D6 difference remains negative in BOTH subgroups (-1.400pp and -0.435pp).
- Tightening stop to -3% lowered target hits to only 6/28; 40-session holding gave 14/28 target hits, mean -0.330% after-cost per entered. These do not rescue it. Data from previously archived adjusted daily stock OHLC only; these are NOT executable cheap call ROI or delta/IV/DTE tests.

## Verdict and implication
**Do not adopt one-day green/higher-low stabilization as an automatic call entry.** One extra up-close is insufficient to distinguish durable buyers from temporary dead-cat rebounds; next-open anti-chase filter also discards many signals. A fixed D6 STOCK buy looked better in these outcomes but cannot be promoted: on company-disjoint AH cases D6 ALL EVENTS gross mean was **-0.4277%**, so that simple timing heuristic is not stable. This is an exploratory sample with prior outcome exposure and no actual option bid/ask, earnings forecast revisions, fees/spreads, or event-dated point-in-time company quality.

The multi-day *recovery phenomenon* remains real, but no early observable trading rule has been verified. **Next research priority is not more threshold fiddling**: take a clean, genuinely unseen issuer/quarter set (roster fixed before forward prices), segment earnings guidance/forward estimate stability AS KNOWN at the decision time where feasible, and compare simple D3/D6/first stabilization, with all no-signal cases and exact stock-path risk. If that improves stock outcomes in an untouched cohort, then try listed affordable contract ask-to-bid premium histories with IV, spreads and calendar DTE. The existing 91 AH data should remain discovery only. No A+ scanner rules, live calls, or scheduled automation changed.

## Reproduce
1. Protocol: `frozen_ah_delayed_secondary_dip_oneday_stabilization_v0_1_2026-10-11.md`.
2. Runner: `run_ah_delayed_secondary_dip_oneday_stabilization_v0_1.mjs`.
3. Machine-readable full 91 events and summary: `ah_delayed_secondary_dip_oneday_stabilization_v0_1_results_2026-10-11.json`.
4. Source panel: `actionable_bounce_price_windows_{92events,72events}_2026-10-10.json` with `earnings_selloff_recovery_92events_2026-10-10.csv`, `holdout_final_136events_2026-10-10.csv`.
