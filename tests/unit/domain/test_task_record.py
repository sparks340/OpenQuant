import pytest

from packages.core.core.enums.task import TaskStatus
from packages.core.core.exceptions.domain import InvariantViolationError
from packages.domain.domain.platform.entities.task_record import TaskRecord


def test_task_record_transition_happy_path() -> None:
    record = TaskRecord(task_id="task-1", task_type="factor_run")

    record.transition_to(TaskStatus.RUNNING)
    record.transition_to(TaskStatus.SUCCESS)

    assert record.started_at is not None
    assert record.finished_at is not None
    assert record.error_message is None


def test_task_record_reject_invalid_transition() -> None:
    record = TaskRecord(task_id="task-2", task_type="factor_run")

    with pytest.raises(InvariantViolationError, match="Invalid task transition"):
        record.transition_to(TaskStatus.SUCCESS)


def test_task_record_failed_requires_error_message() -> None:
    record = TaskRecord(task_id="task-3", task_type="factor_run")

    with pytest.raises(InvariantViolationError, match="requires explicit error_message"):
        record.transition_to(TaskStatus.FAILED)


def test_task_record_constructor_rejects_succeeded_with_error_message() -> None:
    with pytest.raises(InvariantViolationError, match="cannot include error_message"):
        TaskRecord(
            task_id="task-4",
            task_type="factor_run",
            status=TaskStatus.SUCCESS,
            started_at="2026-01-01T00:00:00Z",
            finished_at="2026-01-01T00:10:00Z",
            error_message="should be empty",
        )


def test_task_record_sets_created_at_on_construction_and_keeps_it_stable() -> None:
    record = TaskRecord(task_id="task-5", task_type="factor_run")
    created_at = record.created_at

    record.transition_to(TaskStatus.RUNNING)
    record.transition_to(TaskStatus.SUCCESS)

    assert created_at is not None
    assert record.created_at == created_at


def test_task_record_rejects_empty_task_identity_fields() -> None:
    with pytest.raises(InvariantViolationError, match="task_id"):
        TaskRecord(task_id="   ", task_type="factor_run")

    with pytest.raises(InvariantViolationError, match="task_type"):
        TaskRecord(task_id="task-6", task_type="")
