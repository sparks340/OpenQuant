"""Dependency providers for api_service."""

from apps.api_service.api_service.services.orchestration import InMemoryOrchestrationStore

_store = InMemoryOrchestrationStore()


def get_store() -> InMemoryOrchestrationStore:
    return _store
