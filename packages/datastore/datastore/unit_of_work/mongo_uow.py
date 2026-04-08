"""Datastore unit of work contracts for Mongo-backed implementations."""

from __future__ import annotations

from packages.datastore.datastore.repositories.factor_repository import (
    FactorRepository,
    InMemoryFactorRepository,
)
from packages.datastore.datastore.repositories.strategy_repository import (
    InMemoryStrategyRepository,
    StrategyRepository,
)
from packages.datastore.datastore.repositories.task_repository import (
    InMemoryTaskRepository,
    TaskRepository,
)
from packages.datastore.datastore.repositories.trading_repository import (
    InMemoryTradingRepository,
    TradingRepository,
)


class MongoUnitOfWork:
    """UoW boundary that groups repository operations in one transaction-like scope."""

    def __init__(
        self,
        factor_repository: FactorRepository | None = None,
        strategy_repository: StrategyRepository | None = None,
        trading_repository: TradingRepository | None = None,
        task_repository: TaskRepository | None = None,
    ) -> None:
        self.factor_repository = factor_repository or InMemoryFactorRepository()
        self.strategy_repository = strategy_repository or InMemoryStrategyRepository()
        self.trading_repository = trading_repository or InMemoryTradingRepository()
        self.task_repository = task_repository or InMemoryTaskRepository()
        self.committed = False
        self._snapshots: dict[str, object] = {}

    def __enter__(self) -> "MongoUnitOfWork":
        self._capture_snapshots()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb) -> None:
        if exc_type is None:
            self.commit()
        else:
            self.rollback()

    def _capture_snapshots(self) -> None:
        for name in ("factor_repository", "strategy_repository", "trading_repository", "task_repository"):
            repository = getattr(self, name)
            snapshot_fn = getattr(repository, "snapshot", None)
            if callable(snapshot_fn):
                self._snapshots[name] = snapshot_fn()

    def commit(self) -> None:
        self.committed = True
        self._snapshots = {}

    def rollback(self) -> None:
        for name, state in self._snapshots.items():
            repository = getattr(self, name)
            restore_fn = getattr(repository, "restore", None)
            if callable(restore_fn):
                restore_fn(state)
        self.committed = False
