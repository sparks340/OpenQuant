from packages.core.core.exceptions import ErrorContext, InvariantViolationError


def test_exception_serialization_with_context():
    error = InvariantViolationError(
        "position weight exceeded",
        details={"max": 0.2, "actual": 0.35},
        context=ErrorContext(operation="rebalance", resource="portfolio:demo"),
    )

    payload = error.to_dict()

    assert payload["code"] == "OQ-DOMAIN-INVARIANT"
    assert payload["message"] == "position weight exceeded"
    assert payload["details"]["actual"] == 0.35
    assert payload["context"]["operation"] == "rebalance"
