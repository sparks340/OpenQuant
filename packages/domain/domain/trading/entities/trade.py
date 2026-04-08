"""Trade fill entity."""

from decimal import Decimal

from pydantic import field_validator

from packages.core.core.enums.trading import OrderSide
from packages.core.core.exceptions.domain import InvariantViolationError
from packages.core.core.models.base import CoreModel


class Trade(CoreModel):
    trade_id: str
    order_id: str
    symbol: str
    side: OrderSide
    quantity: Decimal
    price: Decimal

    @field_validator("symbol")
    @classmethod
    def normalize_symbol(cls, value: str) -> str:
        return value.upper()

    @field_validator("quantity", "price")
    @classmethod
    def validate_positive(cls, value: Decimal) -> Decimal:
        if value <= Decimal("0"):
            raise InvariantViolationError("trade quantity/price must be positive")
        return value
