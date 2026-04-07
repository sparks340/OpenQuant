"""Domain-layer exceptions."""

from packages.core.core.exceptions.base import OpenQuantError


class DomainError(OpenQuantError):
    """Raised when a domain invariant or business rule is violated."""

    code = "OQ-DOMAIN"


class InvariantViolationError(DomainError):
    """Raised when entity/value-object invariant validation fails."""

    code = "OQ-DOMAIN-INVARIANT"
