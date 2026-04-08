"""Risk decision models."""

from __future__ import annotations

from packages.core.core.models.base import CoreModel
from packages.portfolio_engine.portfolio_engine.builders.order_intent_builder import OrderIntent


class OrderRiskDecision(CoreModel):
    intent: OrderIntent
    approved: bool
    reasons: list[str]
