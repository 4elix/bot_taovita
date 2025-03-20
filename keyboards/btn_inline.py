from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from typing_extensions import Any

from database.database_manager import SQLActionManager as SAM

db_products = SAM().products
db_carts = SAM().carts


def btn_to_cart_menu(lang: str, product_id: int, price: int, current_quantity: int = 0) -> Any:

    inline = InlineKeyboardMarkup(inline_keyboard=[
        [
            InlineKeyboardButton(text='-', callback_data=f'minus_{product_id}_{current_quantity}'),
            InlineKeyboardButton(text=f'{current_quantity}', callback_data=f'empty?'),
            InlineKeyboardButton(text='+', callback_data=f'plus_{product_id}_{current_quantity}')
        ],
        [
            InlineKeyboardButton(text='Добавить в корзину' if lang == 'RU' else "Savatga qo'shing",
                                 callback_data=f'cart_{product_id}_{current_quantity}_{price}')
        ]
    ])
    return inline


def btn_apply(cart_id: int, lang: str) -> Any:
    btn = InlineKeyboardMarkup(inline_keyboard=[
        [
            InlineKeyboardButton(text='Оформить' if lang == 'RU' else 'Harid qabul qilinsin',
                                 callback_data=f'apply_{cart_id}'),
        ],
        [
            InlineKeyboardButton(text='Очистить корзину' if lang == 'RU' else "Axlat qutisini bo'shating",
                                 callback_data=f'clear_cart_{cart_id}'),
        ]
    ])

    return btn


def btn_action_change_product(lang: str) -> Any:
    btn = InlineKeyboardMarkup(inline_keyboard=[
        [
            InlineKeyboardButton(text='Изменить продукт ✏' if lang == 'RU' else "Mahsulotni o'zgartirish ✏",
                                 callback_data='edit_product')
        ],
        [
            InlineKeyboardButton(text='Удалить продукт ❌' if lang == 'RU' else 'Mahsulotni olib tashlang ❌',
                                 callback_data='delete_product')
        ],
        [
            InlineKeyboardButton(text='Назад 🔙' if lang == 'RU' else 'Orqaga 🔙',
                                 callback_data='back_menu_work_product')
        ]
    ])
    return btn


def btn_post(lang: str) -> Any:
    btn = InlineKeyboardMarkup(inline_keyboard=[
        [
            InlineKeyboardButton(text='Сделать администратором' if lang == 'RU' else 'Administrator qilish',
                                 callback_data='employee_change_admin')
        ],
        [
            InlineKeyboardButton(text='Сделать СЕО' if lang == 'RU' else 'SEO qilish',
                                 callback_data='employee_change_ceo')
        ]
    ])
    return btn


def btn_is_pay(cart_id: int, lang: str) -> Any:
    btn = InlineKeyboardMarkup(inline_keyboard=[
        [
            InlineKeyboardButton(text='Пользователь оплатил' if lang == 'RU' else "Foydalanuvchi to'ladi",
                                 callback_data=f'is_pay_{cart_id}')
        ]
    ])
    return btn


def btn_list_buyers(lang):
    list_buyers = db_carts.get_list_buyers()
    list_btn = [[InlineKeyboardButton(text=str(item[1]), callback_data=f'show_buyer_{item[0]}')] for item in list_buyers]
    back = [InlineKeyboardButton(text='Назад 🔙' if lang == 'RU' else 'Orqaga 🔙', callback_data='back_menu_work_product')]
    list_btn.append(back)

    btn = InlineKeyboardMarkup(inline_keyboard=list_btn)
    return btn
