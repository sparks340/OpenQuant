"""Strategy definition entity."""

from pydantic import ValidationInfo, field_validator

from packages.core.core.exceptions.domain import InvariantViolationError
from packages.core.core.models.base import CoreModel


class StrategyDefinition(CoreModel):
    strategy_id: str
    name: str
    owner_id: str

    @field_validator("strategy_id", "name", "owner_id")
    @classmethod
    def validate_non_empty(cls, value: str, info: ValidationInfo) -> str:
        if not value:
            raise InvariantViolationError(f"{info.field_name} cannot be empty")
        return value
