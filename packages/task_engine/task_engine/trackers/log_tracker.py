"""In-memory task log tracker."""

from __future__ import annotations

from collections import defaultdict

from packages.domain.domain.platform.entities.task_log import TaskLog, TaskLogLevel


class InMemoryLogTracker:
    def __init__(self) -> None:
        self._logs: dict[str, list[TaskLog]] = defaultdict(list)

    def append(self, task_id: str, message: str, *, level: TaskLogLevel = TaskLogLevel.INFO) -> TaskLog:
        sequence = len(self._logs[task_id]) + 1
        log = TaskLog(task_id=task_id, sequence=sequence, level=level, message=message)
        self._logs[task_id].append(log)
        return log

    def list_by_task(self, task_id: str) -> list[TaskLog]:
        return list(self._logs.get(task_id, []))
