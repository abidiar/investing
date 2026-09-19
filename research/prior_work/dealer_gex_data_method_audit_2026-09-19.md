# Data / Sign-Method Audit — Dealer GEX Amplification vs Damping

Audit date: **2026-09-19**
Status: **COMPLETE BEFORE PROTOCOL FREEZE**
Prior-work review: `research/prior_work/dealer_gex_amplification_damping_prior_work_2026-09-19.md`

## Purpose
Determine whether Investing OS can obtain a historical dealer-gamma measure strong enough to test the open question:

> Given an independently observed price impulse, does dealer gamma state improve continuation/reversal and excursion forecasts beyond price, volatility, and liquidity?

## Ideal data hierarchy
1. Observed dealer/customer position or participant-class inventory.
2. Trade-level participant capacity + buy/sell + open/close, allowing inventory reconstruction.
3. Signed option trade-flow classification with Greeks.
4. A published OI-based dealer-sign proxy, explicitly labelled as an assumption.

## Sources checked

### Cboe Enhanced US Options Trade-by-Trade Execution Detail
Strength: transaction-level side, open/close, participant capacity, trade type; C1 history from 2019-10-07. This is the best direct route for SPX/SPXW dealer inventory reconstruction.
Limitation: proprietary/paid; not available through the current Investing OS tool stack.

### Cboe Open-Close Volume Summary
Strength: participant type (customer, professional customer, broker-dealer, market maker), buy/sell, open/close, EOD or intraday summary.
Limitation: proprietary/paid; not currently available to the project.

### OptionMetrics IvyDB Signed Volume / TradeFlow
Strength: buyer/seller initiated classification, bid/ask/midpoint and intraday snapshots since 2016; substantially stronger than OI sign heuristics for flow analysis.
Limitation: commercial data; not currently connected.

### Massive historical option trades
Strength: trade-level historical option prints are potentially accessible.
Limitation: public trade records do not expose participant capacity or dealer/customer inventory, so trade direction alone cannot identify the dealer book.

### Open historical ETF options archive
Source: `anahatsingh-ui/options-dataset-hist` (preserved Dubach dataset).
Coverage: SPY and IWM 2008-2025; QQQ 2011-2025.
Fields include date, expiration, strike, call/put, volume, open interest, IV and vendor Greeks including gamma. Underlying daily OHLCV is also included.
Strength: reproducible, open, direct gamma field, settled OI, long history.
Limitation: no participant capacity, no buy/sell initiator, no dealer inventory. Therefore dealer sign can only be modelled from an assumption.

## Published proxy that is feasible with our data
Baltussen et al. (2021) construct S&P 500 net gamma exposure using an explicit dealer-inventory assumption: calls are treated as dealer long gamma and puts as dealer short gamma. Barbon & Buraschi likewise use a call-minus-put gamma imbalance proxy and normalize by underlying liquidity.

We can reproduce the same family of proxy with the open ETF data:

`DGAMMA_i = gamma_i * open_interest_i * 100 * spot^2 * 0.01`

`SIGNED_DGEX = sum(DGAMMA_calls) - sum(DGAMMA_puts)`

`SIGNED_DGEX_TO_ADV = SIGNED_DGEX / ADV20_DOLLAR`

where `ADV20_DOLLAR` is trailing 20-session underlying dollar volume known before the next session.

Interpretation:
- negative proxy = modelled short-dealer-gamma environment;
- positive proxy = modelled long-dealer-gamma environment.

This is **not observed dealer inventory**. The sign convention is a published structural assumption.

## Why normalize by liquidity
Prior work repeatedly finds that hedge impact depends on hedge demand relative to underlying liquidity. Normalizing dollar gamma by trailing dollar volume directly encodes the mechanism `hedge pressure / available liquidity` and avoids treating the same dollar gamma as equally important in very different liquidity regimes.

## Untouched sample available
The only historical block not already used for an Investing OS gamma verdict is **2008-2010**. QQQ coverage begins in 2011, so a genuinely untouched common sample is available for **SPY and IWM** only.

Proposed clean split:
- seed/development year: **2008**;
- untouched holdout: **2009-2010**;
- instruments: **SPY, IWM**.

This period is old and pre-0DTE, which is a limitation, but it is useful as a strict falsification of whether the published OI-sign proxy adds anything at all beyond price/volatility/liquidity.

## Outcome data limitation
The open archive supplies daily OHLCV, not historical intraday bars. Therefore the first clean proxy test cannot reproduce 30/60/120-minute continuation exactly.

The strongest outcome available without introducing a second non-reproducible data source is an **opening-gap impulse**:
- direction is supplied by the Day-T+1 opening gap;
- continuation is measured from that open through the same RTH session using open-to-close return and open-centered MFE/MAE from daily high/low.

This is a proxy decision study, not a full intraday Investing OS trigger study.

## Audit verdict
**Feasible only as an OI-sign proxy replication.**

We do not currently have direct participant/inventory data. Therefore any positive result can justify only further research or a later test using stronger dealer-side data; it cannot establish that observed dealers caused the effect and cannot enter production scanners.

A negative result would be useful because it would show that the easy/public call-minus-put GEX proxy is not sufficiently additive for Investing OS.

## Required label in all downstream work
Use the phrase **MODELLED DEALER-GEX PROXY**. Do not call this observed dealer gamma, actual dealer inventory, or market-maker position.
