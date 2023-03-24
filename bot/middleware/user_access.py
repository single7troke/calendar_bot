from typing import Callable, Dict, Any, Awaitable

from aiogram import BaseMiddleware
from aiogram.types import Message

from core.config import Config
from core.utils import get_user


config = Config()


class UserAccessMiddleware(BaseMiddleware):
    async def __call__(
        self,
        handler: Callable[[Message, Dict[str, Any]], Awaitable[Any]],
        event: Message,
        data: Dict[str, Any]
    ) -> Any:
        if await get_user(user_id=event.from_user.id):
            return await handler(event, data)


class AdminAccessMiddleware(BaseMiddleware):
    async def __call__(
        self,
        handler: Callable[[Message, Dict[str, Any]], Awaitable[Any]],
        event: Message,
        data: Dict[str, Any]
    ) -> Any:
        user = await get_user(user_id=event.from_user.id)
        if "command" not in data:
            return await handler(event, data)
        if data["command"].command not in config.admin_commands:
            return await handler(event, data)
        if data["command"].command in config.admin_commands and user["role"] in config.admin_roles:
            return await handler(event, data)

        await event.answer(
            "You have no access",
            show_alert=True
        )
