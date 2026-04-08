"""Market data cleaner."""

from dataclasses import dataclass
from datetime import date
from decimal import Decimal

from packages.datahub.datahub.utils.symbol_mapper import normalize_cn_symbol
from packages.datahub.datahub.utils.trading_calendar import parse_trade_date


@dataclass
class CleanMarketBar:
    symbol: str
    trade_date: date
    close: Decimal
    volume: Decimal


def clean_market_rows(rows: list[dict]) -> list[CleanMarketBar]:
    cleaned: list[CleanMarketBar] = []
    for row in rows:
        cleaned.append(
            CleanMarketBar(
                symbol=normalize_cn_symbol(str(row["symbol"]), str(row.get("exchange", ""))),
                trade_date=parse_trade_date(row["trade_date"]),
                close=Decimal(str(row["close"])),
                volume=Decimal(str(row["volume"])),
            )
        )
    return cleaned
