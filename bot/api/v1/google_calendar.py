import json

from aiogram import types, Dispatcher
from aiogram.filters import Command

from core import utils


async def next_event(message: types.Message):
    data = await utils.event_list()
    events = utils.format_time(data)
    event = await utils.event_details(events[0]["id"])
    await message.answer(json.dumps(event, indent=2, ensure_ascii=False))


async def events_list(message: types.Message):
    data = await utils.event_list()
    events = utils.format_time(data)
    keyboard = utils.create_keyboard(events)

    await message.answer(text="hello", reply_markup=keyboard)


async def event_list_callbacks(
        callback: types.CallbackQuery,
        callback_data: utils.GoogleEventCallback):

    data = await utils.event_details(callback_data.event_id)
    await callback.message.answer(json.dumps(data, indent=2, ensure_ascii=False))
    await callback.answer()


def register_google_handlers(dp: Dispatcher):
    dp.message.register(events_list, Command(commands=("list",)))
    dp.message.register(next_event, Command(commands=("next",)))
    dp.callback_query.register(event_list_callbacks, utils.GoogleEventCallback.filter())
