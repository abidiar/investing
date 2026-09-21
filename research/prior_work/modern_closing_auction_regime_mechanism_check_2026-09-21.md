# Modern Closing-Auction Regime — Mechanism/Data Check

Date: 2026-09-21
Status: PRIOR-WORK / DATA-SUFFICIENCY CHECK; NO RETURN RULE CHANGE

## Purpose
Before running another SPY return backtest, determine whether the proposed post-August-2024 closing-auction mechanism can be tested with existing/public data without pretending SPY M5 price/volume proves auction causality.

## Externally documented facts
1. NYSE moved inclusion of Closing D-Orders in closing-auction imbalance information from 3:55 PM to 3:50 PM beginning 2024-08-12.
2. NYSE subsequently reported that the share of entered Closing D-Orders submitted before 3:50 rose from <20% to >27%, while final-seconds entry declined; paired notional built faster and imbalance variability around the old 3:55 disclosure point fell.
3. As of Aug. 2024, Closing D-Orders represented >46% of NYSE Closing Auction executed volume; the NYSE close had risen to ~10.52% of NYSE-listed trading volume.
4. Historical NYSE research already showed >90% of D-Orders were submitted after 3:30 PM, with heavy concentration in the final minutes.
5. NYSE later changed the Significant Imbalance methodology on 2024-10-28, replacing a static 50,000-share threshold with a dynamic threshold tied to each symbol's average closing size plus a notional floor. This is a second post-break market-structure change and means the post-Sep-2024 period is not governed by one single unchanged auction rule.
6. NYSE Arca has its own closing-auction mechanics; SPY is Arca-listed. Therefore the NYSE floor D-Order rule cannot be treated as a direct rule change to SPY itself.
7. Public NYSE research documents auction-level mechanics for NYSE-listed stocks, while true historical auction imbalance/paired-quantity data are available through NYSE TAQ historical products.

## Data-sufficiency verdict
Existing SPY M5 OHLCV is sufficient to test descriptive timing/volume behavior (3:30→3:50, 3:50→close, closing-volume concentration), but it is NOT sufficient to establish that the NYSE D-Order/imbalance mechanism caused the SPY next-open streak. SPY consolidated M5 volume mixes continuous trading, ETF activity and the closing print and does not expose constituent-level imbalance side, paired quantity, indicative match price, or auction-only matched notional.

Therefore a pure SPY M5 'mechanism test' would overclaim what the data identify.

## Clean research decision
Do not run an outcome-driven pre/post optimization on SPY M5 mechanics as if it validates auction causality.

The next defensible branch has two layers:
A. FREE/DESCRIPTIVE: use published NYSE/BMLL evidence to establish that closing-auction timing/composition changed materially in 2024 and separately inspect SPY M5 timing/volume only as descriptive corroboration.
B. CAUSAL/MECHANISM: if we want to test whether auction imbalance explains the 9/9 recent SPY streak, obtain event-level auction data (imbalance side, paired quantity, indicative match price, auction matched notional) for S&P 500 constituents and/or directly relevant Arca/SPY auction data. NYSE TAQ is a documented source; equivalent exchange historical imbalance feeds may also qualify.

## Important falsification clue
The mechanism is not a single clean August-2024 switch. A second NYSE imbalance-methodology change occurred on 2024-10-28. Any eventual mechanism protocol must freeze these dates from exchange documentation and must not choose breakpoints from SPY outcomes.

## Production status
NO SCANNER CHANGE. The prior 3:30→close directional rule remains failed over long history. The 2024-09→2026-09 9/9 run remains a descriptive recent-regime cluster only.