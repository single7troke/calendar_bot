from aiogram import types, Router
from aiogram.filters import Command

from core import utils, keyboards

router = Router()


@router.message(Command(commands=("next",)))
async def next_event(message: types.Message):
    data = await utils.event_list()
    events = data["events"]
    event = await utils.event_details(events[0]["id"])
    await message.answer(f"<b>{event['summary']} - {event['start']}</b>\n\n"
                         f"{event['description']}")


@router.message(Command(commands=("list",)))
async def events_list(message: types.Message):
    data = await utils.event_list()
    events = data["events"]
    keyboard = keyboards.google_events_keyboard(events)

    await message.answer(text="Events:", reply_markup=keyboard)


@router.callback_query(keyboards.GoogleEventCallback.filter())
async def event_list_callbacks(
        callback: types.CallbackQuery,
        callback_data: keyboards.GoogleEventCallback):
    event = await utils.event_details(callback_data.event_id)
    await callback.message.edit_text(f"<b>{event['summary']} - {event['start']}</b>\n\n{event['description']}",
                                     reply_markup=keyboards.back_button(text="back to list",
                                                                        callback_data="event_list"))
    await callback.answer()


@router.callback_query(keyboards.BackButtonCallback.filter())
async def back_to_event_list_callback(
        callback: types.CallbackQuery,
        callback_data: keyboards.BackButtonCallback):
    data = await utils.event_list()
    events = data["events"]
    keyboard = keyboards.google_events_keyboard(events)

    await callback.message.edit_text(text="Events:", reply_markup=keyboard)
