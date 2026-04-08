"""Trading query APIs."""

from fastapi import APIRouter, Depends

from apps.api_service.api_service.deps import get_store
from apps.api_service.api_service.schemas.common import ApiResponse
from apps.api_service.api_service.schemas.trading import (
    AccountData,
    AccountQueryData,
    OrdersQueryData,
    PositionsQueryData,
)
from apps.api_service.api_service.services.orchestration import InMemoryOrchestrationStore

router = APIRouter()


@router.get("/accounts/{account_id}", response_model=ApiResponse[AccountQueryData])
async def get_account(
    account_id: str,
    store: InMemoryOrchestrationStore = Depends(get_store),
) -> ApiResponse[AccountQueryData]:
    account = AccountData(**store.get_account(account_id))
    return ApiResponse(data=AccountQueryData(account=account))


@router.get("/positions", response_model=ApiResponse[PositionsQueryData])
async def get_positions(
    account_id: str,
    store: InMemoryOrchestrationStore = Depends(get_store),
) -> ApiResponse[PositionsQueryData]:
    return ApiResponse(data=PositionsQueryData(account_id=account_id, positions=store.get_positions(account_id)))


@router.get("/orders", response_model=ApiResponse[OrdersQueryData])
async def get_orders(
    account_id: str,
    store: InMemoryOrchestrationStore = Depends(get_store),
) -> ApiResponse[OrdersQueryData]:
    return ApiResponse(data=OrdersQueryData(account_id=account_id, orders=store.get_orders(account_id)))
