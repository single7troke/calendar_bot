import argparse
import asyncio
import json
import logging

from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command
from aiogram.types import BotCommand, FSInputFile
from aiogram.webhook.aiohttp_server import SimpleRequestHandler, setup_application
from aiohttp import web

from api.v1 import users, google_calendar
from core.config import Config
from middleware.user_access import UserAccessMiddleware, AdminAccessMiddleware

config = Config()
parser = argparse.ArgumentParser()
parser.add_argument('--webhook', action=argparse.BooleanOptionalAction)
args = parser.parse_args()


async def welcome(message: types.Message):
    """
    This handler will be called when user sends `/start` command
    """
    await message.reply("Hello my friend🍻")


async def description(message: types.Message):
    """
    This handler will be called when user sends `/about` command
    """
    await message.reply("<b>Как этим пользоваться.</b>\n\n"
                        "Нажми на меню и выбери команду.\n\n"
                        "<b>/next</b> выведет описание ближайшего мероприятия.\n\n"
                        "<b>/list</b> выведет список всех мероприятий\n"
                        "в виде клавиатуры с датами мероприятий.\n"
                        "Нажами на интересующую дату чтобы узнать детали мероприятия.\n\n"
                        "Бот присылает сообщение если в календаре появилось/удалилось мероприятие\n"
                        )


async def admin_description(message: types.Message):
    """
    This handler will be called when user sends `/admin` command
    """
    await message.reply("<b>Описание функционала администратора.</b>\n\n"
                        "Команды:\n\n"
                        "<b>/new_user</b> Добавляет нового пользователя в список тех,\n"
                        "кому разрешено пользоваться ботом.\n"
                        "1. Вводим id ползователя, который он должен предоставить(9ти значное число)\n"
                        "2. Вводим имя пользователя(на свое усмотрение, не длиннее 20 символов).\n\n"
                        "<b>/user_list</b> выведет список всех пользователей\n"
                        "в виде клавиатуры с именами пользователей.\n"
                        "Нажми на пользователя и подтверди его удаление.\n\n"
                        )


async def set_commands(bot: Bot):
    """
    Sets commands menu.
    """
    commands = [
        BotCommand(command="next", description="Ближайшее мероприятие"),
        BotCommand(command="list", description="Список мероприятий"),
        BotCommand(command="about", description="Функционал"),
        BotCommand(command="admin", description="Админка"),
    ]

    await bot.set_my_commands(commands=commands)


async def polling_setup(bot: Bot, dp: Dispatcher):
    """
    Run bot via polling.
    """
    await bot.delete_webhook()
    await set_commands(bot)
    await dp.start_polling(bot)


async def webhook_setup(bot: Bot):
    """
    Run bot via webhook.
    """
    await bot.delete_webhook()
    await set_commands(bot)
    cert = FSInputFile(config.path_to_pem_file)
    await bot.set_webhook(url=config.server_url,
                          ip_address=config.server_ip,
                          certificate=cert)
    info = await bot.get_webhook_info()
    info = json.loads(info.json())
    logging.info(f"webhook info:\n{json.dumps(info, indent=4)}")


if __name__ == '__main__':
    logging.basicConfig(format="%(asctime)s %(message)s",
                        datefmt="%m/%d/%Y %I:%M:%S %p %Z",
                        level=logging.INFO)

    bot = Bot(token=config.tg_bot_token, parse_mode="HTML")
    dp = Dispatcher()
    dp.message.register(description, Command(commands=["about"]))
    dp.message.register(admin_description, Command(commands=["admin"]))
    dp.include_router(google_calendar.router)
    dp.include_router(users.router)
    dp.message.middleware(AdminAccessMiddleware())
    dp.message.outer_middleware(UserAccessMiddleware())

    webhook = args.webhook
    if webhook:
        logging.info("Run webhook")
        dp.startup.register(webhook_setup)
        app = web.Application()
        SimpleRequestHandler(dispatcher=dp, bot=bot).register(app, path="")
        setup_application(app, dp, bot=bot)
        web.run_app(app)
    else:
        logging.info("Run polling")
        asyncio.run(polling_setup(bot=bot, dp=dp))
