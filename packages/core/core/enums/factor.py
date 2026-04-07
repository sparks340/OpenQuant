"""Factor/research enums shared across packages."""

from enum import StrEnum


class FactorRunStatus(StrEnum):
    """Canonical factor run states."""

    PENDING = "PENDING"
    RUNNING = "RUNNING"
    SUCCEEDED = "SUCCEEDED"
    FAILED = "FAILED"
