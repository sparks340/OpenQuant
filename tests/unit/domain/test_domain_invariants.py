from decimal import Decimal

import pytest

from packages.core.core.exceptions.domain import InvariantViolationError
from packages.domain.domain.research.entities.factor_run import FactorRun, FactorRunStatus
from packages.domain.domain.strategy.entities.rebalance_plan import RebalancePlan
from packages.domain.domain.trading.entities.order import Order, OrderSide, OrderStatus


def test_order_status_transition_happy_path() -> None:
    order = Order(
        order_id="ord-1",
        account_id="acct-1",
        symbol="sz000001",
        side=OrderSide.BUY,
        quantity=Decimal("100"),
    )

    order.transition_to(OrderStatus.SUBMITTED)
    order.transition_to(OrderStatus.FILLED)

    assert order.symbol == "SZ000001"
    assert order.submitted_at is not None
    assert order.filled_at is not None


def test_order_status_transition_reject_invalid_jump() -> None:
    order = Order(
        order_id="ord-2",
        account_id="acct-1",
        symbol="SH600000",
        side=OrderSide.SELL,
        quantity=Decimal("100"),
    )

    with pytest.raises(InvariantViolationError, match="Invalid order transition"):
        order.transition_to(OrderStatus.FILLED)


def test_order_filled_requires_submitted_timestamp_and_preserves_state() -> None:
    order = Order(
        order_id="ord-3",
        account_id="acct-1",
        symbol="SH600519",
        side=OrderSide.BUY,
        quantity=Decimal("10"),
    )
    order.transition_to(OrderStatus.SUBMITTED)
    order.submitted_at = None

    with pytest.raises(InvariantViolationError, match="submitted_at"):
        order.transition_to(OrderStatus.FILLED)

    assert order.status == OrderStatus.SUBMITTED
    assert order.filled_at is None


def test_factor_run_lifecycle_requires_valid_sequence() -> None:
    run = FactorRun(run_id="run-1", factor_version_id="fv-1")

    run.transition_to(FactorRunStatus.RUNNING)
    run.transition_to(FactorRunStatus.FAILED, error_message="division by zero")

    assert run.started_at is not None
    assert run.finished_at is not None
    assert run.error_message == "division by zero"


def test_factor_run_failed_transition_requires_error_message() -> None:
    run = FactorRun(run_id="run-4", factor_version_id="fv-4")

    with pytest.raises(InvariantViolationError, match="requires explicit error_message"):
        run.transition_to(FactorRunStatus.FAILED)


def test_factor_run_invalid_transition_rejected() -> None:
    run = FactorRun(run_id="run-2", factor_version_id="fv-2")

    with pytest.raises(InvariantViolationError, match="Invalid factor run transition"):
        run.transition_to(FactorRunStatus.SUCCEEDED)


def test_factor_run_constructor_rejects_succeeded_with_error_message() -> None:
    with pytest.raises(InvariantViolationError, match="cannot include error_message"):
        FactorRun(
            run_id="run-3",
            factor_version_id="fv-3",
            status=FactorRunStatus.SUCCEEDED,
            started_at="2026-01-01T00:00:00Z",
            finished_at="2026-01-01T00:10:00Z",
            error_message="should be empty",
        )


def test_order_constructor_requires_timestamps_for_filled_status() -> None:
    with pytest.raises(InvariantViolationError, match="must include filled_at"):
        Order(
            order_id="ord-4",
            account_id="acct-1",
            symbol="SH601318",
            side=OrderSide.BUY,
            quantity=Decimal("1"),
            status=OrderStatus.FILLED,
            submitted_at="2026-01-01T00:00:00Z",
        )


def test_rebalance_plan_requires_non_empty_targets() -> None:
    with pytest.raises(InvariantViolationError, match="at least one target"):
        RebalancePlan(plan_id="plan-empty", strategy_version_id="sv-1", targets={})


def test_rebalance_plan_total_weight_must_not_exceed_1() -> None:
    with pytest.raises(InvariantViolationError, match="Total target weight"):
        RebalancePlan(
            plan_id="plan-1",
            strategy_version_id="sv-1",
            targets={"SZ000001": Decimal("0.8"), "SH600000": Decimal("0.3")},
        )


def test_rebalance_plan_target_symbol_normalized_to_upper() -> None:
    plan = RebalancePlan(
        plan_id="plan-2",
        strategy_version_id="sv-2",
        targets={"sz000001": Decimal("0.4")},
    )

    assert "SZ000001" in plan.targets


def test_rebalance_plan_rejects_zero_weight() -> None:
    with pytest.raises(InvariantViolationError, match="must be positive"):
        RebalancePlan(
            plan_id="plan-3",
            strategy_version_id="sv-3",
            targets={"SZ000001": Decimal("0")},
        )
