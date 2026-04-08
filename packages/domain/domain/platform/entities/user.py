"""Platform user entity."""

from enum import StrEnum

from pydantic import ValidationInfo, field_validator

from packages.core.core.exceptions.domain import InvariantViolationError
from packages.core.core.models.base import CoreModel


class UserRole(StrEnum):
    ADMIN = "ADMIN"
    RESEARCHER = "RESEARCHER"
    TRADER = "TRADER"


class User(CoreModel):
    user_id: str
    email: str
    role: UserRole = UserRole.RESEARCHER

    @field_validator("user_id", "email")
    @classmethod
    def validate_required_fields(cls, value: str, info: ValidationInfo) -> str:
        if not value:
            raise InvariantViolationError(f"{info.field_name} cannot be empty")
        return value

    @field_validator("email")
    @classmethod
    def validate_email_format(cls, value: str) -> str:
        if "@" not in value:
            raise InvariantViolationError("email must contain @")
        return value.lower()

    @field_validator("role", mode="before")
    @classmethod
    def normalize_role(cls, value: UserRole | str) -> UserRole | str:
        if isinstance(value, str):
            return value.upper()
        return value
