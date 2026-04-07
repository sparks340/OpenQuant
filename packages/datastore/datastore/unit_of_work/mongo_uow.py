"""Datastore unit of work contracts for Mongo-backed implementations."""

from __future__ import annotations

from packages.datastore.datastore.repositories.strategy_repository import (
    InMemoryStrategyRepository,
    StrategyRepository,
)
from packages.datastore.datastore.repositories.trading_repository import (
    InMemoryTradingRepository,
    TradingRepository,
)


class MongoUnitOfWork:
    """UoW boundary that groups repository operations in one transaction-like scope."""

    def __init__(
        self,
        strategy_repository: StrategyRepository | None = None,
        trading_repository: TradingRepository | None = None,
    ) -> None:
        self.strategy_repository = strategy_repository or InMemoryStrategyRepository()
        self.trading_repository = trading_repository or InMemoryTradingRepository()
        self.committed = False

    def __enter__(self) -> "MongoUnitOfWork":
        return self

    def __exit__(self, exc_type, exc_val, exc_tb) -> None:
        if exc_type is None:
            self.commit()
        else:
            self.rollback()

    def commit(self) -> None:
        self.committed = True

    def rollback(self) -> None:
        self.committed = False
