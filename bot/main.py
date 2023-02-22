import argparse
import asyncio
import json
import logging
import os

from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command
from aiogram.types import BotCommand
from aiogram.webhook.aiohttp_server import SimpleRequestHandler, setup_application
from aiohttp import web

from api.v1.google_calendar import register_google_handlers
from middleware.user_access import UserAccessMiddleware


parser = argparse.ArgumentParser()
parser.add_argument('--webhook', action=argparse.BooleanOptionalAction)
args = parser.parse_args()


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


async def polling_setup(bot: Bot, dp: Dispatcher):
    await bot.delete_webhook()
    await set_commands(bot)
    await dp.start_polling(bot)


async def webhook_setup(dispatcher: Dispatcher, bot: Bot):
    await bot.delete_webhook()
    await set_commands(bot)
    # cert = FSInputFile("./cert/PUBLIC.pem")
    await bot.set_webhook(f"https://194.67.109.17", ip_address="194.67.109.17")
    info = await bot.get_webhook_info()
    info = json.loads(info.json())
    logging.info(f"webhook info:\n{json.dumps(info, indent=4)}")


if __name__ == '__main__':
    logging.basicConfig(format="%(asctime)s %(message)s",
                        datefmt="%m/%d/%Y %I:%M:%S %p %Z",
                        level=logging.INFO)

    bot = Bot(token=os.getenv("TG_BOT_TOKEN"), parse_mode="HTML")
    dp = Dispatcher()
    dp.message.register(Command(commands=["start"]))
    register_google_handlers(dp=dp)
    dp.message.outer_middleware(UserAccessMiddleware())

    webhook = args.webhook
    if webhook:
        logging.info("Starting with webhook")
        dp.startup.register(webhook_setup)
        app = web.Application()
        SimpleRequestHandler(dispatcher=dp, bot=bot).register(app, path="")
        setup_application(app, dp, bot=bot)
        web.run_app(app)
    else:
        logging.info("Starting with polling")
        asyncio.run(polling_setup(bot=bot, dp=dp))
