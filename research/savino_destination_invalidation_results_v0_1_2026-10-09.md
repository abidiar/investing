# Savino as destinations — v0.1 six-session pilot RESULTS
Date: 2026-10-09
Rules frozen first: research/savino_destination_invalidation_test_v0_1_frozen_2026-10-09.md (commit a25e80c7495eb9a696d1c014dbf424cc7abcd828).

## Conclusion — descriptive, no demonstrated edge
The independently defined first opening-range + VWAP confirmation signal produced one SPY entry per each of the six preselected dates. Using previous-known-close SPX/SPY ratio to translate posted Savino SPX price levels into approximate SPY destinations:
- Nearest Savino target reached BEFORE independent structural stop: **3/6** first signals.
- Savino target available in trade direction: **5/6**; one had no next posted level in direction.
- Savino targets offering >=2.0R at the independent entry: **1/6**; **0/1** reached target before stop.
- The three target-first outcomes paid only ~0.26R, ~0.29R, ~0.47R (ex ante price target distance / structural stop distance). A touch is not equivalent to a viable trade.
- Savino destination outcomes across six: TARGET_FIRST 3, STOP_FIRST 1, NEITHER 1, NO_TARGET 1.
- Fixed spacing controls, each on SAME six entries/stops, hit target before stop: five grid offsets [0, 5, 10, 15, 20] => **[4/6, 2/6, 3/6, 2/6, 4/6]**. Prior-day high/low => **2/6**. These have different target distances and are not a true distance-matched fairness test.
- No evidence from this small selected-sample pilot that Savino destinations beat basic price-grid benchmarks, and NO indication they should be trading signals or A+ promoters.

## Input price data
- Webull SPY full RTH 5m OHLCV, **exactly 78 completed five-minute bars per session** on all six dates; queried on 2026-10-09 using connected Webull.
- Webull previous trading-session SPY daily high/low/close.
- Previous-session SPX closes from Yahoo Finance S&P 500 historical table: https://nz.finance.yahoo.com/quote/%5EGSPC/history/
- Prior-close SPX/SPY index/ETF ratios were derived per date before signal; NEVER use contemporaneous daily close.
- Exact SPX M5 NOT obtained (Massive index data returned NOT_ENTITLED). Therefore **proxy only**; near-level interactions can be inaccurate due to the shifting SPX-SPY basis.
- Preposted Savino level sets archived in September repo and user screenshots for October 2/8.
- Raw exchange Webull OHLCV bars intentionally NOT republished into the repository; preserves derived observations and API retrieval specification to respect potential provider licensing.

## Recorded first independent signals and Savino destinations
Five-minute candle times below Eastern Daylight Time (UTC minus 4).

| Date | OR+VWAP first signal candle | Next-bar executable entry | Structural stop | Savino T1 SPX (proxy SPY) | R:R to T1 | T1 before stop? |
|---|---|---|---|---|---:|---|
| 2026-09-25 | 10:00 SHORT | 10:05 @ SPY 767.580 | 770.360 | 7700 (766.769) | 0.292R | YES |
| 2026-09-28 | 10:35 SHORT | 10:40 @ SPY 766.435 | 767.510 | 7689 (765.930) | 0.470R | YES |
| 2026-09-29 | 10:45 SHORT | 10:50 @ SPY 764.500 | 765.790 | 7649 (762.154) | 1.819R | NEITHER |
| 2026-09-30 | 10:00 LONG | 10:05 @ SPY 768.590 | 767.010 | 7719 (768.998) | 0.258R | YES |
| 2026-10-02 | 10:20 LONG | 10:25 @ SPY 772.350 | 771.140 | No higher posted level | N/A | NO TARGET |
| 2026-10-08 | 10:05 LONG | 10:10 @ SPY 775.810 | 775.090 | 7813 (778.339) | 3.512R | NO — STOP FIRST |

NOTE: Signal candle timestamp is candle *start*. Confirmation arrives when that five-minute candle closes, so the next-bar entry time is the actual possible execution time. This table previously generated from code values returned by Webull. Fixed stop is a 2-bar extreme plus $0.05 buffer, not a Savino stop; Savino's invalidation role must be researched separately.

## Paired comparison — first entry per date, same stop
| Destination policy | Target first of 6 |
|---|---:|
| Nearest Savino next level | 3 |
| 25-SPX fixed grid, anchor prev SPX close, offset 0 | 4 |
| Grid offset 5 | 2 |
| Grid offset 10 | 3 |
| Grid offset 15 | 2 |
| Grid offset 20 | 4 |
| Previous session high for LONG / low for SHORT | 2 |

Grid controls can hit more often simply because their first qualifying line is nearer. Do NOT interpret comparative counts as a rigorous distance-adjusted outperformance claim.

## Important failure modes seen
1. An independently valid-looking OR+VWAP LONG on October 8 at 10:10 was stopped before the next Savino upside target, ahead of the subsequent selloff. This demonstrates the importance of signal selection; a level map does not determine direction.
2. September 25, September 28, September 30 did touch next Savino destinations first — but each offered <0.5R against the prescribed structural stop. They would fail the frozen A+ fresh >=2:1 qualification regardless of the later touch.
3. October 2 had no posted upside target beyond the independent long entry. Do not invent an extension or use the highest posted line as a late entry destination.
4. Six user-shared dates are selection-prone. The study is retrospective and includes no unexposed out-of-sample observations.

## Follow-up (separately freeze v0.2 before new outcomes)
- For destinations: compare first qualified A+ / 11:00 research-only candidate against Savino targets, previous-day technical destinations and carefully matched equal-distance nulls; test 30–50+ complete posted days.
- For invalidation: predefine whether failure-to-reclaim a broken Savino level or confirmed acceptance back through it improves stop placement versus M5 structural extremes; use *the same independent entries* and account for risk widths before comparing.
- For precision: get entitled **SPX M5** rather than SPY proxy before claiming exact line/sequence hit rates.
- Retain frozen A+ v1.0 and 11:00 state-change spec unchanged; never relabel past trades because Savino map looked accurate afterward.
