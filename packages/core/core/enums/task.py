"""Task status enum used across workers and APIs."""

from enum import StrEnum


class TaskStatus(StrEnum):
    """Canonical task lifecycle states for the rebuilt platform."""

    PENDING = "PENDING"
    RUNNING = "RUNNING"
    SUCCESS = "SUCCESS"
    FAILED = "FAILED"

