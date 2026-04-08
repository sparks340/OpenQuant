"""Index initialization helpers."""

from packages.datastore.datastore.mongo.collections import FACTORS, MARKET_BARS, ORDERS, REBALANCE_PLANS, TASKS
from packages.datastore.datastore.mongo.client import MongoClientManager


def initialize_indexes(client: MongoClientManager) -> dict[str, list[tuple[str, int]]]:
    specs: dict[str, list[tuple[str, int]]] = {
        FACTORS: [("factor_id", 1), ("owner_id", 1)],
        TASKS: [("task_id", 1), ("status", 1)],
        MARKET_BARS: [("symbol", 1), ("trade_date", 1)],
        ORDERS: [("order_id", 1), ("account_id", 1)],
        REBALANCE_PLANS: [("plan_id", 1), ("strategy_version_id", 1)],
    }

    for collection_name, index_specs in specs.items():
        collection = client.get_collection(collection_name)
        for spec in index_specs:
            collection.create_index(spec)

    return specs
