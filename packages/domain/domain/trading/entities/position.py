"""Position entity."""

from decimal import Decimal

from pydantic import field_validator

from packages.core.core.exceptions.domain import InvariantViolationError
from packages.core.core.models.base import CoreModel


class Position(CoreModel):
    symbol: str
    quantity: Decimal
    average_price: Decimal

    @field_validator("symbol")
    @classmethod
    def normalize_symbol(cls, value: str) -> str:
        return value.upper()

    @field_validator("quantity", "average_price")
    @classmethod
    def validate_non_negative(cls, value: Decimal) -> Decimal:
        if value < Decimal("0"):
            raise InvariantViolationError("quantity/average_price cannot be negative")
        return value
