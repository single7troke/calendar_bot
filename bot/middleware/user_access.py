import json
import os
from typing import Callable, Dict, Any, Awaitable

from aiogram import BaseMiddleware
from aiogram.types import Message

from core.config import Config


config = Config()
print(config.base_dir)
users_id = []
with open(os.path.join(config.base_dir, "users_id.json")) as file:
    data = json.load(file)
    for user_id in data["users"].values():
        users_id.append(user_id)


class UserAccessMiddleware(BaseMiddleware):
    async def __call__(
        self,
        handler: Callable[[Message, Dict[str, Any]], Awaitable[Any]],
        event: Message,
        data: Dict[str, Any]
    ) -> Any:

        if event.from_user.id in users_id:
            return await handler(event, data)
