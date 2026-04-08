"""Strategy version entity with lifecycle transitions."""

from enum import StrEnum

from pydantic import Field

from packages.core.core.exceptions.domain import InvariantViolationError
from packages.core.core.models.base import CoreModel


class StrategyLifecycleStatus(StrEnum):
    DRAFT = "DRAFT"
    ACTIVE = "ACTIVE"
    ARCHIVED = "ARCHIVED"


_VALID_TRANSITIONS: dict[StrategyLifecycleStatus, set[StrategyLifecycleStatus]] = {
    StrategyLifecycleStatus.DRAFT: {StrategyLifecycleStatus.ACTIVE, StrategyLifecycleStatus.ARCHIVED},
    StrategyLifecycleStatus.ACTIVE: {StrategyLifecycleStatus.ARCHIVED},
    StrategyLifecycleStatus.ARCHIVED: set(),
}


class StrategyVersion(CoreModel):
    strategy_version_id: str
    strategy_id: str
    version: int = Field(ge=1)
    status: StrategyLifecycleStatus = StrategyLifecycleStatus.DRAFT

    def transition_to(self, target_status: StrategyLifecycleStatus) -> None:
        if target_status not in _VALID_TRANSITIONS[self.status]:
            raise InvariantViolationError(
                f"Invalid strategy version transition: {self.status} -> {target_status}"
            )
        self.status = target_status
