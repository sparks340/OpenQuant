"""Backtest configuration value object."""

from __future__ import annotations

from datetime import date
from decimal import Decimal
from enum import StrEnum

from pydantic import Field, model_validator

from packages.core.core.exceptions.domain import InvariantViolationError
from packages.core.core.models.base import CoreModel


class RebalanceFrequency(StrEnum):
    DAILY = "DAILY"
    WEEKLY = "WEEKLY"
    MONTHLY = "MONTHLY"


class BacktestConfig(CoreModel):
    """Immutable-like configuration for a backtest run."""

    start_date: date
    end_date: date
    benchmark: str
    initial_capital: Decimal = Field(gt=Decimal("0"))
    rebalance_frequency: RebalanceFrequency = RebalanceFrequency.MONTHLY

    @model_validator(mode="after")
    def validate_dates(self) -> "BacktestConfig":
        if self.end_date < self.start_date:
            raise InvariantViolationError("Backtest end_date must be greater than or equal to start_date")
        return self
