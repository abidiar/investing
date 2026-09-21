# Triple-Witching / Post-OPEX Research — Findings and Next Test

Date: 2026-09-21
Status: **RESEARCH SUMMARY FROZEN; 10:20 POST-OPEX ACCEPTANCE TEST PENDING DATA ACCESS**

## Original question
Does what SPY does late on quarterly/triple-witching expiration Friday contain useful information about what SPY is likely to do on the next trading day?

The broader practical question is now:

> After quarterly expiration, is there a reliable actionable tendency in SPY on the next trading day, and can information available by Friday close or Monday morning distinguish continuation from reversal?

## What our prior test found
The simple hypothesis that the direction of SPY's late Friday move predicts the next opening gap did **not** survive the long sample.

- Frozen historical panel: 64 quarterly-expiration events.
- Late-Friday-direction -> next-open-direction match: **33/64 = 51.6%**.
- A recent run beginning around September 2024 produced a striking **9/9** sequence, but this is a recent cluster rather than evidence of a durable all-history rule.

Conclusion: **Do not use `Friday late move direction -> Monday direction` as a standalone directional signal.**

## What public research says
Published market-structure research supports several narrower conclusions:

1. Expiration materially changes trading flows, volume and market microstructure.
2. Expiration-related price pressure can reverse after the mechanical flows end.
3. Classic S&P research found late expiration-Friday price pressure followed by some Monday-opening reversal, but much of the effect was attributed to market microstructure rather than persistent information.
4. Later research supports abnormal expiration-week behavior and some post-expiration giveback/underperformance, but the timing and magnitude are not stable enough to justify a universal bearish or bullish post-OPEX rule.
5. There is no strong published evidence that `triple-witching Friday up/down -> Monday up/down` is a robust directional rule.
6. Closing-auction structure changed materially in 2024. NYSE moved Closing D-Order imbalance visibility from 3:55 PM to 3:50 PM ET effective 2024-08-12 and reported earlier paired-notional accumulation and smoother imbalance adjustment. This is relevant context for the recent regime but does not prove the recent SPY 9/9 streak was caused by the auction change.
7. SPY is NYSE Arca-listed, so NYSE-listed constituent auction mechanics can at most be treated as a market-level mechanism/footprint when studying SPY without direct imbalance data.

## Data-acquisition conclusion
Direct historical auction imbalance / paired-quantity data exist through NYSE TAQ and Databento ARCX.PILLAR, but paid data are **not required for the practical trading question** and should not be purchased for this project at present.

Free SPY OHLCV can show a price/volume footprint but cannot identify actual auction imbalance direction or paired quantity. Therefore do not claim causality from SPY M5 bars.

## Practical interpretation
Triple witching is best treated as a **distortion / regime flag**, not a directional signal.

Friday's close may contain mechanical expiration/rebalance flows. The more useful information arrives when the next session shows whether those prices are accepted or rejected after the expiration flows are gone.

Working interpretation:

> Triple witching tells us Friday may be contaminated; Monday tells us whether the market actually agrees with Friday.

This is contextual only. Triple-witching status contributes **zero STRENGTH points and zero RUNWAY points** by itself.

## Next clean test — POST-OPEX ACCEPTANCE / REJECTION

Primary checkpoint: **10:20 ET on the first trading session after each frozen quarterly-expiration event**.

Secondary diagnostic checkpoints: 9:45 and 10:00 ET.

Classification must use only information available through the checkpoint.

### CONFIRMED
Monday has accepted Friday's directional move rather than merely opening in the same direction. Evidence should include the relevant Friday closing structure being held/accepted plus constructive Monday price behavior. Where available, VWAP acceptance and lack of meaningful opening rejection are supporting evidence.

### REJECTED
Monday has meaningfully reversed Friday's directional move, lost/rejected the relevant Friday closing structure and/or produced a failed VWAP hold/reclaim consistent with the opposite direction.

### AMBIGUOUS
Neither condition is sufficiently established. Do not force-classify.

The exact operational classification must be frozen before exposing post-10:20 outcomes and must not be adjusted event-by-event.

## Outcomes to expose only after classification
From 10:20 ET through the close measure:

- 10:20 -> close return.
- Maximum favorable excursion (MFE).
- Maximum adverse excursion (MAE).
- Whether +0.5% occurs before -0.5% in the classified direction.
- Whether +1.0% occurs before -0.5% and before -1.0% where sample/range permits.
- Whether the 10:20 classified direction survives into the close.
- Friday-close retest / rejection behavior.

Compare CONFIRMED vs REJECTED vs AMBIGUOUS.

If feasible, compare against ordinary Monday acceptance/rejection behavior to determine whether post-OPEX context adds information beyond normal intraday confirmation.

## Anti-overfitting rules
- Use the existing frozen quarterly-expiration event panel.
- Do not choose events based on outcomes.
- Do not redesign thresholds after seeing 10:20->close results.
- The recent 9/9 sequence cannot be used to define the classifier.
- Keep AMBIGUOUS as a legitimate state rather than forcing every observation into CONFIRMED or REJECTED.
- Do not surface a historical conditional win rate as a live probability without separate out-of-sample validation.

## Current blocker
The Webull historical M5-bars path used in the prior 64-event work is not currently exposed in the active session. The GitHub repository contains research state/protocols but not the complete underlying Monday M5 series required to calculate the test honestly.

Do not substitute fabricated results or silently switch to an unvalidated intraday dataset merely to finish the test.

When the historical M5 path is available again, the next operation is mechanical: classify the frozen events at 10:20 using the predeclared rule, then expose the post-10:20 outcomes.

## Production takeaway pending that test
Keep the standing **TRIPLE WITCHING / REBALANCE DISTORTION DAY** risk gate.

Do **not** add a Friday-direction -> Monday-direction signal.

A future `POST-OPEX ACCEPTANCE / REJECTION` context flag may be useful if the frozen 10:20 test shows materially better continuation/reversal discrimination than ordinary intraday confirmation. It must not create a trade by itself and must remain subordinate to price, STRENGTH, RUNWAY, R:R, sponsorship, extension and option-quality rules.
