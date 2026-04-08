"""Risk evaluation context."""

from __future__ import annotations

from decimal import Decimal

from packages.core.core.models.base import CoreModel


class RiskContext(CoreModel):
    account_id: str
    total_equity: Decimal
    cash_available: Decimal
    latest_prices: dict[str, Decimal]
    current_position_weights: dict[str, Decimal]
    blacklist: set[str] = set()

    def get_price(self, symbol: str) -> Decimal:
        return self.latest_prices[symbol.upper()]

    def get_current_weight(self, symbol: str) -> Decimal:
        return self.current_position_weights.get(symbol.upper(), Decimal("0"))

    def is_blacklisted(self, symbol: str) -> bool:
        return symbol.upper() in {item.upper() for item in self.blacklist}
