"""Factor repository placeholder.

Repositories will own persistence details so service code does not talk to
MongoDB or Redis directly.
"""

from packages.domain.domain.research.entities.factor_definition import FactorDefinition


class FactorRepository:
    """In-memory placeholder repository for phase 1 scaffolding."""

    def save(self, factor: FactorDefinition) -> FactorDefinition:
        """Return the entity unchanged until the real datastore layer is wired."""
        return factor

