from aiogram import Router
from aiogram.filters import Command
from aiogram.types import Message

from snabix_bot.clients.backend import BackendClient
from snabix_bot.config import Settings

router = Router(name="admin")


@router.message(Command("health"))
async def health(
        message: Message,
        backend: BackendClient,
        settings: Settings
) -> None:
    if message.from_user is None or message.from_user.id not in settings.admin_ids:
        await message.answer("Команда доступна только администраторам.")
        return

    result = await backend.health()
    status = "OK" if result.ok else "ERROR"

    await message.answer(
        f"Backend health: {status}\n"
        f"HTTP/status: {result.status}\n"
        f"Message: {result.message}"
    )
