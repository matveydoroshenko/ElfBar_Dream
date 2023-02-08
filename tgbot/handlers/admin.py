from aiogram import Dispatcher
from aiogram.types import Message

from tgbot.keyboards.inline import admin_keyboard, sub_admin_keyboard


async def admin_start(message: Message):
    await message.answer(text=f"Привет, {message.chat.full_name}!", reply_markup=sub_admin_keyboard)


def register_admin(dp: Dispatcher):
    dp.register_message_handler(admin_start, commands=["start"], state="*", is_admin=True)
