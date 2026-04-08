from decimal import Decimal

from packages.core.core.enums.trading import OrderSide
from packages.portfolio_engine.portfolio_engine.services.portfolio_service import PortfolioService


def test_portfolio_service_builds_stable_target_weights() -> None:
    service = PortfolioService()

    targets = service.build_target_positions(
        scores={"AAA": Decimal("0.9"), "BBB": Decimal("0.6"), "CCC": Decimal("0.3")},
        top_n=2,
        max_single_weight=Decimal("0.7"),
    )

    assert [item.symbol for item in targets] == ["AAA", "BBB"]
    assert targets[0].target_weight == Decimal("0.6")
    assert targets[1].target_weight == Decimal("0.4")


def test_portfolio_service_builds_explainable_order_intents() -> None:
    service = PortfolioService()

    intents = service.build_order_intents(
        account_id="ACC-001",
        total_equity=Decimal("100000"),
        targets=service.build_target_positions(
            scores={"AAA": Decimal("1.0"), "BBB": Decimal("0.5")},
            top_n=2,
            max_single_weight=Decimal("0.8"),
        ),
        latest_prices={"AAA": Decimal("10"), "BBB": Decimal("20")},
        current_positions={"AAA": Decimal("2000"), "BBB": Decimal("500")},
    )

    # AAA current value=20000, target value~=66666 => buy
    aaa = next(item for item in intents if item.symbol == "AAA")
    assert aaa.side == OrderSide.BUY
    assert aaa.quantity > 0
    assert "target_weight" in aaa.reason

    # BBB current value=10000, target value~=33333 => buy
    bbb = next(item for item in intents if item.symbol == "BBB")
    assert bbb.side == OrderSide.BUY
    assert bbb.quantity > 0


def test_portfolio_service_skips_zero_delta_orders() -> None:
    service = PortfolioService()
    targets = service.build_target_positions(
        scores={"AAA": Decimal("1")},
        top_n=1,
        max_single_weight=Decimal("1"),
    )

    intents = service.build_order_intents(
        account_id="ACC-001",
        total_equity=Decimal("1000"),
        targets=targets,
        latest_prices={"AAA": Decimal("10")},
        current_positions={"AAA": Decimal("100")},
    )

    assert intents == []
