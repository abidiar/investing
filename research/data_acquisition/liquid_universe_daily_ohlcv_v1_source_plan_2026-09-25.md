# Liquid-Universe Daily OHLCV v1 — Acquisition Plan

Date: 2026-09-25
Status: FROZEN BEFORE DISCOVERY OUTCOMES
Parent protocol: `research/stock_repricing_swing_event_outcome_schema_v1_frozen_2026-09-24.md`

## Objective
Build and permanently save exact daily OHLCV coverage needed to construct the 2018-01-02 through 2022-12-30 DISCOVERY feature/event panel without inspecting forward +5/+10/+15 versus -3/-5 outcomes.

## Practical source decision
The public Sharadar cleaning project is used as the anti-leakage/data-quality specification, but its full 41.8M-row Sharadar panel is not publicly distributed. We therefore will not label substitute bars as Sharadar data.

Primary free candidate for historical intraday/daily reconstruction: HF Data Library / PiTrading archive, which documents full consolidated-tape coverage before March 2022 and provides daily aggregates derived from one-minute OHLCV for a fixed research universe. This is useful but does not represent the entire historical U.S. equity universe.

Secondary/validation sources:
- NASDAQ Data Link WIKI prices for history through 2018-03-27 where accessible; useful for early-2018 cross-checks and delisted names, but cannot cover the full 2018-2022 Discovery period.
- Public historical CSV repositories only for symbol/date spot validation, never as an outcome-selected source.
- MarketParquet/HistoricalData.net are documented as survivorship-aware alternatives but require paid historical access for the full period and are not assumed available in v1.

## Frozen data-quality conventions
1. Do not filter securities because they later delisted.
2. Stable security identity is preferred over ticker when the source provides it.
3. For price-level eligibility use as-traded/raw prices when available; adjusted historical levels must not be used as contemporaneous price floors.
4. For returns, ATR/ADR, structural displacement and barrier arithmetic, use a consistently corporate-action-adjusted OHLC series.
5. Liquidity should use contemporaneous dollar volume where raw price/volume permit it; do not compare future-split-adjusted volume levels cross-sectionally.
6. Sort by security/date before rolling calculations.
7. Record source, adjustment convention, missingness and symbol coverage in the permanent manifest.

## Discovery construction policy
Because a free, complete survivorship-clean all-U.S.-equity 2018-2022 archive is not currently available through connected sources, v1 will be explicitly labeled a **liquid research-universe study**, not an all-U.S.-equity study. We will not silently claim universe completeness.

No forward outcome may be calculated while the feature/event candidate panel is being built. Daily OHLCV necessarily contains future dates in storage, but candidate generation code must operate causally and the barrier labels remain in a separate outcome stage after candidate-panel freeze.

## Permanent raw-store target
Normalized rows should use at minimum:
`date, security_id, ticker, open, high, low, close, volume, raw_close_if_available, dollar_volume_if_available, source, adjustment_state`

The eventual store/manifest will document:
- exact ticker/security count
- first/last date per security
- row count
- missing-session diagnostics
- duplicates
- OHLC integrity checks
- nonpositive price/volume checks
- corporate-action convention
- source provenance
- checksum/build commit

## Stop conditions
Do not proceed to Discovery outcome scoring if:
- the source cannot provide exact daily OHLC for candidate securities;
- adjustment conventions are unknown or inconsistent enough to create false gaps/barriers;
- the candidate universe is constructed using future returns or later survival;
- candidate generation has accidentally exposed or used forward barrier outcomes.

## Next operation
Acquire/stage the broadest free exact 2018-2022 OHLCV panel available under this policy, run coverage and integrity diagnostics, and save the normalized raw store/manifest before computing event features.