from aiogram import Bot, F, Router
from aiogram.filters import Command
from aiogram.types import CallbackQuery, InlineKeyboardButton, InlineKeyboardMarkup, Message
from aiohttp import ClientError

from snabix_bot.clients.backend import BackendClient
from snabix_bot.config import Settings
from snabix_bot.schemas.backend import (
    BackendHealthDto,
    BackendServiceIdentityDto,
    BackendStatsDto,
)
from snabix_bot.services.access import AccessService
from snabix_bot.services.commands import setup_bot_commands

router = Router(name="admin")

REFRESH_HEALTH = "admin:refresh:health"
REFRESH_ME = "admin:refresh:me"
REFRESH_STATS = "admin:refresh:stats"


def admin_keyboard(settings: Settings, refresh_callback: str) -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text="Открыть админку", url=settings.admin_panel_url)],
            [InlineKeyboardButton(text="Обновить", callback_data=refresh_callback)],
        ]
    )


def format_health(result: BackendHealthDto) -> str:
    status = "Доступен" if result.ok else "Недоступен"

    return f"Backend health\n\nСтатус: {status}\nHTTP: {result.status}\nСообщение: {result.message}"


def format_identity(identity: BackendServiceIdentityDto) -> str:
    return (
        "Service API\n\n"
        "Подключение: активно\n"
        f"Сервис: {identity.service}\n"
        f"Режим: {identity.mode}\n"
        f"Версия: {identity.version}"
    )


def format_stats(summary: BackendStatsDto) -> str:
    return (
        "Статистика Snabix\n\n"
        f"Пользователи: {summary.users_total}\n"
        f"Объявления всего: {summary.listings_total}\n"
        f"На модерации: {summary.listings_pending_review}\n"
        f"Опубликовано: {summary.listings_published}\n"
        f"В архиве: {summary.listings_archived}"
    )


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


@router.callback_query(F.data == REFRESH_HEALTH)
async def refresh_health(
    callback: CallbackQuery,
    backend: BackendClient,
    access: AccessService,
    settings: Settings,
) -> None:
    if not access.is_admin(callback.from_user):
        await callback.answer("Доступно только администраторам.", show_alert=True)
        return

    if not isinstance(callback.message, Message):
        await callback.answer("Не удалось обновить сообщение.", show_alert=True)
        return

    result = await backend.health()
    await callback.message.edit_text(
        format_health(result),
        reply_markup=admin_keyboard(settings, REFRESH_HEALTH),
    )
    await callback.answer("Обновлено.")


@router.callback_query(F.data == REFRESH_ME)
async def refresh_me(
    callback: CallbackQuery,
    backend: BackendClient,
    access: AccessService,
    settings: Settings,
) -> None:
    if not access.is_admin(callback.from_user):
        await callback.answer("Доступно только администраторам.", show_alert=True)
        return

    if not isinstance(callback.message, Message):
        await callback.answer("Не удалось обновить сообщение.", show_alert=True)
        return

    try:
        identity = await backend.me()
    except ClientError as exc:
        await callback.answer(f"Ошибка: {exc}", show_alert=True)
        return

    await callback.message.edit_text(
        format_identity(identity),
        reply_markup=admin_keyboard(settings, REFRESH_ME),
    )
    await callback.answer("Обновлено.")


@router.callback_query(F.data == REFRESH_STATS)
async def refresh_stats(
    callback: CallbackQuery,
    backend: BackendClient,
    access: AccessService,
    settings: Settings,
) -> None:
    if not access.is_admin(callback.from_user):
        await callback.answer("Доступно только администраторам.", show_alert=True)
        return

    if not isinstance(callback.message, Message):
        await callback.answer("Не удалось обновить сообщение.", show_alert=True)
        return

    try:
        summary = await backend.stats()
    except ClientError as exc:
        await callback.answer(f"Ошибка: {exc}", show_alert=True)
        return

    await callback.message.edit_text(
        format_stats(summary),
        reply_markup=admin_keyboard(settings, REFRESH_STATS),
    )
    await callback.answer("Обновлено.")
