# Capturing quality-company earnings rebounds without entering too early
**Date: October 10, 2026 | Verdict: exploratory; one candidate worth testing, no validated call-buying edge**

## Data, auditability, and design
- [Frozen before new outcome calculations](./actionable_bounce_entry_protocol_2026-10-10.md). 92 previously explored quality-company post-earnings selloffs + 72 historical quality-qualified events from a separate 65-company selection = 164 event opportunities, 61 unique symbols, Jan 2023–June 2026. Original cohorts and their outcomes had already been observed. This is therefore **NOT genuinely new out-of-sample validation of the new signals**; report both separately and demand an untouched time-based period or live forward record before deployment.
- Reconnected Webull RTH daily OHLC, 1,200 candles/symbol; verified each selloff's known 5-session return or the saved day-3 opening price. Frozen exact daily windows in [price series archive](./actionable_bounce_event_price_windows_164_2026-10-10.json); [164×4 modeled entry records](./actionable_bounce_entries_164x4_2026-10-10.csv); [164×6 selloff-close first-touch paths](./actionable_bounce_event_paths_164_2026-10-10.csv). Complete 20, 40, and 60 post-event session coverage.
- **Baseline entries:** buy next opening session or third post-event opening session.
- **SMA5 reclaim:** among post-event sessions 5–20, first session closing above current 5-session closing-price average, when preceding close was at or below its own five-session average, AND current close exceeds preceding day's high. Enter NEXT session open only if that open <=1.08× initial selloff closing price. If first signal gaps >8%, skip event, don't select a later trigger. Otherwise no signal -> no trade.
- **Three-lows break:** among sessions 3–20, first three completed successive session lows nondecreasing and latest close > both preceding session highs. Buy NEXT opening session, with same 8%-above-selloff-close no-chase rule.
- **Exits:** 5% underlying stock price target; −5% or −10% underlying stop, 20 or 40 entry-inclusive sessions; opening gaps fill at OPEN, intraday dual-touch stop-first. Censored none in recorded primary windows. Gross equity returns, no commission/slippage/spread, no option bid/ask/IV/time decay. For filtered rules, skipped opportunities count **zero** toward gross mean per original event.
- **Calendar-DTE proxy:** first +5% underlying target before −10% stock stop within 14/30/45/60 calendar days after actual modeled entry. This is NOT actual option profit, no real contract listing or premium.

## 1. Eventual rebound versus adverse move FIRST from known selloff CLOSE
| Cohort | N | +5% touched anytime in next 60 sessions | +5% first before additional −5% | +5% first before additional −10% |
|---|---:|---:|---:|---:|
| Original | 92 | 65 (70.7%) | 43 (46.7%) | 57 (62.0%) |
| Independent-company sample | 72 | 48 (66.7%) | 35 (48.6%) | 44 (61.1%) |

Median first touch of +5% among event-close touch winners: original 9 sessions; separate 9.5 sessions. Median worst excursion during 60 sessions was material even if the target later hit. These event-close prices are NOT actual entry fills. Greater than one in three eventual +5% rebounders had suffered or could suffer enough adverse movement to make tight calls unviable.

## 2. Fixed and confirmed entries, +5% TARGET / −5% STOP, max 20 entry-inclusive sessions
| Cohort | Method | Trades / event opportunities | Target hits / trades | Gross mean per triggered stock trade | Gross mean per *all* event opportunities |
|---|---|---:|---:|---:|---:|
| Original | Next open | 92/92 | 38/92 | −0.50% | −0.50% |
| Original | Day three | 92/92 | 47/92 | +0.77% | +0.77% |
| Original | SMA5 reclaim | 71/92 | 39/71 | +1.09% | +0.84% |
| Original | Three-lows break | 68/92 | 31/68 | +0.22% | +0.16% |
| Separate | Next open | 72/72 | 34/72 | −0.20% | −0.20% |
| Separate | Day three | 72/72 | 30/72 | −0.76% | −0.76% |
| Separate | SMA5 reclaim | 57/72 | 21/57 | −0.58% | −0.46% |
| Separate | Three-lows break | 52/72 | 27/52 | +0.57% | +0.41% |

Beware selective entry: a small set of easier-looking trades can have higher mean without improving within-event timing.

## 3. Looser stock stop: +5% TARGET / −10% STOP, 20 entry-inclusive sessions
| Cohort | Method | Entered | Target | Stop | Timed out | Gross mean / filled trade | Gross mean / all opportunities |
|---|---|---:|---:|---:|---:|---:|---:|
| Original | Next open | 92 | 53 | 17 | 22 | +0.38% | +0.38% |
| Original | Day 3 | 92 | 54 | 14 | 24 | +1.00% | +1.00% |
| Original | SMA5 reclaim | 71 | 43 | 9 | 19 | +1.69% | +1.30% |
| Original | Three-lows break | 68 | 37 | 7 | 24 | +1.22% | +0.90% |
| Separate | Next open | 72 | 38 | 15 | 19 | −0.39% | −0.39% |
| Separate | Day 3 | 72 | 34 | 14 | 24 | −0.77% | −0.77% |
| Separate | SMA5 reclaim | 57 | 24 | 6 | 27 | −0.04% | −0.03% |
| Separate | Three-lows break | 52 | 29 | 8 | 15 | +0.21% | +0.15% |

On each SMA5-entered event **paired with same-event day-three**, +5/-10, 20-session outcomes:
- Original n=71 (31 distinct stocks): SMA5 +1.69% vs day-three on SAME 71 +0.97%; difference **+0.71 percentage points**, ticker-cluster bootstrap exploratory 95% CI approximately **[−1.16, +2.30]**.
- Separate n=57 (26 distinct stocks): SMA5 −0.04% vs day-three SAME 57 −0.45%; difference **+0.42pp**, ticker-cluster CI approximately **[−0.56, +1.42]**.
Both intervals include zero. More time 40 sessions erodes original SMA5 profitability: +0.74%/filled trade and +0.57%/opportunity versus +1.69% and +1.30% at 20 sessions; separate 40 session +0.03%/filled trade.
- Three-low-break paired 20-session ±5% losses in original are worse than same-case day-three (−0.88pp); +5/−10 paired deltas −0.75pp original, −0.38pp separate. Do NOT promote this signal.

## 4. Time at risk and missed early bounces
- SMA5 entry: 71/92 and 57/72 filled, median lag **9** and **11** trading sessions respectively after the earnings selloff. **17/71** and **17/57** entries occurred AFTER the original selloff-close +5% rebound was already touched, so entering late may chase a *second* move. 14+12 no-signal events and 7+3 gapped-above-8%-chase-filter skips respectively.
- Three-low break: 68/92 and 52/72 entered; median lag 7 sessions in both, 12/68 and 13/52 prior initial +5% rebounds; no robust advantage.
- The original 'quality-company eventually recovers' pattern is therefore not an executable call strategy without additional time/IV/path handling.

## 5. Underlying first +5% before −10% by calendar-DTE window (SMA5 entry)
| Calendar time from entry | Original signals (n=71) | Separate signals (n=57) |
|---:|---:|---:|
| 14 calendar days | 30 (42.3%) | 18 (31.6%) |
| 30 days | 44 (62.0%) | 24 (42.1%) |
| 45 days | 47 (66.2%) | 30 (52.6%) |
| 60 days | 49 (69.0%) | 35 (61.4%) |

The longer window catches more **underlying stock targets**, but also more stops and larger absolute call-premium cost, and does not imply longer calls have superior returns. Theta accelerates for near-expiry calls and earnings IV can change; real premium, strike/delta, spread and implied vol are unmeasured. For +5% target versus −10% stop, a pure hit-or-stop payoff needs at least about 66.7% full-target wins just to break even (before gaps, timeouts and fees); tight option calls can lose much more.

## Conclusion and distinct next hypothesis
Do NOT deploy as A+; the day-three benchmark fails the independent-company cohort and neither new rule proves a stable edge. SMA5 crossover with new high is a *promising candidate for falsification* because mean same-event difference was positive but statistically weak in both cohorts, and its separate cohort was approximately break-even gross before costs. Crucial research target now: can a price-based stabilization entry beat 'too early' after controlling whether the FIRST +5% rebound has already occurred, volatility-adjusted drop and sector-relative strength? Pre-register on an UNTOUCHED 2026Q3+/forward log and test stop risk, independent of options. Then obtain dated historical option quotes from a no-cost provider or clearly hypothetical quote-based Greeks sensitivity for 30/45/60 DTE; no claim that 14-day or 60-day contracts are proven best.

## Additional post-hoc 'already bounced' diagnostic (NOT a new trading rule)
After viewing the main strategy results, subdivided the SMA5-triggered trades by whether the original selloff closing price had already been exceeded by +5% intraday BEFORE the modeled entry and whether an additional -10% had occurred before entry. **This is explicitly post-hoc exploration, not previously frozen, and cannot establish a new filter.**

| Cohort | SMA5 events with early +5% bounce | Gross mean stock return (+5/−10, max 20 sessions) | SMA5 events WITHOUT early +5% bounce | Gross mean |
|---|---:|---:|---:|---:|
| Original | 17 | +0.68% | 54 | +2.00% |
| Separate | 17 | +0.66% | 40 | −0.33% |

The original sample appeared to favor waiting through an extra -10% dislocation and buying below the initial selloff anchor, but the separate sample pointed the opposite way: after an additional -10% decline, SMA5 signal outcome was +4.08% for 10 original events vs **−4.54%** for 9 separate events. Such instability is strong evidence NOT to create 'oversold 10%' filters from this archive. An unsighted forward series and actual option prices remain required.
