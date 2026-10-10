# Earnings-selloff rebound options timing — new premium sensitivity run
Date 2026-10-10. Verdict: **RESEARCH-ONLY / NO VALIDATED CALL BUYING EDGE**.
This is NOT an actual option return backtest. Input was the pre-existing 164 quality-company earnings-selloff daily stock paths; a fixed European Black–Scholes ATM call was modeled with arbitrary IV assumptions, nominal DTE, and approximate costs. NO new price paths were invented.

## What was actually performed
- Read prior work and froze `options_execution_model_protocol_2026-10-10.md` before performing this new pricing calculation. Source code: `run_options_execution_model_2026-10-10.cjs`. Aggregate scenario output: `options_execution_model_results_2026-10-10.json`.
- Reconstructed exact original four entries: next open, day three, first SMA5 reversal after crossover/high break, first three-rising-lows breakout/high break, as of the next regular-session open.
- 576 signal/entry combinations; times five DTE (14,30,45,60,90 days), three entry implied vols (25%, 40%, 60%), three paths (initial IV −10, flat, +10 absolute points over 10 calendar days) = **25,920 modeled call trade-paths**, representing 164 previously inspected events and repeated scenarios, not 25,920 independent trades.
- Model: ATM synthetic strike at each entry open, r=4%, dividends excluded, 2% illustrative combined spread + $0.65 per contract each way. Exit when underlying reaches +5% / −5% from entry (stop-first OHLC), or at 20 sessions / before expiry, whichever occurs first. Premium was repriced at modeled event spot. Not actual exercise, listed contracts, implied volatility term structures, IV crush observations, quotes, slippage, or fills.

## Primary sensitivity scenario, IV 40% at entry and −10 absolute vol points over 10 calendar days
The table gives conditional mean modeled CALL premium return for executed signal trades, all negative. Entries: next-open 92/72, day3 92/72, SMA 71/57, rising-lows 68/52 (original/holdout).

| Entry | Original 45D | Holdout 45D | Original 90D | Holdout 90D |
|---|---:|---:|---:|---:|
| Next open | −22.8% | −22.4% | −20.4% | −20.8% |
| Day three | −15.7% | −28.7% | −15.3% | −25.4% |
| SMA reversal | −12.0% | −31.4% | −13.0% | −26.7% |
| Three rising lows | −23.8% | −19.0% | −21.4% | −18.1% |

For 14-day calls, a large fraction of model exits were forced near nominal expiry without touching +5%/-5%. Across the 45-day primary scenario, modeled profitable trade fraction ranged from about 36.8% to 54.9% depending on method/cohort. Note *modeled* not actual win probability.

## Same-opportunity entry timing comparisons at 45 days, IV40 / −10-point drift
- SMA minus same-event day3: original +8.5 percentage points call-return advantage; distinct-company holdout **−1.8 pp**. No replication.
- Rising lows minus same-event day3: original **−9.0 pp**; holdout **+2.0 pp**. No replication.
- No rule wins reliably across the cohorts; do not use this model to pick a trigger.

## IV sensitivity dominates outcome inference
At 45 days with 40% initial IV: day-three original cohort average went from −15.7% with −10 points IV change to −3.9% with flat IV and +8.4% with +10 points; holdout −28.7% to −16.5% to −3.6%. The original SMA 45-DTE result ranges −12.0% / +0.3% / +13.0% across the same three IV paths, while the holdout remained −31.4% / −18.7% / −5.4%. Thus modeled sensitivity outputs depend heavily on unobserved historical IV and are NOT evidence of realized profitability. Some low-IV/rising-IV scenario cells are positive; no method/DTE had a positive mean consistently across tested scenarios AND both cohorts.

## Premium drawdown and real-world fit
Modeled *intraday low-based* worst interim premium drawdown proxies in the primary scenario for 45-DTE positions averaged roughly −41% to −55%, depending on cohort/method. Those are stress estimates, and within-day sequencing may overstate realized drawdown. The exact ATM option premium for stocks above $100 is often hundreds of dollars per 100-share contract even when 45 days out, so these synthetic ATM trades may be infeasible for an approximately $50 options budget. Affordable out-of-the-money calls have materially different delta/theta and can be more vulnerable; NO such budget-constrained actual contract test was performed.

## Actual historical option price feasibility
- Connected Massive returned 22 daily historical TRADE-derived bars for the specified listed AAPL 2025-05-16 $200 call during April–May 2025, establishing some access to expired options daily bars.
- Correct historical option NBBO endpoint /v3/quotes/O:... returned NOT_ENTITLED; the connected subscription does not include historical executable bid/ask. Do not pay for upgrades.
- Four fixed pilot events were predeclared in the protocol (DELL, QCOM, PYPL, AMAT 2025). Subsequent specific contract-bar requests returned RATE_LIMIT before the sample could be fetched. **PILOT NOT COMPLETED.** Do not present its planned contract list as observed results.
- Alpaca official documentation says option historical data begin Feb 2024, but the connected tools do not expose historical option bar/quote retrieval. Its free indicative quote feed is not OPRA bid/ask.
- Historical daily option last/trade OHLC would only be an indicative comparison: no matched stock/option timestamp, spreads, actual execution price, actual historical available IV, and possible adjusted-underlying mismatch.

## Decision
- Do NOT promote immediate/day3/SMA/rising-lows calls or any specific DTE to scanner or automated buys.
- The full-sample pricing sensitivity indicates substantial modeled premium-loss risk even when stock rebounds, but it is NOT a validated strategy backtest. The huge scenario dependence on IV means it cannot identify the optimal expiration.
- Most important NEW decision variable to obtain for the next stage: historical ACTUAL option ask at candidate entry, IV/skew/term structure and liquidation bid at exit; also contract affordability relative to user debit cap.
- Next clean priority when the connected provider rate limit resets: fixed four-event daily option-trade-bar pilot strictly as non-executable observation, then prospective executable bid/ask shadow log on new earnings-selloff events; if quotes remain inaccessible, perform preregistered *hypothetical* affordable OTM delta/budget and debit-spread sensitivities without overinterpreting the previously inspected cohort.
- Preserve the 164 event sets as development only; untouched prospective cohort is required to validate any rule. 
