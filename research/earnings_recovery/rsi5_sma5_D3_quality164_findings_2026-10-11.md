# D3 RSI5 / SMA5 and VWAP feasibility findings across 164 quality earnings selloffs
**Date: 2026-10-11. Verdict: RESEARCH-ONLY, NOT SUPPORTED AS A D4 BUY-CALL FILTER.** We tested the early daily RSI and SMA data; did NOT have historical 1m/5m OHLCV for actual session or anchored VWAP and cannot claim to have tested them.

## Why these indicators might matter
- **RSI5 (Cutler arithmetic)**: very short daily close momentum/exhaustion, not whether company forward earnings have truly stopped deteriorating.
- **SMA5 distance & slope at D3**: early 5d closing-price repair, speed at which downside momentum is weakening. A higher MA5 at D3 relative to D2 or a less negative slope may indicate less deteriorating price, but not buyer-initiated flows.
- **Session VWAP on D4 and anchored VWAP from earnings selloff D0**: weighted intraday participants’ volume-weighted execution benchmark; price above/holding/reclaiming with high-volume 5m candles is a plausible EARLY entry confirmation, rather than a delayed daily MA5 crossover. Need historical 5m OHLCV or intraday tick data; 164 canonical archived source windows contain only 77 DAILY OHLC bars with 6 preevent bars. Daily bars cannot reconstruct session VWAP, order imbalance or anchored volume reliably. RSI14 Wilder requires more preevent price history and warm-up than the archived 6 sessions; not tested here.
- Prior published broad caution Fang/Qin/Jacobsen (2014) `Technical market indicators: An overview` https://www.sciencedirect.com/science/article/pii/S2214635014000495 : testing 93 technical proxies found little dependable stock-market return predictability with generous assumptions; need pre-frozen single incremental test and no optimization. Schwab VWAP explainer https://www.schwab.com/learn/story/how-to-use-volume-weighted-indicators-trading : price is volume-weighted, institutional execution benchmark, not a causal buyer identity signal.
- Da/Liu/Schaumburg (2014) actual nonfundamental residual reversals require analyst cashflow estimate changes and liquidity context; RSI/MA alone can't represent it https://doi.org/10.1287/mnsc.2013.1766.

## Previously FAILED related test — avoid duplicate mining
`recovery_onset_164event_rs_stabilization_factor_results_2026-10-10.md` previously tested LATE D5–D20 first SMA5 crossing plus close above prior high followed next-session OPEN, +1.5% target before−1% stop, 3-day window: 130 triggers, 52 target first; SPY RS>=1pp and 3 rising lows both failed incremental promotion gates. Earlier repair and RSI5 data families are NOT proven independently.

## Exact new test
Froze `frozen_d3_rsi5_sma5_quality164_exploratory_2026-10-11.md` after required academic and internal prior review, **before D3 feature/label correlations**. Same 164 earnings-qualified dated events 2023–June2026 (91 AH, 73 BMO), two previously outcome-exposed labels: D4 OPEN hypothetical STOCK +3% target before −5% stop over 20 entry-inclusive sessions, and separate full preearnings close recovery any close by D60. Pre-D4 close D3 features **four**, no thresholds: RSI5 Cutler on five close-to-close deltas, change RSI5 D1→D3, D3 close relative to MA5, D2→D3 MA5 slope. These are pre-D4, not RSI14. Count winner/loser medians for whole164, AH91, AH D1–D3 deeper low54, original92 and separate72; replicate original stock-sector ETF same year/release session/sector/similar shock matched control pairs: D4 43 total (25 AH), D60 34 total (20 AH). Nothing retrained/optimized and no lookahead features.

Results *all 164* D4 targets99 vs stop/timeouts65:
- RSI5 D3 median **20.90 winners vs 16.70 failures** (weak separation, both extremely oversold because original earnings shock is in 5d window).
- D3 stock price versus SMA5 median **−1.797% vs −1.797%** (effectively identical).
- SMA5 slope median **−1.573% vs −1.871%** (winners downward MA slightly less steep).
- AH91 D4 target58 vs nonwinner33: RSI5 median 19.61 vs17.11, distance MA5 -1.89% vs -1.74%, SMA5 slope -1.75% vs -1.89%. Shows no clean MA5 relationship.
- All 164 D4 stock trading unconditional previously **−0.312% mean after hypothetical 20bps cost**, still no RSI rule tested by binning due to no legitimate cutoff search.

**Strict matched D4 stock WIN vs FAILURE, 43 pairs**: winner RSI5 higher 24/43 (two-sided sign p=.542); SMA5 distance higher 24/43 (p=.542); SMA5 slope higher 26/43 (p=.222); RSI5 D1→D3 higher 17/43 (p=.222). AH subset RSI5 higher just 12/25; MA5 distance higher 13/25; MA slope higher 15/25. No consistent or significant D4 indicator.
**Strict matched eventual FULL D60 recovery (34 pairs)**: RSI5 higher 21/34 (p=.229); MA5 distance higher 23/34 (p=.0576); **MA5 slope higher 24/34 (median winner−loser +0.723pp, p=.0243 UNCORRECTED)**, AH 14/20, original15/23 and separate9/11. However this was **four correlated factors × two outcome definitions**, so multiplicity correction gives p_adj≥0.194 for best slope and no independent proof. Could be momentum before recovering and selection-to-60d, not entry or economic cause. Underlying D4 matched first hit did not separate by slope.
AH54 additional lower low by D3: 38 D4 targets, 16 stops: RSI5 medians 15.88 vs14.34, MA5 distance -2.94 vs -2.49%, MA5 slope -2.06 vs -2.31%; no unambiguous discriminator.
All outcomes already known, company/event clustering and tech sector concentration from previous ETF study; no historical actual options bid/ask or IV. Do not promote MA5 slope RSI into scanner. A stock can be technically oversold while future EPS is getting cut, and can bounce while RSI remains low.

## Answer to user
**YES**, price indicators can test a narrower mechanism—*is selling actually losing momentum and buyers accepting higher prices*—but cannot reveal WHY analysts will revise up company future cash flows or whether a temporary liquidity shock has ended. Use tiers:
1. Earnings dislocation characterization: quality, disclosed future earning impairment and stock-versus-industry shock (exploratory signal, cannot use naive -7pp thresholds).
2. Downside exhaustion: is price unable to make a new low despite attempts (e.g. 5m higher low, no follow-through under D3 low), and participation/volume visible by SIGNAL time.
3. Early intraday buyer acceptance: 5m session VWAP reclaim/hold with volume, higher low and buyer initiative, NOT late D5–D20 daily SMA5 crossover; anchored VWAP from D0 is secondary reference, not magical reversal line.
4. RSI5/14 and MA5 are secondary descriptive "context" not standalone triggers; require price not too extended since option profit mostly comes from first part of rebound. Do not combine all indicators naively; overlapping price derivatives double count.
5. For trading evidence need actual intraday historical 5m OHLCV and timestamp, earliest entry D4 9:50 or when reclaim confirmed, outcomes on *underlying* first +2/+3 before -1/-2 with bid/ask option premium at intended same time. The 164 daily OHLC panel cannot evaluate these intraday rules; do not pay unless authorized.
One clean priority: collect/connect already available free Webull 5m historical bars for a preregistered, supported event subset and save with dates, confirm source dates and volume. Freeze VWAP/seller-failed-low rule against an explicit matched D4-open and no-VWAP baseline BEFORE seeing forward stock/option outcomes, and do not assume a positive VWAP is institutional flow.

## Reproducibility
- Prior review `research/prior_work/earnings_recovery_rsi_ma5_intraday_vwap_tech_indicators_2026-10-11.md`
- Frozen `research/earnings_recovery/frozen_d3_rsi5_sma5_quality164_exploratory_2026-10-11.md`
- Runner `research/earnings_recovery/run_rsi5_sma5_asofD3_quality164_v1.mjs`
- Data `research/earnings_recovery/rsi5_sma5_164_D3_features_results_2026-10-11.json`
- This readout `research/earnings_recovery/rsi5_sma5_D3_quality164_findings_2026-10-11.md`
