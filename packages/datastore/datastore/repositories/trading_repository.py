"""Trading repository contracts and in-memory implementation."""

from __future__ import annotations

from abc import ABC, abstractmethod

from packages.domain.domain.trading.entities.order import Order


class TradingRepository(ABC):
    """Persistence boundary for trading aggregates."""

    @abstractmethod
    def save_order(self, order: Order) -> Order:
        """Persist or update order aggregate."""

    @abstractmethod
    def get_order(self, order_id: str) -> Order | None:
        """Load order by id."""

    @abstractmethod
    def list_orders(self, account_id: str) -> list[Order]:
        """List orders by account."""


class InMemoryTradingRepository(TradingRepository):
    """Reference implementation used for unit tests and local wiring."""

    def __init__(self) -> None:
        self._orders: dict[str, Order] = {}

    def save_order(self, order: Order) -> Order:
        self._orders[order.order_id] = order
        return order

    def get_order(self, order_id: str) -> Order | None:
        return self._orders.get(order_id)

    def list_orders(self, account_id: str) -> list[Order]:
        return [order for order in self._orders.values() if order.account_id == account_id]
