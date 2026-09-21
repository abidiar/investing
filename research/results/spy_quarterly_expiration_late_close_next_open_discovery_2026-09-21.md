# SPY Quarterly-Expiration Late-Close → Next-Open Discovery

Date logged: 2026-09-21
Status: **DISCOVERY / RESEARCH-ONLY — NOT A PRODUCTION RULE**

## Question
Does SPY's direction during the final 30 minutes of a quarterly options/futures expiration session (3:30 PM ET → RTH close) contain information about the direction of SPY's gap into the next regular trading session?

## Why this was revisited
A prior Investing OS discussion had identified a possible relationship between the late triple-witching move and the following trading session. The exact prior write-up was not recoverable, so the result was reconstructed using already-available Webull M5 SPY history rather than creating a new data pipeline.

## Discovery definition used
- Instrument: SPY.
- Event: quarterly options/futures expiration session, including holiday-adjusted quarterly expiration.
- Signal window: 3:30 PM ET to RTH close.
- Primary outcome: direction from expiration-session close to next RTH open.
- Secondary outcomes: next-session open→close direction and expiration close→next-session close direction.
- No threshold optimization was performed.

## Reconstructed recent panel
Eight completed quarterly-expiration events from 2024-09-20 through 2026-06-18 were inspected using existing Webull M5 history.

| Expiration session | 3:30→close direction | Next-session opening gap direction | Match? |
|---|---|---|---|
| 2024-09-20 | Up (essentially flat) | Up | Yes |
| 2024-12-20 | Down | Down | Yes |
| 2025-03-21 | Up | Up | Yes |
| 2025-06-20 | Up | Up | Yes |
| 2025-09-19 | Down (essentially flat) | Down | Yes |
| 2025-12-19 | Up (essentially flat) | Up | Yes |
| 2026-03-20 | Up | Up | Yes |
| 2026-06-18 | Up | Up | Yes |

Observed recent discovery result: **8/8 directional matches** between the 3:30→close sign and the next-session opening-gap sign.

This must **not** be described as an 8/8 predictive win rate. The panel is tiny, was reconstructed after the hypothesis was already noticed, and includes several very small late-day moves whose sign may be unstable to reasonable alternate definitions.

## Important decomposition
The apparent relationship is concentrated in the **overnight gap**, not in reliable continuation through the following RTH session.

- 3:30→close direction vs next-session open→close direction: **4/8 same direction**.
- 3:30→close direction vs expiration close→next-session close: **5/8 same direction**.

Therefore the discovery does **not** support a rule that the entire next trading day should continue in the late-expiration direction.

## 2026-09-18 → 2026-09-21 observation
2026-09-18 was the September quarterly-expiration session. On 2026-09-21 SPY was strongly higher intraday, providing an additional qualitatively supportive post-expiration observation. This observation is **not yet counted in the frozen historical panel** until the exact 2026-09-18 3:30→close signal and next-open outcome are computed under the same definition.

The 2026-09-21 rally also had independent contemporaneous drivers, so it must not be causally attributed to expiration mechanics alone.

## Prior-work context
Published expiration research has documented expiration-related price/volume distortions and, in some samples, partial reversals associated with expiration microstructure. That literature means a same-direction late-close→next-open relationship is not something to assume is universal or structurally permanent. The Investing OS finding should therefore be treated as a recent-regime discovery requiring out-of-sample historical falsification.

## Anti-moving-goalpost rules
Do not:
- change 3:30 PM to another start time after seeing outcomes;
- add a minimum late-day return threshold after seeing outcomes;
- redefine the outcome from next open to next close because one looks better;
- exclude inconvenient expiration events;
- treat holiday-adjusted expiration sessions differently except for their actual calendar date;
- convert the 8/8 discovery result into a live probability or scanner score;
- give this feature STRENGTH, RUNWAY, trigger, or directional authority before validation.

## Next clean falsification
Freeze the primary test exactly as:

> On each quarterly options/futures expiration session, classify SPY 3:30 PM ET → RTH-close direction by sign. Compare that sign with SPY expiration close → next RTH open gap direction.

Then extend the event panel backward using existing historical data before looking at aggregate outcomes, ideally to 2010 or earlier. Report:
- total N and match rate;
- Wilson confidence interval;
- magnitude of late-day move and next gap;
- results by year/era;
- sensitivity as a robustness check only for 3:00 and 3:45 PM starts, clearly separated from the frozen primary test;
- results excluding near-zero late moves as a **post-primary robustness analysis**, not as a rewritten rule.

The key falsification question is whether the recent 8/8 relationship remains materially above chance on the larger untouched historical panel or collapses toward ~50%.

## Production status
**NO SCANNER CHANGE. NO LIVE PROBABILITY. RESEARCH CONTEXT ONLY.**

The existing quarterly-expiration/rebalance risk gate remains unchanged: expiration/rebalance flows cannot improve STRENGTH, RUNWAY, trigger acceptance, runner conviction, or overnight quality, and late closing-auction behavior remains potentially distorted.