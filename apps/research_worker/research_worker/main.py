"""Research worker entrypoint."""

from __future__ import annotations

from apps.research_worker.research_worker.jobs.run_backtest_job import run_backtest_job
from apps.research_worker.research_worker.jobs.run_factor_job import run_factor_job
from packages.core.core.enums.task import TaskStatus
from packages.task_engine.task_engine.queue.consumer import TaskConsumer
from packages.task_engine.task_engine.queue.producer import InMemoryTaskQueue
from packages.task_engine.task_engine.trackers.log_tracker import InMemoryLogTracker
from packages.task_engine.task_engine.trackers.task_tracker import InMemoryTaskTracker


class ResearchWorker:
    """Consume queued research tasks and update lifecycle status/logs."""

    def __init__(
        self,
        *,
        task_tracker: InMemoryTaskTracker,
        log_tracker: InMemoryLogTracker,
        queue: InMemoryTaskQueue,
    ) -> None:
        self.task_tracker = task_tracker
        self.log_tracker = log_tracker
        self.consumer = TaskConsumer(queue)

    def consume_once(self) -> bool:
        message = self.consumer.pull()
        if message is None:
            return False

        self.task_tracker.transition(message.task_id, TaskStatus.RUNNING)
        self.log_tracker.append(message.task_id, "task running")
        try:
            self._execute(message.task_type, message.payload)
            self.task_tracker.transition(message.task_id, TaskStatus.SUCCESS)
            self.log_tracker.append(message.task_id, "task succeeded")
        except Exception as exc:  # noqa: BLE001
            self.task_tracker.transition(message.task_id, TaskStatus.FAILED, error_message=str(exc))
            self.log_tracker.append(message.task_id, f"task failed: {exc}", level="ERROR")
        return True

    @staticmethod
    def _execute(task_type: str, payload: dict) -> dict:
        if task_type == "RUN_FACTOR":
            return run_factor_job(payload)
        if task_type == "RUN_BACKTEST":
            return run_backtest_job(payload)
        raise ValueError(f"unsupported task_type: {task_type}")


def main() -> None:
    """Start research worker bootstrap."""
    print("research_worker started")


if __name__ == "__main__":
    main()
