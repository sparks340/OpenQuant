"""Order domain service."""

from packages.domain.domain.trading.entities.order import Order
from packages.domain.domain.trading.value_objects.order_request import OrderRequest


class OrderService:
    """Factory helpers for order aggregates."""

    @staticmethod
    def create_order(order_id: str, request: OrderRequest) -> Order:
        return Order(
            order_id=order_id,
            account_id=request.account_id,
            symbol=request.symbol,
            side=request.side,
            quantity=request.quantity,
        )
