"""Settings for {{ cookiecutter.project_name }}.

Environment variable names are flat (no prefix), matching the rest of the BotKit
portfolio. The bot token is read from ``TELEGRAM_BOT_TOKEN``.
"""

from __future__ import annotations

import logging
from typing import Annotated

from pydantic import BeforeValidator, Field, model_validator
from pydantic_settings import BaseSettings

logger = logging.getLogger(__name__)


def parse_admin_ids(v: str | int | list[int] | None) -> list[int]:
    """Parse a comma-separated string of numeric Telegram user IDs."""
    if v is None:
        return []
    if isinstance(v, list):
        return [int(x) for x in v]
    if isinstance(v, int):
        return [v]
    result: list[int] = []
    for token in str(v).split(","):
        token = token.strip()
        if not token:
            continue
        try:
            result.append(int(token))
        except ValueError:
            logger.warning("Invalid admin id ignored: %r", token)
    return result


class Settings(BaseSettings):
    bot_token: str = Field("", validation_alias="TELEGRAM_BOT_TOKEN")
    admin_ids: Annotated[list[int], BeforeValidator(parse_admin_ids)] = []
    database_url: str = "sqlite+aiosqlite:///data/app.db"
    redis_url: str = "redis://127.0.0.1:6379/0"
    webhook_url: str = ""
    webhook_secret_token: str = ""
    sentry_dsn: str = ""
    metrics_port: int = {{ cookiecutter.port }}

    model_config = {"env_file": ".env", "extra": "ignore"}

    @model_validator(mode="after")
    def validate_required(self) -> Settings:
        if not self.bot_token:
            raise RuntimeError("TELEGRAM_BOT_TOKEN is not set")
        return self
