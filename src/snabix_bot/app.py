import asyncio
import logging

from aiogram import Bot, Dispatcher

from snabix_bot.clients.backend import BackendClient
from snabix_bot.config import Settings
from snabix_bot.handlers import admin, callbacks, common, errors
from snabix_bot.services.access import AccessService


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
    dispatcher = Dispatcher(
        access=AccessService(settings.admin_ids),
        backend=backend,
        settings=settings,
    )
    dispatcher.include_router(common.router)
    dispatcher.include_router(admin.router)
    dispatcher.include_router(callbacks.router)
    dispatcher.include_router(errors.router)

    try:
        await dispatcher.start_polling(bot)
    finally:
        await backend.close()
        await bot.session.close()


def main() -> None:
    asyncio.run(run())
