from decimal import Decimal

from packages.datastore.datastore.repositories.strategy_repository import InMemoryStrategyRepository
from packages.datastore.datastore.repositories.trading_repository import InMemoryTradingRepository
from packages.datastore.datastore.unit_of_work.mongo_uow import MongoUnitOfWork
from packages.domain.domain.strategy.entities.rebalance_plan import RebalancePlan
from packages.domain.domain.trading.entities.order import Order, OrderSide


def test_inmemory_strategy_repository_roundtrip() -> None:
    repo = InMemoryStrategyRepository()
    plan = RebalancePlan(
        plan_id="plan-r1",
        strategy_version_id="sv-r1",
        targets={"SZ000001": Decimal("0.5")},
    )

    repo.save_plan(plan)

    assert repo.get_plan("plan-r1") == plan
    assert len(repo.list_plans("sv-r1")) == 1


def test_inmemory_trading_repository_roundtrip() -> None:
    repo = InMemoryTradingRepository()
    order = Order(
        order_id="ord-r1",
        account_id="acct-r1",
        symbol="sz000001",
        side=OrderSide.BUY,
        quantity=Decimal("100"),
    )

    repo.save_order(order)

    assert repo.get_order("ord-r1") == order
    assert len(repo.list_orders("acct-r1")) == 1


def test_unit_of_work_commits_on_success() -> None:
    with MongoUnitOfWork() as uow:
        assert uow.committed is False

    assert uow.committed is True
