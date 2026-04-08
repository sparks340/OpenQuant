"""Analysis report query APIs."""

from fastapi import APIRouter, Depends, HTTPException

from apps.api_service.api_service.deps import get_store
from apps.api_service.api_service.schemas.analysis import ReportQueryData
from apps.api_service.api_service.schemas.common import ApiResponse
from apps.api_service.api_service.services.orchestration import InMemoryOrchestrationStore

router = APIRouter()


@router.get("/reports/{report_id}", response_model=ApiResponse[ReportQueryData])
async def get_report(
    report_id: str,
    store: InMemoryOrchestrationStore = Depends(get_store),
) -> ApiResponse[ReportQueryData]:
    report = store.get_report(report_id)
    if report is None:
        raise HTTPException(status_code=404, detail=f"report not found: {report_id}")
    return ApiResponse(data=ReportQueryData(report_id=report_id, report=report))
