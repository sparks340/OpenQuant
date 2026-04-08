"""Standardization helpers."""

from __future__ import annotations

from math import sqrt


def zscore(values: list[float]) -> list[float]:
    """Standardize values with population standard deviation.

    Returns zeros when variance is zero.
    """

    if not values:
        return []

    mean = sum(values) / len(values)
    variance = sum((value - mean) ** 2 for value in values) / len(values)
    if variance == 0:
        return [0.0 for _ in values]

    std = sqrt(variance)
    return [(value - mean) / std for value in values]
