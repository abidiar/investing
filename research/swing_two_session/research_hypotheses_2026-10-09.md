# Two-session +2% before -1% swing research — hypothesis register (2026-10-09)

Status: literature review and preregistration only. NO historical event-level backtest executed. Not part of frozen A+ DAY DETECTOR v1.0.

## Objective
Among liquid US equities, identify prospectively observable signals with first +2% before -1% over next two regular sessions, using executable entries, stop-first ambiguous bars, overnight gap realism, fees/slippage, and strict point-in-time data. Also report +3%, +5%, MAE/MFE, close returns, sample counts, base rates, and calibration. Never advertise backtest hit rates as live probabilities.

## Families and initial candidate grids (NOT validated)
A. Oversold recovery: 3-day returns <= -6%, RSI(2)<10 or RSI(14)<30, capitulation volume and subsequent higher low/reclaim; stratify catalyst, sector and market regime.
B. Earnings overreaction: earnings gap <= -8%, stratify surprise, raised/unchanged/cut guidance, analyst revisions and first-two-session stabilization. Do not assume bad news is overreaction.
C. Positive catalyst continuation: positive surprise/revisions, elevated RVOL, sector relative strength, VWAP/price acceptance and defined pullback entry.
D. Sympathy selloff/rebound: sector-driven weakness absent comparable company-specific bad news; require point-in-time event classification.
E. Failed breakdown and support reclaim.
F. Prior fourth-down-close and Kingsman hypotheses: historical results unverified; recover source files and freeze event discovery before outcomes.

## Experimental discipline
Historical train/validation/untouched test split chronologically, with purging for overlapping two-day events; no survivor bias, split-adjustment leakage, or hindsight news labels. Compare to unconditional universe, sector-matched and volatility-matched baselines. Use high/low sequencing from minute bars; if ambiguous score stop-first. Report Wilson intervals, subgroup counts, false discovery risk, opportunity rate, realized P&L and capacity. Separate stock outcomes from options execution/IV decay. Predefine first executable trigger and eligibility; no after-the-fact entry choice.

## Literature leads (not proof of the specified outcome)
- Chen et al. (2025), Maxing out short-term reversals in weekly stock returns, Journal of Empirical Finance 82, 101608, DOI 10.1016/j.jempfin.2025.101608. Weekly high-MAX reversal result, with liquidity/retail caveats.
- Fink (2021), A review of the Post-Earnings-Announcement Drift, DOI 10.1016/j.jbef.2020.100446.
- Analyst responsiveness and the post-earnings-announcement drift, Journal of Accounting and Economics 46 (2008), DOI 10.1016/j.jacceco.2008.04.004.
- Chordia et al. (2009), Liquidity and the Post-Earnings-Announcement Drift, Financial Analysts Journal 65: 18-32; transaction costs may consume much of gross anomaly returns.
- Bathke et al. (2019), Investor Overreaction to Earnings Surprises and Post-Earnings-Announcement Reversals, DOI 10.1111/1911-3846.12491.
- 2026 working paper DOI/SSRN abstract_id=6440878 disputes interpreting longer drift purely as underreaction.

## Repository audit
Verified research/a_plus_daily/2026-10-09.md and research/a_plus_cumulative_2026-10-09.md. GitHub code search for reversal, fourth down, Kingsman and 2% yielded no matching files; older event panels remain unverified. Frozen A+ scorecard remains separate and unchanged.

## Next execution
Locate canonical historical OHLCV and corporate-event source, verify coverage/adjustments; build pre-outcome signal table; freeze candidates; then reveal forward paths and compute outcome matrices. Do not claim completion before actual execution.
