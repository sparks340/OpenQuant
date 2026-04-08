"""Base adapter protocol for market/instrument/factor sources."""

from __future__ import annotations

from abc import ABC, abstractmethod


class DataSourceAdapter(ABC):
    @abstractmethod
    def fetch_market_rows(self) -> list[dict]: ...

    @abstractmethod
    def fetch_instrument_rows(self) -> list[dict]: ...

    @abstractmethod
    def fetch_base_factor_rows(self) -> list[dict]: ...
