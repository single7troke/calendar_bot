from aiogram.fsm.state import State, StatesGroup


class BasicForm(StatesGroup):
    user_id = State()
    user_name = State()


class UserForm(BasicForm):
    menu = State()


class DeleteUserForm(BasicForm):
    confirm = State()


class SaveUserForm(BasicForm):
    confirm = State()
