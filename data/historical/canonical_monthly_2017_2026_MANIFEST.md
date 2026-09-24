# Investing OS Canonical Monthly Historical Price Store

Generated: 2026-09-24

## Scope
- Universe: AAPL, MSFT, AMZN, GOOGL, META, NVDA, TSLA, QQQ, SPY
- Coverage: 2017-01 through 2026-09
- Last completed month: 2026-08
- September 2026 is partial through 2026-09-24 and is marked `PARTIAL_MONTH`.
- Frequency: final observed trading session in each calendar month.
- Price basis: split-adjusted close only; dividends are not reinvested and this is not a total-return series.

## Canonical source policy
- 2017-01 through 2020-06: exact daily closes from free public historical CSV snapshots, reduced to month-end.
- 2020-07 onward: Alpaca IEX daily bars, normalized for corporate actions, reduced to month-end.
- Public sources:
  - AAPL, MSFT, AMZN, GOOGL, FB→META, NVDA, TSLA: https://github.com/oscarescuderoarnanz/dtwParallel/tree/32508118a5f5e05fe7e7490e5495d7038e1ad3d5/exampleData/Data/E2_FinanceData/all_data
  - QQQ: https://github.com/lituokobe/CQF-Jan25-Exam3/blob/19e6aa3e2cd278feef89a2da035474962c58a095/data/QQQ_2015-2025.csv
  - SPY: https://github.com/sjsucmpe272-fall21/BlackSwanImpactPredictor/blob/1f0effd9470c8c2237c86da79ad63c87654c8965/ml/stock_data/spy500_historical_data.csv

## Frozen split normalization
- AAPL: Alpaca observations before 2020-08-31 ÷4. The public snapshot already reflects the 2020 split.
- AMZN: observations before 2022-06-06 ÷20.
- GOOGL: observations before 2022-07-18 ÷20.
- NVDA: before 2021-07-20 ÷40; 2021-07-20 through 2024-06-09 ÷10.
- TSLA: before 2020-08-31 ÷15; 2020-08-31 through 2022-08-24 ÷3.
- MSFT, META, QQQ, SPY: no split adjustment required for this window.

## Independent overlap validation
The free public series and normalized Alpaca series overlap from July 2020. A 0.5% absolute-difference review threshold was fixed before accepting the stitch.

- Comparisons: 63
- Mean absolute difference: 6.4372%
- Maximum absolute difference: 400.3145%
- Rows above 0.5%: 1
- Rows above 1.0%: 1
- Alpaca uses IEX prints rather than the consolidated official close, so small differences are expected; larger differences remain visible in this audit.

| Ticker | Month | Free public close | Alpaca normalized | Absolute difference |
|---|---:|---:|---:|---:|
| AAPL | 2020-07 | 106.2600 | 106.3500 | 0.085% |
| AAPL | 2020-08 | 129.0400 | 129.1100 | 0.054% |
| AAPL | 2020-09 | 115.8100 | 115.8400 | 0.026% |
| AAPL | 2020-10 | 108.8600 | 109.1100 | 0.230% |
| AAPL | 2020-11 | 119.0500 | 119.5300 | 0.403% |
| AAPL | 2020-12 | 132.6900 | 132.6500 | 0.030% |
| AAPL | 2021-01 | 131.9600 | 131.7800 | 0.136% |
| MSFT | 2020-07 | 205.0100 | 205.0000 | 0.005% |
| MSFT | 2020-08 | 225.5300 | 225.0000 | 0.235% |
| MSFT | 2020-09 | 210.3300 | 210.2600 | 0.033% |
| MSFT | 2020-10 | 202.4700 | 202.8900 | 0.207% |
| MSFT | 2020-11 | 214.0700 | 214.4600 | 0.182% |
| MSFT | 2020-12 | 222.4200 | 222.8300 | 0.184% |
| MSFT | 2021-01 | 231.9600 | 231.7000 | 0.112% |
| AMZN | 2020-07 | 158.2340 | 158.2100 | 0.015% |
| AMZN | 2020-08 | 172.5480 | 172.6608 | 0.065% |
| AMZN | 2020-09 | 157.4365 | 157.4535 | 0.011% |
| AMZN | 2020-10 | 151.8075 | 151.9083 | 0.066% |
| AMZN | 2020-11 | 158.4020 | 158.4645 | 0.039% |
| AMZN | 2020-12 | 162.8465 | 162.9425 | 0.059% |
| AMZN | 2021-01 | 160.3100 | 160.1618 | 0.092% |
| GOOGL | 2020-07 | 74.3975 | 74.4035 | 0.008% |
| GOOGL | 2020-08 | 81.4765 | 81.6003 | 0.152% |
| GOOGL | 2020-09 | 73.2800 | 73.3010 | 0.029% |
| GOOGL | 2020-10 | 80.8055 | 80.8130 | 0.009% |
| GOOGL | 2020-11 | 87.7200 | 87.8250 | 0.120% |
| GOOGL | 2020-12 | 87.6320 | 87.6260 | 0.007% |
| GOOGL | 2021-01 | 91.3680 | 91.2970 | 0.078% |
| META | 2020-07 | 253.6700 | 253.7100 | 0.016% |
| META | 2020-08 | 293.2000 | 293.9900 | 0.269% |
| META | 2020-09 | 261.9000 | 261.9200 | 0.008% |
| META | 2020-10 | 263.1100 | 263.5500 | 0.167% |
| META | 2020-11 | 276.9700 | 277.5700 | 0.217% |
| META | 2020-12 | 273.1600 | 273.5800 | 0.154% |
| META | 2021-01 | 258.3300 | 258.0900 | 0.093% |
| NVDA | 2020-07 | 10.6148 | 10.5998 | 0.141% |
| NVDA | 2020-08 | 13.3745 | 13.3732 | 0.009% |
| NVDA | 2020-09 | 13.5305 | 13.5345 | 0.030% |
| NVDA | 2020-10 | 12.5340 | 12.5482 | 0.114% |
| NVDA | 2020-11 | 13.4015 | 13.4093 | 0.058% |
| NVDA | 2020-12 | 13.0550 | 13.0607 | 0.044% |
| NVDA | 2021-01 | 12.9898 | 12.9750 | 0.114% |
| TSLA | 2020-07 | 19.0768 | 95.4440 | 400.315% |
| TSLA | 2020-08 | 166.1067 | 166.2367 | 0.078% |
| TSLA | 2020-09 | 143.0033 | 143.0967 | 0.065% |
| TSLA | 2020-10 | 129.3467 | 129.4167 | 0.054% |
| TSLA | 2020-11 | 189.2000 | 188.8367 | 0.192% |
| TSLA | 2020-12 | 235.2233 | 235.2133 | 0.004% |
| TSLA | 2021-01 | 264.5100 | 264.4133 | 0.037% |
| QQQ | 2020-07 | 265.7900 | 265.8000 | 0.004% |
| QQQ | 2020-08 | 294.8800 | 295.0400 | 0.054% |
| QQQ | 2020-09 | 277.8400 | 278.1800 | 0.122% |
| QQQ | 2020-10 | 269.3800 | 269.7500 | 0.137% |
| QQQ | 2020-11 | 299.6200 | 299.5200 | 0.033% |
| QQQ | 2020-12 | 313.7400 | 314.1900 | 0.143% |
| QQQ | 2021-01 | 314.5600 | 314.5200 | 0.013% |
| SPY | 2020-07 | 326.5200 | 326.5400 | 0.006% |
| SPY | 2020-08 | 349.3100 | 349.3400 | 0.009% |
| SPY | 2020-09 | 334.8900 | 334.9000 | 0.003% |
| SPY | 2020-10 | 326.5400 | 326.7800 | 0.073% |
| SPY | 2020-11 | 362.0600 | 362.3200 | 0.072% |
| SPY | 2020-12 | 373.8800 | 373.8500 | 0.008% |
| SPY | 2021-01 | 370.0700 | 370.0100 | 0.016% |

## Completeness
- Canonical rows: 1053
- Calendar months: 117
- Expected rows: 1053
- Missing ticker-month cells: 0

## Research-integrity note
No forward Mag-7 strategy outcomes were used to select the data sources, split factors, stitching date, month-end rule, or validation threshold. This price store is frozen before the long-history strategy results are exposed.
