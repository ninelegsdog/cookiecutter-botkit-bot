"""Entry point for {{ cookiecutter.project_name }}.

Wiring mirrors the rest of the BotKit portfolio: shared logging/tracing/Sentry
setup from ``botkit-core``, the standard middleware stack, a global error
handler and either the aiohttp webhook app or long polling, both exposing
``/health``, ``/version`` and ``/metrics``.
"""

from __future__ import annotations

import asyncio
import logging
import os
import signal

from aiogram import Bot, Dispatcher
from aiohttp import web
from botkit_core.errors import register_error_handler
from botkit_core.logging import setup_logging
from botkit_core.metrics import (
    UpdatesMiddleware,
    health,
    metrics,
    start_metrics_server,
    version,
)
from botkit_core.middleware.logging import LoggingMiddleware
from botkit_core.sentry import init_sentry
from botkit_core.tracing import TracingMiddleware, setup_tracing
from botkit_core.webhook import build_webhook_app

from src.core.config import Settings

logger = logging.getLogger(__name__)

BOT_NAME = "{{ cookiecutter.bot_name }}"


def build_dispatcher() -> Dispatcher:
    """Create the dispatcher with the standard BotKit middleware stack.

    Register your routers on the returned dispatcher.
    """
    dp = Dispatcher()
    dp.update.outer_middleware(LoggingMiddleware())
    dp.update.outer_middleware(TracingMiddleware())
    dp.update.outer_middleware(UpdatesMiddleware())
    register_error_handler(dp)
    return dp


def _build_webhook_app(dp: Dispatcher, bot: Bot, settings: Settings) -> web.Application:
    app = build_webhook_app(dp, bot, settings.webhook_secret_token)
    app.router.add_get("/health", health)
    app.router.add_get("/version", version)
    app.router.add_get("/metrics", metrics)
    return app


async def _run_webhook(settings: Settings, dp: Dispatcher, bot: Bot, shutdown_event: asyncio.Event) -> None:
    app = _build_webhook_app(dp, bot, settings)
    runner = web.AppRunner(app)
    await runner.setup()
    site = web.TCPSite(runner, os.getenv("BIND_HOST", "0.0.0.0"), settings.metrics_port)
    await site.start()
    logger.info("Webhook HTTP server listening on :%s", settings.metrics_port)

    await bot.delete_webhook(drop_pending_updates=True)
    # No certificate is passed on purpose: Telegram pins setWebhook to the CA of
    # the certificate it is given, so a renewal stops delivery while setWebhook
    # still reports success. TLS terminates at the reverse proxy instead.
    await bot.set_webhook(
        url=settings.webhook_url,
        secret_token=settings.webhook_secret_token or None,
    )
    logger.info("Telegram webhook registered: %s", settings.webhook_url)
    try:
        await shutdown_event.wait()
    finally:
        await bot.delete_webhook()
        await runner.cleanup()


async def _run_polling(settings: Settings, dp: Dispatcher, bot: Bot, shutdown_event: asyncio.Event) -> None:
    await bot.delete_webhook(drop_pending_updates=True)
    runner = await start_metrics_server(settings.metrics_port)
    logger.info("Long polling started; metrics on :%s", settings.metrics_port)
    try:
        await asyncio.wait(
            [
                asyncio.create_task(dp.start_polling(bot)),
                asyncio.create_task(shutdown_event.wait()),
            ]
        )
    finally:
        await dp.stop_polling()
        await bot.session.close()
        await runner.cleanup()


async def main() -> None:
    settings = Settings()
    setup_logging(level="INFO", json=True, bot_name=BOT_NAME)
    setup_tracing(service_name=BOT_NAME)
    init_sentry(settings.sentry_dsn)

    dp = build_dispatcher()
    bot = Bot(settings.bot_token)

    shutdown_event = asyncio.Event()

    def _signal_handler() -> None:
        shutdown_event.set()

    loop = asyncio.get_running_loop()
    for sig in (signal.SIGTERM, signal.SIGINT):
        loop.add_signal_handler(sig, _signal_handler)

    if settings.webhook_url:
        await _run_webhook(settings, dp, bot, shutdown_event)
    else:
        await _run_polling(settings, dp, bot, shutdown_event)


if __name__ == "__main__":
    asyncio.run(main())
