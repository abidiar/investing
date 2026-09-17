from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime
from pathlib import Path
from typing import Any, Iterable

from webull.core.client import ApiClient
from webull.data.common.category import Category
from webull.data.common.timespan import Timespan
from webull.data.data_client import DataClient


class WebullError(RuntimeError):
    pass


# Webull requires stock and ETF requests to use different categories.
# Keep the Investing OS universe and common dynamic sector/theme ETFs here.
KNOWN_ETFS = {
    "ARKK",
    "DIA",
    "EEM",
    "EFA",
    "EWJ",
    "FXI",
    "GDX",
    "GLD",
    "HYG",
    "IBB",
    "ICLN",
    "IGV",
    "IWM",
    "KRE",
    "LQD",
    "QQQ",
    "RSP",
    "SLV",
    "SMH",
    "SOXL",
    "SOXS",
    "SOXX",
    "SPXL",
    "SPXS",
    "SPY",
    "SQQQ",
    "TAN",
    "TLT",
    "TQQQ",
    "URA",
    "USO",
    "XBI",
    "XLB",
    "XLC",
    "XLE",
    "XLF",
    "XLI",
    "XLK",
    "XLP",
    "XLRE",
    "XLU",
    "XLV",
    "XLY",
}


def _to_float(value: Any) -> float | None:
    if value in (None, ""):
        return None

    try:
        return float(value)
    except (TypeError, ValueError):
        return None


def _to_int(value: Any) -> int | None:
    if value in (None, ""):
        return None

    try:
        return int(float(value))
    except (TypeError, ValueError):
        return None


def _parse_webull_time(value: Any) -> datetime | None:
    text = str(value or "").strip()

    if not text:
        return None

    try:
        return datetime.fromisoformat(text)
    except ValueError:
        pass

    for fmt in (
        "%Y-%m-%dT%H:%M:%S.%f%z",
        "%Y-%m-%dT%H:%M:%S%z",
    ):
        try:
            return datetime.strptime(text, fmt)
        except ValueError:
            continue

    return None


def _clean_symbols(symbols: Iterable[str]) -> list[str]:
    result: list[str] = []

    for value in symbols:
        symbol = str(value or "").strip().upper()

        if symbol and symbol not in result:
            result.append(symbol)

    return result


def _chunks(
    values: list[str],
    size: int,
) -> Iterable[list[str]]:
    for index in range(0, len(values), size):
        yield values[index:index + size]


@dataclass
class WebullClient:
    app_key: str
    app_secret: str
    region_id: str = "us"
    api_endpoint: str = "api.webull.com"

    # Cloud Run's filesystem is ephemeral, but /tmp is writable.
    token_dir: str | None = "/tmp/webull-openapi-token"
    access_token: str | None = None

    _api_client: ApiClient = field(init=False, repr=False)
    _data_client: DataClient = field(init=False, repr=False)

    def __post_init__(self) -> None:
        self.app_key = self.app_key.strip()
        self.app_secret = self.app_secret.strip()

        if not self.app_key:
            raise WebullError("Webull App Key is missing")

        if not self.app_secret:
            raise WebullError("Webull App Secret is missing")

        try:
            self._api_client = ApiClient(
                self.app_key,
                self.app_secret,
                self.region_id,
            )
            self._api_client.add_endpoint(
                self.region_id,
                self.api_endpoint,
            )

            if self.token_dir:
                self._api_client.set_token_dir(self.token_dir)
                self._seed_token_cache()

            self._data_client = DataClient(self._api_client)
        except Exception as exc:
            raise WebullError(
                f"Failed to initialize Webull SDK: {exc}"
            ) from exc

    def _seed_token_cache(self) -> None:
        """Seed Webull's reusable 2FA token on a Cloud Run cold start."""
        access_token = str(self.access_token or "").strip()

        if not access_token or not self.token_dir:
            return

        token_path = Path(self.token_dir) / "token.txt"

        if token_path.is_file():
            return

        token_path.parent.mkdir(parents=True, exist_ok=True)
        token_path.write_text(
            f"{access_token}\n0\nNORMAL\n",
            encoding="utf-8",
        )

        try:
            token_path.chmod(0o600)
        except OSError:
            pass

    @staticmethod
    def category_for(symbol: str) -> str:
        symbol = symbol.strip().upper()

        if symbol in KNOWN_ETFS:
            return Category.US_ETF.name

        return Category.US_STOCK.name

    def _response_json(
        self,
        response: Any,
        operation: str,
    ) -> Any:
        if response is None:
            raise WebullError(
                f"Webull returned no response for {operation}"
            )

        status_code = getattr(response, "status_code", None)

        if status_code != 200:
            response_text = str(
                getattr(response, "text", "")
            )[:500]
            raise WebullError(
                f"Webull {operation} failed "
                f"(HTTP {status_code}): {response_text}"
            )

        try:
            return response.json()
        except Exception as exc:
            raise WebullError(
                f"Webull returned invalid JSON for {operation}"
            ) from exc

    def _safe_call(
        self,
        operation: str,
        func: Any,
        **kwargs: Any,
    ) -> Any:
        try:
            response = func(**kwargs)
        except Exception as exc:
            raise WebullError(
                f"Webull {operation} failed: {exc}"
            ) from exc

        return self._response_json(response, operation)

    def snapshots(
        self,
        symbols: Iterable[str],
    ) -> dict[str, dict[str, Any]]:
        """Retrieve real-time snapshots, split into stock and ETF calls."""
        cleaned = _clean_symbols(symbols)
        grouped: dict[str, list[str]] = {
            Category.US_STOCK.name: [],
            Category.US_ETF.name: [],
        }

        for symbol in cleaned:
            grouped[self.category_for(symbol)].append(symbol)

        result: dict[str, dict[str, Any]] = {}

        for category, category_symbols in grouped.items():
            if not category_symbols:
                continue

            for batch in _chunks(category_symbols, 20):
                payload = self._safe_call(
                    "snapshot request",
                    self._data_client.market_data.get_snapshot,
                    symbols=batch,
                    category=category,
                    extend_hour_required=False,
                    overnight_required=False,
                )
                records = payload

                if isinstance(payload, dict):
                    if isinstance(payload.get("result"), list):
                        records = payload["result"]
                    elif isinstance(payload.get("data"), list):
                        records = payload["data"]

                if isinstance(records, dict):
                    records = [records]

                if not isinstance(records, list):
                    raise WebullError(
                        "Unexpected Webull snapshot response format"
                    )

                for record in records:
                    if not isinstance(record, dict):
                        continue

                    symbol = str(
                        record.get("symbol") or ""
                    ).strip().upper()

                    if symbol:
                        result[symbol] = record

        return result

    def quotes(
        self,
        symbols: Iterable[str],
    ) -> dict[str, dict[str, Any]]:
        """Return the provider-neutral quote mapping used by calculations."""
        snapshots = self.snapshots(symbols)
        result: dict[str, dict[str, Any]] = {}

        for symbol, raw in snapshots.items():
            last = _to_float(
                raw.get("price")
                or raw.get("last")
                or raw.get("close")
            )

            result[symbol] = {
                "symbol": symbol,
                "last": last,
                "price": last,
                "open": _to_float(raw.get("open")),
                "high": _to_float(raw.get("high")),
                "low": _to_float(raw.get("low")),
                "close": _to_float(raw.get("close")),
                "prevclose": _to_float(
                    raw.get("pre_close")
                    or raw.get("prev_close")
                    or raw.get("prevclose")
                ),
                "volume": _to_int(raw.get("volume")),
                "bid": _to_float(
                    raw.get("bid")
                    or raw.get("bid_price")
                ),
                "ask": _to_float(
                    raw.get("ask")
                    or raw.get("ask_price")
                ),
                "change": _to_float(raw.get("change")),
                "change_percentage": _to_float(
                    raw.get("change_ratio")
                    or raw.get("change_percentage")
                ),
                "_webull_raw": raw,
            }

        return result

    def minute_bars(
        self,
        symbol: str,
        start_et: datetime,
        end_et: datetime,
    ) -> list[dict[str, Any]]:
        """Retrieve completed one-minute RTH bars, oldest to newest."""
        symbol = symbol.strip().upper()

        if not symbol:
            return []

        self._validate_window(start_et, end_et)

        if end_et < start_et:
            return []

        minutes = int(
            (end_et - start_et).total_seconds() // 60
        ) + 1
        count = max(1, min(minutes + 5, 1200))
        payload = self._safe_call(
            f"1-minute bars for {symbol}",
            self._data_client.market_data.get_history_bar,
            symbol=symbol,
            category=self.category_for(symbol),
            timespan=Timespan.M1.name,
            count=str(count),
            real_time_required=False,
            trading_sessions=["RTH"],
            start_time=int(start_et.timestamp() * 1000),
            end_time=int(end_et.timestamp() * 1000),
        )

        return self._normalize_single_bar_payload(
            payload,
            symbol,
            start_et,
            end_et,
        )

    def batch_minute_bars(
        self,
        symbols: Iterable[str],
        start_et: datetime,
        end_et: datetime,
    ) -> dict[str, list[dict[str, Any]]]:
        """Retrieve category-specific one-minute bar batches."""
        cleaned = _clean_symbols(symbols)
        self._validate_window(start_et, end_et)

        if end_et < start_et:
            return {symbol: [] for symbol in cleaned}

        minutes = int(
            (end_et - start_et).total_seconds() // 60
        ) + 1
        count = max(1, min(minutes + 5, 1200))
        grouped: dict[str, list[str]] = {
            Category.US_STOCK.name: [],
            Category.US_ETF.name: [],
        }

        for symbol in cleaned:
            grouped[self.category_for(symbol)].append(symbol)

        result: dict[str, list[dict[str, Any]]] = {
            symbol: []
            for symbol in cleaned
        }

        for category, category_symbols in grouped.items():
            if not category_symbols:
                continue

            for batch in _chunks(category_symbols, 20):
                payload = self._safe_call(
                    f"batch 1-minute bars for {','.join(batch)}",
                    self._data_client.market_data.get_batch_history_bar,
                    symbols=batch,
                    category=category,
                    timespan=Timespan.M1.name,
                    count=str(count),
                    real_time_required=False,
                    trading_sessions=["RTH"],
                    start_time=int(start_et.timestamp() * 1000),
                    end_time=int(end_et.timestamp() * 1000),
                )
                groups = (
                    payload.get("result", [])
                    if isinstance(payload, dict)
                    else payload
                )

                if not isinstance(groups, list):
                    raise WebullError(
                        "Unexpected Webull batch-bar response format"
                    )

                for group in groups:
                    if not isinstance(group, dict):
                        continue

                    symbol = str(
                        group.get("symbol") or ""
                    ).strip().upper()
                    rows = group.get("result", group.get("data", []))

                    if symbol:
                        result[symbol] = self._normalize_bar_rows(
                            rows,
                            symbol,
                            start_et,
                            end_et,
                        )

        return result

    def ticks(
        self,
        symbol: str,
        count: int = 30,
    ) -> list[dict[str, Any]]:
        """Retrieve recent RTH trades for optional future analysis."""
        symbol = symbol.strip().upper()

        if not symbol:
            return []

        count = max(1, min(int(count), 1000))
        payload = self._safe_call(
            f"ticks for {symbol}",
            self._data_client.market_data.get_tick,
            symbol=symbol,
            category=self.category_for(symbol),
            count=str(count),
            trading_sessions=["RTH"],
        )
        records = payload

        if isinstance(payload, dict):
            if isinstance(payload.get("result"), list):
                records = payload["result"]
            elif isinstance(payload.get("data"), list):
                records = payload["data"]

        if not isinstance(records, list):
            raise WebullError(
                "Unexpected Webull tick response format"
            )

        cleaned: list[dict[str, Any]] = []

        for row in records:
            if not isinstance(row, dict):
                continue

            cleaned.append(
                {
                    "symbol": symbol,
                    "time": row.get("time"),
                    "price": _to_float(row.get("price")),
                    "volume": _to_int(row.get("volume")),
                    "side": row.get("side"),
                    "trading_session": row.get("trading_session"),
                }
            )

        return cleaned

    @staticmethod
    def _validate_window(
        start_et: datetime,
        end_et: datetime,
    ) -> None:
        if start_et.tzinfo is None:
            raise WebullError("start_et must be timezone-aware")

        if end_et.tzinfo is None:
            raise WebullError("end_et must be timezone-aware")

    def _normalize_single_bar_payload(
        self,
        payload: Any,
        symbol: str,
        start_et: datetime,
        end_et: datetime,
    ) -> list[dict[str, Any]]:
        rows = payload

        if isinstance(payload, dict):
            if isinstance(payload.get("result"), list):
                rows = payload["result"]
            elif isinstance(payload.get("data"), list):
                rows = payload["data"]

        return self._normalize_bar_rows(
            rows,
            symbol,
            start_et,
            end_et,
        )

    def _normalize_bar_rows(
        self,
        rows: Any,
        symbol: str,
        start_et: datetime,
        end_et: datetime,
    ) -> list[dict[str, Any]]:
        if not isinstance(rows, list):
            return []

        normalized: list[tuple[float, dict[str, Any]]] = []
        start_timestamp = start_et.timestamp()
        end_timestamp = end_et.timestamp()

        for row in rows:
            if not isinstance(row, dict):
                continue

            parsed_time = _parse_webull_time(row.get("time"))

            if parsed_time is None or parsed_time.tzinfo is None:
                continue

            timestamp = parsed_time.timestamp()

            if timestamp < start_timestamp or timestamp > end_timestamp:
                continue

            trading_session = str(
                row.get("trading_session") or ""
            ).upper()

            if trading_session and trading_session != "RTH":
                continue

            open_price = _to_float(row.get("open"))
            high_price = _to_float(row.get("high"))
            low_price = _to_float(row.get("low"))
            close_price = _to_float(row.get("close"))

            if (
                open_price is None
                or high_price is None
                or low_price is None
                or close_price is None
            ):
                continue

            normalized.append(
                (
                    timestamp,
                    {
                        "symbol": symbol,
                        "time": str(row.get("time") or ""),
                        "open": open_price,
                        "high": high_price,
                        "low": low_price,
                        "close": close_price,
                        "volume": _to_int(row.get("volume")) or 0,
                        "trading_session": trading_session or "RTH",
                    },
                )
            )

        normalized.sort(key=lambda item: item[0])
        return [bar for _, bar in normalized]
