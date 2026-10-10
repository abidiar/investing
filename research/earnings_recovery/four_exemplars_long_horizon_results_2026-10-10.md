# Longer-horizon rebounds in DELL, META, QCOM, ORCL

**October 10, 2026.** Descriptive, hindsight-selected case series. This is **not** a statistically representative backtest and is **not** an options return test. Data: [frozen 55-announcement roster](./four_exemplars_long_horizon_protocol_2026-10-10.md), [19-event machine-readable OHLC outcome audit](./four_exemplars_long_horizon_events_2026-10-10.csv). Dates from SEC-linked Quant500; daily regular-session historical Webull prices. META release time unavailable in date source: assume after hours for illustrative scenario, exclude from strict-session-confirmed sample.

For each company's 2023–June 2026 earnings releases, first- or second-session drop in closing stock price >=5% versus final pre-earnings close was a qualifying event. **19 qualified out of 55 dates**: DELL 5, META 3, QCOM 6, ORCL 5. Recovered full price = daily close at least the pre-announcement stock close. Partial rebound = touching at least +5% from the qualifying selloff-day closing price. Both are different from profitable options. Each return horizon below is in trading sessions *after* selloff close; exclude events lacking full horizon.

## Measured recovery curve

| Trading sessions after selloff | Eligible | +5% touch from selloff close | Full intraday pre-announcement price touch | Full pre-announcement closing-price recovery |
|---:|---:|---:|---:|---:|
| 20 | 19 | 14 (73.7%) | 5 (26.3%) | 5 (26.3%) |
| 40 | 19 | 16 (84.2%) | 8 (42.1%) | 7 (36.8%) |
| 60 | 19 | 16 (84.2%) | 11 (57.9%) | 10 (52.6%) |
| 90 | 18 | 16 (88.9%) | 13 (72.2%) | 11 (61.1%) |
| 120 | 17 | 16 (94.1%) | 13 (76.5%) | 11 (64.7%) |

Company-specific 60-session counts (partial +5%; full closing-price recovery): DELL 4/5 and 3/5; META 3/3 and 2/3 (provisional time); QCOM 5/6 and 4/6; ORCL 4/5 and 1/5.

Of the 16 +5% partial rebounders by 60 sessions, median first touch **9.5 trading sessions** after event (range 2–30 sessions). Of the 10 fully closing-price-recovered by 60 sessions, median first recovered close **23 sessions** after event. Median worst intraday price excursion after initial selloff during 60 sessions was **−9.92% below selloff closing price**, regardless of rebound order. This measure can occur after initial bounce; never infer −5% stop-before-target rates from it.

### Dangerous examples
- DELL May 30, 2024: selloff −17.87% vs pre-earnings close; initial +5% rebound touched day 12 but later/overall within 60 sessions price low reached **−37.50%** from selloff close and full pre-earnings close was not reclaimed by day 120.
- DELL February 27, 2025: selloff −11.38%; touched +5% on day 12; fully recovered pre-earnings closing price on day **50**, but during the 60-day window suffered an intraday low **−30.68%** from initial selloff close (timing relative to rebound not determined in this summary).
- META April 24, 2024 (AH release assumed for date classification): selloff −10.56%; +5% bounce day 7, full pre-announcement close day **28**, further 60-session intraday low only −3.23% from selloff close.
- QCOM July 30, 2025: selloff −7.73%; +5% bounce day 9; recovered original price day **18**; 60-session minimum −1.81% beneath selloff close.
- ORCL December 10, 2025: selloff −10.83%; no +5% partial bounce within 60 sessions; first full pre-earnings closing-price recovery by day **115**, and minimum of the first 60 sessions −31.80% below the initial selloff close.

### Independent context from a broader, non-example-selected quality screen
Earlier 50-company / 92-event qualified cohort: **65/92** touched +5% within 60 post-selloff sessions and **48/92** returned to pre-earnings *closing* price within 60. This broader sample remains contemporary-stock-selected and retrospective; its rates are not options success rates. [Source](./earnings_selloff_recovery_92events_2026-10-10.csv).

## Decision
The user's longer-term recovery observation is directionally plausible, especially for partial bounces. Rigid day-three ±5% stops measured short-entry tradeability, not *eventual* recovery. But a +5% intraday rebound is also not automatically tradeable from any entry and can be preceded by much larger drawdown. Options buyers must match expected rebound **timing, price trajectory, IV crush, strike/delta, premium and expiry**.

Next operation: freeze a 92 + 72 quality-event study measuring: (i) +5% **BEFORE** an additional −5% or −10% from the objectively known post-selloff close; (ii) distribution of time to first +5% and further low, and depth/time-to-low; (iii) conditional recovery patterns after stabilization vs buying the initial selloff; (iv) 20/40/60/90/120 trading-session windows, per distinct source cohort and complete available follow-up only. This avoids cherry-picking four names and directly tests whether recovery is actionable. Do not optimize strikes or DTE before measuring path risk. Do not pay for options data without consent.
