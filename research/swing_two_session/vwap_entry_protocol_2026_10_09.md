# Frozen VWAP entry v1

Date: 2026-10-09. Historical backtest protocol, not a live trade instruction.

Universe: META ORCL DELL AMZN AAPL AMD MSFT GOOG CRM QCOM JPM CAT HD COST XOM BAC LLY INTC UBER PYPL.

Daily signal: previous 40 sessions' lowest low defines support, highest high resistance; range width >=6%; at least two prior support touches (low <=1.012*support) separated by >=5 sessions; signal low below support and close above support, with close within 0.995–1.025 times support; minimum five calendar days between signals per ticker; signal volume >=1.2 times prior 20-day average.

Entry next RTH session: calculate cumulative session VWAP using 5-minute typical price times volume; require one completed 5-minute close below VWAP followed by two consecutive completed closes above VWAP; enter at next bar open, no later than noon ET; otherwise no trade. Compare next-day opening baseline.

Exit +2% target, -2% stop, end of second session. Gap fills at open, stop-first for same-bar ambiguity, 0.20% round-trip costs, missed entries zero. Report coverage, hit rate, net per entry and per original event. No parameter changes after earlier-period results. This is retrospective validation, not a pristine untouched holdout.