import asyncio
import logging

from aiogram import Bot, Dispatcher
from aiogram.webhook.aiohttp_server import SimpleRequestHandler, setup_application
from aiohttp import web

from snabix_bot.clients.backend import BackendClient
from snabix_bot.config import Settings
from snabix_bot.handlers import admin, callbacks, common, errors
from snabix_bot.services.access import AccessService

logger = logging.getLogger(__name__)


def build_dispatcher(settings: Settings, backend: BackendClient) -> Dispatcher:
    dispatcher = Dispatcher(
        access=AccessService(settings.admin_ids),
        backend=backend,
        settings=settings,
    )
    dispatcher.include_router(common.router)
    dispatcher.include_router(admin.router)
    dispatcher.include_router(callbacks.router)
    dispatcher.include_router(errors.router)

    return dispatcher


async def run_polling(settings: Settings, bot: Bot, dispatcher: Dispatcher) -> None:
    logger.info("Starting bot in polling mode")
    await bot.delete_webhook(drop_pending_updates=True)
    await dispatcher.start_polling(bot)


async def run_webhook(settings: Settings, bot: Bot, dispatcher: Dispatcher) -> None:
    if not settings.webhook_url:
        raise RuntimeError("SNABIX_BOT_WEBHOOK_URL is required when SNABIX_BOT_MODE=webhook.")

    logger.info(
        "Starting bot in webhook mode on %s:%s",
        settings.webhook_host,
        settings.webhook_port,
    )
    await bot.set_webhook(
        settings.webhook_url,
        secret_token=settings.webhook_secret or None,
        drop_pending_updates=True,
    )

    app = web.Application()
    request_handler = SimpleRequestHandler(
        dispatcher=dispatcher,
        bot=bot,
        secret_token=settings.webhook_secret or None,
    )
    request_handler.register(app, path=settings.webhook_path)
    setup_application(app, dispatcher, bot=bot)

    runner = web.AppRunner(app)
    await runner.setup()
    site = web.TCPSite(runner, host=settings.webhook_host, port=settings.webhook_port)
    await site.start()

    try:
        await asyncio.Event().wait()
    finally:
        await runner.cleanup()


async def run() -> None:
    settings = Settings(**{})
    logging.basicConfig(
        format="%(asctime)s %(levelname)s [%(name)s] %(message)s",
        level=settings.log_level,
    )

    bot = Bot(token=settings.bot_token)
    backend = BackendClient(
        settings.backend_base_url,
        settings.backend_service_token,
    )
    dispatcher = build_dispatcher(settings, backend)

    try:
        if settings.bot_mode == "webhook":
            await run_webhook(settings, bot, dispatcher)
        else:
            await run_polling(settings, bot, dispatcher)
    finally:
        await backend.close()
        await bot.session.close()


def main() -> None:
    asyncio.run(run())
