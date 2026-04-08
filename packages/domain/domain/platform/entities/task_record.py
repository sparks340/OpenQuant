"""Task record entity used by the task system."""

from __future__ import annotations

from datetime import datetime, timezone

from pydantic import Field, ValidationInfo, field_validator, model_validator

from packages.core.core.enums.task import TaskStatus
from packages.core.core.exceptions.domain import InvariantViolationError
from packages.core.core.models.base import CoreModel

_VALID_TRANSITIONS: dict[TaskStatus, set[TaskStatus]] = {
    TaskStatus.PENDING: {TaskStatus.RUNNING, TaskStatus.FAILED},
    TaskStatus.RUNNING: {TaskStatus.SUCCESS, TaskStatus.FAILED},
    TaskStatus.SUCCESS: set(),
    TaskStatus.FAILED: set(),
}


class TaskRecord(CoreModel):
    """Track a task from dispatch to final status."""

    task_id: str
    task_type: str
    status: TaskStatus = TaskStatus.PENDING
    created_at: datetime = Field(default_factory=lambda: datetime.now(tz=timezone.utc))
    started_at: datetime | None = None
    finished_at: datetime | None = None
    error_message: str | None = None

    @field_validator("task_id", "task_type")
    @classmethod
    def validate_identity_fields(cls, value: str, info: ValidationInfo) -> str:
        if not value:
            raise InvariantViolationError(f"{info.field_name} cannot be empty")
        return value

    @model_validator(mode="after")
    def validate_lifecycle_fields(self) -> "TaskRecord":
        if self.status in {TaskStatus.RUNNING, TaskStatus.SUCCESS, TaskStatus.FAILED}:
            if self.started_at is None:
                raise InvariantViolationError("Running/finished task must include started_at")
        if self.status in {TaskStatus.SUCCESS, TaskStatus.FAILED} and self.finished_at is None:
            raise InvariantViolationError("Finished task must include finished_at")
        if self.status == TaskStatus.FAILED and not self.error_message:
            raise InvariantViolationError("Failed task must include error_message")
        if self.status == TaskStatus.SUCCESS and self.error_message:
            raise InvariantViolationError("Succeeded task cannot include error_message")
        if self.finished_at and self.started_at and self.finished_at < self.started_at:
            raise InvariantViolationError("finished_at must be later than started_at")
        return self

    def transition_to(self, target_status: TaskStatus, error_message: str | None = None) -> None:
        """Apply lifecycle transition and update timestamps consistently."""
        if target_status not in _VALID_TRANSITIONS[self.status]:
            raise InvariantViolationError(f"Invalid task transition: {self.status} -> {target_status}")
        if target_status == TaskStatus.FAILED and not error_message:
            raise InvariantViolationError("FAILED transition requires explicit error_message")

        now = datetime.now(tz=timezone.utc)

        self.status = target_status
        if target_status == TaskStatus.RUNNING:
            self.started_at = now
        if target_status == TaskStatus.FAILED and self.started_at is None:
            self.started_at = now
        if target_status in {TaskStatus.SUCCESS, TaskStatus.FAILED}:
            self.finished_at = now

        if target_status == TaskStatus.FAILED:
            self.error_message = error_message
        if target_status == TaskStatus.SUCCESS:
            self.error_message = None
