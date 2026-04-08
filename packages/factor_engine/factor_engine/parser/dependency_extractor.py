"""Dependency extraction for formula expressions."""

from packages.factor_engine.factor_engine.parser.formula_parser import parse_formula


def extract_dependencies(expression: str) -> list[str]:
    _, field, _ = parse_formula(expression)
    return [field]
