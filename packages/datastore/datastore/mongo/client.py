"""In-memory Mongo client manager used for tests and local development wiring."""

from __future__ import annotations

from copy import deepcopy
from dataclasses import dataclass, field


@dataclass
class InMemoryMongoCollection:
    """Minimal Mongo-like collection API."""

    docs: list[dict] = field(default_factory=list)
    indexes: list[tuple[str, int]] = field(default_factory=list)

    def insert_one(self, document: dict) -> None:
        self.docs.append(deepcopy(document))

    def find_one(self, query: dict) -> dict | None:
        return next((deepcopy(doc) for doc in self.docs if _matches(doc, query)), None)

    def find(self, query: dict) -> list[dict]:
        return [deepcopy(doc) for doc in self.docs if _matches(doc, query)]

    def update_one(self, query: dict, update: dict, upsert: bool = False) -> None:
        for idx, doc in enumerate(self.docs):
            if _matches(doc, query):
                if "$set" in update:
                    doc.update(update["$set"])
                    self.docs[idx] = doc
                    return
        if upsert:
            new_doc = deepcopy(query)
            if "$set" in update:
                new_doc.update(update["$set"])
            self.docs.append(new_doc)

    def create_index(self, spec: tuple[str, int]) -> None:
        if spec not in self.indexes:
            self.indexes.append(spec)


class MongoClientManager:
    """Simple manager that provides named in-memory collections."""

    def __init__(self) -> None:
        self._collections: dict[str, InMemoryMongoCollection] = {}

    def get_collection(self, name: str) -> InMemoryMongoCollection:
        if name not in self._collections:
            self._collections[name] = InMemoryMongoCollection()
        return self._collections[name]


def _matches(document: dict, query: dict) -> bool:
    for key, expected in query.items():
        value = document.get(key)
        if isinstance(expected, dict):
            gte = expected.get("$gte")
            lte = expected.get("$lte")
            if gte is not None and value < gte:
                return False
            if lte is not None and value > lte:
                return False
        elif value != expected:
            return False
    return True
