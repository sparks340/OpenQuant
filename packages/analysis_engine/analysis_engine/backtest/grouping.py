"""Factor grouping helpers."""

from __future__ import annotations

from math import ceil


def assign_groups(symbol_scores: dict[str, float], group_count: int = 5) -> dict[str, int]:
    """Assign cross-sectional groups from low score to high score."""

    if group_count <= 0:
        raise ValueError("group_count must be positive")
    if not symbol_scores:
        return {}

    sorted_pairs = sorted(symbol_scores.items(), key=lambda item: (item[1], item[0]))
    bucket_size = ceil(len(sorted_pairs) / group_count)

    groups: dict[str, int] = {}
    for idx, (symbol, _) in enumerate(sorted_pairs):
        group_id = min((idx // bucket_size) + 1, group_count)
        groups[symbol] = group_id
    return groups
