"""Time-series operators."""

from __future__ import annotations

from datetime import date
from decimal import Decimal


def delay_by_symbol(values: dict[str, list[tuple[date, Decimal]]], periods: int) -> dict[str, list[tuple[date, Decimal | None]]]:
    result: dict[str, list[tuple[date, Decimal | None]]] = {}
    for symbol, series in values.items():
        delayed: list[tuple[date, Decimal | None]] = []
        for idx, (trade_date, _) in enumerate(series):
            source_idx = idx - periods
            delayed_value = series[source_idx][1] if source_idx >= 0 else None
            delayed.append((trade_date, delayed_value))
        result[symbol] = delayed
    return result


def ts_mean_by_symbol(values: dict[str, list[tuple[date, Decimal]]], window: int) -> dict[str, list[tuple[date, Decimal]]]:
    result: dict[str, list[tuple[date, Decimal]]] = {}
    for symbol, series in values.items():
        averaged: list[tuple[date, Decimal]] = []
        for idx, (trade_date, _) in enumerate(series):
            start_idx = max(0, idx - window + 1)
            window_values = [value for _, value in series[start_idx : idx + 1]]
            mean = sum(window_values) / Decimal(len(window_values))
            averaged.append((trade_date, mean))
        result[symbol] = averaged
    return result
