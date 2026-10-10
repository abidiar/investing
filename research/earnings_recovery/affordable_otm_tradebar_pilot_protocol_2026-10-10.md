# Frozen extension — affordable OTM historical call pilot (2026-10-10)
Status: EXPLORATORY. Frozen before inspecting OTM option contract outcome data. Inherits source and safety from research/earnings_recovery/options_execution_model_protocol_2026-10-10.md and its prior-work note.

## Exact events (no substitutions)
1. DELL qualifying selloff 2025-03-03, original92
2. QCOM 2025-07-31, original92
3. PYPL 2025-02-04, original92
4. AMAT 2025-02-14, holdout72.

Compare each frozen entry: third-session opening and first three-rising-lows + previous-two-high breakout, enter next opening. Stock exit: +5% underlying versus -5% stop, up to 20 entry-inclusive sessions, stop-first if daily highs and lows straddle both. No manual event retiming.

## Contracts & a strict $50 debit cap
Only *historically listed standard US equity 100-share calls*, not synthetic strike options. For each of eight entry events and two expiry buckets, choose the first actually listed Friday/standard option expiration date ON/AFTER the entry date plus 30 and 60 calendar days (no more than seven days after the nominal target). If no contract is found, mark missing. Strike OTM only: strike > unadjusted entry stock opening price and <=125% of that price. Among those contracts choose the **closest-to-spot** strike whose same-entry-day **first reported options trade price** multiplied by 100 plus an illustrative $0.65 commission <= $50. Entry bar day option volume >=10 contracts and trade open >= $0.01. If closest strike has missing option first-trade price, or volume lower than 10, scan more OTM until one qualifies, without examining subsequent price bars for strike selection. If NONE qualifies, mark no eligible affordable contract, do not impute a premium. Contracts with adjusted deliverables other than 100 shares are not eligible. This is a retrospective price-availability screen, not a real-time executable quote strategy: daily first trade is asynchronous to 9:30 stock open and cannot be known beforehand.

## Price and result
Massive historical option daily TRADE OHLC (option open on entry calendar day, option close on stock-exit calendar day), use *gross first-trade/open to last-trade/close* return for observational illustration and optional illustrative $0.65 on buy and sell costs; no guaranteed bid/ask execution. Exits if option bar missing on stock-exit day: MISSING, not zero or option expiry worth 0. If contract expires before underlying exit, liquidation at final available pre-expiry close; flag expiry truncation and missing bars. Record entry-day and exit-day volume, daily price range and OHLC. No modeled IV extrapolation or strike substitution from the later successful cases. Check source stock raw unadjusted/open against Webull adjusted bar and flag splits/corporate actions.

## Coverage and decision
Predeclare full 4 * 2 * 2 = 16 planned observations. State number of events, entries, expiry buckets, contracts screened, eligible, missing and rate-limited. A four-company historical pilot only tests data feasibility, not profitability or statistical edge. If no entitlement to options NBBO quotes or rate-limited historical prices, mark inconclusive and do not claim actual options ROI. No production promotion. Don't buy data.

## Data-collection discipline
Provider calls may be rate limited. Keep every returned price/contract record and absence; do not treat warnings as price data. Compare with earlier 164-event model as separate theoretical data; do not pool descriptive option-bar yields with theoretical priced returns.