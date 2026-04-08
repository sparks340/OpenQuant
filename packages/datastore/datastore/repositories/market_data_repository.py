"""Market data repository contracts and in-memory implementation."""

from __future__ import annotations

from abc import ABC, abstractmethod
from dataclasses import dataclass
from datetime import date
from decimal import Decimal


@dataclass
class Bar:
    symbol: str
    trade_date: date
    close: Decimal
    volume: Decimal


class MarketDataRepository(ABC):
    @abstractmethod
    def save_bar(self, symbol: str, trade_date: date, close: Decimal, volume: Decimal) -> Bar: ...

    @abstractmethod
    def list_bars(self, symbol: str, start: date, end: date) -> list[Bar]: ...


class InMemoryMarketDataRepository(MarketDataRepository):
    def __init__(self) -> None:
        self._bars: list[Bar] = []

    def save_bar(self, symbol: str, trade_date: date, close: Decimal, volume: Decimal) -> Bar:
        bar = Bar(symbol=symbol.upper(), trade_date=trade_date, close=close, volume=volume)
        self._bars.append(bar)
        return bar

    def list_bars(self, symbol: str, start: date, end: date) -> list[Bar]:
        target = symbol.upper()
        return [bar for bar in self._bars if bar.symbol == target and start <= bar.trade_date <= end]
