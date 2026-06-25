from aiogram import Router
from aiogram.filters import Command
from aiogram.types import Message

router = Router(name="common")


@router.message(Command("start"))
async def start(message: Message) -> None:
    await message.answer(
        "Snabix bot готов к работе.\n\n"
        "Сейчас бот работает как сервисный помощник для админских уведомлений."
    )


@router.message(Command("help"))
async def help_command(message: Message) -> None:
    await message.answer(
        "Доступные команды:\n"
        "/start - запустить бота\n"
        "/help - список команд\n"
        "/health - проверить backend, доступно администраторам"
    )
