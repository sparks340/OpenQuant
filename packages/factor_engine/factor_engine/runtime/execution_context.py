"""Execution context model for factor runtime."""

from packages.core.core.models.base import CoreModel


class ExecutionContext(CoreModel):
    factor_id: str
    run_id: str
