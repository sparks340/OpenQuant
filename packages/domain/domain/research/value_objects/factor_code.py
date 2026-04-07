"""Factor source code value object."""

from __future__ import annotations

from enum import StrEnum

from pydantic import field_validator

from packages.core.core.exceptions.domain import InvariantViolationError
from packages.core.core.models.base import CoreModel


class FactorCodeMode(StrEnum):
    """Factor implementation style."""

    FORMULA = "FORMULA"
    PYTHON = "PYTHON"


class FactorCode(CoreModel):
    """A validated factor code payload."""

    mode: FactorCodeMode
    source: str

    @field_validator("source")
    @classmethod
    def validate_source(cls, value: str) -> str:
        source = value.strip()
        if not source:
            raise InvariantViolationError("Factor code source cannot be empty")
        return source
