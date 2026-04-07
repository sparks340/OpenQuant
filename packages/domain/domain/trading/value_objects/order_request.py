"""Trading order request value object."""

from __future__ import annotations

from decimal import Decimal

from pydantic import Field, field_validator

from packages.core.core.enums.trading import OrderSide
from packages.core.core.models.base import CoreModel


class OrderRequest(CoreModel):
    account_id: str
    symbol: str
    side: OrderSide
    quantity: Decimal = Field(gt=Decimal("0"))
    limit_price: Decimal | None = Field(default=None, gt=Decimal("0"))

    @field_validator("symbol")
    @classmethod
    def normalize_symbol(cls, value: str) -> str:
        return value.upper()
