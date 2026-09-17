from __future__ import annotations

from datetime import datetime, time, timedelta
import logging
import os
import re
from typing import Any
from zoneinfo import ZoneInfo

from flask import Flask, jsonify, request

from calculations import build_snapshot, benchmark_for, relative_strength
from sheets_client import SheetsClient
from webull_client import WebullClient, WebullError


logging.basicConfig(level=os.getenv("LOG_LEVEL", "INFO"))
LOGGER = logging.getLogger("investing-os-post-open")

app = Flask(__name__)

SPREADSHEET_ID = os.environ.get("SPREADSHEET_ID", "").strip()
CONFIRMATION_SHEET = os.environ.get(
    "CONFIRMATION_SHEET",
    "Post-Open Confirmation",
).strip()
BAR_HISTORY_SHEET = os.environ.get(
    "BAR_HISTORY_SHEET",
    "Intraday Bar History",
).strip()

WEBULL_APP_KEY = os.environ.get("WEBULL_APP_KEY", "").strip()
WEBULL_APP_SECRET = os.environ.get("WEBULL_APP_SECRET", "").strip()
WEBULL_ACCESS_TOKEN = os.environ.get(
    "WEBULL_ACCESS_TOKEN",
    "",
).strip()
WEBULL_REGION_ID = os.environ.get(
    "WEBULL_REGION_ID",
    "us",
).strip()
WEBULL_API_ENDPOINT = os.environ.get(
    "WEBULL_API_ENDPOINT",
    "api.webull.com",
).strip()
WEBULL_TOKEN_DIR = os.environ.get(
    "WEBULL_TOKEN_DIR",
    "/tmp/webull-openapi-token",
).strip()

DATA_SOURCE = os.environ.get(
    "DATA_SOURCE",
    "Webull OpenAPI (Nasdaq Basic; non-SIP)",
).strip()
DATA_QUALITY = os.environ.get(
    "DATA_QUALITY",
    "WEBULL_NASDAQ_BASIC_NON_SIP",
).strip()

TIMEZONE = os.environ.get(
    "TIMEZONE",
    "America/New_York",
).strip()

ET = ZoneInfo(TIMEZONE)
UTC = ZoneInfo("UTC")
PHASE = "snapshot-connector-webull-v3-incremental-collector"
VWAP_SOURCE = "Webull 1m OHLCV typical-price VWAP"


def require_configuration() -> None:
    missing = [
        name
        for name, value in {
            "SPREADSHEET_ID": SPREADSHEET_ID,
            "WEBULL_APP_KEY": WEBULL_APP_KEY,
            "WEBULL_APP_SECRET": WEBULL_APP_SECRET,
        }.items()
        if not value
    ]

    if missing:
        raise RuntimeError(
            f"Missing required configuration: {', '.join(missing)}"
        )


def cell(
    rows: list[list[Any]],
    row_number: int,
    column_number: int,
) -> Any:
    row_index = row_number - 1
    col_index = column_number - 1

    if row_index >= len(rows):
        return ""

    row = rows[row_index]

    if col_index >= len(row):
        return ""

    return row[col_index]


def normalize_symbol(value: Any) -> str:
    text = str(value or "").strip().upper()

    if not text:
        return ""

    match = re.search(
        r"\b[A-Z]{1,6}(?:/[A-Z])?\b",
        text,
    )

    return match.group(0) if match else ""


def parse_constituents(value: Any) -> list[str]:
    raw = str(value or "")
    pieces = re.split(r"[,;/|\s]+", raw)
    result: list[str] = []

    for piece in pieces:
        symbol = normalize_symbol(piece)

        if symbol and symbol not in result:
            result.append(symbol)

    return result[:5]


def round_price(value: float | None) -> float | str:
    return "" if value is None else round(value, 4)


def percent_value(value: float | None) -> float | str:
    return "" if value is None else round(value, 6)


def current_market_window(
    now_et: datetime,
) -> tuple[datetime, datetime]:
    start = datetime.combine(
        now_et.date(),
        time(9, 30),
        tzinfo=ET,
    )
    end = (
        now_et.replace(second=0, microsecond=0)
        - timedelta(minutes=1)
    )
    return start, end


def completed_regular_session_minute_expected(
    now_et: datetime,
) -> bool:
    if now_et.weekday() >= 5:
        return False

    local_time = now_et.time().replace(tzinfo=None)
    return time(9, 31) <= local_time < time(16, 0)


def collector_market_window(
    now_et: datetime,
) -> tuple[datetime, datetime]:
    """Return the completed RTH window, including a post-close final pass."""
    start = datetime.combine(
        now_et.date(),
        time(9, 30),
        tzinfo=ET,
    )
    last_rth_minute = datetime.combine(
        now_et.date(),
        time(15, 59),
        tzinfo=ET,
    )
    completed_minute = (
        now_et.replace(second=0, microsecond=0)
        - timedelta(minutes=1)
    )
    return start, min(completed_minute, last_rth_minute)


def collector_window_expected(now_et: datetime) -> bool:
    """Allow intraday collection plus a short post-close finalization window."""
    if now_et.weekday() >= 5:
        return False

    local_time = now_et.time().replace(tzinfo=None)
    return time(9, 31) <= local_time < time(16, 20)


def parse_bar_time(value: Any) -> datetime | None:
    """Parse the normalized Webull bar timestamp without changing semantics."""
    text = str(value or "").strip()

    if not text:
        return None

    if text.endswith("Z"):
        text = text[:-1] + "+00:00"

    try:
        parsed = datetime.fromisoformat(text)
    except ValueError:
        parsed = None

    if parsed is None:
        for fmt in (
            "%Y-%m-%dT%H:%M:%S.%f%z",
            "%Y-%m-%dT%H:%M:%S%z",
        ):
            try:
                parsed = datetime.strptime(text, fmt)
                break
            except ValueError:
                continue

    if parsed is None or parsed.tzinfo is None:
        return None

    return parsed


def build_bar_history_rows(
    symbol: str,
    bars: list[dict[str, Any]],
    retrieved_at_et: datetime,
    *,
    starting_volume: float = 0.0,
    starting_weighted_price: float = 0.0,
) -> list[list[Any]]:
    """Serialize Webull bars for research storage.

    Session VWAP is cumulative and uses the same typical-price, volume-weighted
    method as calculations.build_snapshot. Incremental collector runs seed the
    cumulative totals from already stored bars so the resulting VWAP remains a
    true session-to-date value without refetching the whole session.
    """
    rows: list[list[Any]] = []
    cumulative_volume = float(starting_volume or 0.0)
    cumulative_weighted_price = float(starting_weighted_price or 0.0)
    retrieved_text = retrieved_at_et.isoformat(timespec="seconds")

    for bar in bars:
        parsed_time = parse_bar_time(bar.get("time"))

        if parsed_time is None:
            LOGGER.warning(
                "Skipping history row with unparseable time for %s: %r",
                symbol,
                bar.get("time"),
            )
            continue

        open_price = float(bar["open"])
        high_price = float(bar["high"])
        low_price = float(bar["low"])
        close_price = float(bar["close"])
        volume = float(bar.get("volume") or 0)
        typical_price = (
            high_price + low_price + close_price
        ) / 3.0

        cumulative_volume += volume
        cumulative_weighted_price += typical_price * volume
        session_vwap = (
            cumulative_weighted_price / cumulative_volume
            if cumulative_volume > 0
            else None
        )

        timestamp_et = parsed_time.astimezone(ET).isoformat(
            timespec="seconds"
        )
        timestamp_utc = (
            parsed_time.astimezone(UTC)
            .isoformat(timespec="seconds")
            .replace("+00:00", "Z")
        )
        session = str(
            bar.get("trading_session") or "RTH"
        ).strip().upper()

        rows.append(
            [
                timestamp_et,
                timestamp_utc,
                symbol,
                open_price,
                high_price,
                low_price,
                close_price,
                int(volume) if volume.is_integer() else volume,
                round(typical_price, 6),
                (
                    round(session_vwap, 6)
                    if session_vwap is not None
                    else ""
                ),
                DATA_SOURCE,
                session or "RTH",
                "M1",
                retrieved_text,
                DATA_QUALITY,
            ]
        )

    return rows


def symbols_from_confirmation_rows(
    rows: list[list[Any]],
) -> list[str]:
    """Use the existing Post-Open universe as the history collector universe."""
    symbols: list[str] = []

    for row_number in range(16, 29):
        symbol = normalize_symbol(cell(rows, row_number, 1))

        if symbol and symbol not in symbols:
            symbols.append(symbol)

    for benchmark in ("SPY", "QQQ"):
        if benchmark not in symbols:
            symbols.append(benchmark)

    return symbols


def make_webull_client() -> WebullClient:
    return WebullClient(
        app_key=WEBULL_APP_KEY,
        app_secret=WEBULL_APP_SECRET,
        access_token=WEBULL_ACCESS_TOKEN or None,
        region_id=WEBULL_REGION_ID,
        api_endpoint=WEBULL_API_ENDPOINT,
        token_dir=WEBULL_TOKEN_DIR or None,
    )


@app.get("/health")
def health():
    configured = bool(
        SPREADSHEET_ID
        and WEBULL_APP_KEY
        and WEBULL_APP_SECRET
    )

    return jsonify(
        {
            "ok": configured,
            "service": "investing-os-post-open",
            "phase": PHASE,
            "spreadsheet_configured": bool(SPREADSHEET_ID),
            "confirmation_sheet": CONFIRMATION_SHEET,
            "bar_history_sheet": BAR_HISTORY_SHEET,
            "webull_app_key_configured": bool(WEBULL_APP_KEY),
            "webull_app_secret_configured": bool(WEBULL_APP_SECRET),
            "webull_access_token_configured": bool(WEBULL_ACCESS_TOKEN),
            "data_source": DATA_SOURCE,
            "data_quality": DATA_QUALITY,
            "vwap_source": VWAP_SOURCE,
            "collector_endpoint": "/collect",
            "collector_finalization_window_et": "16:00-16:19",
        }
    ), 200 if configured else 503


@app.post("/collect")
def collect():
    """Persist only missing 1-minute bars for the current RTH session."""
    try:
        require_configuration()
        now_et = datetime.now(ET)

        if not collector_window_expected(now_et):
            return jsonify(
                {
                    "ok": True,
                    "skipped": True,
                    "reason": (
                        "Outside the intraday/post-close collection window"
                    ),
                    "timestamp_et": now_et.isoformat(),
                    "phase": PHASE,
                }
            )

        sheets = SheetsClient(SPREADSHEET_ID)
        webull = make_webull_client()
        confirmation_rows = sheets.read_values(
            f"'{CONFIRMATION_SHEET}'!A1:A28"
        )
        symbols = symbols_from_confirmation_rows(confirmation_rows)

        if not symbols:
            raise RuntimeError(
                "No symbols configured for intraday bar collection"
            )

        session_start_et, end_et = collector_market_window(now_et)

        if end_et < session_start_et:
            return jsonify(
                {
                    "ok": True,
                    "skipped": True,
                    "reason": "No completed RTH minute is available yet",
                    "timestamp_et": now_et.isoformat(),
                    "phase": PHASE,
                }
            )

        session_utc_prefix = (
            session_start_et.astimezone(UTC).date().isoformat()
        )
        state_by_symbol = sheets.bar_history_state(
            BAR_HISTORY_SHEET,
            symbols,
            interval="M1",
            timestamp_utc_prefix=session_utc_prefix,
        )

        rows_to_append: list[list[Any]] = []
        symbol_errors: dict[str, str] = {}
        request_windows: dict[str, dict[str, str]] = {}
        up_to_date: list[str] = []
        no_new_bars: list[str] = []

        for symbol in symbols:
            state = state_by_symbol.get(symbol, {})
            symbol_start_et = session_start_et
            latest_utc = str(
                state.get("latest_timestamp_utc") or ""
            ).strip()

            if latest_utc:
                latest_time = parse_bar_time(latest_utc)

                if latest_time is not None:
                    next_minute = (
                        latest_time.astimezone(ET)
                        .replace(second=0, microsecond=0)
                        + timedelta(minutes=1)
                    )
                    if next_minute > symbol_start_et:
                        symbol_start_et = next_minute

            if symbol_start_et > end_et:
                up_to_date.append(symbol)
                continue

            request_windows[symbol] = {
                "start_et": symbol_start_et.isoformat(timespec="seconds"),
                "end_et": end_et.isoformat(timespec="seconds"),
            }

            try:
                bars = webull.minute_bars(
                    symbol,
                    symbol_start_et,
                    end_et,
                )

                if not bars:
                    no_new_bars.append(symbol)
                    continue

                rows_to_append.extend(
                    build_bar_history_rows(
                        symbol,
                        bars,
                        now_et,
                        starting_volume=float(
                            state.get("cumulative_volume") or 0.0
                        ),
                        starting_weighted_price=float(
                            state.get("cumulative_weighted_price") or 0.0
                        ),
                    )
                )
            except Exception as exc:
                LOGGER.exception(
                    "Incremental bar collection error for %s",
                    symbol,
                )
                symbol_errors[symbol] = str(exc)[:200]

        history_appended = 0
        history_duplicates = 0

        if rows_to_append:
            history_appended, history_duplicates = (
                sheets.append_unique_bar_rows(
                    BAR_HISTORY_SHEET,
                    rows_to_append,
                )
            )

        return jsonify(
            {
                "ok": not bool(symbol_errors),
                "timestamp_et": now_et.isoformat(timespec="seconds"),
                "scheduler_time": request.headers.get(
                    "X-CloudScheduler-ScheduleTime"
                ),
                "symbols_requested": symbols,
                "symbols_up_to_date": up_to_date,
                "symbols_with_no_new_bars": no_new_bars,
                "symbol_errors": symbol_errors,
                "request_windows": request_windows,
                "bar_history_rows_prepared": len(rows_to_append),
                "bar_history_rows_appended": history_appended,
                "bar_history_duplicates_skipped": history_duplicates,
                "bar_history_sheet": BAR_HISTORY_SHEET,
                "collection_end_et": end_et.isoformat(timespec="seconds"),
                "phase": PHASE,
                "note": (
                    "Incremental collector requested only bars after each "
                    "symbol's latest stored M1 timestamp. A run after 16:00 ET "
                    "is clamped to 15:59 ET for end-of-day finalization."
                ),
            }
        ), 200 if not symbol_errors else 207
    except WebullError as exc:
        LOGGER.exception("Webull collector error")
        return jsonify(
            {
                "ok": False,
                "error": str(exc),
            }
        ), 502
    except Exception as exc:
        LOGGER.exception("Incremental collection service failure")
        return jsonify(
            {
                "ok": False,
                "error": str(exc),
            }
        ), 500


@app.post("/confirm")
def confirm():
    try:
        require_configuration()
        now_et = datetime.now(ET)

        # Webull OpenAPI does not expose the Tradier market-clock method.
        # The Cloud Scheduler remains authoritative for invocation timing;
        # this local guard avoids pre-open, after-hours, and weekend pulls.
        if not completed_regular_session_minute_expected(now_et):
            return jsonify(
                {
                    "ok": True,
                    "skipped": True,
                    "reason": (
                        "No completed regular-session minute is "
                        "expected at the current Eastern time"
                    ),
                    "timestamp_et": now_et.isoformat(),
                    "phase": PHASE,
                }
            )

        sheets = SheetsClient(SPREADSHEET_ID)
        webull = make_webull_client()

        rows = sheets.read_values(
            f"'{CONFIRMATION_SHEET}'!A1:P28"
        )
        premarket_valid = (
            str(cell(rows, 5, 2) or "")
            .strip()
            .lower()
        )
        premarket_active = premarket_valid == "yes"
        timestamp_text = now_et.strftime(
            "%Y-%m-%d %H:%M:%S ET"
        )
        base_updates: list[dict[str, Any]] = [
            {
                "range": f"'{CONFIRMATION_SHEET}'!E5:E6",
                "values": [
                    [timestamp_text],
                    [DATA_SOURCE],
                ],
            }
        ]

        # Preserve the v2 split: reset the invalid premarket branch to
        # NO TRADE, but continue collecting the fixed post-open universe.
        if premarket_active:
            expected_leader = str(cell(rows, 9, 2) or "")
            relevant_sector = normalize_symbol(cell(rows, 11, 2))
            constituents = parse_constituents(cell(rows, 12, 2))
        else:
            expected_leader = ""
            relevant_sector = ""
            constituents = []
            base_updates.append(
                {
                    "range": f"'{CONFIRMATION_SHEET}'!L5:L12",
                    "values": [
                        ["NO"],
                        ["NO"],
                        ["No trade"],
                        ["Stand Aside"],
                        ["NO TRADE"],
                        ["UNAVAILABLE"],
                        ["NO SIZE"],
                        ["INCOMPLETE"],
                    ],
                }
            )

        symbols_by_row: dict[int, str] = {}

        # Fixed post-open universe: rows 16-25.
        for row_number in range(16, 26):
            symbol = normalize_symbol(cell(rows, row_number, 1))

            if symbol:
                symbols_by_row[row_number] = symbol

        # Dynamic rows: sector ETF, then the first two constituents.
        # Blank values intentionally clear stale symbols from prior runs.
        dynamic_symbols = [
            relevant_sector if premarket_active else "",
            (
                constituents[0]
                if premarket_active and len(constituents) >= 1
                else ""
            ),
            (
                constituents[1]
                if premarket_active and len(constituents) >= 2
                else ""
            ),
        ]

        for row_number, symbol in zip(
            (26, 27, 28),
            dynamic_symbols,
        ):
            if symbol:
                symbols_by_row[row_number] = symbol

        dynamic_symbol_updates = [
            [symbol]
            for symbol in dynamic_symbols
        ]
        symbols: list[str] = []

        for symbol in symbols_by_row.values():
            if symbol and symbol not in symbols:
                symbols.append(symbol)

        for benchmark in ("SPY", "QQQ"):
            if benchmark not in symbols:
                symbols.append(benchmark)

        if not symbols:
            raise RuntimeError(
                "No symbols configured for post-open snapshot"
            )

        quotes = webull.quotes(symbols)
        start_et, end_et = current_market_window(now_et)

        if end_et < start_et:
            raise RuntimeError(
                "The opening session does not yet have a completed minute"
            )

        snapshots: dict[str, Any] = {}
        symbol_errors: dict[str, str] = {}
        bar_history_rows: list[list[Any]] = []

        for symbol in symbols:
            try:
                bars = webull.minute_bars(
                    symbol,
                    start_et,
                    end_et,
                )

                if not bars:
                    raise RuntimeError(
                        "Webull returned no usable 1m RTH bars"
                    )

                # Preserve the exact in-memory bars used for the snapshot.
                bar_history_rows.extend(
                    build_bar_history_rows(
                        symbol,
                        bars,
                        now_et,
                    )
                )
                snapshots[symbol] = build_snapshot(
                    symbol,
                    bars,
                    quotes.get(symbol),
                )
            except Exception as exc:
                LOGGER.exception("Snapshot error for %s", symbol)
                symbol_errors[symbol] = str(exc)[:200]

        history_appended = 0
        history_duplicates = 0
        history_error = ""

        # Historical persistence is intentionally non-fatal: a temporary
        # history-sheet problem must not break the existing Post-Open output.
        try:
            history_appended, history_duplicates = (
                sheets.append_unique_bar_rows(
                    BAR_HISTORY_SHEET,
                    bar_history_rows,
                )
            )
        except Exception as exc:
            LOGGER.exception("Intraday bar history persistence failed")
            history_error = str(exc)[:300]

        constituent_set = set(constituents)
        bc_rows: list[list[Any]] = []
        en_rows: list[list[Any]] = []
        notes_rows: list[list[Any]] = []

        for row_number in range(16, 29):
            symbol = symbols_by_row.get(row_number, "")
            snapshot = snapshots.get(symbol)

            if not symbol or snapshot is None:
                bc_rows.append(["", ""])
                en_rows.append([""] * 10)
                note = (
                    symbol_errors.get(
                        symbol,
                        "No usable Webull 1m RTH bars",
                    )
                    if symbol
                    else ""
                )
                notes_rows.append([note])
                continue

            benchmark_symbol = benchmark_for(
                symbol=symbol,
                relevant_sector=relevant_sector,
                expected_leader=expected_leader,
                constituent_symbols=constituent_set,
            )
            benchmark_snapshot = (
                snapshots.get(benchmark_symbol)
                if benchmark_symbol
                else None
            )
            rs = relative_strength(snapshot, benchmark_snapshot)

            bc_rows.append(
                [
                    round_price(snapshot.last),
                    round_price(snapshot.session_vwap),
                ]
            )
            en_rows.append(
                [
                    round_price(snapshot.open),
                    round_price(snapshot.high),
                    round_price(snapshot.low),
                    round_price(snapshot.or5_high),
                    round_price(snapshot.or5_low),
                    round_price(snapshot.or15_high),
                    round_price(snapshot.or15_low),
                    percent_value(rs),
                    snapshot.new_session_low,
                    (
                        round(snapshot.volume, 0)
                        if snapshot.volume is not None
                        else ""
                    ),
                ]
            )
            benchmark_note = (
                f" vs {benchmark_symbol}"
                if benchmark_symbol
                else ""
            )
            notes_rows.append(
                [
                    (
                        "Webull OpenAPI 1m RTH OHLCV; typical-price "
                        f"VWAP proxy; non-SIP volume; RS{benchmark_note}; "
                        "last completed bar "
                        f"{snapshot.last_bar_time or 'unavailable'}"
                    )
                ]
            )

        updates = base_updates + [
            {
                "range": f"'{CONFIRMATION_SHEET}'!A26:A28",
                "values": dynamic_symbol_updates,
            },
            {
                "range": f"'{CONFIRMATION_SHEET}'!B16:C28",
                "values": bc_rows,
            },
            {
                "range": f"'{CONFIRMATION_SHEET}'!E16:N28",
                "values": en_rows,
            },
            {
                "range": f"'{CONFIRMATION_SHEET}'!P16:P28",
                "values": notes_rows,
            },
        ]
        sheets.batch_write(updates)

        return jsonify(
            {
                "ok": True,
                "timestamp_et": timestamp_text,
                "scheduler_time": request.headers.get(
                    "X-CloudScheduler-ScheduleTime"
                ),
                "data_source": DATA_SOURCE,
                "data_quality": DATA_QUALITY,
                "vwap_source": VWAP_SOURCE,
                "premarket_active": premarket_active,
                "premarket_status": (
                    "VALID"
                    if premarket_active
                    else "NO VALID SETUP"
                ),
                "symbols_requested": symbols,
                "symbols_completed": sorted(snapshots.keys()),
                "symbol_errors": symbol_errors,
                "sheet": CONFIRMATION_SHEET,
                "bar_history_sheet": BAR_HISTORY_SHEET,
                "bar_history_rows_prepared": len(bar_history_rows),
                "bar_history_rows_appended": history_appended,
                "bar_history_duplicates_skipped": history_duplicates,
                "bar_history_error": history_error,
                "phase": PHASE,
                "note": (
                    "Webull post-open snapshot updated regardless of "
                    "premarket setup status. The exact in-memory Webull "
                    "1m bars used for calculations are also persisted "
                    "idempotently for intraday research. Premarket "
                    "confirmation and independent post-open reversal "
                    "discovery remain separate decision layers."
                ),
            }
        )
    except WebullError as exc:
        LOGGER.exception("Webull error")
        return jsonify(
            {
                "ok": False,
                "error": str(exc),
            }
        ), 502
    except Exception as exc:
        LOGGER.exception("Confirmation service failure")
        return jsonify(
            {
                "ok": False,
                "error": str(exc),
            }
        ), 500
