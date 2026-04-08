from datetime import date
from decimal import Decimal

import pytest

from packages.core.core.enums.trading import OrderSide
from packages.core.core.exceptions.domain import InvariantViolationError
from packages.domain.domain.platform.entities.chat_session import ChatSession, ChatSessionStatus
from packages.domain.domain.platform.entities.task_record import TaskRecord
from packages.domain.domain.platform.entities.user import User, UserRole
from packages.domain.domain.platform.services.task_service import TaskService
from packages.domain.domain.research.entities.factor_definition import FactorDefinition
from packages.domain.domain.research.services.analysis_domain_service import AnalysisDomainService
from packages.domain.domain.research.services.factor_domain_service import FactorDomainService
from packages.domain.domain.strategy.entities.signal import Signal
from packages.domain.domain.strategy.entities.strategy_version import StrategyLifecycleStatus, StrategyVersion
from packages.domain.domain.strategy.services.signal_service import SignalService
from packages.domain.domain.trading.entities.account import Account
from packages.domain.domain.trading.entities.position import Position
from packages.domain.domain.trading.entities.trade import Trade
from packages.domain.domain.trading.services.order_service import OrderService
from packages.domain.domain.trading.services.position_service import PositionService
from packages.domain.domain.trading.value_objects.order_request import OrderRequest


def test_factor_domain_service_builds_incremental_versions() -> None:
    definition = FactorDefinition(
        factor_id="fac-1", name="alpha", code="rank(close)", code_type="formula", owner_id="u1"
    )

    v1 = FactorDomainService.create_version(definition, "rank(close)", existing_versions=[])
    v2 = FactorDomainService.create_version(definition, "rank(volume)", existing_versions=[v1])

    assert v1.version == 1
    assert v2.version == 2


def test_analysis_domain_service_calculates_mean_ic() -> None:
    metrics = AnalysisDomainService.summarize_ic([Decimal("0.1"), Decimal("0.2")])
    assert metrics["ic_mean"] == Decimal("0.15")


def test_strategy_version_transition_rules() -> None:
    sv = StrategyVersion(strategy_version_id="sv-1", strategy_id="s-1", version=1)
    sv.transition_to(StrategyLifecycleStatus.ACTIVE)
    assert sv.status == StrategyLifecycleStatus.ACTIVE

    with pytest.raises(InvariantViolationError):
        sv.transition_to(StrategyLifecycleStatus.DRAFT)


def test_signal_service_ranks_and_deduplicates_by_symbol() -> None:
    ranked = SignalService.rank_signals(
        [
            Signal(symbol="sz000001", score=Decimal("0.2"), as_of=date(2026, 4, 8)),
            Signal(symbol="SZ000001", score=Decimal("0.3"), as_of=date(2026, 4, 8)),
            Signal(symbol="sh600000", score=Decimal("0.1"), as_of=date(2026, 4, 8)),
        ],
        top_n=2,
    )
    assert [s.symbol for s in ranked] == ["SZ000001", "SH600000"]


def test_order_service_creates_pending_order_from_request() -> None:
    req = OrderRequest(
        account_id="acct-1",
        symbol="sz000001",
        side="BUY",
        quantity=Decimal("100"),
        limit_price=Decimal("12.3"),
    )
    order = OrderService.create_order("ord-1", req)
    assert order.side == OrderSide.BUY
    assert order.status.value == "PENDING"


def test_position_service_updates_position_with_buy_trade() -> None:
    position = Position(symbol="SZ000001", quantity=Decimal("100"), average_price=Decimal("10"))
    trade = Trade(
        trade_id="t-1",
        order_id="o-1",
        symbol="SZ000001",
        side="BUY",
        quantity=Decimal("100"),
        price=Decimal("12"),
    )
    updated = PositionService.apply_trade(position, trade)
    assert updated.quantity == Decimal("200")


def test_platform_user_and_chat_session_invariants() -> None:
    user = User(user_id="u-1", email="a@b.com", role="researcher")
    session = ChatSession(session_id="c-1", user_id=user.user_id, title="alpha")
    session.close()
    assert session.status == ChatSessionStatus.CLOSED
    assert user.role == UserRole.RESEARCHER


def test_task_service_creates_task_and_log_entry() -> None:
    record = TaskService.create_task(task_id="task-1", task_type="factor_run")
    assert isinstance(record, TaskRecord)
    log = TaskService.append_log(record, message="started", sequence=1, level="INFO")
    assert log.task_id == record.task_id


def test_account_rejects_negative_cash() -> None:
    with pytest.raises(InvariantViolationError, match="cash"):
        Account(account_id="a-1", cash=Decimal("-1"), currency="CNY")
