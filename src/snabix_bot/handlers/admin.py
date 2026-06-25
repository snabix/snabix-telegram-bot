from aiogram import Bot, Router
from aiogram.filters import Command
from aiogram.types import Message
from aiohttp import ClientError

from snabix_bot.clients.backend import BackendClient
from snabix_bot.services.access import AccessService
from snabix_bot.services.commands import setup_bot_commands

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


@router.message(Command("me"))
async def me(
    message: Message,
    backend: BackendClient,
    access: AccessService,
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
        "Service API подключен.\n"
        f"Service: {identity.service}\n"
        f"Mode: {identity.mode}\n"
        f"Version: {identity.version}"
    )


@router.message(Command("stats"))
async def stats(
    message: Message,
    backend: BackendClient,
    access: AccessService,
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
        "Статистика Snabix:\n"
        f"Пользователей: {summary.users_total}\n"
        f"Объявлений всего: {summary.listings_total}\n"
        f"На модерации: {summary.listings_pending_review}\n"
        f"Опубликовано: {summary.listings_published}\n"
        f"В архиве: {summary.listings_archived}"
    )


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
