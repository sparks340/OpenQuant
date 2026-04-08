import asyncio
from datetime import date

from apps.api_service.api_service.deps import get_store
from apps.api_service.api_service.main import app
from apps.api_service.api_service.routers.analysis import get_report
from apps.api_service.api_service.routers.factors import create_factor, run_factor
from apps.api_service.api_service.routers.trading import get_account, get_orders, get_positions
from apps.api_service.api_service.schemas.factor import FactorCreateRequest, FactorRunRequest, MarketRowPayload


def _sample_market_rows() -> list[MarketRowPayload]:
    return [
        MarketRowPayload(symbol="AAA", trade_date=date(2026, 4, 1), close="10"),
        MarketRowPayload(symbol="AAA", trade_date=date(2026, 4, 2), close="11"),
        MarketRowPayload(symbol="AAA", trade_date=date(2026, 4, 3), close="12"),
        MarketRowPayload(symbol="BBB", trade_date=date(2026, 4, 1), close="10"),
        MarketRowPayload(symbol="BBB", trade_date=date(2026, 4, 2), close="10"),
        MarketRowPayload(symbol="BBB", trade_date=date(2026, 4, 3), close="10"),
        MarketRowPayload(symbol="CCC", trade_date=date(2026, 4, 1), close="10"),
        MarketRowPayload(symbol="CCC", trade_date=date(2026, 4, 2), close="9"),
        MarketRowPayload(symbol="CCC", trade_date=date(2026, 4, 3), close="8"),
    ]


def test_openapi_is_accessible_and_contains_phase_g_routes() -> None:
    schema = app.openapi()
    paths = schema["paths"]

    assert "/factors" in paths
    assert "/factors/runs" in paths
    assert "/analysis/reports/{report_id}" in paths
    assert "/trading/accounts/{account_id}" in paths


def test_factor_create_run_and_report_query_flow() -> None:
    store = get_store()

    create_response = asyncio.run(
        create_factor(
            FactorCreateRequest(name="mom_3", expression="RANK(close)", description="phase-g test"),
            store,
        )
    )
    factor_id = create_response.data.factor_id

    run_response = asyncio.run(
        run_factor(
            FactorRunRequest(
                factor_id=factor_id,
                expression="RANK(close)",
                market_rows=_sample_market_rows(),
                group_count=3,
            ),
            store,
        )
    )

    assert run_response.data.status == "SUCCEEDED"

    report_response = asyncio.run(get_report(run_response.data.report_id, store))
    assert report_response.data.report["summary"]["observations"] >= 1


def test_trading_query_routes_return_unified_response_model() -> None:
    store = get_store()

    account_response = asyncio.run(get_account("ACC-001", store))
    assert account_response.code == "OK"
    assert account_response.data.account.account_id == "ACC-001"

    positions_response = asyncio.run(get_positions("ACC-001", store))
    assert positions_response.code == "OK"
    assert isinstance(positions_response.data.positions, list)

    orders_response = asyncio.run(get_orders("ACC-001", store))
    assert orders_response.code == "OK"
    assert isinstance(orders_response.data.orders, list)
