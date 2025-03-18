import random
import datetime

from aiogram import Router, F, Bot
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, FSInputFile

from ghostwriter import *
from keyboards.btn_text import *
from keyboards.btn_inline import *
from database.database_manager import SQLActionManager as SAM
from support import get_day, get_year, get_month, get_yesterday, write_excel_feedback
from utils import CreateProductState, CreateCategoryState, GetDateState

txt_admin_router = Router()

db_products = SAM().products
db_users = SAM().users
db_carts = SAM().carts


@txt_admin_router.message(F.text.in_(['Работа с продуктом 🛠', 'Mahsulot bilan ishlash 🛠']))
async def react_btn_work_product(message: Message):
    chat_id = message.chat.id
    lang = db_users.get_lang(chat_id)
    status = db_users.staff_manager(chat_id)
    if status == 'CLIENT' or status == '404':
        await message.answer('Ошибка' if lang == 'RU' else 'Xato', reply_markup=btn_start_menu(lang, chat_id))
    else:
        await message.answer('Хорошо, выберите действия' if lang == 'RU' else 'OK, harakatlarni tanlang',
                             reply_markup=btn_action_product(lang))


@txt_admin_router.message(F.text.in_(['Создать новый категорию 🛠', 'Yangi toifani yarating 🛠']))
async def create_new_category(message: Message, state: FSMContext):
    chat_id = message.chat.id
    lang = db_users.get_lang(chat_id)
    status = db_users.staff_manager(chat_id)
    if status == 'CLIENT' or status == '404':
        await message.answer('Ошибка' if lang == 'RU' else 'Xato', reply_markup=btn_start_menu(lang, chat_id))
    else:
        await message.answer('На каком языке будет категория' if lang == 'RU' else "Kategoriya qaysi tilda bo'ladi",
                             reply_markup=btn_lang_choice(lang))
        await state.set_state(CreateCategoryState.lang)


@txt_admin_router.message(CreateCategoryState.lang)
async def get_lang_category(message: Message, state: FSMContext):
    chat_id = message.chat.id
    lang = db_users.get_lang(chat_id)

    if message.text == 'Назад 🔙' or message.text == 'Orqaga 🔙':
        await message.answer('Хорошо' if lang == 'RU' else 'Yaxshi', reply_markup=btn_start_menu(lang, chat_id))
        await state.clear()
    else:
        lang_for_category = message.text[:2]
        if lang_for_category == 'RU' or lang_for_category == 'UZ':
            await state.update_data(lang=lang_for_category)
            await message.answer('Введите имя категории' if lang == 'RU' else 'Kategoriya nomini kiriting',
                                 reply_markup=ReplyKeyboardRemove())
            await state.set_state(CreateCategoryState.cat_name)
        else:
            await message.answer('Нажмите на кнопку' if lang == 'RU' else 'Tugmani bosing',
                                 reply_markup=btn_lang_option)


@txt_admin_router.message(CreateCategoryState.cat_name)
async def save_category(message: Message, state: FSMContext):
    chat_id = message.chat.id
    cat_name = message.text
    lang = db_users.get_lang(chat_id)
    data = await state.get_data()
    lang_for_category = data['lang']

    db_products.save_category(lang_for_category, cat_name)
    await state.clear()
    await message.answer('Категория сохранения' if lang == 'RU' else "Saqlash toifasi",
                         reply_markup=btn_action_product(lang))


@txt_admin_router.message(F.text.in_(['Создать новый продукт 🛠', 'Yangi mahsulot yarating 🛠']))
async def create_new_product(message: Message, state: FSMContext):
    chat_id = message.chat.id
    lang = db_users.get_lang(chat_id)
    status = db_users.staff_manager(chat_id)
    if status == 'CLIENT' or status == '404':
        await message.answer('Ошибка' if lang == 'RU' else 'Xato', reply_markup=btn_start_menu(lang, chat_id))
    else:
        await message.answer('На каком языке будет продукт' if lang == 'RU' else "Mahsulot qaysi tilda bo'ladi",
                             reply_markup=btn_lang_choice(lang))
        await state.set_state(CreateProductState.lang)


@txt_admin_router.message(CreateProductState.lang)
async def get_lang_product(message: Message, state: FSMContext):
    chat_id = message.chat.id
    lang = db_users.get_lang(chat_id)

    if message.text == 'Назад 🔙' or message.text == 'Orqaga 🔙':
        await message.answer('Хорошо' if lang == 'RU' else 'Yaxshi', reply_markup=btn_start_menu(lang, chat_id))
        await state.clear()
    else:
        lang_for_product = message.text[:2]
        if lang_for_product == 'RU' or lang_for_product == 'UZ':
            await state.update_data(lang=lang_for_product)
            await message.answer('Введите название продукта' if lang == 'RU' else "Mahsulot nomini kiriting",
                                 reply_markup=ReplyKeyboardRemove())
            await state.set_state(CreateProductState.title)
        else:
            await message.answer('Нажмите на кнопку' if lang == 'RU' else 'Tugmani bosing',
                                 reply_markup=btn_lang_choice(lang))


@txt_admin_router.message(CreateProductState.title)
async def get_title_product(message: Message, state: FSMContext):
    title = message.text
    chat_id = message.chat.id
    lang = db_users.get_lang(chat_id)

    await state.update_data(title=title)
    await message.answer('Введите стоимость продукта' if lang == 'RU' else "Mahsulot narxini kiriting")
    await state.set_state(CreateProductState.price)


@txt_admin_router.message(CreateProductState.price)
async def get_price_product(message: Message, state: FSMContext):
    chat_id = message.chat.id
    lang = db_users.get_lang(chat_id)

    price = message.text
    check_price = price.isdigit()
    if check_price is True:
        await state.update_data(price=int(price))
        await message.answer('Введите описание продукта' if lang == 'RU' else "Mahsulot tavsifini kiriting")
        await state.set_state(CreateProductState.description)
    else:
        text = error_text_get_price[lang]
        await message.answer(text)
        await state.set_state(CreateProductState.price)


@txt_admin_router.message(CreateProductState.description)
async def get_description_product(message: Message, state: FSMContext):
    description = message.text
    chat_id = message.chat.id
    lang = db_users.get_lang(chat_id)

    await state.update_data(description=description)
    await message.answer('Отправьте фотографию продукта' if lang == 'RU' else "Mahsulot fotosuratini yuboring")
    await state.set_state(CreateProductState.image_path)


@txt_admin_router.message(CreateProductState.image_path, F.photo)
async def get_photo_product(message: Message, state: FSMContext, bot: Bot):
    chat_id = message.chat.id
    lang = db_users.get_lang(chat_id)

    photo = message.photo[-1]
    file_id = photo.file_id
    file_info = await bot.get_file(file_id)
    file_path = file_info.file_path

    get_random_num = random.randint(4000, 8000)
    new_file_id = str(get_random_num) + str(file_id) + str(get_random_num)[::-1][:4]
    path = f"media/images/photo_{new_file_id}.jpg"

    await bot.download_file(file_path, path)
    await state.update_data(image_path=path)
    await message.answer(f'Введите название категории' if lang == 'RU' else "Kategoriya nomini kiriting")
    await state.set_state(CreateProductState.category_name)


@txt_admin_router.message(CreateProductState.category_name)
async def get_category_name_product(message: Message, state: FSMContext):
    chat_id = message.chat.id

    data = await state.get_data()

    lang_for_product = data['lang']
    title = data['title']
    price = data['price']
    description = data['description']
    image_path = data['image_path']
    category_name = message.text
    category_id = db_products.get_cat_id_for_name(category_name)
    await state.clear()

    lang = db_users.get_lang(chat_id)
    db_products.save_product((image_path, title, price, description, lang_for_product, category_id))

    await message.answer(
        'Продукт сохранен, выберете действия' if lang == 'RU' else "Mahsulot saqlanadi, amallarni tanlang",
        reply_markup=btn_start_menu(lang, chat_id))


@txt_admin_router.message(F.text.in_(['Изменения продукта 📜', "Mahsulot o'zgarishi 📜"]))
async def react_btn_change_product(message: Message):
    chat_id = message.chat.id
    lang = db_users.get_lang(chat_id)
    status = db_users.staff_manager(chat_id)
    if status == 'CLIENT' or status == '404':
        await message.answer('Ошибка' if lang == 'RU' else 'Xato', reply_markup=btn_start_menu(lang, chat_id))
    else:
        await message.answer('Хорошо' if lang == 'RU' else 'Yaxshi', reply_markup=ReplyKeyboardRemove())
        await message.answer('Выберите действия' if lang == 'RU' else 'Harakatlarni tanlang',
                             reply_markup=btn_action_change_product(lang))


@txt_admin_router.message(F.text.in_(['Назад 🔙', 'Orqaga 🔙', 'Menyuga qaytish 🔙', 'Назад в меню 🔙']))
async def react_btn_back(message: Message):
    chat_id = message.chat.id
    lang = db_users.get_lang(chat_id)
    await message.answer('Хорошо' if lang == 'RU' else 'Yaxshi', reply_markup=btn_start_menu(lang, chat_id))


@txt_admin_router.message(F.text.in_(['Список отзывов 📜', "Tilni o'zgartiring 📜"]))
async def react_btn_list_feedback(message: Message):
    chat_id = message.chat.id
    lang = db_users.get_lang(chat_id)
    status = db_users.staff_manager(chat_id)
    if status == 'CLIENT' or status == '404':
        await message.answer('Ошибка' if lang == 'RU' else 'Xato', reply_markup=btn_start_menu(lang, chat_id))
    else:
        await message.answer('Отзывы за' if lang == 'RU' else 'Sharhlar', reply_markup=btn_filter_date(lang))


@txt_admin_router.message(F.text.in_(['Сегодняшний день', 'Bugungi kun']))
async def show_feedback_by_now_day(message: Message):
    chat_id = message.chat.id
    lang = db_users.get_lang(chat_id)
    status = db_users.staff_manager(chat_id)
    if status == 'CLIENT' or status == '404':
        await message.answer('Ошибка' if lang == 'RU' else 'Xato', reply_markup=btn_start_menu(lang, chat_id))
    else:
        now_datetime = datetime.datetime.now()
        data = get_day(now_datetime)
        feedback_list = db_users.get_feedback('day', (data,))
        action = 'день'
        path = write_excel_feedback(feedback_list, action, chat_id)
        text = 'Вот отчет' if lang == 'RU' else 'Bu erda hisobot'
        await message.answer(text, reply_markup=btn_start_menu(lang, chat_id))
        text_file = 'Обратная связь за сегодняшний день' if lang == 'RU' else 'Bugungi kun uchun fikr-mulohazalar'
        await message.answer_document(text=text_file, document=FSInputFile(path))


@txt_admin_router.message(F.text.in_(['Вчерашний день', 'Kecha']))
async def show_feedback_by_now_yesterday(message: Message):
    chat_id = message.chat.id
    lang = db_users.get_lang(chat_id)
    status = db_users.staff_manager(chat_id)
    if status == 'CLIENT' or status == '404':
        await message.answer('Ошибка' if lang == 'RU' else 'Xato', reply_markup=btn_start_menu(lang, chat_id))
    else:
        now_datetime = datetime.datetime.now()
        data = get_yesterday(now_datetime)
        feedback_list = db_users.get_feedback('day', (data,))
        action = 'вчерашний день'
        path = write_excel_feedback(feedback_list, action, chat_id)
        text = 'Вот отчет' if lang == 'RU' else 'Bu erda hisobot'
        await message.answer(text, reply_markup=btn_start_menu(lang, chat_id))
        text_file = 'Обратная связь за вчерашний день' if lang == 'RU' else 'Kechagi fikr-mulohazalar'
        await message.answer_document(text=text_file, document=FSInputFile(path))


@txt_admin_router.message(F.text.in_(['Текущий месяц', 'Joriy oy']))
async def show_feedback_by_now_month(message: Message):
    chat_id = message.chat.id
    lang = db_users.get_lang(chat_id)
    status = db_users.staff_manager(chat_id)
    if status == 'CLIENT' or status == '404':
        await message.answer('Ошибка' if lang == 'RU' else 'Xato', reply_markup=btn_start_menu(lang, chat_id))
    else:
        now_datetime = datetime.datetime.now()
        data = get_month(now_datetime)
        feedback_list = db_users.get_feedback('month', (data,))
        action = 'месяц'
        path = write_excel_feedback(feedback_list, action, chat_id)
        text = 'Вот отчет' if lang == 'RU' else 'Bu erda hisobot'
        await message.answer(text, reply_markup=btn_start_menu(lang, chat_id))
        text_file = 'Обратная связь за текущий месяц' if lang == 'RU' else 'Joriy oy uchun fikr-mulohazalar'
        await message.answer_document(text=text_file, document=FSInputFile(path))


@txt_admin_router.message(F.text.in_(['Текущий год', 'Joriy yil']))
async def show_feedback_by_now_year(message: Message):
    chat_id = message.chat.id
    lang = db_users.get_lang(chat_id)
    status = db_users.staff_manager(chat_id)
    if status == 'CLIENT' or status == '404':
        await message.answer('Ошибка' if lang == 'RU' else 'Xato', reply_markup=btn_start_menu(lang, chat_id))
    else:
        now_datetime = datetime.datetime.now()
        data = get_year(now_datetime)
        feedback_list = db_users.get_feedback('year', (data,))
        action = 'год'
        path = write_excel_feedback(feedback_list, action, chat_id)
        text = 'Вот отчет' if lang == 'RU' else 'Bu erda hisobot'
        await message.answer(text, reply_markup=btn_start_menu(lang, chat_id))
        text_file = 'Обратная связь за текущий год' if lang == 'RU' else 'Joriy yil uchun fikr-mulohazalar'
        await message.answer_document(text=text_file, document=FSInputFile(path))


@txt_admin_router.message(F.text.in_(['Самому указать месяц и год', "Oy va yilni o'zingiz belgilang"]))
async def show_feedback_by_custom(message: Message, state: FSMContext):
    chat_id = message.chat.id
    lang = db_users.get_lang(chat_id)
    status = db_users.staff_manager(chat_id)
    if status == 'CLIENT' or status == '404':
        await message.answer('Ошибка' if lang == 'RU' else 'Xato', reply_markup=btn_start_menu(lang, chat_id))
    else:
        await message.answer('Введите месяц и год как в примере: 08, 2025' if lang == 'RU' else
                             "Misoldagi kabi oy va yilni kiriting: 08, 2025")
        await state.set_state(GetDateState.custom_date)


@txt_admin_router.message(GetDateState.custom_date)
async def get_custom_date(message: Message, state: FSMContext):
    await state.clear()

    chat_id = message.chat.id
    custom_data = message.text
    lang = db_users.get_lang(chat_id)

    month, year = custom_data.split(', ')
    month, year = int(month), int(year)
    feedback_list = db_users.get_feedback('custom', (month, year))

    action = 'Самостоятельно указанный месяц и год'
    path = write_excel_feedback(feedback_list, action, chat_id)
    text = 'Вот отчет' if lang == 'RU' else 'Bu erda hisobot'
    await message.answer(text, reply_markup=btn_start_menu(lang, chat_id))
    text_file = 'Обратная связь за указанный месяц и год' if lang == 'RU' else \
        'Belgilangan oy va yil uchun fikr-mulohazalar'
    await message.answer_document(text=text_file, document=FSInputFile(path))


@txt_admin_router.message(F.text.in_(['Текущие Сделки 🤝', 'Joriy Bitimlar 🤝']))
async def reach_current_transactions(message: Message):
    chat_id = message.chat.id
    lang = db_users.get_lang(chat_id)
    status = db_users.staff_manager(chat_id)
    if status == 'CLIENT' or status == '404':
        await message.answer('Ошибка' if lang == 'RU' else 'Xato', reply_markup=btn_start_menu(lang, chat_id))
    else:
        await message.answer('Хорошо' if lang == 'RU' else 'Yaxshi', reply_markup=ReplyKeyboardRemove())
        await message.answer('Список клиентов' if lang == 'RU' else "Mijozlar ro'yxati",
                             reply_markup=btn_list_buyers(lang))
