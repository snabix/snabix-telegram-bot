from typing import Optional

from aiogram.types import User


class AccessService:
    def __init__(self, admin_ids: frozenset[int]) -> None:
        self._admin_ids = admin_ids

    def is_admin(self, user: Optional[User]) -> bool:
        return user is not None and user.id in self._admin_ids
