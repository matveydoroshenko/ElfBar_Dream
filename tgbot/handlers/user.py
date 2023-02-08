import sqlite3
from aiogram import Dispatcher, Bot
from aiogram.types import Message, ContentType
from db_tg.db import Database
from tgbot.keyboards.inline import main_keyboard, admin_keyboard, back_to_add_product_keyboard, puffs_keyboard
from tgbot.misc.states import Product
from aiogram.dispatcher import FSMContext
from tgbot.config import load_config


async def user_start(message: Message):
    db = Database()
    try:
        db.add_user(user_id=message.chat.id)
    except sqlite3.IntegrityError:
        pass
    text = db.select_text(position="/start")[0]
    await message.answer(text=text, reply_markup=main_keyboard())


async def new_text(message: Message, state: FSMContext):
    db = Database()
    data = await state.get_data()
    position = data.get("position")
    db.update_text(position=position, text=message.text)
    await message.answer(text="Текст успешно изменён", reply_markup=admin_keyboard)
    await state.finish()


async def product_name(message: Message, state: FSMContext):
    await state.update_data(product_name=message.text)
    await Product.description.set()
    await message.answer("Введите описание товара:", reply_markup=back_to_add_product_keyboard)


async def product_description(message: Message, state: FSMContext):
    await state.update_data(product_description=message.text)
    await Product.photo.set()
    await message.answer("Отправьте фото для товара:", reply_markup=back_to_add_product_keyboard)


async def product_photo(message: Message, state: FSMContext):
    await state.update_data(product_photo=message.photo[-1].file_id)
    await message.answer("Выберите кол-во тяг:", reply_markup=puffs_keyboard)
    await state.set_state("puffs")


async def mailing(message: Message, state: FSMContext):
    db = Database()
    all_users = db.select_all_users()
    config = load_config(".env")
    bot = Bot(token=config.tg_bot.token, parse_mode='HTML')
    for user in all_users:
        user = user[0]
        await bot.send_message(chat_id=user, text=message.text)
    await state.finish()
    await message.answer("Рассылка завершена!", reply_markup=admin_keyboard)


def register_user(dp: Dispatcher):
    dp.register_message_handler(user_start, commands=["start"], state="*")
    dp.register_message_handler(new_text, state="EditText:new_text")
    dp.register_message_handler(product_name, state="Product:name")
    dp.register_message_handler(product_description, state="Product:description")
    dp.register_message_handler(product_photo, state="Product:photo", content_types=ContentType.PHOTO)
    dp.register_message_handler(mailing, state="mailing")

