import datetime
from aiogram import Router, F, Bot
from aiogram.types import Message, FSInputFile
from aiogram.fsm.context import FSMContext

from bot.commands import react_start
from ghostwriter import *
from keyboards.btn_text import *
from keyboards.btn_inline import btn_to_cart_menu, btn_apply
from utils import RegisterState, ShowProductState, GetFeedbackState
from database.database_manager import SQLActionManager as SAM
from support import check_fio, check_email, manager_staff, remove_code_fio, update_phone_number

txt_router = Router()

db_products = SAM().products
db_users = SAM().users
db_carts = SAM().carts


@txt_router.message(F.text.in_(['RU 🇷🇺', 'UZ 🇸🇱']))
async def react_btn_lang(message: Message):
    lang = message.text.split(' ')[0]
    text = text_register[lang]
    if lang == 'RU':
        await message.answer(text, reply_markup=btn_registration_ru)
    elif lang == 'UZ':
        await message.answer(text, reply_markup=btn_registration_uz)


@txt_router.message(F.text.in_(['Зарегистрироваться', "Ro'yxatdan o'tish"]))
async def react_btn_register(message: Message, state: FSMContext):
    lang = 'RU' if message.text == 'Зарегистрироваться' else 'UZ'
    await state.set_state(RegisterState.lang)
    await state.update_data(lang=lang)
    text = text_get_fio[lang]
    await message.answer(text, reply_markup=ReplyKeyboardRemove())
    await state.set_state(RegisterState.fio)


@txt_router.message(RegisterState.fio)
async def get_fio(message: Message, state: FSMContext):
    fio = message.text
    try_fio = fio.split(' ')
    status_code = check_fio(try_fio)
    data = await state.get_data()
    lang = data['lang']

    if status_code == 404:
        text = error_text_get_fio[lang]
        await message.answer(text)
        await state.set_state(RegisterState.fio)
    else:
        await state.update_data(fio=fio)
        text = text_get_email[lang]
        await message.answer(text)
        await state.set_state(RegisterState.email)


@txt_router.message(RegisterState.email)
async def get_email(message: Message, state: FSMContext):
    email = message.text
    data = await state.get_data()
    lang = data['lang']

    status_code = check_email(email)

    if status_code == 404:
        text = error_text_get_email[lang]
        await message.answer(text)
        await state.set_state(RegisterState.email)
    else:
        await state.update_data(email=email)
        text = text_get_phone_number[lang]
        await state.set_state(RegisterState.phone_number)
        if lang == 'RU':
            await message.answer(text, reply_markup=btn_send_contact_ru)
        elif lang == 'UZ':
            await message.answer(text, reply_markup=btn_send_contact_uz)


@txt_router.message(RegisterState.phone_number, F.contact)
async def reach_btn_contact(message: Message, state: FSMContext):
    data = await state.get_data()
    lang = data['lang']
    chat_id = message.chat.id
    try:
        fio = data['fio']
        email = data['email']
        phone_number = message.contact.phone_number
        phone_number = update_phone_number(str(phone_number))
        is_admin, is_ceo, is_client = manager_staff(fio)

        fio_new = remove_code_fio(fio)
        await state.clear()

        data_user = (fio_new, email, phone_number, lang, is_admin, is_ceo, is_client, chat_id)
        db_users.save_user(data_user)

        text = text_success_register[lang]
        user_pk = db_users.get_user(chat_id)[0]
        db_carts.add_cart_user_id(user_pk)

        await message.answer(text, reply_markup=btn_start_menu(lang, chat_id))
    except Exception as error:
        print(f'{error.__class__} {error.__class__.__name__} --- reach_btn_contact')
        text = error_text_success_register[lang]
        await message.answer(text)
        await react_start(message)


@txt_router.message(F.text.in_(['Посмотреть категории 📚', "Kategoriyalarni ko'rish 📚"]))
async def show_categories(message: Message):
    chat_id = message.chat.id
    lang = db_users.get_lang(chat_id)
    text = 'Список категорий' if lang == 'RU' else "Kategoriyalar ro'yxati"
    await message.answer(text, reply_markup=btn_list_categories(lang))


@txt_router.message(F.text.in_(['Назад в меню 🔙', 'Menyuga qaytish 🔙']))
@txt_router.message(F.text.in_(db_products.show_all_list_categories()))
async def show_products(message: Message, state: FSMContext):
    chat_id = message.chat.id
    category_name = message.text
    lang = db_users.get_lang(chat_id)

    if category_name == 'Назад в меню 🔙' or category_name == 'Menyuga qaytish 🔙':
        await message.answer('Хорошо' if lang == 'RU' else 'Yaxshi', reply_markup=btn_start_menu(lang, chat_id))
    else:
        cat_id = db_products.get_cat_id_for_name(category_name)
        products = db_products.show_list_products(cat_id, lang)
        text = text_list_categories[lang]
        await message.answer(text, reply_markup=btn_list_products(products, lang))
        await state.set_state(ShowProductState.product_name)


@txt_router.message(ShowProductState.product_name)
async def show_product_info(message: Message, state: FSMContext):
    chat_id = message.chat.id
    lang = db_users.get_lang(chat_id)
    product_name = message.text

    if product_name == 'Назад к категория 🔙' or product_name == 'Orqaga kategoriya 🔙':
        await message.answer('Хорошо' if lang == 'RU' else 'Yaxshi', reply_markup=btn_list_categories(lang))
        await state.clear()
        return
    else:
        pk, image_path, title, price, \
            structure, vitamins, description, \
            quantity, lang, category_id = db_products.get_product_info(product_name)
        text = text_info_product(lang, title, price, structure, vitamins, description, quantity)
        await message.answer_photo(photo=FSInputFile(image_path), caption=text,
                                   reply_markup=btn_to_cart_menu(lang, pk, price))


@txt_router.message(F.text.in_(['Отзывы покупателей 👩‍💻👨‍💻', "Mijozlarning sharhlari 👩‍💻👨‍💻"]))
async def react_feedback(message: Message):
    chat_id = message.chat.id
    lang = db_users.get_lang(message.chat.id)

    text = text_link_channel[lang]
    await message.answer(text, reply_markup=btn_start_menu(lang, chat_id))
    await message.answer('https://t.me/sogliq_yoli')


@txt_router.message(F.text.in_(['Обратная связь 📞', 'Fikr-mulohaza 📞']))
async def react_feedback(message: Message, state: FSMContext):
    lang = db_users.get_lang(message.chat.id)

    text = text_get_feedback[lang]
    if lang == 'RU':
        await message.answer(text, reply_markup=btn_back_ru)
        await state.set_state(GetFeedbackState.text)
    elif lang == 'UZ':
        await message.answer(text, reply_markup=btn_back_uz)
        await state.set_state(GetFeedbackState.text)


@txt_router.message(GetFeedbackState.text)
async def get_feedback(message: Message, state: FSMContext):
    text_feedback = message.text
    await state.update_data(text=text_feedback)

    lang = db_users.get_lang(message.chat.id)
    text = text_get_rating[lang]
    await message.answer(text)
    await state.set_state(GetFeedbackState.rating)


@txt_router.message(GetFeedbackState.rating)
async def get_rating(message: Message, state: FSMContext):
    chat_id = message.chat.id
    rating = message.text
    lang = db_users.get_lang(chat_id)

    if rating.isdigit():
        rating = int(rating)
        if rating <= 5:
            data = await state.get_data()
            feedback_text = data['text']
            datetime_create = datetime.datetime.now()
            user_id = db_users.get_user(chat_id)[0]
            db_users.save_feedback(feedback_text, rating, datetime_create, user_id)
            text = success_send_feedback[lang]
            await message.answer(text,
                                 reply_markup=btn_start_menu(lang, chat_id))
            await state.clear()
        else:
            text = error_text_get_rating[lang]
            await message.answer(text)
            await state.set_state(GetFeedbackState.rating)
    else:
        text = error_text_get_rating[lang]
        await message.answer(text)
        await state.set_state(GetFeedbackState.rating)


@txt_router.message(F.text.in_(['Поменять язык 🌍', "Tilni o'zgartiring 🌍"]))
async def react_btn_change_lang(message: Message):
    chat_id = message.chat.id
    lang = db_users.get_lang(chat_id)
    if lang == 'RU':
        db_users.change_lang(chat_id, 'UZ')
        await message.answer("Til muvaffaqiyatli o'zgartirildi", reply_markup=btn_start_menu('UZ', chat_id))
    elif lang == 'UZ':
        db_users.change_lang(chat_id, 'RU')
        await message.answer('Язык успешно изменен', reply_markup=btn_start_menu('RU', chat_id))


@txt_router.message(F.text.in_(['Корзина 🛒', 'Savat 🛒']))
async def reach_btn_cart(message: Message):
    chat_id = message.chat.id
    lang = db_users.get_lang(chat_id)
    user_id = db_users.get_user(chat_id)[0]
    cart_id = db_carts.get_cart_id(user_id)
    cart_products = db_carts.show_cart_items(cart_id)
    total_price, total_quantity = db_carts.get_cart_info(user_id)

    if not cart_products:
        await message.answer('Корзина пуста' if lang == 'RU' else "Savat bo'sh",
                             reply_markup=btn_start_menu(lang, chat_id))

    text = text_cart(lang, cart_products, total_quantity, total_price)

    await message.answer(text, reply_markup=btn_apply(cart_id, lang))
