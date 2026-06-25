from aiogram import Router
from aiogram.filters import Command
from aiogram.types import Message

from snabix_bot.services.access import AccessService

router = Router(name="common")


@router.message(Command("start"))
async def start(message: Message, access: AccessService) -> None:
    is_admin = access.is_admin(message.from_user)
    admin_note = (
        "\n\nВы определены как администратор. Доступны команды: /health."
        if is_admin
        else "\n\nЕсли вы администратор, добавьте свой Telegram ID в SNABIX_ADMIN_TELEGRAM_IDS."
    )

    await message.answer(
        "Добро пожаловать в Snabix Bot.\n\n"
        "Сейчас я работаю как сервисный помощник проекта: буду помогать с "
        "админскими уведомлениями, проверкой backend и будущей модерацией объявлений."
        f"{admin_note}"
    )


@router.message(Command("help"))
async def help_command(message: Message) -> None:
    await message.answer(
        "Доступные команды:\n"
        "/start - запустить бота\n"
        "/help - список команд\n"
        "/health - проверить backend, доступно администраторам\n"
        "/me - проверить service API, доступно администраторам\n"
        "/stats - базовая статистика, доступно администраторам"
    )
