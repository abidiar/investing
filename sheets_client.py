from __future__ import annotations

from dataclasses import dataclass
from typing import Any
import google.auth
from googleapiclient.discovery import build


SHEETS_SCOPE = "https://www.googleapis.com/auth/spreadsheets"


@dataclass
class SheetsClient:
    spreadsheet_id: str

    def __post_init__(self) -> None:
        credentials, _ = google.auth.default(scopes=[SHEETS_SCOPE])
        self.service = build(
            "sheets",
            "v4",
            credentials=credentials,
            cache_discovery=False,
        )

    def read_values(self, range_a1: str) -> list[list[Any]]:
        response = (
            self.service.spreadsheets()
            .values()
            .get(
                spreadsheetId=self.spreadsheet_id,
                range=range_a1,
                valueRenderOption="UNFORMATTED_VALUE",
            )
            .execute()
        )
        return response.get("values", [])

    def batch_write(self, updates: list[dict[str, Any]]) -> None:
        body = {"valueInputOption": "USER_ENTERED", "data": updates}
        (
            self.service.spreadsheets()
            .values()
            .batchUpdate(
                spreadsheetId=self.spreadsheet_id,
                body=body,
            )
            .execute()
        )

    @staticmethod
    def _quote_sheet_name(sheet_name: str) -> str:
        return "'" + str(sheet_name).replace("'", "''") + "'"

    def _existing_bar_history_keys(
        self,
        sheet_name: str,
    ) -> set[tuple[str, str, str]]:
        """Return existing (symbol, timestamp UTC, interval) keys.

        Only the three key columns are read so a growing history table does
        not require pulling all OHLCV/VWAP cells on every persistence pass.
        """
        quoted = self._quote_sheet_name(sheet_name)
        ranges = [
            f"{quoted}!B2:C",
            f"{quoted}!M2:M",
        ]
        response = (
            self.service.spreadsheets()
            .values()
            .batchGet(
                spreadsheetId=self.spreadsheet_id,
                ranges=ranges,
                valueRenderOption="FORMATTED_VALUE",
                majorDimension="ROWS",
            )
            .execute()
        )
        value_ranges = response.get("valueRanges", [])
        timestamp_symbol_rows = (
            value_ranges[0].get("values", [])
            if len(value_ranges) >= 1
            else []
        )
        interval_rows = (
            value_ranges[1].get("values", [])
            if len(value_ranges) >= 2
            else []
        )
        keys: set[tuple[str, str, str]] = set()
        row_count = max(
            len(timestamp_symbol_rows),
            len(interval_rows),
        )

        for index in range(row_count):
            timestamp_utc = ""
            symbol = ""
            interval = ""

            if index < len(timestamp_symbol_rows):
                row = timestamp_symbol_rows[index]
                if len(row) >= 1:
                    timestamp_utc = str(row[0] or "").strip()
                if len(row) >= 2:
                    symbol = str(row[1] or "").strip().upper()

            if index < len(interval_rows):
                row = interval_rows[index]
                if row:
                    interval = str(row[0] or "").strip().upper()

            if symbol and timestamp_utc and interval:
                keys.add((symbol, timestamp_utc, interval))

        return keys

    def append_unique_bar_rows(
        self,
        sheet_name: str,
        rows: list[list[Any]],
    ) -> tuple[int, int]:
        """Append raw bar rows once per Symbol + Timestamp UTC + Interval.

        The expected schema is the Investing OS `Intraday Bar History` table:
        Timestamp ET, Timestamp UTC, Symbol, O/H/L/C, Volume, Typical Price,
        Session VWAP, Feed, Session, Interval, Retrieved At ET, Data Quality.

        Returns (rows_appended, duplicates_skipped).
        """
        if not rows:
            return 0, 0

        existing_keys = self._existing_bar_history_keys(sheet_name)
        seen_keys = set(existing_keys)
        new_rows: list[list[Any]] = []
        duplicates = 0

        for row in rows:
            if len(row) < 13:
                raise ValueError(
                    "Intraday bar history row must contain at least 13 columns"
                )

            timestamp_utc = str(row[1] or "").strip()
            symbol = str(row[2] or "").strip().upper()
            interval = str(row[12] or "").strip().upper()
            key = (symbol, timestamp_utc, interval)

            if not symbol or not timestamp_utc or not interval:
                raise ValueError(
                    "Intraday bar history key fields cannot be blank"
                )

            if key in seen_keys:
                duplicates += 1
                continue

            seen_keys.add(key)
            new_rows.append(row)

        if not new_rows:
            return 0, duplicates

        quoted = self._quote_sheet_name(sheet_name)
        body = {"values": new_rows}
        (
            self.service.spreadsheets()
            .values()
            .append(
                spreadsheetId=self.spreadsheet_id,
                range=f"{quoted}!A:O",
                valueInputOption="RAW",
                insertDataOption="INSERT_ROWS",
                body=body,
            )
            .execute()
        )

        return len(new_rows), duplicates
