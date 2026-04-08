"""Public factor executor service."""

from packages.factor_engine.factor_engine.models.factor_frame import FactorFrame
from packages.factor_engine.factor_engine.runtime.formula_executor import FormulaExecutor
from packages.factor_engine.factor_engine.runtime.python_executor import PythonExecutor


class FactorExecutorService:
    @staticmethod
    def execute_formula(expression: str, market_rows: list[dict]) -> FactorFrame:
        return FormulaExecutor.execute(expression, market_rows)

    @staticmethod
    def validate_python(code: str) -> bool:
        return PythonExecutor.validate(code).is_valid
