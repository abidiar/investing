from __future__ import annotations

from dataclasses import dataclass
from typing import Any


@dataclass
class Snapshot:
    symbol: str
    last: float | None
    session_vwap: float | None
    open: float | None
    high: float | None
    low: float | None
    or5_high: float | None
    or5_low: float | None
    or15_high: float | None
    or15_low: float | None
    return_since_open: float | None
    new_session_low: str
    volume: float | None
    last_bar_time: str


def _range_stats(
    bars: list[dict[str, Any]],
    count: int,
) -> tuple[float | None, float | None]:
    selected = bars[:count]

    if len(selected) < count:
        return None, None

    return (
        max(float(bar["high"]) for bar in selected),
        min(float(bar["low"]) for bar in selected),
    )


def build_snapshot(
    symbol: str,
    bars: list[dict[str, Any]],
    quote: dict[str, Any] | None,
) -> Snapshot:
    quote = quote or {}

    if not bars:
        last_value = quote.get("last")

        try:
            last = (
                float(last_value)
                if last_value is not None
                else None
            )
        except (TypeError, ValueError):
            last = None

        return Snapshot(
            symbol=symbol,
            last=last,
            session_vwap=None,
            open=None,
            high=None,
            low=None,
            or5_high=None,
            or5_low=None,
            or15_high=None,
            or15_low=None,
            return_since_open=None,
            new_session_low="Unavailable",
            volume=None,
            last_bar_time="",
        )

    session_open = float(bars[0]["open"])
    session_high = max(float(bar["high"]) for bar in bars)
    session_low = min(float(bar["low"]) for bar in bars)
    total_volume = sum(
        float(bar.get("volume") or 0)
        for bar in bars
    )

    # Webull one-minute bars provide OHLCV but no native per-bar VWAP.
    # Use each bar's typical price, weighted by its volume, to calculate
    # a transparent session VWAP proxy from the completed RTH bars.
    weighted_vwap = sum(
        (
            (
                float(bar["high"])
                + float(bar["low"])
                + float(bar["close"])
            )
            / 3.0
        )
        * float(bar.get("volume") or 0)
        for bar in bars
    )

    session_vwap = (
        weighted_vwap / total_volume
        if total_volume > 0
        else None
    )

    quote_last = quote.get("last")

    try:
        last = (
            float(quote_last)
            if quote_last is not None
            else float(bars[-1]["close"])
        )
    except (TypeError, ValueError):
        last = float(bars[-1]["close"])

    or5_high, or5_low = _range_stats(bars, 5)
    or15_high, or15_low = _range_stats(bars, 15)
    ret = (
        (last / session_open - 1.0)
        if session_open
        else None
    )

    if len(bars) < 2:
        new_low = "Unavailable"
    else:
        prior_low = min(
            float(bar["low"])
            for bar in bars[:-1]
        )
        latest_low = float(bars[-1]["low"])
        new_low = "Yes" if latest_low < prior_low else "No"

    return Snapshot(
        symbol=symbol,
        last=last,
        session_vwap=session_vwap,
        open=session_open,
        high=session_high,
        low=session_low,
        or5_high=or5_high,
        or5_low=or5_low,
        or15_high=or15_high,
        or15_low=or15_low,
        return_since_open=ret,
        new_session_low=new_low,
        volume=total_volume,
        last_bar_time=str(bars[-1].get("time") or ""),
    )


def benchmark_for(
    symbol: str,
    relevant_sector: str,
    expected_leader: str,
    constituent_symbols: set[str],
) -> str | None:
    symbol = symbol.upper()
    relevant_sector = relevant_sector.upper()
    leader_text = expected_leader.lower()

    if symbol == "SPY":
        return None

    if symbol in {"QQQ", "RSP", "IWM", "SPXL"}:
        return "SPY"

    if symbol in {"XLK", "SMH", "SOXX", "TQQQ", "SOXL"}:
        return "QQQ"

    if symbol in constituent_symbols and relevant_sector:
        return relevant_sector

    if symbol == relevant_sector:
        return (
            "QQQ"
            if (
                "tech" in leader_text
                or "semi" in leader_text
            )
            else "SPY"
        )

    return "SPY"


def relative_strength(
    snapshot: Snapshot,
    benchmark: Snapshot | None,
) -> float | None:
    if snapshot.return_since_open is None:
        return None

    if benchmark is None:
        return snapshot.return_since_open

    if benchmark.return_since_open is None:
        return None

    return (
        snapshot.return_since_open
        - benchmark.return_since_open
    )
