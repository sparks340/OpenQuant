"""FastAPI application entrypoint for OpenQuant API service."""

from fastapi import FastAPI

from apps.api_service.api_service.routers.analysis import router as analysis_router
from apps.api_service.api_service.routers.factors import router as factors_router
from apps.api_service.api_service.routers.health import router as health_router
from apps.api_service.api_service.routers.trading import router as trading_router

app = FastAPI(
    title="OpenQuant API Service",
    version="0.3.0",
    description="HTTP gateway for research, strategy, trading, and task workflows.",
)

app.include_router(health_router, prefix="/health", tags=["health"])
app.include_router(factors_router, prefix="/factors", tags=["factors"])
app.include_router(analysis_router, prefix="/analysis", tags=["analysis"])
app.include_router(trading_router, prefix="/trading", tags=["trading"])


@app.get("/")
async def root() -> dict[str, str]:
    """Basic smoke-check endpoint."""
    return {"message": "openquant api_service is running"}
