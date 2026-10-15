# Frozen October 12 watchlist -> October 13 threshold-first audit

Status: NO TRADE. This is a stronger temporal test than retrospective October 14 candidate selection, but **not a full unbiased universe or valid sector/ATR-matched study**. Original report exists at research/oversold_rebound/scans/2026-10-12_1555_ET.md and selected TXG, IREN, ARM, AXTI, IONQ before Oct 13 outcomes. Historical Webull RTH M5 bars. Reference: last completed Oct 12 M5 candle 15:50–15:55 ET (Oct 12 19:50 UTC timestamp), not executable closing auction fill. Check Oct 13 09:30 onward for high >= reference*1.02 or low <= reference*0.99; first reached is counted, ties ambiguous. These are hypothetical price thresholds, NOT actual scanner confirmation entries or realistic stop fills; overnight gap can exceed nominal -1% loss.

|Symbol|Oct12 reference|Oct13 close|Oct13 close return %|First threshold|First threshold bar start ET|
|---|---:|---:|---:|---|---|
|TXG|74.88|71.79|-4.13|-1%|09:30|
|IREN|34.92|34.80|-0.34|-1%|09:30|
|ARM|254.815|255.39|+0.23|-1%|09:30|
|AXTI|62.075|64.63|+4.12|-1%|09:30|
|IONQ|36.235|34.73|-4.15|-1%|09:30|

Target-first 0/5; stop-first 5/5. **Not** a claim that frozen next-day Grimes failure-test strategy took five trades; its conditional 10:30–12 confirmations were never verified. Avoid overstating loss: no executable orders simulated.

Contemporaneously suggested sector/ATR peers from Oct 12 scan are TWST (TXG), CLSK/CIFR (IREN), NVTS (ARM), AEHR (AXTI), QBTS/RGTI (IONQ). These peers were also sold off in the report, so **they are not valid nonselloff controls**. Hypothetical next-day threshold-first outcomes from same 15:55 reference: TWST stop-first, CLSK stop-first, CIFR stop-first, NVTS target-first, AEHR stop-first, QBTS stop-first, RGTI stop-first. These do not establish matched causal effects. Nonselloff control study still requires dated comprehensive universe, sector/industry and ATR calipers fixed before outcomes. The October 12 scanner did not generate a market-wide exhaustive candidate list, so no population-level recall/false-positive estimate.

Research conclusion: automatic next-session calls on an oversold alert unsupported; distinguish discovery from confirmation and options execution. Keep existing frozen execution gates, original 283-event negative audit, and 49-name negative replication. No strategy edge validated.
