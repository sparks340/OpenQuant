"""Smoke tests for the rebuilt project scaffold."""

from apps.api.api.main import app
from packages.core.core.config.settings import settings


def test_app_title() -> None:
    """The API app should expose the expected title."""
    assert app.title == "OpenQuant API"


def test_settings_defaults() -> None:
    """The default environment should remain stable for local development."""
    assert settings.app_env == "dev"
