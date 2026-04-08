"""Factor repository contracts and in-memory implementation."""

from __future__ import annotations

from abc import ABC, abstractmethod
from copy import deepcopy

from packages.domain.domain.research.entities.factor_definition import FactorDefinition


class FactorRepository(ABC):
    @abstractmethod
    def save(self, factor: FactorDefinition) -> FactorDefinition: ...

    @abstractmethod
    def get(self, factor_id: str) -> FactorDefinition | None: ...


class InMemoryFactorRepository(FactorRepository):
    def __init__(self) -> None:
        self._factors: dict[str, FactorDefinition] = {}

    def save(self, factor: FactorDefinition) -> FactorDefinition:
        self._factors[factor.factor_id] = factor
        return factor

    def get(self, factor_id: str) -> FactorDefinition | None:
        return self._factors.get(factor_id)

    def snapshot(self) -> dict[str, FactorDefinition]:
        return deepcopy(self._factors)

    def restore(self, state: dict[str, FactorDefinition]) -> None:
        self._factors = deepcopy(state)
