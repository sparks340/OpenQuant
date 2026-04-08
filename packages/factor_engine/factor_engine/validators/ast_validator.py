"""AST-level validation placeholder using parser constraints."""

from packages.factor_engine.factor_engine.parser.formula_parser import parse_formula


def validate_expression_shape(expression: str) -> bool:
    parse_formula(expression)
    return True
