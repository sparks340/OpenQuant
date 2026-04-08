"""Blacklist rule."""

from __future__ import annotations

from packages.portfolio_engine.portfolio_engine.builders.order_intent_builder import OrderIntent
from packages.risk_engine.risk_engine.models.risk_context import RiskContext


def check_blacklist(intent: OrderIntent, context: RiskContext) -> str | None:
    if context.is_blacklisted(intent.symbol):
        return f"blacklist: symbol {intent.symbol} is blocked"
    return None
