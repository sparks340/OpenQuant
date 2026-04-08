"""Instrument cleaner."""

from packages.datastore.datastore.repositories.instrument_repository import Instrument
from packages.datahub.datahub.utils.symbol_mapper import normalize_cn_symbol


def clean_instrument_rows(rows: list[dict]) -> list[Instrument]:
    result: list[Instrument] = []
    for row in rows:
        result.append(
            Instrument(
                symbol=normalize_cn_symbol(str(row["symbol"]), str(row.get("exchange", ""))),
                name=str(row["name"]).strip().upper(),
            )
        )
    return result
