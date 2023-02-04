import asyncio
import os

from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command
from aiogram.types import BotCommand

from api.v1.google_calendar import register_google_handlers
from middleware.user_access import UserAccessMiddleware

bot = Bot(token=os.getenv("TG_BOT_TOKEN"))
dp = Dispatcher()


@dp.message(Command(commands=["start"]))
async def send_welcome(message: types.Message):
    """
    This handler will be called when user sends `/start` command
    """
    await message.reply("Hello🍻")


async def set_commands(bot: Bot):
    commands = [
        BotCommand(command="start", description="Приветствие"),
        BotCommand(command="about", description="Описание"),
        BotCommand(command="next", description="Ближайшее событие"),
        BotCommand(command="list", description="Список событий"),
    ]

    await bot.set_my_commands(commands=commands)


async def main(bot: Bot, dp: Dispatcher):
    register_google_handlers(dp=dp)
    dp.message.outer_middleware(UserAccessMiddleware())
    await set_commands(bot)
    await dp.start_polling(bot)


if __name__ == '__main__':
    asyncio.run(main(bot, dp))
