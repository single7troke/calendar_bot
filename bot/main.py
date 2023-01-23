import asyncio
import json
import os

from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command
from aiogram.types import BotCommand

from core import utils


bot = Bot(token=os.getenv("TG_BOT_TOKEN"))
dp = Dispatcher()


@dp.message(Command(commands=["start", "hello"]))
async def send_welcome(message: types.Message):
    """
    This handler will be called when user sends `/start` or `/help` command
    """
    await message.reply("Hello🍻")


@dp.message(Command(commands=["list"]))
async def echo(message: types.Message):
    data = await utils.event_list()
    events = utils.format_time(data)
    keyboard = utils.create_keyboard(events)

    await message.answer(text="hello", reply_markup=keyboard)


@dp.callback_query(utils.GoogleEventCallback.filter())
async def google_calendar_callbacks(
        callback: types.CallbackQuery,
        callback_data: utils.GoogleEventCallback):

    data = await utils.event_details(callback_data.event_id)
    await callback.message.answer(json.dumps(data, indent=2, ensure_ascii=False))#, parse_mode="HTML")
    await callback.answer()


async def set_commands(bot: Bot):
    commands = [
        BotCommand(command="start", description="Запустить бота"),
        BotCommand(command="help", description="Помощь"),
        BotCommand(command="next", description="Ближайшее событие"),
        BotCommand(command="list", description="Список событий"),
    ]

    await bot.set_my_commands(commands=commands)


async def main(bot, dp):
    await set_commands(bot)
    await dp.start_polling(bot)


if __name__ == '__main__':
    asyncio.run(main(bot, dp))
