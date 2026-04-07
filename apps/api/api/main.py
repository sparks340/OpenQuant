"""FastAPI application entrypoint.

This service only exposes HTTP endpoints and delegates real work to domain
services and task dispatchers. Keeping this file thin helps us avoid turning
the API service into a god module later.
"""

from fastapi import FastAPI

from apps.api.api.routers.health import router as health_router


app = FastAPI(
    title="OpenQuant API",
    version="0.1.0",
    description="Unified API for research, strategy, and trading workflows.",
)

app.include_router(health_router, tags=["health"])


@app.get("/")
async def root() -> dict[str, str]:
    """Return a tiny root payload so deployments have a simple smoke test."""
    return {"message": "openquant api is running"}
