"""Smoke tests for current api_service scaffold."""

from apps.api_service.api_service.main import app


def test_app_title() -> None:
    """API title should match new service naming."""
    assert app.title == "OpenQuant API Service"
