"""Safety validation for user expressions."""

BLOCKED_TOKENS = {"__", "import", "exec", "eval", "os.", "sys."}


def is_safe_expression(expression: str) -> bool:
    lowered = expression.lower()
    return not any(token in lowered for token in BLOCKED_TOKENS)
