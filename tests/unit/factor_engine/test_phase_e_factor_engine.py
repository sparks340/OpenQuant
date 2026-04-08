from datetime import date
from decimal import Decimal

import pytest

from packages.factor_engine.factor_engine.models.factor_frame import FactorFrame
from packages.factor_engine.factor_engine.runtime.formula_executor import FormulaExecutor
from packages.factor_engine.factor_engine.validators.formula_validator import FormulaValidator


def _sample_market() -> list[dict]:
    return [
        {"symbol": "SZ000001", "trade_date": date(2026, 4, 1), "close": Decimal("10")},
        {"symbol": "SZ000001", "trade_date": date(2026, 4, 2), "close": Decimal("11")},
        {"symbol": "SZ000001", "trade_date": date(2026, 4, 3), "close": Decimal("12")},
        {"symbol": "SH600000", "trade_date": date(2026, 4, 1), "close": Decimal("20")},
        {"symbol": "SH600000", "trade_date": date(2026, 4, 2), "close": Decimal("19")},
        {"symbol": "SH600000", "trade_date": date(2026, 4, 3), "close": Decimal("18")},
    ]


def test_formula_validator_accepts_supported_expressions() -> None:
    assert FormulaValidator.validate("RANK(close)").is_valid is True
    assert FormulaValidator.validate("DELAY(close,1)").is_valid is True
    assert FormulaValidator.validate("TS_MEAN(close,2)").is_valid is True


def test_formula_validator_rejects_unsafe_or_unknown_expression() -> None:
    invalid = FormulaValidator.validate("__import__('os').system('rm -rf /')")
    assert invalid.is_valid is False


def test_formula_executor_rank_and_delay_and_ts_mean() -> None:
    market = _sample_market()

    rank_frame = FormulaExecutor.execute("RANK(close)", market)
    delay_frame = FormulaExecutor.execute("DELAY(close,1)", market)
    mean_frame = FormulaExecutor.execute("TS_MEAN(close,2)", market)

    assert isinstance(rank_frame, FactorFrame)
    assert rank_frame.get("SH600000", date(2026, 4, 1)) == Decimal("1")
    assert rank_frame.get("SZ000001", date(2026, 4, 1)) == Decimal("0")

    assert delay_frame.get("SZ000001", date(2026, 4, 2)) == Decimal("10")
    assert delay_frame.get("SZ000001", date(2026, 4, 1)) is None

    assert mean_frame.get("SZ000001", date(2026, 4, 2)) == Decimal("10.5")


def test_formula_executor_rejects_invalid_expression() -> None:
    with pytest.raises(ValueError):
        FormulaExecutor.execute("UNKNOWN(close)", _sample_market())
