import logging

from aiogram import Router
from aiogram.types import ErrorEvent

router = Router(name="errors")
logger = logging.getLogger(__name__)


@router.errors()
async def handle_error(event: ErrorEvent) -> None:
    logger.exception("Unhandled bot update error", exc_info=event.exception)
