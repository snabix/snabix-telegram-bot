from aiogram import F, Router
from aiogram.types import CallbackQuery

router = Router(name="callbacks")


@router.callback_query(F.data == "noop")
async def noop(callback: CallbackQuery) -> None:
    await callback.answer()
