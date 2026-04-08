"""In-memory Redis-like client used for local tests."""


class RedisClientManager:
    """Tiny key-value API subset for cache/state tests."""

    def __init__(self) -> None:
        self._store: dict[str, str] = {}

    def set(self, key: str, value: str) -> None:
        self._store[key] = value

    def get(self, key: str) -> str | None:
        return self._store.get(key)

    def delete(self, key: str) -> None:
        self._store.pop(key, None)
