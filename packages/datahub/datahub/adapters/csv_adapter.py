"""CSV adapter represented by injected row dictionaries for MVP tests."""

from packages.datahub.datahub.adapters.base import DataSourceAdapter


class CSVDataAdapter(DataSourceAdapter):
    def __init__(
        self,
        market_rows: list[dict] | None = None,
        instrument_rows: list[dict] | None = None,
        base_factor_rows: list[dict] | None = None,
    ) -> None:
        self._market_rows = market_rows or []
        self._instrument_rows = instrument_rows or []
        self._base_factor_rows = base_factor_rows or []

    def fetch_market_rows(self) -> list[dict]:
        return list(self._market_rows)

    def fetch_instrument_rows(self) -> list[dict]:
        return list(self._instrument_rows)

    def fetch_base_factor_rows(self) -> list[dict]:
        return list(self._base_factor_rows)
