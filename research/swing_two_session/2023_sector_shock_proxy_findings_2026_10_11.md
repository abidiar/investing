# 2023 frozen range false-break shock-source PROXY test — NEGATIVE / INCONCLUSIVE
As-of: 2026-10-11. No trading instruction or automation change.

## Research integrity and inputs
- External prior literature reviewed BEFORE test (Da/Liu/Schaumburg, Management Science 2014 https://doi.org/10.1287/mnsc.2013.1766 ; Chiang/Kirby/Nie JBF 2021 https://doi.org/10.1016/j.jbankfin.2021.106068 ).
- Frozen **before** examining 2023 event outcomes: `research/swing_two_session/frozen_shock_source_proxy_2023_v1_2026_10_11.md` (commit fe61ef2).
- Previously archived 49-stock Webull DAILY forward-adjusted OHLCV batches, 2022-10-06 through 2026-10-01; fresh 10 sector ETFs Webull D source saved `data/frozen2023_sector_etf_webull_daily_close_2026_10_11.csv` (commit 193df24).
- Mechanism/group labels frozen in `data/frozen_2023_sector_shock_signal_manifest_2026_10_11.json` (commit d0d3b96) **before** future-bar examination. Original 40-day support false break, two separate touches, >=6% prior range, volume >=1.2x20, 5-calendar-day dedup unchanged.
- Earlier 106 independent issuer price OUTCOMES came from 2024-Sept2026; this sample uses earlier **2023 calendar dates**, 45 previously unscored events across 27 of the same issuers. Therefore earlier in *time*, but **NOT issuer-independent or true forward test**; historical prices retrospectively adjusted, survivors selected from 2026-name universe, unknown true corporate-action as-of consistency.

## Pre-frozen mechanical source proxies
Across three sessions up to event CLOSE, compute stock return and sector ETF return (sector pairs prespecified in frozen protocol); issuer residual = stock return - sector return.
- SHARED_SECTOR_PRESSURE: ETF 3d <=-1.5%, stock 3d negative, stock minus ETF >= -2 percentage points.
- ISSUER_RELATIVE_WEAKNESS: stock minus ETF <= -3 percentage points.
- UNCLASSIFIED otherwise.
This does **not** measure true liquidity-initiated flows, analyst FY EPS expectations, orders, margins, or dated company news. Negative own-stock residual may be due to either price pressure or genuine bad news. Thus this tests ONLY a quantifiable proxy for *who was selling relative to sector*; it does NOT directly test the economic causal mechanism.

## Outcome: next trading day OPEN; +2% target vs -2% stop; hold at most two sessions
Daily bar O/H/L/C limit-order first hit modeled conservatively: same-day target+stop ambiguity defaults STOP, gap at worse/better open, terminal second-session close. This is **not five-minute VWAP entry**, and does **not establish executable bid/ask**. No ambiguous both-barrier day observed for 45. Holidays/2023 half-session days were checked; 45/45 followup daily records available, no early close. Model friction=0.50% total roundtrip for primary result.

| Frozen group | N | distinct tickers | target | stop | timeout | gross % per signal | net % per signal at 50bp |
|---|---:|---:|---:|---:|---:|---:|---:|
| Shared sector pressure | 18 | 13 | 7 | 5 | 6 | +0.2813 | **-0.2187** |
| Issuer-relative weakness | 9 | 8 | 4 | 2 | 3 | +0.4582 | **-0.0418** |
| Unclassified | 18 | 15 | 11 | 1 | 6 | +1.2828 | **+0.7828** |
| ALL | 45 | 27 | 22 | 8 | 15 | +0.7173 | **+0.2173** |

Net @20bp all +0.5173%; @100bp -0.2827%. Target-first all 22/45 = 48.9%; not an options hit-rate. Stronger UNCLASSIFIED is descriptive, **do not promote** or tune thresholds after seeing it. The shared-sector mechanical hypothesis **did not outperform** the issuer-weakness group: difference -0.1769 percentage points. Ticker cluster bootstrap 10,000 draws seeded 20261011 **95% difference CI [-1.6359,+1.5094] pp**, zero inside. Shared net mean CI [-1.165,+0.771]%, issuer weakness mean CI [-1.322,+1.010]%, all CI [-0.320,+0.728]%. No reliable positive net expectancy. 2023 totals should not be pooled as proof with earlier 2024–2026 negative issuer-disjoint price panel.

## Verdict and the genuinely needed next question
**No validated shared-sector-selloff or issuer-residual recovery edge.** Class N (18/9) dramatically short of predeclared >=40/class, no CI support, test is only daily price proxy and is not a true forecast-revision/earnings-news causal test. Published findings concern decompositions of news versus residual, not necessarily the sector-price split tested here. Test the **actual source of company-specific new information** using original-date filings/releases and contemporaneous analyst estimate revisions, orders, guidance and margins, tagging as `NO_MATERIAL_BAD_NEWS` versus `PERSISTENT_FUNDAMENTAL_DOWNGRADE` versus `UNKNOWN` *before outcome read*. Freeze untouched events/periods and primary costs; do not relabel these 45 seen outcomes into a new discovery test. No options calls claim until affordable historical option bid/ask and dated IV/DTE obtained. No paid feeds.

Machine event results and pre-outcome manifest:
- `research/swing_two_session/data/2023_sector_shock_proxy_forward_daily_trade_diagnostic_2026_10_11.json`
- `research/swing_two_session/data/frozen_2023_sector_shock_signal_manifest_2026_10_11.json`
