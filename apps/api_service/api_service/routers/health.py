"""Health check router."""

from fastapi import APIRouter

router = APIRouter()


@router.get("")
async def health() -> dict[str, str]:
    """Readiness endpoint."""
    return {"status": "ok"}
