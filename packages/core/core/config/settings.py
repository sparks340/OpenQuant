"""Shared application settings.

We centralize runtime configuration here so later services can reuse a single
source of truth instead of each module hand-loading environment variables.
"""

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Runtime settings loaded from environment variables or a local .env file."""

    app_env: str = "dev"
    log_level: str = "INFO"
    api_host: str = "0.0.0.0"
    api_port: int = 8000
    mongo_uri: str = "mongodb://127.0.0.1:27017"
    mongo_db: str = "quant_platform"
    redis_url: str = "redis://127.0.0.1:6379/0"
    llm_base_url: str = "https://api.openai.com/v1"
    llm_api_key: str = ""
    llm_model: str = "gpt-4o-mini"

    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8", extra="ignore")


settings = Settings()

