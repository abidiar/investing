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
        self.service = build("sheets", "v4", credentials=credentials, cache_discovery=False)

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
            .batchUpdate(spreadsheetId=self.spreadsheet_id, body=body)
            .execute()
        )
