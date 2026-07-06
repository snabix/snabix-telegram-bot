from aiogram import Router

from snabix_bot.handlers.admin import callbacks, command_sync, status_handlers

router = Router(name="admin")
router.include_router(status_handlers.router)
router.include_router(command_sync.router)
router.include_router(callbacks.router)

__all__ = ["router"]
