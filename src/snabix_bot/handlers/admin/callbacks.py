from aiogram import F, Router
from aiogram.types import CallbackQuery, Message
from aiohttp import ClientError

from snabix_bot.clients.backend import BackendClient
from snabix_bot.config import Settings
from snabix_bot.handlers.admin.callback_data import REFRESH_HEALTH, REFRESH_ME, REFRESH_STATS
from snabix_bot.handlers.admin.formatters import format_health, format_identity, format_stats
from snabix_bot.handlers.admin.keyboards import admin_keyboard
from snabix_bot.services.access import AccessService

router = Router(name="admin_callbacks")


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
