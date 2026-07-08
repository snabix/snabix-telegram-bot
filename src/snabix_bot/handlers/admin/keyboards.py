from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

from snabix_bot.config import Settings


def admin_keyboard(settings: Settings, refresh_callback: str) -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text="Открыть админку", url=settings.admin_panel_url)],
            [InlineKeyboardButton(text="Обновить", callback_data=refresh_callback)],
        ]
    )
