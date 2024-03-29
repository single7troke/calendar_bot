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


class BackButtonCallback(CallbackData, prefix="back"):
    data: str


class MainMenuCallback(CallbackData, prefix="main_menu"):
    data: str


def main_menu_keyboard():
    buttons = [
        [types.InlineKeyboardButton(text=config.buttons.next, callback_data=MainMenuCallback(data="next").pack())],
        [types.InlineKeyboardButton(text=config.buttons.list, callback_data=MainMenuCallback(data="list").pack())]
    ]
    keyboard = types.InlineKeyboardMarkup(inline_keyboard=buttons)
    return keyboard


def back_button(callback_data, text=config.buttons.back):
    buttons = [
        [types.InlineKeyboardButton(text=text, callback_data=BackButtonCallback(data=callback_data).pack())]]
    keyboard = types.InlineKeyboardMarkup(inline_keyboard=buttons)
    return keyboard


def google_events_keyboard(events) -> InlineKeyboardMarkup:
    buttons = list()
    for event in events:
        text = f'{event["start"]} {event["summary"].split("/")[-1]}' \
            if "отсутствует" not in event["summary"] else event["start"]
        buttons.append(
            [types.InlineKeyboardButton(
                text=text,
                callback_data=GoogleEventCallback(event_id=event["id"]).pack())]
        )
    buttons.append(
        [types.InlineKeyboardButton(text=config.buttons.back,
                                    callback_data=BackButtonCallback(data="menu").pack())
         ]
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
