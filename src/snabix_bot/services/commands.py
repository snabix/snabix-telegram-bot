import logging

from aiogram import Bot
from aiogram.types import BotCommand

logger = logging.getLogger(__name__)

BOT_COMMANDS = [
    BotCommand(command="start", description="Запустить Snabix Bot"),
    BotCommand(command="help", description="Показать подсказку"),
    BotCommand(command="whoami", description="Показать Telegram ID"),
    BotCommand(command="health", description="Проверить backend"),
    BotCommand(command="me", description="Проверить service API"),
    BotCommand(command="stats", description="Показать статистику"),
    BotCommand(command="sync_commands", description="Обновить меню команд"),
]


async def setup_bot_commands(bot: Bot) -> None:
    await bot.set_my_commands(BOT_COMMANDS)
    logger.info("Telegram command menu synchronized: %s commands.", len(BOT_COMMANDS))
