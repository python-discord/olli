"""Configuration loading and validation."""

import json
import typing as t

from loguru import logger
from pydantic import BaseModel, field_validator, fields
from pydantic_settings import BaseSettings, PydanticBaseSettingsSource


def custom_decode_complex_value(
    __: str,
    ___: fields.FieldInfo,
    value: t.Any,
) -> t.Any:
    """Parse complex values as CSV if they cannot be parsed as JSON."""
    try:
        return json.loads(value)
    except ValueError:
        return value.split(",")


class EnvConfig(
    BaseSettings,
    env_file=".env",
    env_file_encoding="utf-8",
    env_nested_delimiter="__",
    extra="ignore",
):
    """Our default configuration for models that should load from .env files."""

    @classmethod
    def settings_customise_sources(
        cls,
        settings_cls: type[BaseSettings],
        init_settings: PydanticBaseSettingsSource,
        env_settings: PydanticBaseSettingsSource,
        dotenv_settings: PydanticBaseSettingsSource,
        file_secret_settings: PydanticBaseSettingsSource,
    ) -> tuple[PydanticBaseSettingsSource, ...]:
        """Monkey patch default sources to have the custom CSV parser fallback."""
        dotenv_settings.decode_complex_value = custom_decode_complex_value
        env_settings.decode_complex_value = custom_decode_complex_value
        return (
            init_settings,
            env_settings,
            dotenv_settings,
            file_secret_settings,
        )


class _LokiConfig(EnvConfig, env_prefix="loki_"):
    """Loki specific configuration."""

    api_url: str
    jobs: list[str]
    max_logs: int | None = 5_000

    @field_validator("api_url")
    @classmethod
    def rstrip_api_url(cls, value: str) -> str:
        """Strip trailing slashes from the api_url as this breaks API calls."""
        return value.rstrip("/")


LOKI_CONFIG = _LokiConfig()


class _DiscordConfig(EnvConfig, env_prefix="discord_"):
    """Configuration for Discord alerting."""

    webhook_url: str | None


DISCORD_CONFIG = _DiscordConfig()


class TokenConfig(BaseModel):
    """Class representing a token config entry."""

    token: str
    color: str | None = "#7289DA"
    case_sensitive: bool | None = False


class _ServiceConfig(EnvConfig, env_prefix="service_"):
    """Configuration of the Olli status."""

    interval_minutes: int
    tokens: list[TokenConfig]

    @field_validator("interval_minutes")
    @classmethod
    def must_be_above_zero(cls, value: int) -> int:
        """Validate that the interval minutes is 1 or greater."""
        if value < 1:
            msg = "Interval must be above zero minutes."
            raise ValueError(msg)

        return value

    @field_validator("tokens")
    @classmethod
    def warn_above_ten(cls, value: list[TokenConfig]) -> list[TokenConfig]:
        """
        Warn a user if they have more than 10 tokens.

        This is because we cannot handle more than 10 token triggers at once until we
        batch triggers into groups of 10 to distribute to the webhook.
        """
        if len(value) > 10:
            logger.warning("More than 10 token triggers in one period cannot be handled, be careful.")

        return value


SERVICE_CONFIG = _ServiceConfig()
