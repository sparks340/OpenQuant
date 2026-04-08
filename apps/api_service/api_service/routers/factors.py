"""Factor APIs (orchestration only)."""

from fastapi import APIRouter, Depends, status

from apps.api_service.api_service.deps import get_store
from apps.api_service.api_service.schemas.common import ApiResponse
from apps.api_service.api_service.schemas.factor import (
    FactorCreateData,
    FactorCreateRequest,
    FactorRunData,
    FactorRunRequest,
)
from apps.api_service.api_service.services.orchestration import InMemoryOrchestrationStore, normalize_market_rows

router = APIRouter()


@router.post("", response_model=ApiResponse[FactorCreateData], status_code=status.HTTP_201_CREATED)
async def create_factor(
    payload: FactorCreateRequest,
    store: InMemoryOrchestrationStore = Depends(get_store),
) -> ApiResponse[FactorCreateData]:
    factor = store.create_factor(name=payload.name, expression=payload.expression, description=payload.description)
    return ApiResponse(data=FactorCreateData(**factor))


@router.post("/runs", response_model=ApiResponse[FactorRunData])
async def run_factor(
    payload: FactorRunRequest,
    store: InMemoryOrchestrationStore = Depends(get_store),
) -> ApiResponse[FactorRunData]:
    market_rows = normalize_market_rows([row.model_dump() for row in payload.market_rows])
    run = store.run_factor(
        factor_id=payload.factor_id,
        expression=payload.expression,
        market_rows=market_rows,
        group_count=payload.group_count,
    )
    return ApiResponse(data=FactorRunData(**run))
