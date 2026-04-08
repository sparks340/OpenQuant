"""Cross-sectional operators."""

from __future__ import annotations

from datetime import date
from decimal import Decimal


def rank_by_date(values: dict[date, dict[str, Decimal]]) -> dict[date, dict[str, Decimal]]:
    ranked: dict[date, dict[str, Decimal]] = {}
    for trade_date, symbol_values in values.items():
        ordered = sorted(symbol_values.items(), key=lambda item: item[1])
        count = max(len(ordered) - 1, 1)
        ranked[trade_date] = {
            symbol: Decimal(str(idx / count)) for idx, (symbol, _) in enumerate(ordered)
        }
    return ranked
