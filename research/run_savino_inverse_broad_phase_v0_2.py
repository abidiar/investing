#!/usr/bin/env python3
"""Reproduce Savino v0.2 October-8 broad directional phase metrics.

This is EXPLORATORY post-outcome analysis, not out-of-sample backtesting.
Reads immutable v0.1 forecast digitization and price endpoint CSV only.
No new image tracing and no tuning of thresholds.
"""
from __future__ import annotations

import csv
from collections import Counter
from pathlib import Path

HERE = Path(__file__).resolve().parent
SOURCE = HERE / "results" / "savino_inverse_poc_2026-10-08_intervals.csv"
EXPECTED = HERE / "results" / "savino_inverse_broad_phase_v0_2_windows.csv"

with SOURCE.open(newline="") as fh:
    old = list(csv.DictReader(fh))
assert len(old) == 12, f"expected 12 half-hour rows, got {len(old)}"

pixels = [float(old[0]["forecast_pixel_y_start"])] + [
    float(row["forecast_pixel_y_end"]) for row in old
]
spy = [float(old[0]["spy_close_start"])] + [
    float(row["spy_close_end"]) for row in old
]

def clock(k: int) -> str:
    return f"{10 + k // 2:02d}:{'30' if k % 2 else '00'}"

def direction(change: float, tolerance: float) -> str:
    if change > tolerance:
        return "UP"
    if change < -tolerance:
        return "DOWN"
    return "FLAT"

def one_window(start: int, duration: int, grid: str) -> dict[str, str]:
    end = start + duration // 30
    fc = direction(pixels[start] - pixels[end], 12.0)
    # Must match fixed v0.1 inclusive actual epsilon: >= 0.15.
    change = spy[end] - spy[start]
    ac = "UP" if change >= 0.15 else "DOWN" if change <= -0.15 else "FLAT"
    return {
        "date": "2026-10-08", "minutes": str(duration), "grid": grid,
        "window_et": f"{clock(start)}-{clock(end)}",
        "forecast": fc, "actual": ac, "spy_change": f"{change:.4f}",
        "match": str(int(fc == ac)),
        "start_idx": str(start), "end_idx": str(end)
    }

compiled: list[dict[str, str]] = []
for mins in (30, 60, 90, 120):
    width = mins // 30
    starts = {
        "fixed_1000": list(range(0, 13 - width, width)),
        "sliding_30min": list(range(13 - width)),
        "fixed_1030": list(range(1, 13 - width, width))
    }
    for grid, starts_for_grid in starts.items():
        matches = [one_window(idx, mins, grid) for idx in starts_for_grid]
        compiled.extend(matches)
        counts = Counter(row["actual"] for row in matches)
        hits = sum(int(row["match"]) for row in matches)
        print(f"{mins:>3}m {grid:>14}: {hits}/{len(matches)} matches; "
              f"UP-only {counts['UP']}/{len(matches)}; DOWN-only {counts['DOWN']}/{len(matches)}")

with EXPECTED.open(newline="") as fh:
    stored = list(csv.DictReader(fh))
assert len(compiled) == len(stored) == 88, (len(compiled), len(stored))
for row_num, (a, b) in enumerate(zip(compiled, stored), start=2):
    for key, value in a.items():
        assert b[key] == value, f"line {row_num} {key}: recomputed={value!r}, persisted={b[key]!r}"

def result(minutes: int, grid: str) -> tuple[int, int]:
    subset = [x for x in compiled if x["minutes"] == str(minutes) and x["grid"] == grid]
    return (sum(int(x["match"]) for x in subset), len(subset))

assert result(30, "fixed_1000") == (6, 12)
assert result(60, "fixed_1000") == (2, 6)
assert result(90, "fixed_1000") == (4, 4)
assert result(120, "fixed_1000") == (3, 3)
assert result(60, "sliding_30min") == (5, 11)
assert result(90, "sliding_30min") == (9, 10)
assert result(120, "sliding_30min") == (7, 9)
assert result(120, "fixed_1030") == (1, 2)
print("PASS: all 88 fixed/sliding-window derived rows and checks align with archived v0.1 input.")
