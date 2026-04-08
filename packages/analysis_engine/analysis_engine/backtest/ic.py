"""IC (Information Coefficient) helpers."""

from __future__ import annotations

from math import sqrt


def pearson_ic(factor_values: list[float], forward_returns: list[float]) -> float:
    """Compute Pearson IC for one cross-section."""

    if len(factor_values) != len(forward_returns):
        raise ValueError("factor_values and forward_returns must have same length")
    if not factor_values:
        return 0.0

    mean_x = sum(factor_values) / len(factor_values)
    mean_y = sum(forward_returns) / len(forward_returns)

    cov = sum((x - mean_x) * (y - mean_y) for x, y in zip(factor_values, forward_returns))
    var_x = sum((x - mean_x) ** 2 for x in factor_values)
    var_y = sum((y - mean_y) ** 2 for y in forward_returns)

    if var_x == 0 or var_y == 0:
        return 0.0
    return cov / sqrt(var_x * var_y)
