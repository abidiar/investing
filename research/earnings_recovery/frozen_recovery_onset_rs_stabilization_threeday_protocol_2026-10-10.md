# Frozen recovery-onset discriminators — compact historical audit
Frozen 2026-10-10 (before fetching NEW 3-session outcomes for this factor specification).

## What is being tested
Question: after quality-company earnings selloffs, which known-at-entry factors identify *immediate* 1–3-session rebound strength among a clearly defined price-repair entry signal, rather than the eventual recovery over months? This is **an exploratory stock-path proxy for META-style rapid option repricing**, NOT an executable options backtest or a previously observed winning condition.

## Cohort and split
ALL original 164 saved historically quality-screened selloff events 2023–June 2026 from `actionable_bounce_event_price_windows_164_2026-10-10.json`, with original92 and separate-company holdout72 reported independently. Existing event outcomes have been analyzed before: neither group is blind, but this exact new three-session primary endpoint and feature definitions are frozen before new retrieval. All no-signals and missing prices remain in denominator. Original92 development, holdout72 replication only; don't move thresholds based on data.

## Data and timing
Fetch unadjusted-as-traded stock daily RTH price OHLC from Yahoo historical quote bars, never dividend adjusted 'Adj Close'; undo later splits to calculate nominal as-traded basis. Fetch SPY identical dates, and compare same split-normalized relative performance. Exclude/no result for split during trade and label price-feed mismatches. No candle information after the signal date may enter the feature calculation.

First *price-repair* signal using already frozen original SMA5 reclaim:
  - Scan 5–20 trading sessions after the qualifying selloff day. Signal at session k CLOSE when close[k] > SMA5(close[k-4..k]), close[k-1] <= SMA5(close[k-5..k-1]), and close[k] > high[k-1]. Choose FIRST qualifying close, enter NEXT daily regular-session OPEN (k+1).
  - The previously declared no-chase screen applies unchanged: if the signal's next opening price > 1.08×the selloff day close, SKIP event; no late attempts. This uses next opening for a pass/fail that can be decided at order placement (not a blind market-on-open fill). Outcomes count event coverage and no-signals.
  - Features are read at k close, **before** the k+1 stock entry. Signal does not rely on intraday VWAP or real-time option prints.

Exactly TWO intended ex ante binary discriminators:
  1. **relative_strength**: 3-session stock close-to-close return (close[k]/close[k-3]-1) minus SPY's close-to-close return over exact same signal and k-3 dates >= +1.0 percentage point, observed by signal close.
  2. **stabilized_lows**: low[k-2] <= low[k-1] <= low[k] (three consecutive rising or flat daily lows), observed by signal close.
Also evaluate combined AND filter and four disjoint 2×2 groups; do not select a 'winning' threshold after seeing outcomes. Record initial event selloff severity, signal-day lag, price runway below pre-earnings close only as descriptive (NOT screen) to identify next candidate research, no multiple post-hoc significance claims.

PRIMARY endpoint: after stock purchase at the next session OPEN, price HIGH reaches +1.5% before LOW breaches −1.0%, within THREE entry-inclusive daily sessions; opening price gap checked first on subsequent sessions; if both intraday touched, STOP first. If neither, sell at third session closing price. No commission/slippage/spread. Positive is a **+1.5% STOCK move**, not an option gain. Record wins, stops, timeouts, mean 3-session gross returns, times to target; compute outcome differences both *per triggered signal* and *per all qualifying events*, with no-trade=0. Compare signal/filters with day3 third-following-session OPEN under SAME primary endpoint on same cohort and paired subset, not compare unlike risk targets. SPY three-session absolute return at matching entry as market context, if available.

**Success bar:** relative-strength/low-stabilization combined filter has >=20 triggered qualifying events in separate-company holdout72, increases target-before-stop rate by >=10 percentage points among holdout price-repair signals relative to first-price-repair trigger without feature filter, AND does not reduce +1.5%-before−1% successes as fraction of ALL holdout events; profitable after plausible commission/spread remains UNKNOWN. If sample fewer than 20 or misses opportunity capture, call INCONCLUSIVE/NOT USEFUL, and DO NOT promote or optimize thresholds on that cohort. Report raw differences and ticker-cluster uncertainty, no false confidence. If no systematic result, stop feature fishing.

This deliberately tests only price repair and SPY-relative strength DAILY proxies because full historical synchronized 5-minute VWAP/sector option quotes have not been demonstrated available. 5-minute VWAP, sector-relative RS, analyst upgrades, guidance revisions, 10am genuine call bid/ask, 2–4-week calls, and delta are NOT measured. This is not the actual META 0DTE overnight setup and does not test every kind of rebound trade.
