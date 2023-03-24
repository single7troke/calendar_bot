from aiogram import types
from aiogram.filters.callback_data import CallbackData
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton, ReplyKeyboardMarkup, KeyboardButton

from core.utils import get_user
from core.config import Config

config = Config()


class GoogleEventCallback(CallbackData, prefix="id"):
    event_id: str


class UserListCallback(CallbackData, prefix="user"):
    user_id: str
    user_name: str


def google_events_keyboard(events) -> InlineKeyboardMarkup:
    buttons = list()
    for event in events:
        buttons.append(
            [types.InlineKeyboardButton(
                text=event["start"],
                callback_data=GoogleEventCallback(event_id=event["id"]).pack())]
        )
    keyboard = InlineKeyboardMarkup(inline_keyboard=buttons)
    return keyboard


async def user_list_keyboard(id_list: list) -> InlineKeyboardMarkup:
    buttons = list()
    for user_id in id_list:
        user = await get_user(user_id=user_id)
        if user["role"] in config.admin_roles:
            continue
        buttons.append(
            [InlineKeyboardButton(
                text=user["name"],
                callback_data=UserListCallback(user_id=user_id, user_name=user["name"]).pack()
            )]
        )
    keyboard = InlineKeyboardMarkup(inline_keyboard=buttons)
    return keyboard


def user_menu() -> ReplyKeyboardMarkup:
    keyboard = ReplyKeyboardMarkup(
        keyboard=[
            [
                KeyboardButton(text="Delete user"),
                KeyboardButton(text="Exit"),
            ]
        ],
        resize_keyboard=True,
    )
    return keyboard


def yes_no() -> ReplyKeyboardMarkup:
    keyboard = ReplyKeyboardMarkup(
        keyboard=[
            [
                KeyboardButton(text="Yes"),
                KeyboardButton(text="No"),
            ]
        ],
        resize_keyboard=True,
    )
    return keyboard


def cancel_button() -> ReplyKeyboardMarkup:
    keyboard = ReplyKeyboardMarkup(
        keyboard=[
            [
                KeyboardButton(text="Cancel"),
            ]
        ],
        resize_keyboard=True,
    )
    return keyboard
