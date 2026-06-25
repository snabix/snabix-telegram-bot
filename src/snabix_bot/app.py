import asyncio
import logging

from aiogram import Bot, Dispatcher

from snabix_bot.clients.backend import BackendClient
from snabix_bot.config import Settings
from snabix_bot.handlers import admin, common


async def run() -> None:
    settings = Settings(**{})
    logging.basicConfig(
        format="%(asctime)s %(levelname)s [%(name)s] %(message)s",
        level=settings.log_level,
    )

    bot = Bot(token=settings.bot_token)
    dispatcher = Dispatcher(
        backend=BackendClient(
            settings.backend_base_url,
            settings.backend_service_token
        ),
        settings=settings,
    )
    dispatcher.include_router(common.router)
    dispatcher.include_router(admin.router)

    await dispatcher.start_polling(bot)


def main() -> None:
    asyncio.run(run())
