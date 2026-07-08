from aiogram import Bot, Router
from aiogram.filters import Command
from aiogram.types import Message

from snabix_bot.services.access import AccessService
from snabix_bot.services.commands import setup_bot_commands

router = Router(name="admin_command_sync")


@router.message(Command("sync_commands"))
async def sync_commands(
    message: Message,
    bot: Bot,
    access: AccessService,
) -> None:
    if not access.is_admin(message.from_user):
        await message.answer("Команда доступна только администраторам.")
        return

    await setup_bot_commands(bot)
    await message.answer(
        "Меню команд Telegram обновлено.\n"
        "Если список все еще не виден, закройте и откройте чат с ботом или отправьте /start."
    )
