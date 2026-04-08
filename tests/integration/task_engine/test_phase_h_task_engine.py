from packages.core.core.enums.task import TaskStatus
from packages.task_engine.task_engine.services.task_dispatcher import TaskDispatcher
from packages.task_engine.task_engine.trackers.log_tracker import InMemoryLogTracker
from packages.task_engine.task_engine.trackers.task_tracker import InMemoryTaskTracker
from apps.research_worker.research_worker.main import ResearchWorker


def test_task_submit_and_success_status_flow_is_observable() -> None:
    tracker = InMemoryTaskTracker()
    logs = InMemoryLogTracker()
    dispatcher = TaskDispatcher(task_tracker=tracker, log_tracker=logs)
    worker = ResearchWorker(task_tracker=tracker, log_tracker=logs, queue=dispatcher.queue)

    record = dispatcher.dispatch(task_type="RUN_FACTOR", payload={"factor_id": "FAC-0001"})

    assert tracker.get(record.task_id).status == TaskStatus.PENDING

    handled = worker.consume_once()
    assert handled is True

    updated = tracker.get(record.task_id)
    assert updated.status == TaskStatus.SUCCESS
    assert tracker.get_status_history(record.task_id) == [
        TaskStatus.PENDING,
        TaskStatus.RUNNING,
        TaskStatus.SUCCESS,
    ]


def test_task_failure_status_flow_is_observable() -> None:
    tracker = InMemoryTaskTracker()
    logs = InMemoryLogTracker()
    dispatcher = TaskDispatcher(task_tracker=tracker, log_tracker=logs)
    worker = ResearchWorker(task_tracker=tracker, log_tracker=logs, queue=dispatcher.queue)

    record = dispatcher.dispatch(task_type="RUN_BACKTEST", payload={"should_fail": True})
    handled = worker.consume_once()

    assert handled is True
    failed = tracker.get(record.task_id)
    assert failed.status == TaskStatus.FAILED
    assert failed.error_message == "backtest job failed by payload flag"
    assert tracker.get_status_history(record.task_id) == [
        TaskStatus.PENDING,
        TaskStatus.RUNNING,
        TaskStatus.FAILED,
    ]

    timeline = logs.list_by_task(record.task_id)
    assert len(timeline) >= 2
    assert timeline[-1].level.value == "ERROR"
