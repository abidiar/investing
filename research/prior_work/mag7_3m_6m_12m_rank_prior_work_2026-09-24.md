# Prior-Work Review — Mag-7 3M/6M/12M Cross-Sectional Rank Signal

Date: 2026-09-24
Status: COMPLETE BEFORE OUTCOME TEST

## Question
Within a fixed retrospective cohort of AAPL, MSFT, AMZN, GOOGL, META, NVDA, and TSLA, does a composite of trailing 3-, 6-, and 12-month price performance contain information about the following month's relative return?

## What prior research says
1. Intermediate-horizon momentum is well established in broad equity universes. Jegadeesh & Titman (1993) documented that past winners outperformed past losers over intermediate horizons, including formation/holding windows in the 3-to-12-month range.
2. Reversal also exists, but the best-known long-horizon evidence is materially longer than the proposed 3/6/12-month composite. De Bondt & Thaler (1985) documented multi-year loser-versus-winner reversal.
3. Short-horizon reversal/predictability literature cautions that recent returns can behave differently from intermediate-horizon momentum, which is one reason standard momentum implementations often separate the most recent month from longer lookbacks.
4. None of those classic results establishes that the same effect must hold inside only seven mega-cap technology/growth stocks. This is a concentrated, correlated, survivorship-biased retrospective cohort.

## Open question for Investing OS
The useful unresolved question is not whether momentum or reversal can exist generally. It is whether a simple 3M/6M/12M relative-strength ranking has stable predictive information inside this specific seven-stock cohort, and whether the sign is consistently momentum-like or reversal-like.

## Design implications
- Do not choose momentum versus contrarian after seeing outcomes.
- Pre-register both top-ranked and bottom-ranked arms.
- Make the primary test direction-neutral: cross-sectional rank information coefficient (Spearman) versus next-month return.
- Use equal weights across 3M, 6M, and 12M ranks; do not tune horizon weights after results.
- Compare with equal-weight Mag-7 and QQQ/SPY references, but do not infer a broadly investable historical strategy because the cohort is defined using today's surviving names.
- Treat same-close month-end portfolio returns as a signal-research approximation, not executable trade P&L.

## Sources
- Narasimhan Jegadeesh and Sheridan Titman, "Returns to Buying Winners and Selling Losers: Implications for Stock Market Efficiency," Journal of Finance 48(1), 1993.
- Werner F. M. De Bondt and Richard Thaler, "Does the Stock Market Overreact?", Journal of Finance 40(3), 1985.
- Narasimhan Jegadeesh, "Evidence of Predictable Behavior of Security Returns," Journal of Finance 45(3), 1990.

## Prior-work conclusion
A symmetric rank-information test is justified. A one-sided "buy winners" or "buy losers" protocol is not justified from the missing original rule, because selecting the direction now would introduce researcher discretion. Freeze both arms and the direction-neutral primary statistic before exposing 2017-2026 outcomes.
