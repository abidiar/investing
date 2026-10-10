# Does stable/raised forward guidance predict quality-company post-earnings recoveries?

**Completed 2026-10-10. VERDICT: the precise analyst-consensus-revision hypothesis is NOT TESTED because usable contemporaneous consensus snapshots were unavailable.** A narrower, retrospective *management-guidance proxy* was measured across the same 72 qualified events. Proxy results do NOT establish an edge for buy-on-day-3 call strategies; 60-session full recovery is directionally compatible with the intuition but massively underpowered.

## Frozen event cohort and methods
- Prior unrelated-company holdout: 65 new firms screened; 625 session-dated announcements 2023 through June 2026; 136 >=5% earnings selloffs; 72 PASS point-in-time accounting quality (positive TTM net income/FCF, last quarterly revenue YoY positive, debt/equity 0-2). 29 unique issuers. Events were already explored for price outcomes prior to historical manual guidance labelling; therefore **label-outcome review is retrospective/exploratory and NOT a blind holdout**.
- [2025-2026 label protocol](./outlook_guidance_feasibility_protocol_2025_2026.md) and [2023-2024 exact-roster extension](./outlook_guidance_2023_2024_extension_protocol.md) were committed before fetching each guidance source.
- Operational definition: compare ORIGINAL issuer SEC/IR releases that explicitly revisited EPS and/or companywide revenue guidance **for the same fiscal year**, with previous official guidance for that same fiscal year. Unchanged/raised = STABLE_OR_UP; lower with none higher = DOWN; contradictory EPS and revenue = MIXED; absent initial-year forecasts, only next-quarter outlook, no documented prior/current comparison, or invalid source = UNKNOWN. 27 events had sufficient traceable guidance evidence (23 stable/up, 3 down, one mixed); 45 remained unknown. This proxy is **management guidance**, not a measure of sell-side consensus changes, 1–5-day individual analyst EPS revisions, or pre/post expected 12-month EPS.
- Original tradable stock rule: open of third post-selloff trading session; +5% target or −5% stop, whichever touched first, opening gaps at open, same-bar ambiguity stop-first, otherwise end of entry-inclusive session 20. All stock prices from connected Webull RTH. Extend unchanged first-hit stop/target semantics through session 40/60 as sensitivity only. No options premiums, execution costs, dividends or slippage.
- Alternate non-trading endpoint: daily close regains pre-earnings close at least once within 20/40/60 post-selloff trading sessions, irrespective of interim drawdown. This measures **eventual price recovery**, not profitable execution.

## Primary results: day-three stock entry with ±5% stop/target, 20 sessions

| Guidance proxy | Events | +5% target first | −5% stop first | Timeouts | Mean gross stock P&L |
|---|---:|---:|---:|---:|---:|
| STABLE_OR_UP | 23 | 5 (21.7%) | 14 | 4 | −2.30% |
| DOWN | 3 | 1 (33.3%) | 2 | 0 | −1.37% |
| MIXED | 1 | 1 | 0 | 0 | +5.00% |
| UNKNOWN | 45 | 23 (51.1%) | 20 | 2 | −0.06% |

Fisher two-sided exact comparison of stable/up against down 20-session target-hit odds p=1.00; Wilson 95% intervals: stable/up ~[9.7%, 41.9%], down ~[6.1%, 79.2%]. **No evidence of improved short-horizon trade profitability from guidance maintenance; the down group is just 3 trades.** UNKNOWN is neither stable nor worsening and must not be relabelled as zero-change.

## Extended target-before-stop tests
| Guidance proxy | 40-session +5% targets | 40-session stops | 60-session +5% targets | 60-session stops | 60-session gross managed mean |
|---|---:|---:|---:|---:|---:|
| STABLE_OR_UP (n=23) | 6 | 17 | 6 | 17 | −2.39% |
| DOWN (n=3) | 1 | 2 | 1 | 2 | −1.37% |
| MIXED (n=1) | 1 | 0 | 1 | 0 | +5.00% |
| UNKNOWN (n=45) | 24 | 20 | 25 | 20 | +0.14% |

Extending stop-based position life did NOT rescue most stable/up-guidance cases: 17/23 eventually stopped by 60 sessions. Median/options effects cannot be inferred.

## Longer-horizon EVENTUAL full recovery (no stops)
The below refers to at least one closing price >= pre-earnings price within the window from SELL-OFF day, even if interim price went substantially lower.

| Guidance proxy | Within 20 sessions | Within 40 sessions | Within 60 sessions |
|---|---:|---:|---:|
| STABLE_OR_UP (n=23) | 2 (8.7%) | 6 (26.1%) | 11 (47.8%) |
| DOWN (n=3) | 0 | 0 | 0 |
| MIXED (n=1) | 0 | 0 | 0 |
| UNKNOWN (n=45) | 15 (33.3%) | 23 (51.1%) | 27 (60.0%) |

**No statistical conclusion** can be drawn for 11/23 versus 0/3: Fisher two-sided p≈0.238 and unmatched company sector composition. Yet it points to the meaningful *separation* between eventual recovery and a risk-limited option/call entry. At 60 sessions, stable/up had mean unmanaged 60-session return +1.71% from day-three open, even while its stop-managed counterpart was −2.39%; it is not possible to turn those paths into an automatic options win.

## Exact illustrative source links (all sources tied to announcement date)
- [NOC April 22, 2025](https://www.sec.gov/Archives/edgar/data/1133421/000113342125000022/noc-03312025xearningsrelea.htm): adjusted FY2025 EPS $27.85–28.25 cut to $24.95–25.35, sales reaffirmed. Full-year guidance DOWN.
- [DLTR May 25, 2023](https://corporate.dollartree.com/news-media/press-releases/detail/245/dollar-tree-inc-reports-results-for-the-first-quarter): EPS cut with annual sales maintained. DOWN.
- [DG August 31, 2023](https://www.sec.gov/Archives/edgar/data/29534/000115752323001382/a53546712ex99.htm): both FY sales and EPS cut. DOWN.
- [ZBH May 5, 2025](https://investor.zimmerbiomet.com/news-and-events/news/2025/05-05-2025-113050819): FY EPS cut but reported-sales guidance lifted by a business acquisition while organic growth guidance unchanged. MIXED (EPS-only sensitivity = DOWN).
- [WAB July 24, 2025](https://ir.wabteccorp.com/news-releases/news-release-details/wabtec-reports-second-quarter-2025-results-raises-adjusted-eps): annual EPS & revenue raised. STABLE_OR_UP.
- [ZBH April 28, 2026](https://investor.zimmerbiomet.com/news-and-events/news/2026/04-28-2026-113031821): FY EPS raised $8.30–8.45 to $8.40–8.55, companywide sales outlook unchanged. STABLE_OR_UP.
- [ADP Jan 25, 2023](https://www.sec.gov/Archives/edgar/data/8670/000000867023000002/q2fy23exhibit99.htm): FY revenue and adjusted EPS maintained. STABLE_OR_UP.
- All label sources included **per event** in audit CSV.

## EPS direction only sensitivity
Restrict to observed EPS changes (rather than EPS-or-revenue):
- EPS RAISED: 9, with 1 +5% target, mean managed −3.55%.
- EPS STABLE: 14, with 4 +5% target, mean managed −1.49%.
- EPS LOWERED: 4 (includes mixed ZBH May 2025), with 2 +5% targets, mean managed +0.22%.
- EPS UNKNOWN: 45, with 23 +5% targets, mean managed −0.06%.
This also fails to support a short-term recovery advantage from a positive EPS-guidance revision in this selected group. Still severely underpowered.

## Why exact analyst revision hypothesis is not measured
- Webull forecast EPS feed only returned latest reported-quarter estimates, not historical pre-release and +1/+3-day *revisions to the same future quarter or fiscal year*.
- Connected Google Sheet **Revisions** tab contains only column headers and zero observations.
- Other connected historical analyst-data sources tested: Financial Datasets has zero credit balance, TipRanks quota exhausted, Quartr requires Pro. We did not purchase data or represent reports of EPS surprises as forward revisions.
- Point-in-time analyst revisions would require e.g. daily snapshots of FY1 EPS consensus, stamped before earnings release and 3 days after. Special consideration for EPS denominator when a company reports its quarter and FY1 rolls.
- Published academic work: Jonathan Milian, *The Information Content of Guidance and Earnings* (European Accounting Review 2018), shows management guidance contains information about drift; *Analyst Responsiveness and the Post-Earnings-Announcement Drift* (JAE 2008), relates revisions' timeliness to return drift. These papers are general background, not evidence our specific filter works on our sample.

## Caveats and recommendation
1. 27 classified events / 72 quality events (37.5%); 3 cuts is insufficient for a useful inference, and guide issuers are systematically unlike companies without comparable guidance.
2. Hindsight manual labels were assigned after original returns had been observed. This can induce analyst judgement/selection bias even with predetermined labeling rules.
3. Future revenue and EPS guidance can be distorted by acquisitions, FX and tariff impacts; comparing nominal revenue across firms could be wrong. Downward EPS guidance can include one-off adjustments.
4. Early historical earnings announcements may lack correct press-release timestamps (SEC 8-K filing later than issuer release); 2023-2026 contemporary ticker selection is survivorship-biased. Financial publication dates can be restated after the event.
5. Longer stock recovery may occur long after a 5% stop, cannot be equated with tradable call profits. Call strike, DTE, implied volatility changes, bid/ask and theta all unmodeled.
6. **Do not promote a guidance filter, a day-three buy, or any calls strategy to A+.** The useful next data operation is obtain *true point-in-time FY1 EPS consensus snapshots* for before earnings and +3 trading days, then redo 72 events and separate operationally actionable results from later-information signals. Do not pay for data without explicit authorization.

## Saved reproducible data
- [72-event dated-source label audit](./forward_guidance_proxy_audit_72events_2026-10-10.csv)
- [72-event 20/40/60 outcomes, management proxy](./forward_guidance_proxy_72events_horizon_audit_2026-10-10.csv)
- [Original independent company holdout](./holdout_results_missing_factors_2026-10-10.md)
