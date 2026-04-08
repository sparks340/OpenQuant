"""Max position weight rule."""

from __future__ import annotations

from decimal import Decimal

from packages.core.core.enums.trading import OrderSide
from packages.portfolio_engine.portfolio_engine.builders.order_intent_builder import OrderIntent
from packages.risk_engine.risk_engine.models.risk_context import RiskContext


def check_max_position_weight(
    intent: OrderIntent,
    context: RiskContext,
    max_position_weight: Decimal,
) -> str | None:
    if intent.side != OrderSide.BUY:
        return None

    price = context.get_price(intent.symbol)
    order_value = intent.quantity * price
    delta_weight = order_value / context.total_equity
    projected_weight = context.get_current_weight(intent.symbol) + delta_weight

    if projected_weight > max_position_weight:
        return (
            "max_position_weight: projected "
            f"{projected_weight} exceeds limit {max_position_weight}"
        )
    return None
