from datetime import date
from decimal import Decimal

import pytest

from packages.core.core.exceptions.domain import InvariantViolationError
from packages.domain.domain.research.value_objects.backtest_config import BacktestConfig
from packages.domain.domain.research.value_objects.factor_code import FactorCode, FactorCodeMode
from packages.domain.domain.trading.value_objects.money import Money
from packages.domain.domain.trading.value_objects.order_request import OrderRequest


def test_factor_code_rejects_empty_source() -> None:
    with pytest.raises(InvariantViolationError, match="cannot be empty"):
        FactorCode(mode=FactorCodeMode.FORMULA, source="   ")


def test_backtest_config_requires_valid_date_range() -> None:
    with pytest.raises(InvariantViolationError, match="end_date"):
        BacktestConfig(
            start_date=date(2026, 3, 1),
            end_date=date(2026, 2, 1),
            benchmark="000300.SH",
            initial_capital=Decimal("1000000"),
        )


def test_money_operations_require_same_currency() -> None:
    cny = Money(amount=Decimal("100"), currency="cny")
    usd = Money(amount=Decimal("10"), currency="USD")

    with pytest.raises(InvariantViolationError, match="Currency mismatch"):
        cny.add(usd)


def test_money_subtract_rejects_negative_result() -> None:
    cash = Money(amount=Decimal("10"), currency="CNY")

    with pytest.raises(InvariantViolationError, match="cannot produce negative"):
        cash.subtract(Money(amount=Decimal("11"), currency="CNY"))


def test_order_request_normalizes_symbol() -> None:
    request = OrderRequest(
        account_id="acct-1",
        symbol="sz000001",
        side="BUY",
        quantity=Decimal("100"),
        limit_price=Decimal("12.34"),
    )

    assert request.symbol == "SZ000001"
