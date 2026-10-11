# Pre-outcome frozen protocol — established double-pivot support failure (2022 independent calendar, version 1)

**Frozen on October 11, 2026 prior to examining ANY new 2022 candidate, D+1 or D+2 pattern outcomes.** Not an authentic published Adam Grimes backtest; this is a *Grimes-inspired algorithmic significant-support* test designed to distinguish an established support zone from the prior-session-low experiment. Existing 2023 price-only results and 2024-25 broad oversold outcomes were already exposed and this new test is motivated by them. Do not claim preregistration before all reversal research. 2022 is separate calendar from 2023/2024-25 studies, but universe comes from later-available 2023 archive, creating possible survivor and selection bias.

## Universe, period and data gating

- Exactly **90 predeclared US equities**, full list saved in `data/grimes_2022_pivot_support_universe_frozen_2026_10_11.json`. Chosen as all distinct historical stock symbols in the five previously archived 2023 v4 daily batches, **NOT** selected from returns or 2022 outcomes. No adding/replacing tickers to improve results. Delisted/unavailable stocks are UNKNOWN, never silent omission.
- Eligible dates are **2022-01-03 to 2022-10-31**, inclusive. Retrieve adjusted historical daily bars through **2022-10-31 only** for feature discovery, with earlier history going back far enough (2021-06-01 requested) for at least 130 trading sessions; **do not retrieve D+1/D+2 five-minute bars until the entire candidate manifest, with dates and support prices, has been written and committed**.
- Standard regular-session daily bars, sort by exchange-local session date; compare *consecutive trading days*, not calendar days. Use daily data `D0` known only after close for pattern eligibility; D1 is the next exchange session.
- Missing, duplicate, out-of-order, invalid, truncated, or unexpected share-basis data remain `UNKNOWN`, not substituted. Source OHLC must have low <= open/close <= high, positive prices, nonnegative volume, and enough trailing daily history. Stock splits and corporate-action mismatches may limit valid cases.
- No hidden exclusion based on event outcomes. Mark observations with incomplete support history or missing vendor daily coverage `UNKNOWN`. If 2022 sample is too small, report underpowered and **do not** silently widen criteria, dates, or issuer universe.

## Objective established support definition (strictly as-of D0)

For each symbol/date D0 in date range:
1. D0 close-to-prior-close return <= **-3.00%** and D0 total regular-hours volume / mean D-20 through D-1 volume >= **1.20**. D0 close strictly above 0; previous 20 volumes must be valid. Record predeclared severe-selloff stratum <= -7%, but primary cohort is -3%.
2. Examine **120 consecutive preceding trading sessions D-120..D-1** and identify *confirmed 3-left / 3-right daily pivot lows*: low at index i <= each of its 3 preceding and 3 following session lows; right-hand confirmation must have completed no later than D-1; pivot day itself must be **at least 10 trading sessions before D0**. Tie pivots resolve by chronological earliest index (the same low plateau cannot generate artificial pairs).
3. Find **two such confirmed pivot lows separated by >=5 trading sessions** and priced within **1.00% of each other**, symmetric relative difference `abs(a-b)/min(a,b) <= 0.01`. Choose the **most recent pair** based on later pivot date; tie choose latest earlier pivot; no outcome-driven choice. This is a double-pivot established support reference. The exact support = **minimum of their two daily pivot LOW prices** (basis-adjusted).
4. Require all daily closes from the second/latest pivot through D0-1 >= **0.99 * support**: otherwise support was decisively broken before D0 and the pair is INVALID; do not look for alternate earlier pairs (for determinism, perform pair selection first, then this validity check). D0 close must be in range **[support, 1.04*support]** so the support is still intact and nearby at decision time. D0 intraday low may puncture, but D0 close must not be below support.
5. Only one support level per D0. Same ticker may have multiple D0 events; retain all and label ticker/date dependencies. Do not prune correlated days after outcome review.

## Entry and exit — new frozen primary

- On D1 RTH five-minute bars beginning 09:30 ET, look for **first** bar from 09:30 to 11:45 ET whose LOW is strictly below **0.999 * support**, immediately followed by a close >= support on that same five-minute bar or on the *immediately following* five-minute bar. Confirmation must finish by 11:50 ET; enter at **next candle OPEN <= noon ET**. If multiple, first chronological only, max one trade per ticker/day. No VWAP, volume, sector, breadth or higher-low gate.
- Entry opening price cannot exceed **1.02 * support**; skip extended otherwise. Structural stop = `min(low of breach bar, low of immediately following confirmation bar if used)*0.999`. Require stop distance [**0.35%, 2.00%**] relative to entry, otherwise skip risk-invalid. Profit target exactly **+2.00%** versus entry.
- Follow remaining D1 and all D2 5-minute RTH OHLC; if exit bar opens through target or stop, fill at OPEN, else when both thresholds touched in a bar resolve STOP first. At D2 15:55 ET bar close exit TIMEOUT if neither touched. 0.50% roundtrip **stock-equivalent** costs per entered trade; each skip contributes 0 to per-eligible-event mean. Missing full **78-bar** coverage for D0/D1/D2 => UNKNOWN, excluded from evaluable denominators and never imputed.
- Prior daily adjusted basis must be converted using D0 M5 closing-price ratio before applying support to M5. If rebased D0 daily close/high/low differs from D0 M5 more than **3%** on any field, mark UNKNOWN BASIS_MISMATCH.

## Frozen benchmarks and inference

- Primary: target-first fraction among executed trades and mean after-cost per executed trade; also mean after-cost *per evaluable eligible D0 signal* including skips=0. Expose counts for frozen daily candidates, unknown M5, no-pattern, extended, invalid-risk, targets, stops, timeouts, gap-through stops and ambiguous bars.
- Benchmark A: buy D1 09:30 M5 OPEN on each same eligible D0 signal, +2% target/-2% stop, D2 timeout and 50bp costs, same conservative bar logic. Compare **paired per-signal** net difference with the primary.
- Benchmark B (descriptive only): fixed 2% stop on the same primary failure-pattern entries, preserving 2% extension cap, and no 0.35-2% structural stop gate. This is not a tuning sweep.
- Secondary descriptive control: D1 five-minute bar low **[support, 1.001*support]** and close >= support, without any **prior intraday breach** of 0.999*support, enter the next M5 OPEN by noon, same +2% structural-stop methodology / cap. Choose first touch; if later a breach occurs it doesn't change the earlier entry. Different market sequence; not causal matching. Avoid overlap with primary if same event generates both: label both but use separately only.
- Ticker-cluster and D0-date-cluster bootstrap (10,000 fixed-seed replicates) for mean returns and paired difference; report uncertainty, multiple signal days and correlated tickers. No claims of 80% with <30 fills; 80% target-first alone not enough if options lose money.
- Report per-year regime limitation: **2022 bear market** may generalize poorly. This is an out-of-period *calendar* check, not survivorship-clean universe, options NBBO, or live forward study. For any promising stock outcome, next phase needs real option bid/ask, DTE, 30–60 delta or affordable contracts, and <$50 option premium, plus independent subsequent calendar regime.

## Pre-outcome validation gate

1. Save/commit THIS protocol and exact 90-stock universe BEFORE fetching the 2022 signal histories (except AAPL/MSFT two-symbol data-availability feasibility check, not in 90-stock universe, with no calculations of candidate setups or returns).
2. Retrieve historical daily series only, audit D0 date coverage/stock universe, identify and SAVE/COMMIT full date/ticker/support candidate manifest *without M5 or forward returns*.
3. Only after manifest commit, fetch precise D0/D1/D2 Webull RTH M5 histories and calculate stock-level executions.
4. Save original vendor M5 bytes, code/protocol, per-event outcomes and comparison; do not alter thresholds after outcome inspection.

Reference exploratory prior: `grimes_priceonly_prior_session_low_2023_exploratory_analysis_2026_10_11.md`.
