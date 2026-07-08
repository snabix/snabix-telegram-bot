from aiogram import Router
from aiogram.filters import Command
from aiogram.types import Message
from aiohttp import ClientError

from snabix_bot.clients.backend import BackendClient
from snabix_bot.config import Settings
from snabix_bot.handlers.admin.callback_data import REFRESH_HEALTH, REFRESH_ME, REFRESH_STATS
from snabix_bot.handlers.admin.formatters import format_health, format_identity, format_stats
from snabix_bot.handlers.admin.keyboards import admin_keyboard
from snabix_bot.services.access import AccessService

router = Router(name="admin_status")


@router.message(Command("health"))
async def health(
    message: Message,
    backend: BackendClient,
    access: AccessService,
    settings: Settings,
) -> None:
    if not access.is_admin(message.from_user):
        await message.answer("Команда доступна только администраторам.")
        return

    result = await backend.health()
    await message.answer(
        format_health(result),
        reply_markup=admin_keyboard(settings, REFRESH_HEALTH),
    )


@router.message(Command("me"))
async def me(
    message: Message,
    backend: BackendClient,
    access: AccessService,
    settings: Settings,
) -> None:
    if not access.is_admin(message.from_user):
        await message.answer("Команда доступна только администраторам.")
        return

    try:
        identity = await backend.me()
    except ClientError as exc:
        await message.answer(f"Не удалось получить service identity: {exc}")
        return

    await message.answer(
        format_identity(identity),
        reply_markup=admin_keyboard(settings, REFRESH_ME),
    )


@router.message(Command("stats"))
async def stats(
    message: Message,
    backend: BackendClient,
    access: AccessService,
    settings: Settings,
) -> None:
    if not access.is_admin(message.from_user):
        await message.answer("Команда доступна только администраторам.")
        return

    try:
        summary = await backend.stats()
    except ClientError as exc:
        await message.answer(f"Не удалось получить статистику: {exc}")
        return

    await message.answer(
        format_stats(summary),
        reply_markup=admin_keyboard(settings, REFRESH_STATS),
    )
