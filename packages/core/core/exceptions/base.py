"""Base exception hierarchy used across all layers."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any


@dataclass(slots=True)
class ErrorContext:
    """Structured context attached to errors for logs and API responses."""

    operation: str | None = None
    resource: str | None = None


class OpenQuantError(Exception):
    """Root exception type for the platform."""

    code = "OQ-0000"

    def __init__(
        self,
        message: str,
        *,
        code: str | None = None,
        details: dict[str, Any] | None = None,
        context: ErrorContext | None = None,
    ) -> None:
        super().__init__(message)
        self.message = message
        self.error_code = code or self.code
        self.details = details or {}
        self.context = context

    def to_dict(self) -> dict[str, Any]:
        """Serialize the exception for logs/API transport."""
        payload: dict[str, Any] = {
            "code": self.error_code,
            "message": self.message,
            "details": self.details,
        }
        if self.context:
            payload["context"] = {
                "operation": self.context.operation,
                "resource": self.context.resource,
            }
        return payload
