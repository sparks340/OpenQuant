from datetime import date
from decimal import Decimal

from packages.datahub.datahub.adapters.csv_adapter import CSVDataAdapter
from packages.datahub.datahub.services.sync_base_factors import sync_base_factors
from packages.datahub.datahub.services.sync_instruments import sync_instruments
from packages.datahub.datahub.services.sync_market_data import sync_market_data
from packages.datastore.datastore.repositories.factor_repository import InMemoryFactorRepository
from packages.datastore.datastore.repositories.instrument_repository import InMemoryInstrumentRepository
from packages.datastore.datastore.repositories.market_data_repository import InMemoryMarketDataRepository
from packages.domain.domain.research.entities.factor_definition import FactorDefinition


def test_sync_market_data_standardizes_and_persists() -> None:
    adapter = CSVDataAdapter(
        market_rows=[
            {"symbol": "000001", "exchange": "sz", "trade_date": "2026-04-08", "close": "12.3", "volume": "100"}
        ]
    )
    repo = InMemoryMarketDataRepository()

    count = sync_market_data(adapter, repo)

    bars = repo.list_bars("SZ000001", start=date(2026, 4, 1), end=date(2026, 4, 30))
    assert count == 1
    assert bars[0].close == Decimal("12.3")


def test_sync_instruments_standardizes_symbol_and_name() -> None:
    adapter = CSVDataAdapter(instrument_rows=[{"symbol": "600000", "exchange": "sh", "name": " pf bank "}])
    repo = InMemoryInstrumentRepository()

    count = sync_instruments(adapter, repo)

    instruments = repo.list_all()
    assert count == 1
    assert instruments[0].symbol == "SH600000"
    assert instruments[0].name == "PF BANK"


def test_sync_base_factors_creates_factor_definitions() -> None:
    adapter = CSVDataAdapter(base_factor_rows=[{"factor_id": "mom_5", "name": "Mom 5", "code": "close/delay(close,5)-1"}])
    repo = InMemoryFactorRepository()

    count = sync_base_factors(adapter, repo, owner_id="system")

    stored = repo.get("mom_5")
    assert count == 1
    assert isinstance(stored, FactorDefinition)
