"""Common API response model."""

from pydantic import BaseModel


class ApiResponse(BaseModel):
    """Uniform response envelope for simple service endpoints."""

    code: str = "200"
    message: str = "ok"

