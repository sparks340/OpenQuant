"""Python-mode executor stub for MVP stage."""

from packages.factor_engine.factor_engine.models.validation_result import ValidationResult


class PythonExecutor:
    @staticmethod
    def validate(code: str) -> ValidationResult:
        if not code.strip():
            return ValidationResult(is_valid=False, errors=["Python factor code cannot be empty"])
        return ValidationResult(is_valid=True, errors=[])
