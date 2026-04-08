"""In-memory task status tracker."""

from __future__ import annotations

from collections import defaultdict

from packages.core.core.enums.task import TaskStatus
from packages.domain.domain.platform.entities.task_record import TaskRecord


class InMemoryTaskTracker:
    def __init__(self) -> None:
        self._records: dict[str, TaskRecord] = {}
        self._status_history: dict[str, list[TaskStatus]] = defaultdict(list)

    def create(self, task_id: str, task_type: str) -> TaskRecord:
        record = TaskRecord(task_id=task_id, task_type=task_type)
        self._records[task_id] = record
        self._status_history[task_id].append(record.status)
        return record

    def get(self, task_id: str) -> TaskRecord:
        return self._records[task_id]

    def transition(self, task_id: str, target: TaskStatus, *, error_message: str | None = None) -> TaskRecord:
        record = self._records[task_id]
        record.transition_to(target, error_message=error_message)
        self._status_history[task_id].append(record.status)
        return record

    def get_status_history(self, task_id: str) -> list[TaskStatus]:
        return list(self._status_history.get(task_id, []))
