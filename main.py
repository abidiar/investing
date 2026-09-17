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

TIMEZONE = os.environ.get(
    "TIMEZONE",
    "America/New_York",
).strip()

ET = ZoneInfo(TIMEZONE)
PHASE = "snapshot-connector-webull-v1"
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
            "webull_app_key_configured": bool(WEBULL_APP_KEY),
            "webull_app_secret_configured": bool(WEBULL_APP_SECRET),
            "webull_access_token_configured": bool(WEBULL_ACCESS_TOKEN),
            "data_source": DATA_SOURCE,
            "vwap_source": VWAP_SOURCE,
        }
    ), 200 if configured else 503


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
        webull = WebullClient(
            app_key=WEBULL_APP_KEY,
            app_secret=WEBULL_APP_SECRET,
            access_token=WEBULL_ACCESS_TOKEN or None,
            region_id=WEBULL_REGION_ID,
            api_endpoint=WEBULL_API_ENDPOINT,
            token_dir=WEBULL_TOKEN_DIR or None,
        )

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

                snapshots[symbol] = build_snapshot(
                    symbol,
                    bars,
                    quotes.get(symbol),
                )
            except Exception as exc:
                LOGGER.exception("Snapshot error for %s", symbol)
                symbol_errors[symbol] = str(exc)[:200]

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
                "phase": PHASE,
                "note": (
                    "Webull post-open snapshot updated regardless of "
                    "premarket setup status. Premarket confirmation and "
                    "independent post-open reversal discovery remain "
                    "separate decision layers."
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
