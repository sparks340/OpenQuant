"""Platform task domain service."""

from packages.domain.domain.platform.entities.task_log import TaskLog, TaskLogLevel
from packages.domain.domain.platform.entities.task_record import TaskRecord


class TaskService:
    """Factory helpers for task records and timeline logs."""

    @staticmethod
    def create_task(task_id: str, task_type: str) -> TaskRecord:
        return TaskRecord(task_id=task_id, task_type=task_type)

    @staticmethod
    def append_log(record: TaskRecord, message: str, sequence: int, level: TaskLogLevel | str) -> TaskLog:
        return TaskLog(task_id=record.task_id, sequence=sequence, level=level, message=message)
