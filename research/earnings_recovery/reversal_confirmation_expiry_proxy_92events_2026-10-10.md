# Reversal confirmation vs day-three entry; calendar-DTE stock proxies

October 10, 2026. Exploratory, NOT a validated options strategy. Source: [previously frozen 92-event earnings-selloff cohort](./earnings_selloff_recovery_92events_2026-10-10.csv), 32 tickers, 2023–June 2026; price paths from connected Webull RTH 1,100 daily bars per stock, validated against the earlier source study's first five-session return (within 0.06 percentage points). Contemporary ticker selection and published financial records impose survivor, selection, vintage/restatement and timestamp biases.

## Signals
- **Day three:** buy open of third regular session AFTER qualifying selloff close, all 92 opportunities.
- **Two-up confirmation:** first post-selloff day, within 10 sessions, with two successive higher CLOSES and current daily LOW > prior session LOW; enter NEXT session open. No trigger = no entry.
- **High reclaim:** first daily close ABOVE qualifying selloff day's daily HIGH within 10 following sessions; enter NEXT session open. No trigger = no entry.

Exit test: 20 *entry-inclusive* trading sessions. Underlying stock profit +5%, stop −5% from entry open. For a stop or target at the open, execute at open; if both are touched within the same bar, assume the STOP occurred first. Neither touched => sell at 20th close. No commissions, spreads, slippage, tax, dividends, or option pricing. Each strategy may enter at a different calendar time. All 92 events, including untriggered, remain visible in the event-level audit.

| Rule | Entries / 92 | +5% targets | −5% stops | Timeouts | Average gross underlying stock return |
|---|---:|---:|---:|---:|---:|
| day3 | 92/92 | 47 (51.09%) | 35 | 10 | 0.77% |
| two_up | 73/92 | 38 (52.05%) | 25 | 10 | 0.88% |
| reclaim | 37/92 | 21 (56.76%) | 12 | 4 | 1.60% |

## Matched opportunity comparison (controls for selective triggering)

| Signal cohort | N | Day-three baseline target hits | Day-three mean | Confirmed-signal targets | Confirmed-signal mean | Signal minus Day-three |
|---|---:|---:|---:|---:|---:|---:|
| two_up | 73 | 41 | 1.24% | 38 | 0.88% | -0.36 pp |
| reclaim | 37 | 25 | 2.66% | 21 | 1.60% | -1.06 pp |

Signal versus day-three paired ticker-cluster bootstrap 95% intervals from the same study (4000 bootstrap replicates): two-up change −0.36pp [−1.33,+0.60], reclaim change −1.06pp [−2.54,+0.40]; both include zero. These exploratory contrasts may overfit the previously studied universe, and are not independent prospective tests.

## Expiration-horizon *stock-price* proxy
This is **not actual call-option profitability**. Evaluate each signal from next-open entry over **7/14/30/45/60/90 CALENDAR days**; check the underlying +5% BEFORE −5% from entry. Count targets, stops and timeouts, stop-first on ambiguous bars and open gap execution. For unresolved trades, stock-price return is the last regular-session closing value at/before the nominal calendar cutoff. No claim that actual listed option expires that day; no strike, delta, IV, theta, bid/ask, commissions or premium modeled. Longer DTE calls generally cost more; greater stock target success with time does NOT imply better option risk/reward.

| Calendar-DTE proxy | Day 3 target hits | Two-up target hits | High reclaim target hits |
|---|---:|---:|---:|
| 7 | 22/92 (23.91%) | 22/73 (30.14%) | 15/37 (40.54%) |
| 14 | 37/92 (40.22%) | 32/73 (43.84%) | 20/37 (54.05%) |
| 30 | 47/92 (51.09%) | 38/73 (52.05%) | 21/37 (56.76%) |
| 45 | 49/92 (53.26%) | 41/73 (56.16%) | 24/37 (64.86%) |
| 60 | 50/92 (54.35%) | 42/73 (57.53%) | 25/37 (67.57%) |
| 90 | 53/92 (57.61%) | 43/73 (58.90%) | 25/37 (67.57%) |

### Target, stop and unresolved counts
| Strategy | Days | Targets | Stops | Timeouts | Avg managed underlying return |
|---|---:|---:|---:|---:|---:|
| day3 | 7 | 22 | 22 | 48 | 0.20% |
| day3 | 14 | 37 | 27 | 28 | 0.32% |
| day3 | 30 | 47 | 36 | 9 | 0.74% |
| day3 | 45 | 49 | 37 | 6 | 0.69% |
| day3 | 60 | 50 | 38 | 4 | 0.64% |
| day3 | 90 | 53 | 39 | 0 | 0.78% |
| two_up | 7 | 22 | 14 | 37 | 0.57% |
| two_up | 14 | 32 | 20 | 21 | 0.62% |
| two_up | 30 | 38 | 26 | 9 | 0.76% |
| two_up | 45 | 41 | 29 | 3 | 0.80% |
| two_up | 60 | 42 | 29 | 2 | 0.85% |
| two_up | 90 | 43 | 30 | 0 | 0.84% |
| reclaim | 7 | 15 | 3 | 19 | 1.80% |
| reclaim | 14 | 20 | 6 | 11 | 2.11% |
| reclaim | 30 | 21 | 12 | 4 | 1.60% |
| reclaim | 45 | 24 | 12 | 1 | 1.81% |
| reclaim | 60 | 25 | 12 | 0 | 1.99% |
| reclaim | 90 | 25 | 12 | 0 | 1.99% |

## Decision
The two confirmation rules failed to improve day-three trading outcomes on matched opportunities (n=73, n=37). No A+ trade rule. For day-three, +5% before −5% occurred in 22/92 by 7 calendar days and 47/92 by day 30; 53/92 by day 90. Additional waiting also exposes entries to more stops. This does not rank call expirations because option premiums and IV differ dramatically with DTE. Most useful next *distinct* operation is a frozen out-of-sample entry validation, then contract-level options pricing if free historical option data can be verified. Do not pay for data without permission.

Audit: [276-row per-event/per-method CSV](./reversal_confirmation_expiry_proxy_92events_2026-10-10.csv).