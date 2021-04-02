"""Configuration loading and validation."""
import os
from pathlib import Path
from typing import Optional

import toml
from dotenv import load_dotenv
from loguru import logger
from pydantic import BaseModel, validator

load_dotenv()


# All the locations where we might find a config file
CONFIG_PATHS = [
    "./olli.toml",
    "/config/olli.toml",
    "/olli/config.toml",
    "/etc/olli/config.toml"
]


class TokenConfig(BaseModel):
    """Class representing a token config entry."""

    token: str
    color: str = "#7289DA"


class LokiConfig(BaseModel):
    """Loki specific configuration."""

    api_url: str
    jobs: list[str]
    max_logs: Optional[int] = 5_000


class DiscordConfig(BaseModel):
    """Configuration for Discord alerting."""

    webhook_url: Optional[str]

    @validator("webhook_url", always=True)
    def env_provided_webhook(cls, value: Optional[str]) -> str:
        """
        If no webhook is specified in the config, try fetch from environment.

        If not found in the environment either then raise a validation error.
        """
        if value:
            return value

        if webhook := os.environ.get("WEBHOOK_URL"):
            return webhook

        raise ValueError(
            "Must specify webhook_url under [discord] or WEBHOOK_URL env var"
        )


class ServiceConfig(BaseModel):
    """Configuration of the Olli status."""

    interval_minutes: int
    tokens: list[TokenConfig]

    @validator("interval_minutes")
    def must_be_above_zero(cls, value: int) -> int:
        """Validate that the interval minutes is 1 or greater."""
        if value < 1:
            raise ValueError("Interval must be above zero minutes.")

        return value

    @validator("tokens")
    def warn_above_ten(cls, value: list[TokenConfig]) -> list[TokenConfig]:
        """
        Warn a user if they have more than 10 tokens.

        This is because we cannot handle more than 10 token triggers at once until we
        batch triggers into groups of 10 to distribute to the webhook.
        """
        if len(value) > 10:
            logger.warning(
                "More than 10 token triggers in one period cannot be handled, be careful."
            )

        return value


class OlliConfig(BaseModel):
    """Class representing root Olli config."""

    loki: LokiConfig
    olli: ServiceConfig
    discord: DiscordConfig = DiscordConfig()


def get_config() -> OlliConfig:
    """Open the config file, parse the TOML and convert to Pydantic objects."""
    logger.info("Searching for config file")

    path = None

    for file_path in CONFIG_PATHS:
        if (config_file := Path(file_path)).exists():
            path = config_file
            logger.info(f"Found config at {file_path}")
            break

    if not path:
        logger.critical("Could not find a config file. Please refer to the documentation.")
        raise SystemExit(1)

    with open(config_file) as conf_file:
        return OlliConfig(**toml.load(conf_file))


CONFIG = get_config()
