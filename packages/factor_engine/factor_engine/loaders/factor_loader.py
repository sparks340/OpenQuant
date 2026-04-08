"""Factor loader utility."""

from packages.domain.domain.research.entities.factor_definition import FactorDefinition


def load_factor_source(factor: FactorDefinition) -> str:
    return factor.code
