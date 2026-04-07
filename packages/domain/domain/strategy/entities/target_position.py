"""Target position entity."""

from __future__ import annotations

from decimal import Decimal

from pydantic import Field, field_validator

from packages.core.core.models.base import CoreModel


class TargetPosition(CoreModel):
    """Desired position expressed by portfolio weight."""

    symbol: str
    target_weight: Decimal = Field(gt=Decimal("0"), le=Decimal("1"))

    @field_validator("symbol")
    @classmethod
    def normalize_symbol(cls, value: str) -> str:
        return value.upper()
