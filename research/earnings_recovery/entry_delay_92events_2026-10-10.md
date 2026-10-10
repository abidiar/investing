# Quality earnings-selloff: delayed-entry comparison (92 events)

**Computed:** 2026-10-10. **Status:** exploratory, retrospective stock-price analysis; NOT an options P&L or deployable signal.

## Objective and frozen sample
Reuse the 92 financially qualified events / 32 tickers from [the recovery-horizon dataset](./earnings_selloff_recovery_92events_2026-10-10.csv) (166 raw declines in 50 contemporary stocks, from 2023-01-01 through 2026-06-30). Do not tune quality rules or add selected companies. Re-query connected Webull daily regular-session OHLC, 1,100 completed bars per ticker, for the original selloff dates and later prices. All 92 events match their original five-session close return to within 0.06 percentage points. No new fundamental or event-date validation in this follow-up.

## Entry and exits
Entries: buy the underlying stock at the open of the 1st, 3rd, 5th, or 10th regular trading session *after* the qualified selloff day. Each eligible event gets all four offsets, without retroactively filtering out stocks that have already recovered. Compare (a) unhedged close-to-close gross return over 20 entry-inclusive sessions, (b) 40-session gross close return, and (c) a **+5% profit target / −5% stop** triggered by daily OHLC during 20 entry-inclusive sessions, otherwise exit at 20th-session close. Gaps fill at open, a stop is assumed to occur first when a daily bar touches both levels. No fees, spreads, taxes or stock/option slippage. Inputs are historical provider price bars with possible corporate-action adjustments.

## Results

| Wait after selloff | Events | +5% target | −5% stop | Timed out | Mean return with target/stop | Median 20-day raw stock return | Mean 20-day raw stock return | Median 40-day raw stock return | Entries still below pre-earnings price |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| 1 session | 92 | 38 (41.304%) | 46 | 8 | -0.503% | 1.145% | 2.224% | 1.610% | 92 |
| 3 sessions | 92 | 47 (51.087%) | 35 | 10 | 0.769% | 1.183% | 2.365% | 2.288% | 90 |
| 5 sessions | 92 | 41 (44.565%) | 40 | 11 | 0.113% | 0.636% | 1.863% | 2.618% | 88 |
| 10 sessions | 92 | 46 (50.000%) | 36 | 10 | 0.647% | 0.729% | 1.693% | 2.670% | 84 |

## Decision
Day-3 entry beats next-session entry for this retrospectively chosen 20-day ±5% exit rule, but +0.77% average gross stock return is a narrow margin and NOT validation. Waiting five or ten sessions does not show a monotonic gain. The initial 2025 cohort has negative average 20-session buy-and-hold price returns across every wait offset. A later wait may miss earlier rebounds and an options contract may decay even when the underlying rises. The 2026 events are limited and the dataset is clustered by ticker and regime. Selection among four waits creates multiple-testing risk. Do not label any setting A+.

## Needed before options testing
Freeze an exit/entry candidate from this exploratory work. Test a genuinely untouched time period or independently selected universe, then price specified strike/delta, premium, IV, spread and expiration. Without actual historical options quotes, characterize 7-, 14-, 30-, 45-, 60-, and 90-day expiries as scenarios rather than realized backtests.

## Machine-readable audit
[Entry-level 368-row result file](./entry_delay_92events_2026-10-10.csv). Webull symbols: ABNB, ADBE, AMD, ANET, COIN, CRM, CRWD, CSCO, CVS, DELL, DIS, DOW, FDX, GE, GILD, GOOG, HON, HPE, IBM, ISRG, JCI, KLAC, LOW, NFLX, NOW, PANW, PYPL, QCOM, SBUX, TGT, TXN, UPS.
