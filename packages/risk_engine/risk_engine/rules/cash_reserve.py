"""Cash reserve rule."""

from __future__ import annotations

from decimal import Decimal

from packages.core.core.enums.trading import OrderSide
from packages.portfolio_engine.portfolio_engine.builders.order_intent_builder import OrderIntent
from packages.risk_engine.risk_engine.models.risk_context import RiskContext


def check_cash_reserve(intent: OrderIntent, context: RiskContext, min_cash_reserve: Decimal) -> str | None:
    if intent.side != OrderSide.BUY:
        return None

    price = context.get_price(intent.symbol)
    order_value = intent.quantity * price
    reserve_floor = context.total_equity * min_cash_reserve
    remaining_cash = context.cash_available - order_value

    if remaining_cash < reserve_floor:
        return (
            "cash_reserve: remaining_cash "
            f"{remaining_cash} is below reserve floor {reserve_floor}"
        )
    return None
