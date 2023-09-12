"""Configuration loading and validation."""


from loguru import logger
from pydantic import BaseModel, field_validator
from pydantic_settings import BaseSettings


class EnvConfig(
    BaseSettings,
    env_file=".env",
    env_file_encoding="utf-8",
    env_nested_delimiter="__",
    extra="ignore",
):
    """Our default configuration for models that should load from .env files."""


class _LokiConfig(EnvConfig, env_prefix="loki_"):
    """Loki specific configuration."""

    api_url: str
    jobs: list[str]
    max_logs: int | None = 5_000


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
        if len(value) > 10:  # noqa: PLR2004
            logger.warning("More than 10 token triggers in one period cannot be handled, be careful.")

        return value


SERVICE_CONFIG = _ServiceConfig()
