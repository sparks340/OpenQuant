"""Task record entity used by the task system."""

from pydantic import BaseModel, Field

from packages.core.core.enums.task import TaskStatus


class TaskRecord(BaseModel):
    """Track a task from dispatch to final status."""

    task_id: str = Field(..., description="Unique task identifier.")
    task_type: str = Field(..., description="Task category, such as factor_run.")
    status: TaskStatus = Field(default=TaskStatus.PENDING, description="Current lifecycle status.")

