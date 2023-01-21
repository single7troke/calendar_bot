import os

from aiogram import Bot, Dispatcher, executor, types
import aiohttp

chat_id = 432093294

bot = Bot(token=os.getenv("TG_BOT_TOKEN"))
dp = Dispatcher(bot)


async def request_to_app():

    async with aiohttp.ClientSession() as session:

        url = "http://app:8000/api/v1/google-calendar"
        async with session.get(url) as resp:
            data = await resp.json()
            return data


async def set_default_commands(dp):
    await dp.bot.set_my_commands([
        types.BotCommand("start", "Запустить бота"),
        types.BotCommand("help", "Помощь"),
        types.BotCommand("next", "Ближайшее событие"),
        types.BotCommand("list", "Список событий"),
    ])


@dp.message_handler(commands=['start', "hello"])
async def send_welcome(message: types.Message):
    """
    This handler will be called when user sends `/start` or `/help` command
    """
    await message.reply("Hi!\nI'm EchoBot!\nPowered by aiogram.")
    print(message.__dir__())
    print(message.chat.id)
    print(message.from_id)


@dp.message_handler()
async def echo(message: types.Message):
    data = await request_to_app()
    await message.reply(data)


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True, on_startup=[set_default_commands])
