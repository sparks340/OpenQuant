from datetime import date
from decimal import Decimal

import pytest

from packages.core.core.exceptions.domain import InvariantViolationError
from packages.domain.domain.strategy.entities.signal import Signal
from packages.domain.domain.strategy.services.rebalance_service import RebalanceService


def test_rebalance_service_builds_plan_from_top_positive_signals() -> None:
    service = RebalanceService()
    signals = [
        Signal(symbol="sz000001", score=Decimal("0.8"), as_of=date(2026, 4, 7)),
        Signal(symbol="sh600000", score=Decimal("0.4"), as_of=date(2026, 4, 7)),
        Signal(symbol="sh601318", score=Decimal("-0.2"), as_of=date(2026, 4, 7)),
    ]

    plan = service.build_plan(
        plan_id="plan-10",
        strategy_version_id="sv-10",
        signals=signals,
        top_n=2,
        max_single_weight=Decimal("0.7"),
    )

    assert set(plan.targets.keys()) == {"SZ000001", "SH600000"}
    assert sum(plan.targets.values(), start=Decimal("0")) <= Decimal("1")


def test_rebalance_service_rejects_no_positive_signal() -> None:
    service = RebalanceService()
    signals = [Signal(symbol="sh601318", score=Decimal("-0.1"), as_of=date(2026, 4, 7))]

    with pytest.raises(InvariantViolationError, match="No positive signals"):
        service.build_plan(plan_id="plan-11", strategy_version_id="sv-11", signals=signals)


def test_signal_score_range_enforced() -> None:
    with pytest.raises(InvariantViolationError, match=r"within \[-1, 1\]"):
        Signal(symbol="sh600519", score=Decimal("1.2"), as_of=date(2026, 4, 7))


def test_rebalance_service_respects_single_name_cap_after_allocation() -> None:
    service = RebalanceService()
    signals = [
        Signal(symbol="sz000001", score=Decimal("0.9"), as_of=date(2026, 4, 7)),
        Signal(symbol="sh600000", score=Decimal("0.05"), as_of=date(2026, 4, 7)),
        Signal(symbol="sh601318", score=Decimal("0.05"), as_of=date(2026, 4, 7)),
    ]

    plan = service.build_plan(
        plan_id="plan-12",
        strategy_version_id="sv-12",
        signals=signals,
        top_n=3,
        max_single_weight=Decimal("0.4"),
    )

    assert max(plan.targets.values()) <= Decimal("0.4")
