"""Task dispatcher for phase H MVP."""

from __future__ import annotations

from itertools import count

from packages.core.core.logging.logger import get_logger
from packages.domain.domain.platform.entities.task_record import TaskRecord
from packages.task_engine.task_engine.queue.producer import InMemoryTaskQueue, TaskMessage
from packages.task_engine.task_engine.trackers.log_tracker import InMemoryLogTracker
from packages.task_engine.task_engine.trackers.task_tracker import InMemoryTaskTracker

logger = get_logger(__name__)


class TaskDispatcher:
    """Dispatch tasks to in-memory queue and record task state/logs."""

    def __init__(
        self,
        *,
        task_tracker: InMemoryTaskTracker,
        log_tracker: InMemoryLogTracker,
        queue: InMemoryTaskQueue | None = None,
    ) -> None:
        self.task_tracker = task_tracker
        self.log_tracker = log_tracker
        self.queue = queue or InMemoryTaskQueue()
        self._seq = count(start=1)

    def dispatch(self, *, task_type: str, payload: dict) -> TaskRecord:
        task_id = f"TASK-{next(self._seq):06d}"
        record = self.task_tracker.create(task_id=task_id, task_type=task_type)
        self.queue.publish(TaskMessage(task_id=task_id, task_type=task_type, payload=payload))
        self.log_tracker.append(task_id, f"task dispatched: {task_type}")
        logger.info("dispatched task %s type=%s", task_id, task_type)
        return record
