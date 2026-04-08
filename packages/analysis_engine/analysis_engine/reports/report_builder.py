"""Analysis report builder."""

from __future__ import annotations


def build_report(
    *,
    ic_by_date: dict[str, float],
    mean_ic: float,
    group_return_by_date: dict[str, dict[str, float]],
    top_minus_bottom_mean: float,
) -> dict:
    """Build minimal JSON-serializable report payload."""

    return {
        "summary": {
            "ic_mean": round(mean_ic, 6),
            "top_minus_bottom_mean": round(top_minus_bottom_mean, 6),
            "observations": len(ic_by_date),
        },
        "series": {
            "ic_by_date": {date_key: round(value, 6) for date_key, value in sorted(ic_by_date.items())},
            "group_return_by_date": {
                date_key: {group_key: round(group_value, 6) for group_key, group_value in sorted(group_values.items())}
                for date_key, group_values in sorted(group_return_by_date.items())
            },
        },
    }
