"""Strategy signal entity."""

from __future__ import annotations

from datetime import date
from decimal import Decimal

from pydantic import field_validator

from packages.core.core.exceptions.domain import InvariantViolationError
from packages.core.core.models.base import CoreModel


class Signal(CoreModel):
    """Per-symbol alpha signal."""

    symbol: str
    score: Decimal
    as_of: date

    @field_validator("symbol")
    @classmethod
    def normalize_symbol(cls, value: str) -> str:
        return value.upper()

    @field_validator("score")
    @classmethod
    def validate_score_range(cls, value: Decimal) -> Decimal:
        # Keep scores bounded for stable normalization in MVP stage.
        if value < Decimal("-1") or value > Decimal("1"):
            raise InvariantViolationError("Signal score must be within [-1, 1]")
        return value
