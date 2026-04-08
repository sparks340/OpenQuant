"""Simple formula parser for MVP operators."""

from __future__ import annotations

import re

_PATTERN = re.compile(r"^(?P<op>[A-Z_]+)\((?P<field>[a-z_]+)(,(?P<arg>\d+))?\)$")


def parse_formula(expression: str) -> tuple[str, str, int | None]:
    match = _PATTERN.fullmatch(expression.strip())
    if not match:
        raise ValueError(f"Invalid formula expression: {expression}")
    op = match.group("op")
    field = match.group("field")
    arg = match.group("arg")
    return op, field, int(arg) if arg is not None else None
