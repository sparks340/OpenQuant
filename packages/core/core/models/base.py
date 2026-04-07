"""Common base model helpers."""

from pydantic import BaseModel, ConfigDict


class CoreModel(BaseModel):
    """Base model with consistent serialization behavior."""

    model_config = ConfigDict(extra="forbid", populate_by_name=True, str_strip_whitespace=True)
