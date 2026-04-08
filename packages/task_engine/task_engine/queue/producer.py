"""In-memory producer for phase H task queue."""

from __future__ import annotations

from dataclasses import dataclass
from queue import SimpleQueue


@dataclass(slots=True)
class TaskMessage:
    task_id: str
    task_type: str
    payload: dict


class InMemoryTaskQueue:
    """Simple process-local FIFO queue for task dispatch/consume."""

    def __init__(self) -> None:
        self._queue: SimpleQueue[TaskMessage] = SimpleQueue()

    def publish(self, message: TaskMessage) -> None:
        self._queue.put(message)

    def consume(self) -> TaskMessage | None:
        if self._queue.empty():
            return None
        return self._queue.get()
