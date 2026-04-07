from packages.core.core.config.settings import Settings


def test_settings_reads_environment_overrides(monkeypatch):
    monkeypatch.setenv("APP_ENV", "test")
    monkeypatch.setenv("API_PORT", "9010")

    instance = Settings()

    assert instance.app_env == "test"
    assert instance.api_port == 9010
