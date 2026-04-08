"""Analysis report aggregate for factor runs."""

from datetime import datetime, timezone
from decimal import Decimal

from pydantic import Field

from packages.core.core.exceptions.domain import InvariantViolationError
from packages.core.core.models.base import CoreModel


class AnalysisReport(CoreModel):
    report_id: str
    run_id: str
    generated_at: datetime = Field(default_factory=lambda: datetime.now(tz=timezone.utc))
    metrics: dict[str, Decimal]

    def metric(self, key: str) -> Decimal:
        if key not in self.metrics:
            raise InvariantViolationError(f"Metric not found: {key}")
        return self.metrics[key]
