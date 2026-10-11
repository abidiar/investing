# Completed PRIOR WORK + frozen 5m failed-low VWAP-volume D4 earnings rebound test: 12→91 AH
Date 2026-10-11 | VERDICT: **RESEARCH-ONLY, NOT SUPPORTED AS A RELIABLE OR PROFITABLE D4 LONG-CALL ENTRY RULE.** Strict 5m condition too sparse; VWAP confirmation did not improve entry timing on the events where it triggered. All numbers are underlying STOCK simulated price, not option ask-to-bid P&L.

## Published outside evidence — closest, and contradictory
- Miwa (2019) `Short-Term Return Reversals and Intraday Transactions` https://doi.org/10.1142/S2010139219500022 : following-week price reversals strongly linked to negative *intraday* returns, stronger in illiquid/high vol names, plausibly transient liquidity price pressure. NOT failed-low+VWAP postearnings options.
- Brogaard Han Kim working paper (last revised October 2 2026) `Intraday Price Pressures` https://papers.ssrn.com/sol3/papers.cfm?abstract_id=4731947 : 30-min issuer-idiosyncratic return residual reverses more strongly than unfiltered return shock; cross-stock portfolio model NOT D4 VWAP retail contract fill. No causal investor intent.
- Zhang et al 2024 https://www.sciencedirect.com/science/article/pii/S1057521924002485 : REAL signed order imbalance after earnings is relevant to drift/negative price reaction; a candle with high total volume is not signed buyer/seller flow.
- Berkowitz et al 1988 https://doi.org/10.1111/j.1540-6261.1988.tb02591.x : VWAP mainly execution benchmark, not independently validated reversal predictor.
- Practitioner negative evidence: Chat-Backtest Aug5 2026 VWAP reversion on SPY/QQQ https://chatbacktest.com/blog/vwap-strategy-backtest lost; Guanalyser opening range 149 stocks 9417 trades Apr–Sep2026 mean -0.013% gross and -0.053% with assumed 4bps cost https://guanalyser.com/test-bench/opening-range-breakout/ . These differ in signal/universe, don't invalidate our setup but disprove unconditional "VWAP/ORB is reliable" sweeping claims.
- Earlier Investing OS daily SMA5 and D3 RSI/MA5 164 tests already FAILED as reliably incremental, so the new 5m test was warranted and not those duplicate technical rules. Prior-work review `research/prior_work/failed_low_vwap_earnings_rebound_5m_literature_2026-10-11.md`.

## Freeze / data
First **12 events pre-selected** as six company/year/daypart/drop-magnitude matched AH earnings winners and failures, fixed release news test; froze in `frozen_12AH_D4_failed_low_vwap_volume_M5_v1_2026-10-11.md`, fetched exactly full Webull RTH five-minute OHLCV for D4/D5/D6 (12/12 complete 78 candles per day), scored no tuning. Early pilot strict entry only 1/12, it STOPPED and net -1.20% after modeled costs; VWAP only 4/12 (1 target,3 stops), stock average -0.45%/entry; buy 09:50 all12 2 targets/10 stops, avg -0.8786%/entry.

Then froze **unchanged** replication in `frozen_91AH_D4_failed_low_vwap_volume_M5_expansion_2026-10-11.md`, roster ALL 91 AH earnings selloffs (same 164 historic quality company universe, 2023–Jun2026) *before* fetching 79 remaining historical 5m events. Roster `roster_91AH_exact_D4_D6_M5_v1_2026-10-11.json`; raw 12 pilot `raw_12AH_3d_webull_M5_OHLCV_2026-10-11.json`; raw 79 further `raw_79AH_M5_expansion_part0..7_2026-10-11.json` all saved. All 91 requested retrieval complete 91/91; *3* 3-day windows span planned Black Friday EARLY-CLOSE 42-bar Nov24 2023 / Nov28 2025 RTH sessions and were predeclared invalid for >=75 regular bars (CSCO Nov22 2023 D4, PANW Nov22 2023 D4, PANW Nov26 2025 D4). **88 VALID** full-length-like 3day sequences, including 12 pilot, 76 new (of intended 79). Additional small gaps in a few low volume M5 windows MPWR 76/77 bars/day were accepted under preregistered >=75 minimum with intact 9:30–12:00 D4 and day-close checkpoints; biases remain possible if a stop/target occurred in an unavailable 5m bar.
Provider historical Webull OHLCV raw prices not same as previously saved adjusted Yahoo daily (e.g. AMAT); all entries and targets use SAME Webull raw five-minute price source. VWAP uses HLC3×five-minute total candle volume divided by summed volume, reset per trading session. This is only approximate VWAP and NOT trade signed order flow / buyer initiative.

## Exact frozen D4 trade
Seller FAILED new session low after first 15-min opening bars but before 11:15: first 5m low below any prior b0..b[k−1] lows, close back > prior trough and candle midpoint. NEXT 6 bars (with cutoff) first upward 5m close crossing *cumulative session VWAP* with bullish body, 5m total volume >= median of prior 4–6 candles, and next 5m OPEN before/noon with price <=1.5% above 9:30 opening and <=2% above failed-low candle. NEVER RE-ARM if first low failed to qualify. Compared against VWAP-only same volume and chase gates and baseline 09:50 b4 open.
Exit ALL entries +2% price TARGET BEFORE -1% stop through remainder D4+ D5+D6 (3 sessions), same candle stop first, subsequent gap exits at bar OPEN, timeouts D6 close; cost assumed 0.20% stock roundtrip. Skipped trades count 0 in per-eligible outcome; external no-trade baseline 0. No options strike, premium, IV, DTE or executable bid-ask model.

## HEADLINE 88 valid complete cohort
| Rule | Signals | Target +2 first | Stop -1 first | Timeouts | Mean modeled net STOCK return PER TRADE | Mean modeled net per ALL 88 eligible incl SKIPS=0 |
| Strict seller-failed-low + VWAP volume | **5/88** |2|2|1| **+0.2823%** | **+0.0160%** |
| VWAP-only reclaim + volume |35/88|11|22|2|**−0.1543%**|**−0.0614%**|
| D4 09:50 stock OPEN, every event |88/88|29|57|2|**−0.2028%**|**−0.2028%**|
The strict model's +0.016% per candidate is tiny and close to ZERO-no-trade, fewer than predeclared 8 signals, NOT validated and cannot justify option costs.
Attrition: new seller-failed low b3–21 in 34/88; at least one within-six-bars VWAP upward crossing after fail in 9/88; volume-qualified after fail in 6/88; chase restriction rejected one; just 5 final entries.
SIGNAL ENTRY PRICE still rose median **+0.841% from earliest observed D4 session low** at time of signal, and median **−0.425% below the D4 opening price**. While it can catch earlier than MA5, considerable move could already happen prior confirmation. Actual call premium value cannot be inferred.
**CRITICAL matched entry timing check:** On SAME FIVE strict signal events, both waiting for signal and entering at 09:50 had **identical eventual target/stop/timeout classifications** (2 target,2 stops,1 timeout). Same signal subset mean baseline net +0.31384%, strict later confirmation +0.28226%, **strict entry timing was WORSE by −0.03159pp on its own signaled sample**. All five signals only differ by whether candidate events are skipped; no conversion of loser to winner. Thus total event baseline comparison advantage (+0.219pp) is due largely to abstention/selection, not improved timing.
VWAP-only subset 35 same-event baseline net -0.14165%, VWAP-entry -0.15431%, **-0.01265pp disadvantage**. 29/35 same outcome class, 7 higher PnL, 7 lower and 21 unchanged. VWAP-only does not improve timing on selected entries.

## Detailed five strict signals
|D4 date|Company|Source cohort|5m next-open entry at|Outcome 3 sessions|Hyp stock return incl 20bps|
|2023-05-09|AMD|original92|10:00 ET|TARGET|+1.80%|
|2024-02-14|PYPL|original92|10:20 ET|TARGET|+1.80%|
|2025-05-06|OKE|separate72|10:20 ET|STOP|-1.20%|
|2025-05-14|FTNT|separate72|10:25 ET|STOP|-1.20%|
|2025-08-21|CSCO|original92|10:10 ET|TIMEOUT|+0.2113%|
(A raw timestamp in file is UTC; printed times translated by -4 hours EDT for May-Aug, -5 hours EST for February.) All five under same buy D4 9:50 target-stop categories. Five trigger days spread across years but hardly any observations.
**By company-group:** original92 62 valid cases 3 signals (2 TARGET/0 STOP/1 timeout, mean +1.27% per 3), different-company72 26 valid cases 2 signals (**BOTH STOP**, -1.20% each); confirms no disjoint company replication, 2026 AH valid13 had ZERO strict signals. 12 historical pilot 1 stop; nonpilot remaining 76 valid4 signals, 2 targets 1 stop 1 timeout, only +0.0344% per remaining qualified event incl skips. A favorable result in full aggregate hides stark issuer group instability and tiny n.

## Conclusions
- Genuine failure of sellers to make new low + confirmation of higher volume may be a valid **market microstructure concept**, academic literature supports transient stock-specific price pressure reversal. But retail **five-minute OHLCV total volume + VWAP** is a *weak proxy* for actual informed buying or whether earnings damage will persist. We did not verify mechanism.
- VWAP alone was unprofitable as executed in this afterhours earnings study. Strict combo too RARE, tiny positive per-event mean indistinguishable economically from staying in cash, not portable across issuer cohorts. It did NOT generate better trade exits on its 5 signaled cases versus earlier 9:50 entry and no +2 before−1 guaranteed even after confirm. D4 underlying 2% targets can produce highly nonlinear call profit or loss; need real NBBO/IV/time-decay.
- User wants early entry before upside option becomes too expensive. These signals appeared ~10:00–10:25am ET and at ~0.8% above low; buying cheap calls STILL not established because five event outcomes and time-declining call value not modeled.
- Prior academic and user research suggests **stock-specific, sector-neutral residual pressure + genuine EPS forward expectation stability** are conceptually more promising than adding indicators. A point-in-time historical **trade-signed flow / depth** source or richer investor evidence would test mechanism; avoid gratuitous new signal thresholds based on known outcomes. Better next clean design needs different years/companies truly unseen and contract-level options NBBO with sufficient n, no paid data.
**No scanner/automation changes.** Verdict: research-only NOT SUPPORTED. Do not optimize volume≥0.8/1.2, no forced modification because n5. 
## Reproduce
- Prior work `research/prior_work/failed_low_vwap_earnings_rebound_5m_literature_2026-10-11.md`
- Original pilot freeze `research/earnings_recovery/frozen_12AH_D4_failed_low_vwap_volume_M5_v1_2026-10-11.md`, results `research/earnings_recovery/D4_failed_low_vwap_volume_12AH_M5_pilot_results_2026-10-11.json`
- Extension freeze `research/earnings_recovery/frozen_91AH_D4_failed_low_vwap_volume_M5_expansion_2026-10-11.md`
- Machine data & exact events `research/earnings_recovery/D4_failed_low_vwap_M5_91AH_full_expansion_results_2026-10-11.json`
- Executable Node `research/earnings_recovery/run_91AH_D4_failed_low_vwap_M5_v1.mjs`
- Raw M5 `research/earnings_recovery/raw_12AH_3d_webull_M5_OHLCV_2026-10-11.json` and `research/earnings_recovery/raw_79AH_M5_expansion_part0..7_2026-10-11.json`
