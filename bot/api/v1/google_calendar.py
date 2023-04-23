from aiogram import types, Router
from aiogram.filters import Command

from core import utils, keyboards

router = Router()


@router.message(Command(commands=("menu",)))
async def main_menu(message: types.Message):
    await message.answer(text="Menu",
                         reply_markup=keyboards.main_menu_keyboard())


async def next_event(message: types.Message):
    data = await utils.event_list()
    events = data["events"]
    event = await utils.event_details(events[0]["id"])
    await message.edit_text(f"<b>{event['summary']} - {event['start']}</b>\n\n"f"{event['description']}",
                            reply_markup=keyboards.back_button(
                                callback_data="menu"
                            ))


async def events_list(message: types.Message):
    data = await utils.event_list()
    events = data["events"]
    keyboard = keyboards.google_events_keyboard(events)

    await message.answer(text="Events:", reply_markup=keyboard)


@router.callback_query(keyboards.MainMenuCallback.filter())
async def main_menu_callback(
        callback: types.CallbackQuery,
        callback_data: keyboards.MainMenuCallback):
    if callback_data.data == "next":
        await next_event(callback.message)
    elif callback_data.data == "list":
        await events_list(callback.message)


@router.callback_query(keyboards.GoogleEventCallback.filter())
async def event_list_callbacks(
        callback: types.CallbackQuery,
        callback_data: keyboards.GoogleEventCallback):
    event = await utils.event_details(callback_data.event_id)
    await callback.message.edit_text(f"<b>{event['summary']} - {event['start']}</b>\n\n{event['description']}",
                                     reply_markup=keyboards.back_button(callback_data="event_list"))
    await callback.answer()


@router.callback_query(keyboards.BackButtonCallback.filter())
async def back_button_callback(
        callback: types.CallbackQuery,
        callback_data: keyboards.BackButtonCallback):
    if callback_data.data == "event_list":
        data = await utils.event_list()
        events = data["events"]
        keyboard = keyboards.google_events_keyboard(events)
        await callback.message.edit_text(text="Events:", reply_markup=keyboard)
    elif callback_data.data == "menu":
        await callback.message.edit_text(text="Menu",
                                         reply_markup=keyboards.main_menu_keyboard())
