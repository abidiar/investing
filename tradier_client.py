from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime
from typing import Any
import requests


class TradierError(RuntimeError):
    pass


@dataclass
class TradierClient:
    token: str
    base_url: str = "https://api.tradier.com/v1"
    timeout_seconds: int = 25

    @property
    def headers(self) -> dict[str, str]:
        return {
            "Authorization": f"Bearer {self.token}",
            "Accept": "application/json",
            "User-Agent": "InvestingOS-PostOpen/1.0",
        }

    def _get(self, path: str, params: dict[str, Any] | None = None) -> dict[str, Any]:
        url = f"{self.base_url.rstrip('/')}/{path.lstrip('/')}"
        response = requests.get(
            url,
            headers=self.headers,
            params=params or {},
            timeout=self.timeout_seconds,
        )
        if response.status_code != 200:
            detail = response.text[:500]
            raise TradierError(
                f"Tradier request failed ({response.status_code}) for {path}: {detail}"
            )
        try:
            payload = response.json()
        except ValueError as exc:
            raise TradierError(f"Tradier returned non-JSON data for {path}") from exc
        if not isinstance(payload, dict):
            raise TradierError(f"Unexpected Tradier response type for {path}")
        return payload

    def market_clock(self) -> dict[str, Any]:
        payload = self._get("/markets/clock")
        return payload.get("clock") or {}

    def quotes(self, symbols: list[str]) -> dict[str, dict[str, Any]]:
        cleaned = [s.strip().upper() for s in symbols if s and s.strip()]
        if not cleaned:
            return {}

        payload = self._get(
            "/markets/quotes",
            params={"symbols": ",".join(cleaned), "greeks": "false"},
        )
        quote_value = (payload.get("quotes") or {}).get("quote")
        if quote_value is None:
            return {}

        rows = quote_value if isinstance(quote_value, list) else [quote_value]
        result: dict[str, dict[str, Any]] = {}
        for row in rows:
            if isinstance(row, dict) and row.get("symbol"):
                result[str(row["symbol"]).upper()] = row
        return result

    def minute_bars(
        self,
        symbol: str,
        start_et: datetime,
        end_et: datetime,
    ) -> list[dict[str, Any]]:
        payload = self._get(
            "/markets/timesales",
            params={
                "symbol": symbol.upper(),
                "interval": "1min",
                "start": start_et.strftime("%Y-%m-%d %H:%M"),
                "end": end_et.strftime("%Y-%m-%d %H:%M"),
                "session_filter": "open",
            },
        )

        data = (payload.get("series") or {}).get("data")
        if data is None:
            return []
        rows = data if isinstance(data, list) else [data]

        cleaned: list[dict[str, Any]] = []
        for row in rows:
            if not isinstance(row, dict):
                continue
            try:
                cleaned.append(
                    {
                        "time": str(row.get("time") or ""),
                        "timestamp": int(row.get("timestamp") or 0),
                        "open": float(row["open"]),
                        "high": float(row["high"]),
                        "low": float(row["low"]),
                        "close": float(row["close"]),
                        "volume": float(row.get("volume") or 0),
                        "vwap": float(row.get("vwap") or row["close"]),
                    }
                )
            except (KeyError, TypeError, ValueError):
                continue

        cleaned.sort(key=lambda item: (item["timestamp"], item["time"]))
        return cleaned
