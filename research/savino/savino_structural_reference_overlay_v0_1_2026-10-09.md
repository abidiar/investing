# Investing OS — Savino structural reference overlay v0.1
Date: 2026-10-09
Authority: RESEARCH-ONLY / OPTIONAL DISPLAY. NOT a production rule, entry trigger, hard veto or substitute for certified destination/runway.
Applies to: A+ 09:20/09:50/10:20 and after-close scorecard **reporting context only**, and exploratory research on independent entries.
Does NOT change: permanently frozen A+ DAY DETECTOR v1.0, late-state-change v0, scanner Strength >=4/5 and Runway >=4/5, VWAP/M5 acceptance, >=~2:1 R:R, events and option-quality gates.

## Why this reference is retained
Six retrospective screenshot-selected Savino days (Sep 25, 28, 29, 30; Oct 2, 8) were tested with the first independent opening-range+VWAP SPY M5 signal of each day. A nearest translated Savino destination was reached before the independently specified structural stop on 3 of 6 signals, but the reached targets offered only 0.258R–0.470R at entry. Only one of six cases offered a nearest target >=2R; it stopped out. Plain 25-SPX-step control grids yielded 2–4/6 target-first counts under the same entries/stops, with different target distances. There is **no demonstrated incremental edge** or validated Savino-based stop placement. Full results: research/savino_destination_invalidation_results_v0_1_2026-10-09.md.
Do NOT interpret any fraction as a live probability or trade-hit rate. Do not change v0.1 protocol in place.

## Optional morning reference workflow — NOT used to generate an actionable signal
A) SOURCE GATE
- Use only exact, timestamped Savino SPX levels verifiably posted before the evaluated checkpoint. Preserve date, post timestamp in ET, screenshot/source and descending list. No assumed levels if missing or stale.
- For later level revisions, timestamp as new version; do not rewrite older checkpoints. Archive screenshots if feasible.
- If unavailable, print "SAVINO MAP: UNAVAILABLE (not posted/verified)" and do not backfill after an outcome.
B) FIRST SOLVE THE TRADE INDEPENDENTLY
- Determine causal driver, risk regime, direction, breadth and accepted M5 trigger independently; select an independent structural stop and destination with fresh reward:risk >=~2:1, adequate ADR/runway, viable options, and acceptable vetoes. If any hard gate fails, WATCH/NO TRADE regardless of proximity to a Savino level.
- NEVER let Savino levels establish direction, trigger acceptance, add Strength/Runway points, raise A+ confidence, or promote WATCH/NO TRADE. Never use a Savino line alone to certify a stop or 2:1 runway.
C) ANNOTATE THE EXISTING SETUP AFTERWARD
- Show nearest Savino major level above/below CURRENT *SPX* if exact SPX is available, as optional reference; otherwise present an explicitly approximate SPY proxy, with pricing basis/time. SPX / 10 is NOT exact. If no reliable SPX/ETF basis, display SPX levels only, no precise SPY translation.
- Fields: MAP STATUS VERIFIED/UNAVAILABLE; AS-OF ET; SPX LEVELS; CURRENT SPX (timestamp/source) if available; NEXT LEVEL ABOVE/BELOW; independent T1 and independent invalidation; Savino nearest potential destination (RESEARCH REFERENCE); Savino key reaction/reclaim zone (RESEARCH REFERENCE); distance from accepted independent trigger to proposed level; whether this reference would constrain or conflict with independently certified runway; OBSERVATION ONLY.
- Distinguish major vs chart-inferred subdivision. A subdivision is lower confidence and never a substitute for a major level.
- If Savino lies *inside* independently selected T1: mark "INTERVENING REFERENCE / POTENTIAL FRICTION — UNVALIDATED"; investigate, do NOT automatically veto or shrink target.
- If Savino lies *beyond* independent T1: mark "BEYOND BASE TARGET — NOT AUTOMATIC T2"; do NOT inflate prospective upside.
- For stop context, "loss/reclaim/rejection of Savino level" is only an **invalidation hypothesis** requiring independently accepted M5 failure and a preexisting structural stop. Do not move stops to fit line or auto-exit based on a touch.
D) AFTER CLOSE
- Freeze A+ 09:20/09:50/10:20 classifications and trade-specific fields first; report Savino as a SEPARATE research block only.
- Score levels as exactly touched, approached (with explicit tolerance), or not reached using exact SPX data; log time/order of first break, rejection, regain, closest excursion, and target-before-independent-stop with same-bar conservatism when data permit.
- If exact SPX M5 is missing, explicitly "UNSCORABLE EXACT LEVEL SEQUENCE" and provide approximate SPY-proxy analysis separately. Do not use retrospective levels to rewrite trade authorization or day classification.

## Compact recommended output for future scans
SAVINO STRUCTURAL MAP (optional, research-only): STATUS / source as-of / posted SPX levels / nearest levels above and below / independently selected entry/stop/T1 / map proximity & friction note / exact SPX vs SPY proxy method / NEVER an entry, score, veto, or hard stop.

## Next research (not approved for production)
(1) Prior-work review per research/PRIOR_WORK_REVIEW_STANDARD.md BEFORE freezing a new v0.2 protocol.
(2) Validate canonical exact SPX M5, larger complete timestamped level archive, >=30–50 untouched days, distance-matched null targets and price-only alternatives.
(3) Independently test Savino-based failed-reclaim/acceptance stop placement versus structural M5 stops on the same independently generated entries with risk-width and slippage/option economics.
(4) Only if prespecified out-of-sample promotion conditions pass may a new version modify executable T1, invalidation, or runway calculation.

## Scope and deployment truth
This is a REPORTING/RESEARCH annotation specification only. Existing repo Cloud Run service in main.py is a Webull-to-Sheets market-data collector, not a Savino-signal executor, and is not changed or redeployed by this documentation. The current Google Sheet and any in-market option recommendations do NOT gain an implemented, validated Savino target/stop engine from this file.
