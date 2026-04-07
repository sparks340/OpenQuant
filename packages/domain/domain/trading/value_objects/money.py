"""Money value object with currency consistency rules."""

from __future__ import annotations

from decimal import Decimal

from pydantic import Field, field_validator

from packages.core.core.exceptions.domain import InvariantViolationError
from packages.core.core.models.base import CoreModel


class Money(CoreModel):
    amount: Decimal = Field(ge=Decimal("0"))
    currency: str = "CNY"

    @field_validator("currency")
    @classmethod
    def normalize_currency(cls, value: str) -> str:
        normalized = value.strip().upper()
        if len(normalized) != 3:
            raise InvariantViolationError("Currency must be a 3-letter ISO code")
        return normalized

    def add(self, other: "Money") -> "Money":
        self._ensure_same_currency(other)
        return Money(amount=self.amount + other.amount, currency=self.currency)

    def subtract(self, other: "Money") -> "Money":
        self._ensure_same_currency(other)
        if other.amount > self.amount:
            raise InvariantViolationError("Money subtraction cannot produce negative amount")
        return Money(amount=self.amount - other.amount, currency=self.currency)

    def _ensure_same_currency(self, other: "Money") -> None:
        if self.currency != other.currency:
            raise InvariantViolationError(
                f"Currency mismatch: {self.currency} vs {other.currency}"
            )
