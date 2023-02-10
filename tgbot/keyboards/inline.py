from aiogram.utils.callback_data import CallbackData
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

from db_tg.db import Database

product_callback = CallbackData("product", "item_id")
text_callback = CallbackData("text", "position")
order_callback = CallbackData("order", "item_id")
delete_callback = CallbackData("delete", "item_id")
puffs_callback = CallbackData("puffs", "puffs_number")
puffs_product_callback = CallbackData("puffs_product", "puffs_number")

admin_keyboard = InlineKeyboardMarkup()
sub_admin_keyboard = InlineKeyboardMarkup()
add_delete_admin_keyboard = InlineKeyboardMarkup()
back_to_admin_keyboard = InlineKeyboardMarkup()
back_to_edit_text_keyboard = InlineKeyboardMarkup()
back_to_add_product_keyboard = InlineKeyboardMarkup()
puffs_keyboard = InlineKeyboardMarkup()

admin_menu_button = InlineKeyboardButton(text="Панель админа", callback_data="admin_menu")
add_delete_product_button = InlineKeyboardButton(text="Добавить/Удалить товар", callback_data="add_delete_product")
add_product_button = InlineKeyboardButton(text="Добавить товар", callback_data="add_product")
delete_product_button = InlineKeyboardButton(text="Удалить товар", callback_data="delete_product")
edit_text_button = InlineKeyboardButton(text="Изменить текст", callback_data="edit_text")
mailing_button = InlineKeyboardButton(text="Рассылка", callback_data="mailing")
back_to_admin_button = InlineKeyboardButton(text="Назад ↩️", callback_data="back_to_admin")
back_to_sub_admin_button = InlineKeyboardButton(text="Назад ↩️", callback_data="back_to_sub_admin")
back_to_edit_text_button = InlineKeyboardButton(text="Назад ↩️", callback_data="back_to_edit_text")
back_to_add_product_button = InlineKeyboardButton(text="Назад ↩️", callback_data="back_to_add_product")
back_to_user_button = InlineKeyboardButton(text="Назад ↩️", callback_data="back_to_user")
back_to_categories_button = InlineKeyboardButton(text="Назад ↩️", callback_data="back_to_categories")
back_to_list_button = InlineKeyboardButton(text="Назад ↩️", callback_data="back_to_list")
puffs_1500_button = InlineKeyboardButton(text="1500", callback_data=puffs_callback.new(puffs_number=1500))
puffs_2000_button = InlineKeyboardButton(text="2000", callback_data=puffs_callback.new(puffs_number=2000))
puffs_2500_button = InlineKeyboardButton(text="2500", callback_data=puffs_callback.new(puffs_number=2500))
puffs_3600_button = InlineKeyboardButton(text="3600", callback_data=puffs_callback.new(puffs_number=3600))
puffs_4000_button = InlineKeyboardButton(text="4000", callback_data=puffs_callback.new(puffs_number=4000))
puffs_5000_button = InlineKeyboardButton(text="5000", callback_data=puffs_callback.new(puffs_number=5000))

admin_keyboard.add(admin_menu_button)
sub_admin_keyboard.add(add_delete_product_button)
sub_admin_keyboard.add(edit_text_button)
sub_admin_keyboard.add(mailing_button)
sub_admin_keyboard.add(back_to_admin_button)
add_delete_admin_keyboard.add(add_product_button)
add_delete_admin_keyboard.add(delete_product_button)
add_delete_admin_keyboard.add(back_to_sub_admin_button)
puffs_keyboard.add(puffs_1500_button)
puffs_keyboard.add(puffs_2000_button)
puffs_keyboard.add(puffs_2500_button)
puffs_keyboard.add(puffs_3600_button)
puffs_keyboard.add(puffs_4000_button)
puffs_keyboard.add(puffs_5000_button)
back_to_admin_keyboard.add(back_to_admin_button)
back_to_edit_text_keyboard.add(back_to_edit_text_button)
back_to_add_product_keyboard.add(back_to_add_product_button)


def texts():
    db = Database()
    positions = db.select_all_positions_texts()
    keyboard = InlineKeyboardMarkup()
    for position in positions:
        button = InlineKeyboardButton(text=position[0], callback_data=text_callback.new(position=position[0]))
        keyboard.add(button)
    keyboard.add(back_to_sub_admin_button)
    return keyboard


def delete():
    db = Database()
    buttons_data = db.select_all_product_names_id()
    keyboard = InlineKeyboardMarkup()
    for button_data in buttons_data:
        button = InlineKeyboardButton(text=button_data[0], callback_data=delete_callback.new(item_id=button_data[1]))
        keyboard.add(button)
    keyboard.add(back_to_add_product_button)
    return keyboard


def products_list(puffs_number):
    db = Database()
    puffs_number = int(puffs_number)
    buttons_data = db.select_all_product_names_id_puffs()
    keyboard = InlineKeyboardMarkup()
    for button_data in buttons_data:
        if button_data[2] == puffs_number:
            button = InlineKeyboardButton(text=button_data[0],
                                          callback_data=product_callback.new(item_id=button_data[1]))
            keyboard.add(button)
    keyboard.add(back_to_categories_button)
    return keyboard


def categories():
    db = Database()
    puffs = db.select_all_puffs()
    puffs = list(set(puffs))
    puffs.sort()
    keyboard = InlineKeyboardMarkup()
    for puff in puffs:
        puff = puff[0]
        button = InlineKeyboardButton(text=f"{puff} тяг", callback_data=puffs_product_callback.new(puffs_number=puff))
        keyboard.add(button)
    keyboard.add(back_to_user_button)
    return keyboard


def order(item_id):
    keyboard = InlineKeyboardMarkup()
    button = InlineKeyboardButton(text="Оформить заказ", callback_data=order_callback.new(item_id))
    keyboard.add(button)
    keyboard.add(back_to_list_button)
    return keyboard


def main_keyboard():
    db = Database()
    text = db.select_text(position="Кнопка списка товаров")[0]
    url = db.select_text(position="Оригинальность")[0]
    keyboard = InlineKeyboardMarkup()
    contacts_button = InlineKeyboardButton(text="📞 Контакты 📞", callback_data="contacts")
    button = InlineKeyboardButton(text=text, callback_data="products")
    reviews_button = InlineKeyboardButton(text="💭 Отзывы 💭", callback_data="reviews")
    original_button = InlineKeyboardButton(text="☑️ Оригинальность ☑️", url=url)
    keyboard.add(button)
    keyboard.add(contacts_button)
    keyboard.add(reviews_button)
    keyboard.add(original_button)
    return keyboard
