"""Factor frame model storing per symbol/date values."""

from __future__ import annotations

from datetime import date
from decimal import Decimal

from packages.core.core.models.base import CoreModel


class FactorPoint(CoreModel):
    symbol: str
    trade_date: date
    value: Decimal


class FactorFrame(CoreModel):
    points: list[FactorPoint]

    def get(self, symbol: str, trade_date: date) -> Decimal | None:
        target = symbol.upper()
        for point in self.points:
            if point.symbol == target and point.trade_date == trade_date:
                return point.value
        return None
