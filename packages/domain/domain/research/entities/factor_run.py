"""Factor run entity with lifecycle invariants."""

from __future__ import annotations

from datetime import datetime, timezone

from pydantic import model_validator

from packages.core.core.enums.factor import FactorRunStatus
from packages.core.core.exceptions.domain import InvariantViolationError
from packages.core.core.models.base import CoreModel


_VALID_TRANSITIONS: dict[FactorRunStatus, set[FactorRunStatus]] = {
    FactorRunStatus.PENDING: {FactorRunStatus.RUNNING, FactorRunStatus.FAILED},
    FactorRunStatus.RUNNING: {FactorRunStatus.SUCCEEDED, FactorRunStatus.FAILED},
    FactorRunStatus.SUCCEEDED: set(),
    FactorRunStatus.FAILED: set(),
}


class FactorRun(CoreModel):
    """A single factor execution record."""

    run_id: str
    factor_version_id: str
    status: FactorRunStatus = FactorRunStatus.PENDING
    started_at: datetime | None = None
    finished_at: datetime | None = None
    error_message: str | None = None

    @model_validator(mode="after")
    def validate_timestamp_consistency(self) -> "FactorRun":
        if self.status in {FactorRunStatus.RUNNING, FactorRunStatus.SUCCEEDED, FactorRunStatus.FAILED}:
            if self.started_at is None:
                raise InvariantViolationError("Running/finished factor run must include started_at")
        if self.status in {FactorRunStatus.SUCCEEDED, FactorRunStatus.FAILED}:
            if self.finished_at is None:
                raise InvariantViolationError("Finished factor run must include finished_at")
        if self.status == FactorRunStatus.FAILED and not self.error_message:
            raise InvariantViolationError("Failed factor run must include error_message")
        if self.status == FactorRunStatus.SUCCEEDED and self.error_message:
            raise InvariantViolationError("Succeeded factor run cannot include error_message")
        if self.finished_at and self.started_at and self.finished_at < self.started_at:
            raise InvariantViolationError("finished_at must be later than started_at")
        return self

    def transition_to(self, target_status: FactorRunStatus, error_message: str | None = None) -> None:
        """Apply lifecycle transition and materialize timestamps."""
        if target_status not in _VALID_TRANSITIONS[self.status]:
            raise InvariantViolationError(
                f"Invalid factor run transition: {self.status} -> {target_status}"
            )
        if target_status == FactorRunStatus.FAILED and not error_message:
            raise InvariantViolationError("FAILED transition requires explicit error_message")

        now = datetime.now(tz=timezone.utc)
        self.status = target_status
        if target_status == FactorRunStatus.RUNNING:
            self.started_at = now
        if target_status == FactorRunStatus.FAILED and self.started_at is None:
            self.started_at = now
        if target_status in {FactorRunStatus.SUCCEEDED, FactorRunStatus.FAILED}:
            self.finished_at = now
        if target_status == FactorRunStatus.FAILED:
            self.error_message = error_message
        if target_status == FactorRunStatus.SUCCEEDED:
            self.error_message = None
