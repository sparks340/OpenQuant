from datetime import date
from decimal import Decimal

import pytest

from packages.analysis_engine.analysis_engine.services.analysis_service import AnalysisService


REQUIRED_FACTOR_KEYS = {"symbol", "trade_date", "factor_value"}
REQUIRED_MARKET_KEYS = {"symbol", "trade_date", "close"}


def _market_rows() -> list[dict]:
    return [
        {"symbol": "AAA", "trade_date": date(2026, 4, 1), "close": Decimal("10")},
        {"symbol": "AAA", "trade_date": date(2026, 4, 2), "close": Decimal("11")},
        {"symbol": "AAA", "trade_date": date(2026, 4, 3), "close": Decimal("12")},
        {"symbol": "AAA", "trade_date": date(2026, 4, 4), "close": Decimal("13")},
        {"symbol": "BBB", "trade_date": date(2026, 4, 1), "close": Decimal("10")},
        {"symbol": "BBB", "trade_date": date(2026, 4, 2), "close": Decimal("10")},
        {"symbol": "BBB", "trade_date": date(2026, 4, 3), "close": Decimal("10")},
        {"symbol": "BBB", "trade_date": date(2026, 4, 4), "close": Decimal("10")},
        {"symbol": "CCC", "trade_date": date(2026, 4, 1), "close": Decimal("10")},
        {"symbol": "CCC", "trade_date": date(2026, 4, 2), "close": Decimal("9")},
        {"symbol": "CCC", "trade_date": date(2026, 4, 3), "close": Decimal("8")},
        {"symbol": "CCC", "trade_date": date(2026, 4, 4), "close": Decimal("7")},
    ]


def _factor_rows() -> list[dict]:
    rows: list[dict] = []
    for trade_date in [date(2026, 4, 1), date(2026, 4, 2), date(2026, 4, 3), date(2026, 4, 4)]:
        rows.extend(
            [
                {"symbol": "AAA", "trade_date": trade_date, "factor_value": Decimal("2")},
                {"symbol": "BBB", "trade_date": trade_date, "factor_value": Decimal("1")},
                {"symbol": "CCC", "trade_date": trade_date, "factor_value": Decimal("0")},
            ]
        )
    return rows


def test_analysis_service_generates_deterministic_report() -> None:
    report = AnalysisService.run(_factor_rows(), _market_rows(), group_count=3)

    assert report["summary"]["observations"] == 3
    assert report["summary"]["ic_mean"] > 0.99
    assert report["summary"]["top_minus_bottom_mean"] > 0.18

    assert "2026-04-01" in report["series"]["ic_by_date"]
    first_day_groups = report["series"]["group_return_by_date"]["2026-04-01"]
    assert first_day_groups["3"] > first_day_groups["1"]


def test_analysis_service_report_is_input_order_independent() -> None:
    report_a = AnalysisService.run(_factor_rows(), _market_rows(), group_count=3)
    report_b = AnalysisService.run(list(reversed(_factor_rows())), list(reversed(_market_rows())), group_count=3)

    assert report_a == report_b


def test_analysis_service_handles_group_count_larger_than_sample_size() -> None:
    report = AnalysisService.run(_factor_rows(), _market_rows(), group_count=5)

    assert report["summary"]["observations"] == 3
    assert report["summary"]["top_minus_bottom_mean"] > 0


def test_analysis_service_rejects_missing_required_fields() -> None:
    bad_factor_rows = [{key: value for key, value in row.items() if key != "factor_value"} for row in _factor_rows()]
    with pytest.raises(ValueError, match="factor_rows"):
        AnalysisService.run(bad_factor_rows, _market_rows())

    bad_market_rows = [{key: value for key, value in row.items() if key != "close"} for row in _market_rows()]
    with pytest.raises(ValueError, match="market_rows"):
        AnalysisService.run(_factor_rows(), bad_market_rows)


def test_test_data_contains_required_keys() -> None:
    for row in _factor_rows():
        assert REQUIRED_FACTOR_KEYS.issubset(row.keys())
    for row in _market_rows():
        assert REQUIRED_MARKET_KEYS.issubset(row.keys())
