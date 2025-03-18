from typing_extensions import Any
from aiogram.types import ReplyKeyboardMarkup, ReplyKeyboardRemove, KeyboardButton

from database.database_manager import SQLActionManager as SAM

db_products = SAM().products
db_users = SAM().users

btn_lang_option = ReplyKeyboardMarkup(resize_keyboard=True, keyboard=[
    [KeyboardButton(text='RU 🇷🇺'), KeyboardButton(text='UZ 🇸🇱')]
])

btn_registration_ru = ReplyKeyboardMarkup(resize_keyboard=True, keyboard=[[KeyboardButton(text='Зарегистрироваться')]])
btn_registration_uz = ReplyKeyboardMarkup(resize_keyboard=True, keyboard=[[KeyboardButton(text="Ro'yxatdan o'tish")]])

btn_send_contact_ru = ReplyKeyboardMarkup(resize_keyboard=True, keyboard=[
    [KeyboardButton(text='Поделиться контактом', request_contact=True)]
])

btn_send_contact_uz = ReplyKeyboardMarkup(resize_keyboard=True, keyboard=[
    [KeyboardButton(text="Kontaktni baham ko'ring", request_contact=True)]
])

btn_back_ru = ReplyKeyboardMarkup(resize_keyboard=True, keyboard=[[KeyboardButton(text='Назад')]])
btn_back_uz = ReplyKeyboardMarkup(resize_keyboard=True, keyboard=[[KeyboardButton(text='Orqaga')]])


def btn_start_menu(lang: str, tg_id: int) -> Any:
    status_user = db_users.staff_manager(tg_id)
    btn = None
    if status_user == 'CLIENT':
        btn = [
            [KeyboardButton(text='Посмотреть категории 📚' if lang == 'RU' else "Kategoriyalarni ko'rish 📚")],
            [KeyboardButton(text='Обратная связь 📞' if lang == 'RU' else "Fikr-mulohaza 📞")],
            [KeyboardButton(text='Отзывы покупателей 👩‍💻👨‍💻' if lang == 'RU' else "Mijozlarning sharhlari 👩‍💻👨‍💻")],
            [KeyboardButton(text='Корзина 🛒' if lang == 'RU' else "Savat 🛒")],
            [KeyboardButton(text='Поменять язык 🌍' if lang == 'RU' else "Tilni o'zgartiring 🌍")]
        ]
    elif status_user == 'ADMIN':
        btn = [
            [KeyboardButton(text='Работа с продуктом 🛠' if lang == 'RU' else "Mahsulot bilan ishlash 🛠")],
            [KeyboardButton(text='Посмотреть категории 📚' if lang == 'RU' else "Kategoriyalarni ko'rish 📚")],
            [KeyboardButton(text='Поменять язык 🌍' if lang == 'RU' else "Tilni o'zgartiring 🌍")],
            [KeyboardButton(text='Список отзывов 📜' if lang == 'RU' else "Natija ro'yxati 📜")],
            [KeyboardButton(text='Текущие Сделки 🤝' if lang == 'RU' else "Joriy Bitimlar 🤝")]
        ]
    elif status_user == 'CEO':
        btn = [
            [KeyboardButton(text='Работа с персоналом 🛠' if lang == 'RU' else "Xodimlar bilan ishlash 🛠")],
            [KeyboardButton(text='Посмотреть категории 📚' if lang == 'RU' else "Kategoriyalarni ko'rish 📚")],
            [KeyboardButton(text='Список отзывов 📜' if lang == 'RU' else "Natija ro'yxati 📜")],
            [KeyboardButton(text='Поменять язык 🌍' if lang == 'RU' else "Tilni o'zgartiring 🌍")],
            [KeyboardButton(text='Текущие Сделки 🤝' if lang == 'RU' else "Joriy Bitimlar 🤝")],
            [KeyboardButton(text='Информация по продажам 📖' if lang == 'RU' else "Savdo haqida ma'lumot 📖")]
        ]

    markup = ReplyKeyboardMarkup(resize_keyboard=True, keyboard=btn)

    return markup


def btn_list_categories(lang: str) -> Any:
    list_categories = db_products.show_list_categories(lang)
    btn = [
        [KeyboardButton(text=cat)] for cat in list_categories
    ]
    back = [KeyboardButton(text='Назад в меню 🔙' if lang == 'RU' else 'Menyuga qaytish 🔙')]
    btn.append(back)

    markup = ReplyKeyboardMarkup(resize_keyboard=True, keyboard=btn)
    return markup


def btn_list_products(list_products: tuple, lang: str) -> Any:
    btn = [[KeyboardButton(text=product_name)] for product_name in list_products]
    back = [KeyboardButton(text='Назад к категория 🔙' if lang == 'RU' else 'Orqaga kategoriya 🔙')]
    btn.append(back)

    markup = ReplyKeyboardMarkup(resize_keyboard=True, keyboard=btn)
    return markup


def btn_action_product(lang: str) -> Any:
    btn = [
        [KeyboardButton(text='Создать новый продукт 🛠' if lang == 'RU' else "Yangi mahsulot yarating 🛠")],
        [KeyboardButton(text='Создать новый категорию 🛠' if lang == 'RU' else "Yangi toifani yarating 🛠")],
        [KeyboardButton(text='Изменения продукта 📜' if lang == 'RU' else "Mahsulot o'zgarishi 📜")],
        [KeyboardButton(text='Назад 🔙' if lang == 'RU' else 'Orqaga 🔙')]
    ]

    markup = ReplyKeyboardMarkup(resize_keyboard=True, keyboard=btn)

    return markup


def btn_lang_choice(lang: str) -> Any:
    markup = ReplyKeyboardMarkup(resize_keyboard=True, keyboard=[
        [
            KeyboardButton(text='RU 🇷🇺'),
            KeyboardButton(text='UZ 🇸🇱')
        ],
        [
            KeyboardButton(text='Назад 🔙' if lang == 'RU' else 'Orqaga 🔙')
        ]
    ])
    return markup


def btn_filter_date(lang: str) -> Any:
    markup = ReplyKeyboardMarkup(resize_keyboard=True, keyboard=[
        [KeyboardButton(text='Назад в меню 🔙' if lang == 'RU' else 'Menyuga qaytish 🔙')],
        [KeyboardButton(text='Сегодняшний день' if lang == 'RU' else 'Bugungi kun')],
        [KeyboardButton(text='Вчерашний день' if lang == 'RU' else 'Kecha')],
        [KeyboardButton(text='Текущий месяц' if lang == 'RU' else 'Joriy oy')],
        [KeyboardButton(text='Текущий год' if lang == 'RU' else 'Joriy yil')],
        [KeyboardButton(text='Самому указать месяц и год' if lang == 'RU' else "Oy va yilni o'zingiz belgilang")],
    ])
    return markup


def btn_action_employee(lang: str) -> Any:
    markup = ReplyKeyboardMarkup(resize_keyboard=True, keyboard=[
        [KeyboardButton(text='Назад к меню 🔙' if lang == 'RU' else 'Menyuga qaytish 🔙')],
        [KeyboardButton(text='Список сотрудника 📃' if lang == 'RU' else "Xodimlar ro'yxati 📃")],
        [KeyboardButton(text='Удалить сотрудника ❌' if lang == 'RU' else 'Xodimni olib tashlang ❌')],
        [KeyboardButton(text='Изменить данный сотрудника ✏' if lang == 'RU' else "Ushbu xodimni o'zgartiring ✏")]
    ])
    return markup
