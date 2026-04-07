"""Rebalance plan entity with allocation invariants."""

from __future__ import annotations

from decimal import Decimal

from pydantic import Field, field_validator, model_validator

from packages.core.core.exceptions.domain import InvariantViolationError
from packages.core.core.models.base import CoreModel


class RebalancePlan(CoreModel):
    """Target allocation produced by strategy outputs."""

    plan_id: str
    strategy_version_id: str
    targets: dict[str, Decimal] = Field(default_factory=dict)

    @field_validator("targets")
    @classmethod
    def normalize_target_symbols(cls, value: dict[str, Decimal]) -> dict[str, Decimal]:
        return {symbol.upper(): weight for symbol, weight in value.items()}

    @model_validator(mode="after")
    def validate_targets(self) -> "RebalancePlan":
        if not self.targets:
            raise InvariantViolationError("Rebalance plan requires at least one target symbol")

        total = Decimal("0")
        for symbol, weight in self.targets.items():
            if weight <= Decimal("0"):
                raise InvariantViolationError(f"Target weight must be positive: {symbol}")
            total += weight
        if total > Decimal("1"):
            raise InvariantViolationError(f"Total target weight must not exceed 1.0, got {total}")
        return self
