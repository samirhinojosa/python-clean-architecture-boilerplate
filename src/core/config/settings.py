import os
from enum import StrEnum
from functools import lru_cache
from pathlib import Path
from typing import Any

from pydantic import Field, model_validator
from pydantic_settings import BaseSettings, SettingsConfigDict


class LogLevel(StrEnum):
    DEBUG = "DEBUG"
    INFO = "INFO"
    WARNING = "WARNING"
    ERROR = "ERROR"
    CRITICAL = "CRITICAL"


class DatabaseSettings(BaseSettings):
    url: str = Field(
        default="postgresql://postgres:postgres@localhost:5432/app_db",
        alias="DATABASE_URL",
    )


class Settings(BaseSettings):
    """
    Handles application settings: Env Vars > .env file > Defaults.
    """

    # Paths (Resolved dynamically for local dev)
    BASE_DIR: Path = Path(__file__).resolve().parents[3]

    # Environment Detection
    APP_ENV: str = Field(default="local", alias="APP_ENV")
    IS_CLOUD: bool = Field(default=False)

    # Logging
    LOG_LEVEL: LogLevel = Field(default=LogLevel.INFO, alias="LOG_LEVEL")
    LOG_JSON_FORMAT: bool = Field(default=False)

    # Nested Domains
    db: DatabaseSettings = Field(default_factory=DatabaseSettings)

    @model_validator(mode="after")
    def auto_configure_environment(self) -> "Settings":
        """
        Post-load logic.
        Configures defaults based on the detected environment (AWS or GCP).
        """
        # AWS and GCP environment variables standard injection
        is_aws = os.getenv("AWS_EXECUTION_ENV") or os.getenv(
            "ECS_CONTAINER_METADATA_URI"
        )
        is_gcp = os.getenv("CLOUD_ML_JOB_ID") or os.getenv("K_SERVICE")

        if is_aws or is_gcp or self.APP_ENV == "production":
            self.IS_CLOUD = True
            # Force JSON for Cloud Logging/CloudWatch indexers
            self.LOG_JSON_FORMAT = True
            # Use strict container working directory
            self.BASE_DIR = Path("/app")

        return self


class RuntimeSettings(Settings):
    model_config = SettingsConfigDict(
        env_file=".env", env_file_encoding="utf-8", case_sensitive=True, extra="ignore"
    )


class TestSettings(Settings):
    model_config = SettingsConfigDict(
        env_file=None, case_sensitive=True, extra="ignore"
    )


@lru_cache
def get_settings(*, read_env: bool = True, **overrides: Any) -> Settings:
    """
    Returns a singleton instance of the project settings.
    """
    cls = TestSettings if not read_env else RuntimeSettings
    return cls(**overrides)