"""Service: sync instruments from adapter to repository."""

from packages.datahub.datahub.adapters.base import DataSourceAdapter
from packages.datahub.datahub.cleaners.instrument_cleaner import clean_instrument_rows
from packages.datastore.datastore.repositories.instrument_repository import InstrumentRepository


def sync_instruments(adapter: DataSourceAdapter, repository: InstrumentRepository) -> int:
    rows = adapter.fetch_instrument_rows()
    instruments = clean_instrument_rows(rows)
    for instrument in instruments:
        repository.save(instrument)
    return len(instruments)
