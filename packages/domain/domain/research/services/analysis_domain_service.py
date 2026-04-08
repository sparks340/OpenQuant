"""Analysis domain service."""

from decimal import Decimal

from packages.core.core.exceptions.domain import InvariantViolationError


class AnalysisDomainService:
    """Build deterministic summary metrics for MVP."""

    @staticmethod
    def summarize_ic(values: list[Decimal]) -> dict[str, Decimal]:
        if not values:
            raise InvariantViolationError("values cannot be empty")
        return {"ic_mean": sum(values) / Decimal(len(values))}
