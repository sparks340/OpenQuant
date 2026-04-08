"""Factor value point entity."""

from datetime import date
from decimal import Decimal

from pydantic import field_validator

from packages.core.core.models.base import CoreModel


class FactorValue(CoreModel):
    run_id: str
    symbol: str
    as_of: date
    value: Decimal

    @field_validator("symbol")
    @classmethod
    def normalize_symbol(cls, value: str) -> str:
        return value.upper()
