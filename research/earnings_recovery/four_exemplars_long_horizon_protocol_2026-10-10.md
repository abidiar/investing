# Four-company recovery case series: pre-analysis protocol

Frozen 2026-10-10. Motivation: deliberately selected DELL, META, QCOM, ORCL as the user's exemplars of longer-term rebound after earnings selloffs. **This is a hindsight-selected illustrative series, NOT validation or an unbiased market-wide hit rate.** Earnings roster captured via Quant500 historical SEC 8-K dates before measuring future returns. For META, Quant500 does NOT confirm press-release time; mark its session UNVERIFIED, run a *provisional* earnings-after-close scenario only, and exclude from strict-date counts pending primary press-release timestamp verification. For others, use independently reported after-close date. 

Rules: reaction first regular session following AH announcement (for META scenario assume AH) or on a BMO date; day-one or day-two end-of-day close at least −5% versus last pre-announcement closing price qualifies (first occurrence). Each qualified event indexed to close on selloff day, not hindsight low. Show all qualifying declines, including failures. Observables: initial drop, next 20/40/60/90/120 regular-session close-high reclaim probability of pre-announcement closing price, +5% price from selloff close, first-day and median recovery days, max further low before recovery, and market/SPY benchmark if possible. Evaluate separately at each fully observed forward horizon; no extrapolation on insufficient windows. If both +5% and −5% intra-day using OHLC, adverse first. Also compute fixed day-three and stock underlying optional outcomes as a separate benchmark, not 'recovery failure'.

The word recovery refers distinctly to (a) +5% bounce from dislocation close and (b) complete return to pre-announcement price; measure both. No premiums/option trading results. Do not label the chosen exemplars A+ or generalize.

### Dated source roster

ticker,earnings_date,session,time_source
DELL,2023-06-01,AH,https://quant500.com/earnings-date/DELL
DELL,2023-08-31,AH,https://quant500.com/earnings-date/DELL
DELL,2023-11-30,AH,https://quant500.com/earnings-date/DELL
DELL,2024-02-29,AH,https://quant500.com/earnings-date/DELL
DELL,2024-05-30,AH,https://quant500.com/earnings-date/DELL
DELL,2024-08-29,AH,https://quant500.com/earnings-date/DELL
DELL,2024-11-26,AH,https://quant500.com/earnings-date/DELL
DELL,2025-02-27,AH,https://quant500.com/earnings-date/DELL
DELL,2025-05-29,AH,https://quant500.com/earnings-date/DELL
DELL,2025-08-28,AH,https://quant500.com/earnings-date/DELL
DELL,2025-11-25,AH,https://quant500.com/earnings-date/DELL
DELL,2026-02-26,AH,https://quant500.com/earnings-date/DELL
DELL,2026-05-28,AH,https://quant500.com/earnings-date/DELL
META,2023-02-01,UNVERIFIED,https://quant500.com/earnings-date/META
META,2023-04-26,UNVERIFIED,https://quant500.com/earnings-date/META
META,2023-07-26,UNVERIFIED,https://quant500.com/earnings-date/META
META,2023-10-25,UNVERIFIED,https://quant500.com/earnings-date/META
META,2024-02-01,UNVERIFIED,https://quant500.com/earnings-date/META
META,2024-04-24,UNVERIFIED,https://quant500.com/earnings-date/META
META,2024-07-31,UNVERIFIED,https://quant500.com/earnings-date/META
META,2024-10-30,UNVERIFIED,https://quant500.com/earnings-date/META
META,2025-01-29,UNVERIFIED,https://quant500.com/earnings-date/META
META,2025-04-30,UNVERIFIED,https://quant500.com/earnings-date/META
META,2025-07-30,UNVERIFIED,https://quant500.com/earnings-date/META
META,2025-10-29,UNVERIFIED,https://quant500.com/earnings-date/META
META,2026-01-28,UNVERIFIED,https://quant500.com/earnings-date/META
META,2026-04-29,UNVERIFIED,https://quant500.com/earnings-date/META
ORCL,2023-03-09,AH,https://quant500.com/earnings-date/ORCL
ORCL,2023-06-12,AH,https://quant500.com/earnings-date/ORCL
ORCL,2023-09-11,AH,https://quant500.com/earnings-date/ORCL
ORCL,2023-12-11,AH,https://quant500.com/earnings-date/ORCL
ORCL,2024-03-11,AH,https://quant500.com/earnings-date/ORCL
ORCL,2024-06-11,AH,https://quant500.com/earnings-date/ORCL
ORCL,2024-09-09,AH,https://quant500.com/earnings-date/ORCL
ORCL,2024-12-09,AH,https://quant500.com/earnings-date/ORCL
ORCL,2025-03-10,AH,https://quant500.com/earnings-date/ORCL
ORCL,2025-06-11,AH,https://quant500.com/earnings-date/ORCL
ORCL,2025-09-09,AH,https://quant500.com/earnings-date/ORCL
ORCL,2025-12-10,AH,https://quant500.com/earnings-date/ORCL
ORCL,2026-03-10,AH,https://quant500.com/earnings-date/ORCL
ORCL,2026-06-10,AH,https://quant500.com/earnings-date/ORCL
QCOM,2023-02-02,AH,https://quant500.com/earnings-date/QCOM
QCOM,2023-05-03,AH,https://quant500.com/earnings-date/QCOM
QCOM,2023-08-02,AH,https://quant500.com/earnings-date/QCOM
QCOM,2023-11-01,AH,https://quant500.com/earnings-date/QCOM
QCOM,2024-01-31,AH,https://quant500.com/earnings-date/QCOM
QCOM,2024-05-01,AH,https://quant500.com/earnings-date/QCOM
QCOM,2024-07-31,AH,https://quant500.com/earnings-date/QCOM
QCOM,2024-11-06,AH,https://quant500.com/earnings-date/QCOM
QCOM,2025-02-05,AH,https://quant500.com/earnings-date/QCOM
QCOM,2025-04-30,AH,https://quant500.com/earnings-date/QCOM
QCOM,2025-07-30,AH,https://quant500.com/earnings-date/QCOM
QCOM,2025-11-05,AH,https://quant500.com/earnings-date/QCOM
QCOM,2026-02-04,AH,https://quant500.com/earnings-date/QCOM
QCOM,2026-04-29,AH,https://quant500.com/earnings-date/QCOM
