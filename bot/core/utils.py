import aiohttp
from aiogram import types
from aiogram.filters.callback_data import CallbackData

from core.config import Config

config = Config()


class GoogleEventCallback(CallbackData, prefix="id"):
    event_id: str


def create_keyboard(events):
    buttons = []
    for event in events:
        buttons.append(
            [types.InlineKeyboardButton(
                text=event["start"],
                callback_data=GoogleEventCallback(event_id=event["id"]).pack())]
        )
    keyboard = types.InlineKeyboardMarkup(inline_keyboard=buttons)
    return keyboard


async def event_list():
    async with aiohttp.ClientSession() as session:
        url = config.url
        async with session.get(url) as resp:
            data = await resp.json()
            return data


async def event_details(event_id: str):
    async with aiohttp.ClientSession() as session:
        url = f"{config.url}{event_id}"
        async with session.get(url) as resp:
            data = await resp.json()
            return data
