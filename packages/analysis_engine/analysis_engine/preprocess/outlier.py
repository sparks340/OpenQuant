"""Outlier preprocessing helpers."""

from __future__ import annotations

from statistics import median


def clip_by_mad(values: list[float], n_mad: float = 3.0) -> list[float]:
    """Clip outliers using median absolute deviation.

    The function is deterministic and keeps order unchanged.
    """

    if not values:
        return []

    med = median(values)
    deviations = [abs(value - med) for value in values]
    mad = median(deviations)
    if mad == 0:
        return list(values)

    lower = med - (n_mad * mad)
    upper = med + (n_mad * mad)
    return [min(max(value, lower), upper) for value in values]
