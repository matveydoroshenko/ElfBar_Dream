import random
import datetime
from data.items import create_items_list
from db_tg.db import Database
from aiogram import Dispatcher, Bot
from aiogram.dispatcher import FSMContext
from aiogram.utils.markdown import hitalic, hbold
from aiogram.types import CallbackQuery, ParseMode
from tgbot.config import load_config
from tgbot.misc.states import EditText, Product
from tgbot.keyboards.inline import text_callback, admin_keyboard, sub_admin_keyboard, add_delete_admin_keyboard, \
    back_to_edit_text_keyboard, texts, back_to_add_product_keyboard, main_keyboard, products_list, product_callback, \
    order, order_callback, delete_callback, delete, back_to_admin_keyboard, puffs_callback, categories, \
    puffs_product_callback


async def admin_menu(call: CallbackQuery):
    db = Database()
    text = db.select_text(position="/start")[0]
    await call.message.edit_text(text=text, reply_markup=sub_admin_keyboard)


async def add_delete_product(call: CallbackQuery):
    db = Database()
    text = db.select_text(position="/start")[0]
    await call.message.edit_text(text=text,
                                 reply_markup=add_delete_admin_keyboard)


async def edit_text(call: CallbackQuery):
    db = Database()
    text = db.select_text(position="/start")[0]
    await call.message.edit_text(text=text,
                                 reply_markup=texts())


async def back_to_admin(call: CallbackQuery, state: FSMContext):
    db = Database()
    text = db.select_text(position="/start")[0]
    await call.message.edit_text(text=text, reply_markup=admin_keyboard)
    await state.finish()


async def back_to_sub_admin(call: CallbackQuery, state: FSMContext):
    db = Database()
    text = db.select_text(position="/start")[0]
    await call.message.edit_text(text=text, reply_markup=sub_admin_keyboard)
    await state.finish()


async def back_to_edit_text(call: CallbackQuery, state: FSMContext):
    db = Database()
    text = db.select_text(position="/start")[0]
    await call.message.edit_text(text=text, reply_markup=texts())
    await state.finish()


async def back_to_add_product(call: CallbackQuery, state: FSMContext):
    db = Database()
    text = db.select_text(position="/start")[0]
    await call.message.edit_text(text=text, reply_markup=add_delete_admin_keyboard)
    await state.finish()


async def back_to_user(call: CallbackQuery, state: FSMContext):
    db = Database()
    text = db.select_text(position="/start")[0]
    await call.message.edit_text(text=text, reply_markup=main_keyboard())
    await state.finish()


async def back_to_list(call: CallbackQuery, state: FSMContext):
    db = Database()
    text = db.select_text(position="/start")[0]
    data = await state.get_data()
    puffs = data.get("puffs_number")
    await call.message.delete()
    await call.message.answer(text=text, reply_markup=products_list(puffs))
    await state.finish()


async def back_to_categories(call: CallbackQuery, state: FSMContext):
    await call.message.delete()
    await call.message.answer(text="💨 Выбери кол-во тяг:", reply_markup=categories())
    await state.finish()


async def edit_text_buttons(call: CallbackQuery, callback_data: dict, state: FSMContext):
    db = Database()
    position = callback_data.get("position")
    await state.update_data(position=position)
    current_text = db.select_text(position=position)[0]
    text = ("Текущий текст:",
            "",
            hitalic(current_text),
            "",
            "Введите новый текст:")
    await EditText.new_text.set()
    await call.message.edit_text(text="\n".join(text),
                                 reply_markup=back_to_edit_text_keyboard,
                                 parse_mode=ParseMode.HTML)


async def add_product(call: CallbackQuery):
    await Product.name.set()
    await call.message.edit_text(text="Введите название товара: ", reply_markup=back_to_add_product_keyboard)


async def contacts(call: CallbackQuery):
    db = Database()
    text = db.select_text(position="Контакты")[0]
    await call.message.edit_text(text=text, reply_markup=main_keyboard())


async def products(call: CallbackQuery):
    await call.message.edit_text(text="💨 Выбери кол-во тяг:", reply_markup=categories())


async def mailing(call: CallbackQuery, state: FSMContext):
    await call.message.edit_text("Введите текст для рассылки:", reply_markup=back_to_admin_keyboard)
    await state.set_state("mailing")


async def products_callback(call: CallbackQuery, callback_data: dict, state: FSMContext):
    await call.message.delete()
    item, puffs = create_items_list(item_id=callback_data.get("item_id"))
    text = """{name}
    
{description}"""

    await call.message.answer_photo(photo=item.photo,
                                    caption=text.format(name=item.name, description=item.description),
                                    reply_markup=order(item_id=callback_data.get("item_id")))
    await state.update_data(puffs_number=puffs)


async def order_callback_buttons(call: CallbackQuery, callback_data: dict):
    db = Database()
    await call.message.delete()
    config = load_config(".env")
    bot = Bot(token=config.tg_bot.token, parse_mode='HTML')
    product = db.select_product(item_id=callback_data.get("item_id"))
    time = call.message.date - datetime.timedelta(hours=2)
    number = random.randint(1000000, 9999999)
    if call.message.chat.username is not None:
        text = (hbold("✅ Заказ успешно оформлен ✅\n"),
                f"📦 Номер заказа: №{random.randint(1000000, 9999999)}\n",
                f"⏰ Время заказа: {time}\n",
                hbold("📍С вами скоро свяжется менеджер ✨"))
        admin_text = (f"Товар: {product[1]}",
                      f"Никнейм: @{call.message.chat.username}")
    elif call.message.chat.username is None:
        text = (hbold("✅ Заказ успешно оформлен ✅\n"),
                f"📦 Номер заказа: №{number}\n",
                f"⏰ Время заказа: {time}\n",
                hbold("📍Отправьте номер заказа менеджеру: @elfbar_dream_manager ✨"))
        admin_text = (f"Товар: {product[1]}",
                      f"Нет ника!",
                      f"Номер заказа: {number}")
    for chat_id in config.tg_bot.admin_ids:
        await bot.send_message(chat_id=chat_id, text="\n".join(admin_text))
    await call.message.answer("\n".join(text), parse_mode=ParseMode.HTML)
    text = db.select_text(position="/start")[0]
    await call.message.answer(text, reply_markup=main_keyboard())


async def delete_product(call: CallbackQuery):
    await call.message.edit_text("Выберите товар:", reply_markup=delete())


async def delete_callback_buttons(call: CallbackQuery, callback_data: dict):
    db = Database()
    db.delete_product(item_id=callback_data.get("item_id"))
    await call.message.delete()
    await call.message.answer("Товар успешно удалён")
    text = db.select_text(position="/start")[0]
    await call.message.answer(text, reply_markup=admin_keyboard)


async def puffs_product(call: CallbackQuery, callback_data: dict):
    puffs_number = callback_data.get("puffs_number")
    await call.message.edit_text(text="🤤 Выбери вкус:", reply_markup=products_list(puffs_number))


async def product_puffs(call: CallbackQuery, state: FSMContext, callback_data: dict):
    db = Database()
    await state.update_data(product_puffs=callback_data.get("puffs_number"))
    data = await state.get_data()
    photo = data.get("product_photo")
    name = data.get("product_name")
    description = data.get("product_description")
    puffs = data.get("product_puffs")
    text = (name,
            "",
            description,
            "",
            f"Кол-во тяг: {puffs}")
    db.add_product(name=name, description=description, photo=photo, puffs_number=puffs)
    await call.message.answer_photo(photo=photo, caption="\n".join(text))
    await call.message.answer("Товар успешно добавлен!")
    text = db.select_text(position="/start")[0]
    await call.message.answer(text, reply_markup=admin_keyboard)
    await state.finish()


async def reviews(call: CallbackQuery):
    db = Database()
    text = db.select_text(position="Отзывы")[0]
    await call.message.edit_text(text=text, reply_markup=main_keyboard())


async def original(call: CallbackQuery):
    db = Database()
    text = db.select_text(position="Оригинальность")[0]
    await call.message.edit_text(text=text, reply_markup=main_keyboard())


def register_inline(dp: Dispatcher):
    dp.register_callback_query_handler(admin_menu, text="admin_menu", state="*", is_admin=True)
    dp.register_callback_query_handler(add_delete_product, text="add_delete_product", state="*", is_admin=True)
    dp.register_callback_query_handler(edit_text, text="edit_text", state="*", is_admin=True)
    dp.register_callback_query_handler(edit_text_buttons, text_callback.filter(), state="*", is_admin=True)
    dp.register_callback_query_handler(delete_callback_buttons, delete_callback.filter(), state="*", is_admin=True)
    dp.register_callback_query_handler(add_product, text="add_product", state="*", is_admin=True)
    dp.register_callback_query_handler(delete_product, text="delete_product", is_admin=True)
    dp.register_callback_query_handler(contacts, text="contacts", state="*")
    dp.register_callback_query_handler(products, text="products", state="*")
    dp.register_callback_query_handler(products_callback, product_callback.filter(), state="*")
    dp.register_callback_query_handler(order_callback_buttons, order_callback.filter(), state="*")
    dp.register_callback_query_handler(mailing, text="mailing", state="*", is_admin=True)
    dp.register_callback_query_handler(product_puffs, puffs_callback.filter(), state="puffs")
    dp.register_callback_query_handler(puffs_product, puffs_product_callback.filter(), state="*")
    dp.register_callback_query_handler(reviews, text="reviews", state="*")
    dp.register_callback_query_handler(original, text="original", state="*")
    dp.register_callback_query_handler(back_to_admin, text="back_to_admin", state="*", is_admin=True)
    dp.register_callback_query_handler(back_to_sub_admin, text="back_to_sub_admin", state="*", is_admin=True)
    dp.register_callback_query_handler(back_to_edit_text, text="back_to_edit_text", state="*", is_admin=True)
    dp.register_callback_query_handler(back_to_add_product, text="back_to_add_product", state="*", is_admin=True)
    dp.register_callback_query_handler(back_to_user, text="back_to_user", state="*")
    dp.register_callback_query_handler(back_to_list, text="back_to_list", state="*")
    dp.register_callback_query_handler(back_to_categories, text="back_to_categories", state="*")
