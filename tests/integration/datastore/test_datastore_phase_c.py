from datetime import date
from decimal import Decimal

from packages.datastore.datastore.mongo.client import MongoClientManager
from packages.datastore.datastore.mongo.indexes import initialize_indexes
from packages.datastore.datastore.redis.client import RedisClientManager
from packages.datastore.datastore.repositories.factor_repository import InMemoryFactorRepository
from packages.datastore.datastore.repositories.market_data_repository import InMemoryMarketDataRepository
from packages.datastore.datastore.repositories.task_repository import InMemoryTaskRepository
from packages.datastore.datastore.unit_of_work.mongo_uow import MongoUnitOfWork
from packages.domain.domain.platform.entities.task_record import TaskRecord
from packages.domain.domain.research.entities.factor_definition import FactorDefinition


def test_mongo_and_redis_clients_basic_ops() -> None:
    mongo = MongoClientManager()
    redis = RedisClientManager()

    coll = mongo.get_collection("factors")
    coll.insert_one({"_id": "f1", "name": "alpha"})
    assert coll.find_one({"_id": "f1"})["name"] == "alpha"

    redis.set("k", "v")
    assert redis.get("k") == "v"


def test_initialize_indexes_contains_expected_collections() -> None:
    mongo = MongoClientManager()
    result = initialize_indexes(mongo)
    assert "factors" in result
    assert ("factor_id", 1) in result["factors"]


def test_repository_crud_and_query_roundtrip() -> None:
    factor_repo = InMemoryFactorRepository()
    task_repo = InMemoryTaskRepository()
    market_repo = InMemoryMarketDataRepository()

    factor = FactorDefinition(
        factor_id="f-1", name="alpha", code="rank(close)", code_type="formula", owner_id="u-1"
    )
    factor_repo.save(factor)
    assert factor_repo.get("f-1") == factor

    task = TaskRecord(task_id="t-1", task_type="factor_run")
    task_repo.save(task)
    assert task_repo.get("t-1") == task

    market_repo.save_bar(
        symbol="SZ000001",
        trade_date=date(2026, 4, 8),
        close=Decimal("12.34"),
        volume=Decimal("100000"),
    )
    bars = market_repo.list_bars(symbol="SZ000001", start=date(2026, 4, 1), end=date(2026, 4, 30))
    assert len(bars) == 1


def test_unit_of_work_rolls_back_when_exception_raised() -> None:
    factor_repo = InMemoryFactorRepository()

    try:
        with MongoUnitOfWork(factor_repository=factor_repo) as uow:
            uow.factor_repository.save(
                FactorDefinition(
                    factor_id="f-rollback",
                    name="alpha",
                    code="rank(close)",
                    code_type="formula",
                    owner_id="u-1",
                )
            )
            raise RuntimeError("boom")
    except RuntimeError:
        pass

    assert factor_repo.get("f-rollback") is None
