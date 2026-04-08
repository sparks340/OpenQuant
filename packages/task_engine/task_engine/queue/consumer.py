"""Consumer wrapper for phase H queue."""

from __future__ import annotations

from packages.task_engine.task_engine.queue.producer import InMemoryTaskQueue, TaskMessage


class TaskConsumer:
    def __init__(self, queue: InMemoryTaskQueue) -> None:
        self._queue = queue

    def pull(self) -> TaskMessage | None:
        return self._queue.consume()
