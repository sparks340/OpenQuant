"""Factor version entity."""

from datetime import datetime, timezone

from pydantic import Field, ValidationInfo, field_validator

from packages.core.core.exceptions.domain import InvariantViolationError
from packages.core.core.models.base import CoreModel


class FactorVersion(CoreModel):
    factor_version_id: str
    factor_id: str
    version: int = Field(ge=1)
    code_snapshot: str
    created_at: datetime = Field(default_factory=lambda: datetime.now(tz=timezone.utc))

    @field_validator("factor_version_id", "factor_id", "code_snapshot")
    @classmethod
    def validate_non_empty(cls, value: str, info: ValidationInfo) -> str:
        if not value:
            raise InvariantViolationError(f"{info.field_name} cannot be empty")
        return value
