"""Build order intents from target positions and account state."""

from __future__ import annotations

from decimal import Decimal, ROUND_DOWN

from pydantic import BaseModel

from packages.core.core.enums.trading import OrderSide


class OrderIntent(BaseModel):
    account_id: str
    symbol: str
    side: OrderSide
    quantity: Decimal
    reason: str


class OrderIntentBuilder:
    @staticmethod
    def build(
        *,
        account_id: str,
        total_equity: Decimal,
        target_weights: dict[str, Decimal],
        latest_prices: dict[str, Decimal],
        current_positions: dict[str, Decimal],
    ) -> list[OrderIntent]:
        intents: list[OrderIntent] = []

        for symbol, target_weight in sorted(target_weights.items()):
            price = latest_prices[symbol]
            current_qty = current_positions.get(symbol, Decimal("0"))
            current_value = current_qty * price
            target_value = total_equity * target_weight
            delta_value = target_value - current_value

            raw_qty = (abs(delta_value) / price).quantize(Decimal("1"), rounding=ROUND_DOWN)
            if raw_qty <= Decimal("0"):
                continue

            side = OrderSide.BUY if delta_value > 0 else OrderSide.SELL
            reason = (
                f"target_weight={target_weight},target_value={target_value},"
                f"current_value={current_value},delta_value={delta_value}"
            )
            intents.append(
                OrderIntent(
                    account_id=account_id,
                    symbol=symbol,
                    side=side,
                    quantity=raw_qty,
                    reason=reason,
                )
            )

        return intents
