"""Task log entity for per-task timeline events."""

from __future__ import annotations

from datetime import datetime, timezone
from enum import StrEnum

from pydantic import Field, ValidationInfo, field_validator

from packages.core.core.exceptions.domain import InvariantViolationError
from packages.core.core.models.base import CoreModel


class TaskLogLevel(StrEnum):
    """Supported task log severities."""

    INFO = "INFO"
    WARNING = "WARNING"
    ERROR = "ERROR"


class TaskLog(CoreModel):
    """Immutable event generated during task execution."""

    task_id: str
    sequence: int
    level: TaskLogLevel = TaskLogLevel.INFO
    message: str
    created_at: datetime = Field(default_factory=lambda: datetime.now(tz=timezone.utc))

    @field_validator("task_id", "message")
    @classmethod
    def validate_non_empty_text_fields(cls, value: str, info: ValidationInfo) -> str:
        if not value:
            raise InvariantViolationError(f"{info.field_name} cannot be empty")
        return value

    @field_validator("sequence")
    @classmethod
    def validate_sequence(cls, value: int) -> int:
        if value <= 0:
            raise InvariantViolationError("sequence must be positive")
        return value

    @field_validator("level", mode="before")
    @classmethod
    def normalize_level(cls, value: TaskLogLevel | str) -> TaskLogLevel | str:
        if isinstance(value, str):
            return value.upper()
        return value
