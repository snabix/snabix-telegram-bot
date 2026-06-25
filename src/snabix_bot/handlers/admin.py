from aiogram import Router
from aiogram.filters import Command
from aiogram.types import Message

from snabix_bot.clients.backend import BackendClient
from snabix_bot.services.access import AccessService

router = Router(name="admin")


@router.message(Command("health"))
async def health(
    message: Message,
    backend: BackendClient,
    access: AccessService,
) -> None:
    if not access.is_admin(message.from_user):
        await message.answer("Команда доступна только администраторам.")
        return

    result = await backend.health()
    status = "OK" if result.ok else "ERROR"

    await message.answer(
        f"Backend health: {status}\n"
        f"HTTP/status: {result.status}\n"
        f"Message: {result.message}"
    )
