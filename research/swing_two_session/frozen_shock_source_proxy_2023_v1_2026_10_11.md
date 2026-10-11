# PRE-OUTCOME FROZEN: shared-sector vs issuer-specific selling before support false-break
Frozen 2026-10-11, before inspecting any 2023 candidate/outcome rows or fetching ETF history.
RESEARCH-ONLY; mechanism proxy, not an identified liquidity shock or measured profit revisions.

## Motivation and prior work
Zhi Da, Qianqiu Liu, Ernst Schaumburg, Management Science 2014, doi:10.1287/mnsc.2013.1766: nonfundamental residual reversals stronger than ordinary short-horizon reversal historically; liquidity pressure vs fundamental news.
Chiang/Kirby/Nie 2021 J Banking Finance doi:10.1016/j.jbankfin.2021.106068: news-related returns can trend, short-term liquidity pressure can revert.
No claim this test is novel or proof of cause.

## Universe/time/sources frozen
Use EXACT same 49 issuer-disjoint vs original 63 cohort, as frozen 2026-10-11 in frozen_issuer_disjoint_range_vwap_replication_v2_2026_10_11.md, but **NEW UNEXPOSED calendar year 2023-01-03 to 2023-12-27**, never included in previously reported 106 2024-26 events. Source existing 5 archived Webull adjusted D CSV batches with 1000 sessions each (2022-10-06 to 2026-10-01); query as-of ETF daily Webull for sector returns with same adjustment convention; preserve every event irrespective of return.
ETF map fixed:
SMH NVDA AVGO MU TXN KLAC LRCX AMAT ASML TSM
XLK CSCO ANET
IGV PANW CRWD FTNT NOW ADBE SNOW DDOG
XLC NFLX DIS
XLP TGT WMT PG KO PEP
XLY MCD SBUX NKE
XLF V MA GS MS C WFC
XLV UNH ABBV JNJ MRK PFE
XLI NOC GE HON DE UPS FDX BA
XLE CVX SLB COP.
No ETF mapping changes after reading outcomes. ETF source failure = missing mechanism classification, not assumed neutral.

## Screen and classification
Exact old ORIGINAL daily support false break: preceding 40 trading sessions support lowest LOW and resistance highest HIGH; range >=6%; >=2 within 1.2% touches separated >=5 sessions; event day LOW <support, CLOSE >support and in [0.995,1.025]*support; event VOL>=1.2x trailing20; 5-calendar-day ticker dedup. No class-specific scan.
Three completed sessions event-close backward: rStock3 = 100*(C(t)/C(t-3)-1), rETF3 similarly. Extra3 = rStock3-rETF3 (percentage points). Mutually exclusive point-in-time categories:
SHARED_SECTOR_PRESSURE: rETF3 <= -1.5%, stock rStock3<0%, and Extra3 >=-2 pp.
ISSUER_RELATIVE_WEAKNESS: Extra3 <=-3 pp.
UNCLASSIFIED: all others. Missing ETF source -> UNKNOWN classification.
These price-only classes DO NOT distinguish true fundamentals from liquidation, are proxies only. Any dated earnings or guidance surprise evaluation requires a separately coded source dataset; do NOT assert absence of negative earnings news simply because ETF is down.

## Primary outcome
Next RTH D(t+1) OPEN buy (not VWAP), stock +/-2% first touched until end D(t+2), gap at open adverse/attainable opening fill, both stop and target crossed within one daily bar = conservative STOP; timeout at t+2 CLOSE. 0, 20, 50, 100 bps total roundtrip trade friction, primary 50 bps. No flat positive-return selection. If signal followup on 2023 known shortened sessions July03 or Nov24, treat UNKNOWN rather than silent removal. With daily OHL first-hit sequence intraday is ambiguous; audit both-hit counts, strictly diagnostic stock proxy, NOT options execution.
Primary group estimands are net per eligible event at 50bps and shared-minus-relative difference. Also gross price returns, target/stop/timeout, median, exact N, share of survivors, bootstrap resampling TICKERS at 95% CI for group difference (10k deterministic draws) if both n>=5. No publication/production validation unless >=40 observations per group, sufficiently diversified, source/CA PIT certified, robust CI lower>0 net AND group difference CI excludes zero. Repeat NEVER retune thresholds on already exposed sample.
Control: unclassified and pooled; calendar 2023 separate from 2024-26, same issuers not independent; survivorship biased and no news as-of coding. Results if N insufficient -> INCONCLUSIVE, not profitable.
