"""Factor definition entity.

This model describes what a user writes, not the result of a factor run.
Keeping these separate is one of the first intentional improvements over the
old codebase design.
"""

from pydantic import BaseModel, Field


class FactorDefinition(BaseModel):
    """User-authored factor source definition."""

    factor_id: str = Field(..., description="Stable factor identifier.")
    name: str = Field(..., description="Display name of the factor.")
    code: str = Field(..., description="Formula or Python source code.")
    code_type: str = Field(..., description="Either formula or python.")
    owner_id: str = Field(..., description="User id that owns the factor.")

