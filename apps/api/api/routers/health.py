"""Health endpoints used by local development and deployment checks."""

from fastapi import APIRouter


router = APIRouter()


@router.get("/health")
async def health() -> dict[str, str]:
    """Return a stable health payload for probes and quick local checks."""
    return {"status": "ok"}

