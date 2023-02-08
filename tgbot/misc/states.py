from aiogram.dispatcher.filters.state import State, StatesGroup


class EditText(StatesGroup):
    new_text = State()


class Product(StatesGroup):
    name = State()
    description = State()
    photo = State()
