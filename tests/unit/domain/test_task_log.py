from datetime import datetime, timezone

import pytest

from packages.core.core.exceptions.domain import InvariantViolationError
from packages.domain.domain.platform.entities.task_log import TaskLog, TaskLogLevel


def test_task_log_defaults_created_at_and_normalizes_level() -> None:
    log = TaskLog(task_id="task-1", sequence=1, level="info", message="started")

    assert isinstance(log.created_at, datetime)
    assert log.created_at.tzinfo == timezone.utc
    assert log.level == TaskLogLevel.INFO


def test_task_log_rejects_empty_identity_or_message() -> None:
    with pytest.raises(InvariantViolationError, match="task_id"):
        TaskLog(task_id="", sequence=1, level="INFO", message="ok")

    with pytest.raises(InvariantViolationError, match="message"):
        TaskLog(task_id="task-2", sequence=1, level="INFO", message="   ")


def test_task_log_rejects_non_positive_sequence() -> None:
    with pytest.raises(InvariantViolationError, match="sequence"):
        TaskLog(task_id="task-3", sequence=0, level="INFO", message="ok")
