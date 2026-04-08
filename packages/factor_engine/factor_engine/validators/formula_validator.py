"""Formula validator for MVP operators."""

from packages.factor_engine.factor_engine.models.validation_result import ValidationResult
from packages.factor_engine.factor_engine.operators.core import SUPPORTED_OPERATORS
from packages.factor_engine.factor_engine.parser.formula_parser import parse_formula
from packages.factor_engine.factor_engine.validators.safety_validator import is_safe_expression


class FormulaValidator:
    @staticmethod
    def validate(expression: str) -> ValidationResult:
        if not is_safe_expression(expression):
            return ValidationResult(is_valid=False, errors=["Unsafe expression"])

        try:
            op, _, arg = parse_formula(expression)
        except ValueError as exc:
            return ValidationResult(is_valid=False, errors=[str(exc)])

        if op not in SUPPORTED_OPERATORS:
            return ValidationResult(is_valid=False, errors=[f"Unsupported operator: {op}"])
        if op in {"DELAY", "TS_MEAN"} and (arg is None or arg <= 0):
            return ValidationResult(is_valid=False, errors=[f"{op} requires positive integer arg"])
        return ValidationResult(is_valid=True, errors=[])
