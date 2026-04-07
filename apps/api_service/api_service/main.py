"""FastAPI application entrypoint for OpenQuant API service."""

from fastapi import FastAPI

from apps.api_service.api_service.routers.health import router as health_router

app = FastAPI(
    title="OpenQuant API Service",
    version="0.2.0",
    description="HTTP gateway for research, strategy, trading, and task workflows.",
)

app.include_router(health_router, prefix="/health", tags=["health"])


@app.get("/")
async def root() -> dict[str, str]:
    """Basic smoke-check endpoint."""
    return {"message": "openquant api_service is running"}
