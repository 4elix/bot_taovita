import datetime

from aiogram import Router
from aiogram.types import CallbackQuery, Message
from aiogram.fsm.context import FSMContext

from ghostwriter import error_text_get_price, text_cart_for_admin
from keyboards.btn_inline import btn_is_pay, btn_action_change_product
from utils import GetProductForDelete, EditProductState
from keyboards.btn_text import btn_action_product, btn_start_menu
from database.database_manager import SQLActionManager as SAM

db_products = SAM().products
db_users = SAM().users
db_carts = SAM().carts

admin_call_router = Router()


@admin_call_router.callback_query(lambda call: 'edit_product' in call.data)
async def react_btn_edit_product(callback: CallbackQuery, state: FSMContext):
    chat_id = callback.message.chat.id
    lang = db_users.get_lang(chat_id)
    await callback.message.answer('Введите название продукта для изменения' if lang == 'RU' else
                                  "O'zgartirish uchun mahsulot nomini kiriting")
    await state.set_state(EditProductState.title)


@admin_call_router.message(EditProductState.title)
async def get_title_product(message: Message, state: FSMContext):
    title = message.text
    chat_id = message.chat.id
    lang = db_users.get_lang(chat_id)

    await state.update_data(title=title)
    await message.answer('Введите новую стоимость продукта' if lang == 'RU' else "Mahsulotning yangi narxini kiriting")
    await state.set_state(EditProductState.price)


@admin_call_router.message(EditProductState.price)
async def get_price_product(message: Message, state: FSMContext):
    chat_id = message.chat.id
    lang = db_users.get_lang(chat_id)

    price = message.text
    check_price = price.isdigit()
    if check_price is True:
        await state.update_data(price=int(price))
        data = await state.get_data()
        title = data['title']
        price = data['price']
        await state.clear()

        lang = db_users.get_lang(chat_id)
        db_products.update_product((price, title))
        await message.answer(
            'Данные продукта изменены, выберете действия' if lang == 'RU' else "Mahsulot saqlanadi, amallarni tanlang",
            reply_markup=btn_start_menu(lang, chat_id))

    else:
        text = error_text_get_price[lang]
        await message.answer(text)
        await state.set_state(EditProductState.price)


@admin_call_router.callback_query(lambda call: 'delete_product' in call.data)
async def react_btn_delete_product(callback: CallbackQuery, state: FSMContext):
    chat_id = callback.message.chat.id
    lang = db_users.get_lang(chat_id)
    await state.set_state(GetProductForDelete.product_name)
    await callback.message.answer(
        'Введите название продукта продукта для удаления' if lang == 'RU' else
        'Olib tashlash uchun mahsulot nomini kiriting')


@admin_call_router.message(GetProductForDelete.product_name)
async def delete_product(message: Message, state: FSMContext):
    chat_id = message.chat.id
    lang = db_users.get_lang(chat_id)

    product_name = message.text
    await state.clear()
    status_delete = db_products.delete_product(product_name)
    if status_delete == 404:
        await message.answer(
            'Вы ввели неправильно название продукта, попробуете ещё раз' if lang == 'RU' else
            "Siz mahsulot nomini noto'g'ri kiritdingiz, yana urinib ko'ring")
    else:
        await message.answer('Продукта успешно удален !' if lang == 'RU' else
                             'Mahsulot muvaffaqiyatli olib tashlandi !', reply_markup=btn_action_change_product(lang))


@admin_call_router.callback_query(lambda call: 'back_menu_work_product' in call.data)
async def back_menu_work_product(callback: CallbackQuery):
    chat_id = callback.message.chat.id
    lang = db_users.get_lang(chat_id)
    await callback.message.answer('Хорошо' if lang == 'RU' else 'Yaxshi', reply_markup=btn_start_menu(lang, chat_id))


@admin_call_router.callback_query(lambda call: 'is_pay' in call.data)
async def react_btn_is_pay(callback: CallbackQuery):
    chat_id = callback.message.chat.id
    lang = db_users.get_lang(chat_id)
    _, _, cart_id = callback.data.split('_')

    (total_quantity, total_price, fio, email, phone_number,
     shipping_address, sub_phone_number, tg_id, shipping_id) = db_carts.get_info_user_cart_shipping(cart_id)

    data = datetime.datetime.now()

    db_carts.add_history_buy(
        total_quantity, total_price, fio, email, phone_number,
        shipping_address, sub_phone_number, tg_id, shipping_id, data)

    await callback.message.answer('Оплата сохранена в базе данных' if lang == 'RU' else
                                  "To'lov ma'lumotlar bazasida saqlanadi", reply_markup=btn_start_menu(lang, chat_id))


@admin_call_router.callback_query(lambda call: 'show_buyer' in call.data)
async def react_btn_show_buyer(callback: CallbackQuery):
    chat_id = callback.message.chat.id
    lang = db_users.get_lang(chat_id)
    _, _, cart_id = callback.data.split('_')

    (total_quantity, total_price, fio, email, phone_number,
     shipping_address, sub_phone_number, tg_id, shipping_id) = db_carts.get_info_user_cart_shipping(cart_id)

    text = text_cart_for_admin(fio, email, phone_number, sub_phone_number,
                               shipping_address, total_quantity, total_price, lang)

    await callback.message.answer(text, reply_markup=btn_is_pay(cart_id, lang))
