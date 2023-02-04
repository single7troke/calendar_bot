import os
from typing import Callable, Dict, Any, Awaitable

from aiogram import BaseMiddleware
from aiogram.types import Message


chat_id_list = [int(i) for i in os.getenv("CHAT_IDS").split(",") if i.isdigit()]


class UserAccessMiddleware(BaseMiddleware):
    async def __call__(
        self,
        handler: Callable[[Message, Dict[str, Any]], Awaitable[Any]],
        event: Message,
        data: Dict[str, Any]
    ) -> Any:

        if event.from_user.id in chat_id_list:
            return await handler(event, data)
