# Oversold rebound v2 — discovery specification (2026-10-15)

Status: PROSPECTIVE RESEARCH CHANGE ONLY. NO TRADE, NO ORDERS. Frozen 4D/A+ and execution gates unchanged. This is not a validated trading edge.

## Universe
Liquid US common stocks with price >= $5, 20-day median dollar volume >= $20m, at least 60 daily bars; exclude ETFs, halted symbols and stocks with unreliable bars. These are operational starting filters, not optimized alpha thresholds. Log universe and exclusions as of timestamp.

## Four independent discovery lanes (union, not intersection)
A. Oversold: 3–10-session drawdown, RSI2/RSI14, ATR-normalized decline, support distance and abnormal volume. Record raw features, not just rank.
B. Failure-test: pre-existing pivot from prior completed bars, marginal undercut (express in ATR units), swift reclaim, later confirmed higher low and participation from completed M5 candles. No single VWAP reclaim/two bars qualify. Partial sequences still discoverable as WATCH.
C. Relative resilience: recovery from session low and performance versus SPY, QQQ, sector ETF and same-day ATR-matched nonselloff controls. Avoid absolute rebound-size ranking alone.
D. Catalyst recovery: original dated catalyst and verified guidance/orders/margin revisions; INTACT/WORSENING/MIXED/UNKNOWN. UNKNOWN never equals INTACT.

## Selection and logging
Build a broad union across all lanes BEFORE choosing at most five to display. Preserve all screened symbols, pass/fail and lane membership, ranked and nonranked names, reasons for rejection, as-of source timestamps and peer definitions. Deduplicate by symbol. A candidate can enter from any lane; no RSI-only cutoff. Select final five by documented, predeclared multi-criteria process: structural progress, room to resistance, relative resilience, verified fundamental context and event risk. Do not train or tune weights using HOOD/MU October 15 outcomes. Keep HOOD/MU as diagnostic holdouts and perform blind as-of reconstruction separately.

## Execution separation
Discovery WATCH is not BUY. Next-session 10:30–12 ET confirmation remains PENDING until observed. Entry requires pre-existing pivot, marginal breakdown, swift rejection, later higher low, completed candle participation, independent stop, >=2:1 reward/risk to genuine resistance from actual entry. Log +2/3/5 references without treating them as targets. Hanna CBI/TomOscillator/breadth thrust missing => REGIME EVIDENCE UNKNOWN. Option chain executable bid/ask, strike, DTE, delta, IV, 1-contract premium, theta and slippage required; else OPTION NOT VERIFIED / NO OPTION.

## Evaluation
Prospective forward-only snapshots at 15:00 ET and 10:30–12 next session, record all WATCH/NO TRADE, nonselected candidates and same-day sector/ATR-matched controls. Assess target-first and stop-first path, gaps, transaction costs, options affordability where available. Compare discovery recall, false positives, realized net performance and matched-control excess returns. Maintain 283-event negative audit and 49-name independent negative failure-test context. No threshold fitting on exposed events.
