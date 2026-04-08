from decimal import Decimal

from packages.core.core.enums.trading import OrderSide
from packages.portfolio_engine.portfolio_engine.builders.order_intent_builder import OrderIntent
from packages.risk_engine.risk_engine.models.risk_context import RiskContext
from packages.risk_engine.risk_engine.services.risk_service import RiskService


def _intent(symbol: str, side: OrderSide, qty: str) -> OrderIntent:
    return OrderIntent(
        account_id="ACC-001",
        symbol=symbol,
        side=side,
        quantity=Decimal(qty),
        reason="test",
    )


def test_risk_service_returns_rule_decisions_per_order() -> None:
    service = RiskService(max_position_weight=Decimal("0.5"), min_cash_reserve=Decimal("0.1"))
    context = RiskContext(
        account_id="ACC-001",
        total_equity=Decimal("100000"),
        cash_available=Decimal("20000"),
        latest_prices={"AAA": Decimal("10"), "BBB": Decimal("20"), "CCC": Decimal("50")},
        current_position_weights={"AAA": Decimal("0.45")},
        blacklist={"BBB"},
    )

    intents = [
        _intent("AAA", OrderSide.BUY, "600"),   # 6000 value => pushes AAA to 0.51
        _intent("BBB", OrderSide.BUY, "100"),   # blacklisted
        _intent("CCC", OrderSide.BUY, "220"),   # 11000 value => cash would drop below reserve
        _intent("AAA", OrderSide.SELL, "100"),  # should pass baseline rules
    ]

    decisions = service.evaluate_orders(intents=intents, context=context)

    assert len(decisions) == 4
    assert decisions[0].approved is False
    assert any(reason.startswith("max_position_weight") for reason in decisions[0].reasons)

    assert decisions[1].approved is False
    assert any("blacklist" in reason for reason in decisions[1].reasons)

    assert decisions[2].approved is False
    assert any(reason.startswith("cash_reserve") for reason in decisions[2].reasons)

    assert decisions[3].approved is True
    assert decisions[3].reasons == ["approved"]
