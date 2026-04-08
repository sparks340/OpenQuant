"""Domain helpers for factor definitions and versions."""

from packages.domain.domain.research.entities.factor_definition import FactorDefinition
from packages.domain.domain.research.entities.factor_version import FactorVersion


class FactorDomainService:
    """Build factor versions from factor definitions."""

    @staticmethod
    def create_version(
        definition: FactorDefinition,
        code_snapshot: str,
        existing_versions: list[FactorVersion],
    ) -> FactorVersion:
        next_version = max((v.version for v in existing_versions), default=0) + 1
        return FactorVersion(
            factor_version_id=f"{definition.factor_id}-v{next_version}",
            factor_id=definition.factor_id,
            version=next_version,
            code_snapshot=code_snapshot,
        )
