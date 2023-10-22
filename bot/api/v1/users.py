import re

from aiogram import Router
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.types import (
    CallbackQuery,
    Message,
    ReplyKeyboardRemove,
)
from core import utils, keyboards, forms

router = Router()


async def cancel_handler(message: Message, state: FSMContext = None) -> None:
    """
    Allow user to cancel any action
    """
    if state:
        await state.clear()
    await message.answer(
        "Cancelled.",
        reply_markup=ReplyKeyboardRemove()
    )


@router.message(Command("new_user"))
async def new_user(message: Message, state: FSMContext):
    await state.set_state(forms.UserForm.user_id)
    await message.answer(
        "Enter user id",
        reply_markup=keyboards.cancel_button()
    )


@router.message(forms.UserForm.user_id)
async def set_user_id(message: Message, state: FSMContext):
    user_id = message.text
    cancel_button = keyboards.cancel_button()
    if user_id == "Cancel":
        await cancel_handler(message=message, state=state)
    elif not user_id.isdigit() or not len(user_id) in [9, 10]:
        await message.answer("Invalid id.\n"
                             "id should be nine-digit number\n"
                             "Try again",
                             reply_markup=cancel_button)
    elif await utils.get_user(user_id=user_id):
        await message.answer(f"User with id: {user_id} already exists.\n"
                             f"Try again",
                             reply_markup=cancel_button)
    else:
        await state.update_data(user_id=user_id)
        await state.set_state(forms.UserForm.user_name)
        await message.answer("Enter user name",
                             reply_markup=cancel_button)


@router.message(forms.UserForm.user_name)
async def set_user_name(message: Message, state: FSMContext):
    text = message.text
    if text == "Cancel":
        await cancel_handler(message=message, state=state)
    elif re.match(pattern="^[a-zA-Z0-9 _-]*$", string=text) and len(text) <= 20:
        await state.update_data(user_name=text)
        user_data = await state.get_data()
        await state.set_state(forms.SaveUserForm.confirm)
        await message.answer(f"Save user with id {user_data['user_id']}\n"
                             f"and username {user_data['user_name']}?",
                             reply_markup=keyboards.yes_no())
    else:
        keyboard = keyboards.cancel_button()
        await message.answer("Invalid user name\n"
                             "User name should be max 20 simbols.\n"
                             "Only letters, digits, spaces, '-' and '_' available.\n"
                             "Please try one more time.",
                             reply_markup=keyboard)


@router.message(forms.SaveUserForm.confirm)
async def save_new_user(message: Message, state: FSMContext):
    data = await state.get_data()
    if message.text == "Yes":
        saved = await utils.create_or_update_user(user_id=data["user_id"],
                                                  name=data["user_name"])
        if saved:
            await message.answer(f"User with id <b>{data['user_id']}</b>\n"
                                 f"and user name <b>{data['user_name']}</b>\n"
                                 "was saved",
                                 reply_markup=ReplyKeyboardRemove())
            await state.clear()
        else:
            await message.answer(f"User <b>{data['user_name']}</b> Wasn't created.\n"
                                 f"Try later.")
            await cancel_handler(message=message, state=state)
    else:
        await cancel_handler(message=message, state=state)


@router.message(Command("user_list"))
async def all_users(message: Message):
    data = await utils.get_all_users()
    users_id = data["users_id"]
    keyboard = await keyboards.user_list_keyboard(id_list=users_id)
    await message.answer(text="Users:", reply_markup=keyboard)


@router.callback_query(keyboards.UserListCallback.filter())
async def user_list_callback(
        callback: CallbackQuery,
        callback_data: keyboards.UserListCallback,
        state: FSMContext):
    await state.update_data(user_id=callback_data.user_id, user_name=callback_data.user_name)

    keyboard = keyboards.user_menu()
    await state.set_state(forms.UserForm.menu)
    await callback.message.answer(callback_data.user_name, reply_markup=keyboard)


@router.message(forms.UserForm.menu)
async def user_menu(message: Message, state: FSMContext):
    data = await state.get_data()
    keyboard = keyboards.yes_no()
    text = message.text
    if text == "Delete user":
        await state.set_state(forms.DeleteUserForm.confirm)
        await message.answer(text=f"Delete user {data['user_name']}?",
                             reply_markup=keyboard)
    else:
        await cancel_handler(message=message, state=state)


@router.message(forms.DeleteUserForm.confirm)
async def delete_user(message: Message, state: FSMContext):
    text = message.text
    data = await state.get_data()
    if text == "Yes":
        deleted = await utils.delete_user(data["user_id"])
        if deleted:
            await message.answer(f"User <b>{data['user_name']}</b> was deleted.",
                                 reply_markup=ReplyKeyboardRemove())
            await state.clear()
        else:
            await message.answer(f"User <b>{data['user_name']}</b> Wasn't deleted.\n"
                                 f"Try later.")
            await cancel_handler(message=message, state=state)
    else:
        await cancel_handler(message=message, state=state)
