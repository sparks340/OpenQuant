"""Infrastructure-layer exceptions."""

from packages.core.core.exceptions.base import OpenQuantError


class InfrastructureError(OpenQuantError):
    """Raised when external systems fail (DB, MQ, APIs, etc.)."""

    code = "OQ-INFRA"


class RepositoryError(InfrastructureError):
    """Raised when repository operations fail."""

    code = "OQ-INFRA-REPOSITORY"
