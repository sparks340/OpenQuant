"""Chat session entity for assistant interactions."""

from enum import StrEnum

from pydantic import Field, ValidationInfo, field_validator

from packages.core.core.exceptions.domain import InvariantViolationError
from packages.core.core.models.base import CoreModel


class ChatSessionStatus(StrEnum):
    OPEN = "OPEN"
    CLOSED = "CLOSED"


class ChatSession(CoreModel):
    session_id: str
    user_id: str
    title: str
    status: ChatSessionStatus = ChatSessionStatus.OPEN
    message_count: int = Field(default=0, ge=0)

    @field_validator("session_id", "user_id", "title")
    @classmethod
    def validate_non_empty(cls, value: str, info: ValidationInfo) -> str:
        if not value:
            raise InvariantViolationError(f"{info.field_name} cannot be empty")
        return value

    def close(self) -> None:
        self.status = ChatSessionStatus.CLOSED
