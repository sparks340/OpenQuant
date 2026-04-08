"""Validation result model."""

from pydantic import Field

from packages.core.core.models.base import CoreModel


class ValidationResult(CoreModel):
    is_valid: bool
    errors: list[str] = Field(default_factory=list)
