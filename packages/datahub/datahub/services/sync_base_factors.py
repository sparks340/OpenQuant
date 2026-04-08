"""Service: sync base factors from adapter to repository."""

from packages.datahub.datahub.adapters.base import DataSourceAdapter
from packages.datahub.datahub.cleaners.base_factor_cleaner import clean_base_factor_rows
from packages.datastore.datastore.repositories.factor_repository import FactorRepository
from packages.domain.domain.research.entities.factor_definition import FactorDefinition


def sync_base_factors(adapter: DataSourceAdapter, repository: FactorRepository, owner_id: str) -> int:
    rows = adapter.fetch_base_factor_rows()
    cleaned = clean_base_factor_rows(rows)
    for row in cleaned:
        repository.save(
            FactorDefinition(
                factor_id=row["factor_id"],
                name=row["name"],
                code=row["code"],
                code_type="formula",
                owner_id=owner_id,
            )
        )
    return len(cleaned)
