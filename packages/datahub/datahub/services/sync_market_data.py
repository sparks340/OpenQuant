"""Service: sync market rows from adapter to repository."""

from packages.datahub.datahub.adapters.base import DataSourceAdapter
from packages.datahub.datahub.cleaners.market_cleaner import clean_market_rows
from packages.datastore.datastore.repositories.market_data_repository import MarketDataRepository


def sync_market_data(adapter: DataSourceAdapter, repository: MarketDataRepository) -> int:
    rows = adapter.fetch_market_rows()
    cleaned = clean_market_rows(rows)
    for bar in cleaned:
        repository.save_bar(
            symbol=bar.symbol,
            trade_date=bar.trade_date,
            close=bar.close,
            volume=bar.volume,
        )
    return len(cleaned)
