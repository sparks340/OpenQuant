"""Trading order entity with minimal lifecycle invariants."""

from __future__ import annotations

from datetime import datetime, timezone
from decimal import Decimal

from pydantic import Field, field_validator, model_validator

from packages.core.core.enums.trading import OrderSide, OrderStatus
from packages.core.core.exceptions.domain import InvariantViolationError
from packages.core.core.models.base import CoreModel


_VALID_TRANSITIONS: dict[OrderStatus, set[OrderStatus]] = {
    OrderStatus.PENDING: {OrderStatus.SUBMITTED, OrderStatus.CANCELED, OrderStatus.REJECTED},
    OrderStatus.SUBMITTED: {OrderStatus.FILLED, OrderStatus.CANCELED, OrderStatus.REJECTED},
    OrderStatus.FILLED: set(),
    OrderStatus.CANCELED: set(),
    OrderStatus.REJECTED: set(),
}


class Order(CoreModel):
    """Order aggregate root used by trading flow."""

    order_id: str
    account_id: str
    symbol: str
    side: OrderSide
    quantity: Decimal = Field(gt=Decimal("0"))
    status: OrderStatus = OrderStatus.PENDING
    submitted_at: datetime | None = None
    filled_at: datetime | None = None

    @model_validator(mode="after")
    def validate_timestamp_consistency(self) -> "Order":
        if self.status in {OrderStatus.SUBMITTED, OrderStatus.FILLED} and self.submitted_at is None:
            raise InvariantViolationError("Submitted/filled order must include submitted_at")
        if self.status == OrderStatus.FILLED and self.filled_at is None:
            raise InvariantViolationError("Filled order must include filled_at")
        if self.filled_at and self.submitted_at and self.filled_at < self.submitted_at:
            raise InvariantViolationError("filled_at must be later than submitted_at")
        return self

    @field_validator("symbol")
    @classmethod
    def normalize_symbol(cls, value: str) -> str:
        return value.upper()

    def transition_to(self, target_status: OrderStatus) -> None:
        """Transition order status with invariant checks."""
        if target_status not in _VALID_TRANSITIONS[self.status]:
            raise InvariantViolationError(
                f"Invalid order transition: {self.status} -> {target_status}"
            )
        if target_status == OrderStatus.FILLED and self.submitted_at is None:
            raise InvariantViolationError("Filled order must have submitted_at timestamp")

        self.status = target_status
        now = datetime.now(tz=timezone.utc)
        if target_status == OrderStatus.SUBMITTED:
            self.submitted_at = now
        if target_status == OrderStatus.FILLED:
            self.filled_at = now
