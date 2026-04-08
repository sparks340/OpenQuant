"""Task repository contracts and in-memory implementation."""

from __future__ import annotations

from abc import ABC, abstractmethod
from copy import deepcopy

from packages.domain.domain.platform.entities.task_record import TaskRecord


class TaskRepository(ABC):
    @abstractmethod
    def save(self, task: TaskRecord) -> TaskRecord: ...

    @abstractmethod
    def get(self, task_id: str) -> TaskRecord | None: ...


class InMemoryTaskRepository(TaskRepository):
    def __init__(self) -> None:
        self._tasks: dict[str, TaskRecord] = {}

    def save(self, task: TaskRecord) -> TaskRecord:
        self._tasks[task.task_id] = task
        return task

    def get(self, task_id: str) -> TaskRecord | None:
        return self._tasks.get(task_id)

    def snapshot(self) -> dict[str, TaskRecord]:
        return deepcopy(self._tasks)

    def restore(self, state: dict[str, TaskRecord]) -> None:
        self._tasks = deepcopy(state)
