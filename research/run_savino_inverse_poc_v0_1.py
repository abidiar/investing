#!/usr/bin/env python3
"""Re-score the October 8 Savino inverse pilot from persisted 30-minute data.

A retrospective engineering demonstration, NOT prospective validation.
Input: results/savino_inverse_poc_2026-10-08_intervals.csv
The forecast_pixel_* values were read from the premarket chart ONLY,
not the red line on Savino's post-close result screenshot.
Original premarket screenshot SHA256:
c6f0e58c5b5bb2e2710c477d1b885fc9e4bd611f86613d96522f2c5130d726e9
PRE screenshot time: 2026-10-08 approx 08:58 ET.
SPY candles are a Webull five-minute proxy, not exact SPX index intraday bars.
"""
from pathlib import Path
import csv
from collections import Counter

CSV = Path(__file__).parent / "results" / "savino_inverse_poc_2026-10-08_intervals.csv"

def fsign(y0, y1):
    d = y0 - y1   # Screen y decreases when red forecast points higher.
    return "UP" if d > 12 else "DOWN" if d < -12 else "FLAT"

def psign(p0, p1):
    d = p1 - p0
    return "UP" if d >= 0.15 else "DOWN" if d <= -0.15 else "FLAT"

with CSV.open(newline="") as file:
    records = list(csv.DictReader(file))
assert len(records) == 12, f"Expected twelve fixed half-hour windows; found {len(records)}"

matches = 0
actual = []
for r in records:
    forecast = fsign(float(r["forecast_pixel_y_start"]), float(r["forecast_pixel_y_end"]))
    observed = psign(float(r["spy_close_start"]), float(r["spy_close_end"]))
    assert forecast == r["forecast_direction"], r["window_et"]
    assert observed == r["actual_spy_direction"], r["window_et"]
    assert (forecast == observed) == bool(int(r["matched"]))
    matches += int(forecast == observed)
    actual.append(observed)

print(f"Morning inverse vs Webull SPY signs: {matches}/{len(records)}")
print(f"Always-UP benchmark: {sum(x == 'UP' for x in actual)}/{len(records)}")
print(f"Always-DOWN benchmark: {sum(x == 'DOWN' for x in actual)}/{len(records)}")
assert matches == 6
assert Counter(actual)["UP"] == 6 and Counter(actual)["DOWN"] == 6
print("PASS: fixed 12-window pilot matches persisted source-derived values.")
