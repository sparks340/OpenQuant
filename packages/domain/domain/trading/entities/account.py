"""Trading account entity."""

from decimal import Decimal

from pydantic import field_validator

from packages.core.core.exceptions.domain import InvariantViolationError
from packages.core.core.models.base import CoreModel


class Account(CoreModel):
    account_id: str
    cash: Decimal
    currency: str = "CNY"

    @field_validator("cash")
    @classmethod
    def validate_non_negative_cash(cls, value: Decimal) -> Decimal:
        if value < Decimal("0"):
            raise InvariantViolationError("cash cannot be negative")
        return value

    @field_validator("currency")
    @classmethod
    def normalize_currency(cls, value: str) -> str:
        return value.upper()
