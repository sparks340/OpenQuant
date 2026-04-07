"""Task dispatcher placeholder.

The dispatcher will later publish jobs to Celery, Redis queues, or another task
backend. Starting with a dedicated module keeps orchestration code centralized.
"""

from packages.core.core.logging.logger import get_logger
from packages.domain.domain.platform.entities.task_record import TaskRecord


logger = get_logger(__name__)


class TaskDispatcher:
    """Dispatch tasks to background workers."""

    def dispatch(self, task: TaskRecord) -> TaskRecord:
        """Log the dispatch and return the task unchanged in phase 1."""
        logger.info("dispatching task %s of type %s", task.task_id, task.task_type)
        return task

