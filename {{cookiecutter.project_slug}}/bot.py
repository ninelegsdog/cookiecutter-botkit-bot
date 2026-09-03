import asyncio
import logging
from src.core.config import Settings
from src.core.logging import setup_logging
from src.core.tracing import setup_tracing
from src.core.sentry import init_sentry

async def main() -> None:
    settings = Settings()
    setup_logging(level="INFO", json=True, bot_name="{{ cookiecutter.bot_name }}")
    setup_tracing(service_name="{{ cookiecutter.bot_name }}")
    init_sentry(settings.sentry_dsn)
    logging.info("Bot {{ cookiecutter.bot_name }} started")

if __name__ == "__main__":
    asyncio.run(main())
