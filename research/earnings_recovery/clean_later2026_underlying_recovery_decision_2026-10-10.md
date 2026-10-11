# Clean later-2026 earnings-selloff stock-only recovery test — completed

Research date: 2026-10-10. Status: **executed, underpowered, not an A+ trading edge**.

## What was frozen BEFORE looking at outcome stock paths
1. All 61 distinct companies previously quality-qualified in the prior 164-event research, without excluding or manually adding names after knowing post-earnings returns. **New 2026 financial quality was not independently re-screened point-in-time**. Universe freeze: `frozen_jul_sep2026_clean_stock_rebound_test_protocol_2026-10-10.md` and commit `0ace7f64e58706112099c85083571aaee5d16021`.
2. SEC-linked Quant500 announced earnings date/time and ONE-DAY first reaction CLOSE <= −5% between 2026-07-01 and 2026-09-04 inclusive; this is intentionally narrower than the earlier two-session window. No earnings dates after September 4 selected to limit unresolved exits. All 61 issuer discovery records and qualifying 15 events were separately frozen and COMMITTED before any subsequent stock-price outcome retrieval. Source event list `frozen_jul_sep2026_earnings_selloff_discovery_2026-10-10.json`.
3. Compare **day3** after selloff opening versus **three-rising-lows plus previous-two-high CLOSE breakout** first signal occurring selloff days 3–20, enter following open, skip if chase >8% above selloff close. Both entry strategies use unadjusted actual historical stock OHLC; +5% target, −5% stop from respective entry opening, first touched wins with adverse stop-first ambiguity, maximum 20 entry-inclusive sessions; gaps filled at actual open, day20 time exit at close. No options, fees or spreads.
4. Decision required >=20 distinct qualifying events, >=60% successful confirmation targets among **all** events including skips, +10 percentage points target-hit advantage over day3, and positive mean paired gross-return advantage, before entertaining further confirmation research. NO promotion to production/A+ from one late-2026 period even if all passed.

## Event selection/source completeness
- Precommitted issuer universe: 61 distinct earlier quality-pass companies.
- Quant500 SEC-linked earnings pages: 55 had machine-readable announcement AND closing reaction data, six had announcements but lacked usable reaction-price rows (**AMAT, HON, HPE, REGN, WAB, ZBH**). Their reaction-date eligibility/outcomes were UNKNOWN, not considered non-selloffs.
- Exactly **15 first-session <=−5% earnings selloffs** frozen; all 15 had subsequent as-traded Yahoo stock bars recovered and reaction-return reconciliation within 1.0 percentage point, so **15/15 outcome-evaluable**. The 15 are: ISRG 7/17, NFLX 7/17, HAL 7/21, CMCSA 7/23, GOOG 7/23, GLW 7/28, UPS 7/28, KLAC 7/29, COIN 7/31, AMD 8/05, CVS 8/05, EOG 8/05, CSCO 8/13, TPR 8/13, PANW 9/02 (all dates 2026).
- Outcome snapshots fetched ONLY after event list saved in a separate earlier commit, using Yahoo chart `quote` OHLC **not dividend-adjusted AdjClose**, restoring split units when needed, through **2026-10-09**; all trades resolved (no right-censored event in this 15-company cohort).

## Results

| Outcome | Day-three following selloff open | First three-rising-lows breakout -> next open |
|---|---:|---:|
| Fixed eligible earnings selloff events | 15 | 15 |
| Trades executed | 15 | 10 |
| +5% profit target before −5% stop | **8** | **6** |
| −5% stop first | 4 | 4 |
| 20-session time exit | 3 | 0 |
| No trade due to chase >8% | 0 | 4 |
| No signal | 0 | 1 |
| **Target wins as percentage of ALL 15** | **53.33%** | **40.00%** |
| Win% among only executed trades (selection-biased) | 53.33% | 60.00% |
| Mean gross return per **ALL 15**, skips zero | **+1.440%** | **+0.648%** |
| Mean gross return among executed trades | +1.440% | +0.972% |

In the **10 events where BOTH strategies actually traded**, the rising-lows setup had a small **+0.949 percentage-point paired average gross-return difference**, with three events favoring confirmation, three favoring day3, and four equal. But this is **conditional on the future event producing the rising-lows entry**. Across the actual 15-event investment opportunity set, confirmation had FIVE no-trades; FOUR of those five were day-three target winners (CMCSA, KLAC, COIN, PANW). The fifth CSCO day-three timed out at approximately −1.50%. Confirmation missed sizable, important gains; its 60% win% among executed events thus MISLEADS relative to overall capture rate.

Notable disagreements:
- HAL: day3 hit −5% stop, confirmation subsequently hit +5% (confirmation helpful).
- GLW: day3 gap-stopped −6.19%, confirmation hit +5% (helpful).
- AMD: day3 hit +5%, confirmation later gap-stopped roughly −5.17% (harmful).
- UPS: day3 timed out ~−0.06%, confirmation hit −5% (harmful).
- Chase skips of CMCSA, KLAC, COIN, PANW all gave profitable day3 outcomes; don't cherry-pick them away.

**All four ex ante promotion decision gates did NOT pass:** sample under 20, confirmation event-level 40% target rate below 60%, confirmation target hit 13.33 percentage points BELOW baseline instead of >=10pp above, even though within-only-paired mean is positive. A retrospective single-quarter 15-event comparison cannot establish that **day3 itself is reliably profitable**. It earned an indicative +1.44% per event **gross stock percentage**, and eight target hits, but has no market-matched passive comparator, commissions/slippage, and contemporary company quality recertification; issuer-survival and Quant500 missingness biases remain. The test only supports REJECTING the claim that the frozen confirmation improves full-event recoveries.

## Decision / stop rule
**No go on three-rising-lows confirmation as a reliable earnings-rebound CALL entry.** Do not spend more cycles optimizing 10am option execution, 30/60 DTE or theta based on it. Day3 was better in this narrow period but is NOT a validated A+ call strategy, so don't recommend it for actual trading as proven. Do not silently extend threshold hunting or select only breakout winners from the 15.

This fulfilled the user's clean next priority. A truly independent stock test on a future quarter could resolve whether day3 edges above chance/market control; further digging now is not required.

## Reproducibility
- `frozen_jul_sep2026_clean_stock_rebound_test_protocol_2026-10-10.md`
- `frozen_jul_sep2026_earnings_selloff_discovery_2026-10-10.json` (15 event names, 61 issuer coverage and historical earnings reaction only; committed before future price download)
- `discover_jul_sep2026_earnings_reactions_preoutcome.py`
- `clean_jul_sep2026_stock_recovery_actual_outcomes_2026-10-10.json` (complete actual wins, stops, returns, no trades and decision gates)
- `clean_jul_sep2026_stock_recovery_stock_bars_2026-10-10.json`
- `run_clean_2026_stock_only_two_entry_test.py`
- `.github/workflows/earnings-clean-2026-freeze-list.yml` and `.github/workflows/earnings-clean-2026-stock-outcomes.yml`.
