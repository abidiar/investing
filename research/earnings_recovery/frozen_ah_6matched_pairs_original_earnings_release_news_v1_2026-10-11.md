# FROZEN as-of-source review protocol: 6 AH earnings D4 first-passage winner-failure pairs
Frozen 2026-10-11, **BEFORE systematic original press-release evidence extraction / feature scoring**.
Prior study: `research/prior_work/ah_earnings_new_information_release_case_control_review_2026-10-11.md`.
All outcomes were previously known and fixed as part of the 164 study. This is a systematic **retrospective qualitative mechanism/coverage audit**, NOT prospective prediction.

## Exactly fixed matched 6 pairs, no picking/adding easier pairs
These are literally `matched_quality164_fundamentals_v1_all_events_pairs_2026-10-11.json` matched72.d4.pairRows whose `releaseSession==="AH"`. Winner is DAY FOUR trade +3% stock target before -5% stop within 20 sessions, loser is stop or timeout. Cases and controls already quality PASS and same-year AH matched within <=5 percentage points initial fall and different company; but sectors, months, market betas are NOT matched. Preserve all 12 events even if public release unavailable.
1. AMAT 2025-05-15 (selloff 2025-05-16; WIN) vs OKE 2025-08-04 (2025-08-05; FAIL).
2. LEN 2025-06-17/18 (earnings event 2025-06-18 according to our roster; selloff 2025-06-18, WIN) vs CPRT 2025-11-20 (selloff 2025-11-24, FAIL).
3. NEM 2025-10-23 (roster exact date 2025-10-23 or 2025-10-24? use saved machine roster below; WIN) vs FTNT 2025-11-05 (roster date 2025-11-05 or 2025-11-06? use saved roster; FAIL).
4. OKE 2025-04-29 (selloff 2025-04-30; WIN) vs MPWR 2025-10-30 (selloff 2025-10-31; FAIL).
5. CPRT 2024-09-04 (selloff 2024-09-05; WIN) vs LEN 2024-12-18 (selloff 2024-12-19; FAIL).
6. AMAT 2025-08-14 (selloff 2025-08-15; WIN) vs CPRT 2025-05-22 (selloff 2025-05-23; FAIL).
NOTE roster's `earningsDate` is controlling, not guessed headline date; if news publication time contradicts stored AH session, flag PROVENANCE CONFLICT and exclude from predictive claim but retain analysis row.

## Frozen evidence collection
For each issuer/event (12), gather original 8-K Exhibit 99.1 and dated issuer investor-relations press release physically published AFTER CLOSE earnings day, or dated slides/call prepared remarks available BY D3 close; DO NOT use later SEC 10-Q filing if issued after D3, later earnings, current FY actuals, or commentary posted after D3. Two independent website/page corroborations where ambiguities. If can't find, leave UNKNOWN with error. Record public URL(s), original publication day, price-release timing issues. News sources can contextualize expectation surprise (document actual contemporaneous analyst consensus) but must not substitute for original release. Current access date != historical as-of availability.

## Exact blind-to-feature desired coding schema (though labels previously seen)
Per event:
- `issuer_release_verified`: true only if original dated source found.
- `reported_revenue_change_yoy_pct`, `reported_eps_change_yoy_pct` optional (with GAAP/adjusted type recorded); neither is consensus *surprise*.
- `reported_margin_change_yoy_pp` if directly computable within same GAAP measure.
- `outlook_direction`: RAISED / REAFFIRMED / LOWERED / MIXED / NEW_WITHOUT_PRIOR / NO_COMP_REPORT / UNKNOWN, versus identifiable SAME FISCAL PERIOD previously issued guidance, original source citation required; do NOT map a one-quarter sequential comparison to FY estimate movement. Do not reassert old guidance-proxy filter as independent evidence.
- `explicit_demand_concerns`: PRESENT / ABSENT_IN_REVIEWED_ORIGINAL_RELEASE / UNKNOWN_UNREAD. PRESENT requires explicit documented negative business demand/volume/bookings/customer outlook, not mere generic safe-harbor; distinguish actual versus anticipated and organic vs acquisition effect.
- `explicit_material_external_constraint`: PRESENT / ABSENT_IN_REVIEWED_ORIGINAL_RELEASE / UNKNOWN_UNREAD. PRESENT requires clearly tied to business (export control/commodity/pricing/trade restriction, regional exposure), not general filing boilerplate risk.
- `identified_oneoff_charge`: PRESENT / ABSENT_IN_REVIEWED_ORIGINAL_RELEASE / UNKNOWN_UNREAD; note dollars and whether material.
- `next_quarter_outlook`: numeric and qualitative only if from contemporaneous release, no historical street comparison unless explicitly sourced at event time.
- `narrative`: anchored to evidence, preserve both positive and negative elements, original URLs and short attributed excerpts/paraphrase.
NO retrospective assigning "temporary" vs "permanent" as fact from outcome. If actual earnings day was earlier than saved roster session, flag, not silently repair.

## Primary descriptive tests and falsification
- Coverage rate 12/12 and by outcomes; if <8 originals found, stop at coverage INCONCLUSIVE, no factor tally.
- At least 5 complete matched pairs needed for any paired descriptive signs. Count pairwise **explicit_demand_concerns** (case vs control), **external-constraint** signal, and `outlook_direction` when validly measurable BOTH; all N<10 UNDERPOWERED. No regression/threshold fitting or standalone text sentiment score. Report any contradictions (positive forward outlook with failed trade, negative orders warning with successful trade).
- Distinguish historical issuer *announced* news from **surprise relative to Wall St. expectations** (unknown unless contemporaneous estimate verified).
- Even perfect 6/6 is NOT tradeable scientific edge without unseen sector/date-matched >30 pairs, option quotes, and correction for feature search. No live scanner or automated tasks changes. Save raw 12-row evidence, coding, pair results and full result summary, and update research index + Google Doc.
