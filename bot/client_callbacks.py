from aiogram import Router, Bot
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery, Message

from utils import ShippingAddress
from ghostwriter import text_cart_for_admin
from keyboards.btn_text import btn_start_menu
from keyboards.btn_inline import btn_to_cart_menu, btn_is_pay
from database.database_manager import SQLActionManager as SAM

db_products = SAM().products
db_users = SAM().users
db_carts = SAM().carts

client_call_router = Router()


@client_call_router.callback_query(lambda call: "minus" in call.data)
async def prev_products(callback: CallbackQuery):
    _, product_id, quantity = callback.data.split("_")
    price = db_products.get_product_price(int(product_id))
    chat_id = callback.message.chat.id
    lang = db_users.get_lang(chat_id)

    print(quantity)
    if int(quantity) <= 0:
        await callback.answer()
    else:
        quantity = int(quantity) - 1
        await callback.message.edit_reply_markup(
            reply_markup=btn_to_cart_menu(lang, product_id, int(price), int(quantity))
        )


@client_call_router.callback_query(lambda call: "plus" in call.data)
async def next_products(callback: CallbackQuery):
    _, product_id, quantity = callback.data.split("_")
    price = db_products.get_product_price(int(product_id))
    chat_id = callback.message.chat.id
    lang = db_users.get_lang(chat_id)

    product_total_quantity = db_products.get_product_quantity(int(product_id))
    if int(quantity) > int(product_total_quantity):
        await callback.answer()
    else:
        quantity = int(quantity) + 1
        await callback.message.edit_reply_markup(reply_markup=btn_to_cart_menu(lang, product_id,
                                                                               int(price), int(quantity)))


@client_call_router.callback_query(lambda call: 'clear_cart' in call.data)
async def react_btn_clear_cart(callback: CallbackQuery):
    chat_id = callback.message.chat.id
    lang = db_users.get_lang(chat_id)

    _, _, cart_id = callback.data.split('_')
    db_carts.clear_cart(cart_id)
    await callback.message.delete()
    await callback.message.answer('Корзина очищена' if lang == 'RU' else 'Savat tozalangan',
                                  reply_markup=btn_start_menu(lang, chat_id))


@client_call_router.callback_query(lambda call: 'cart' in call.data)
async def reach_btn_to_card(callback: CallbackQuery):
    chat_id = callback.message.chat.id
    lang = db_users.get_lang(chat_id)

    _, product_id, quantity, price = callback.data.split('_')
    user_pk = db_users.get_user(callback.message.chat.id)[0]
    cart_id = db_carts.get_cart_id(user_pk)
    db_carts.add_or_update_to_cart(cart_id, product_id, price, quantity)
    await callback.answer('Добавлено в корзине' if lang == 'RU' else "Savatga qo'shildi")
    await callback.message.delete()


@client_call_router.callback_query(lambda call: 'apply' in call.data)
async def react_btn_pay(callback: CallbackQuery, state: FSMContext):
    chat_id = callback.message.chat.id
    lang = db_users.get_lang(chat_id)

    _, cart_id = callback.data.split('_')
    await state.set_state(ShippingAddress.cart_id)
    await state.update_data(cart_id=cart_id)
    await callback.message.answer('Введите дополнительный номер телефона' if lang == 'RU' else
                                  "Qo'shimcha telefon raqamini kiriting")
    await state.set_state(ShippingAddress.sub_phone_number)


@client_call_router.message(ShippingAddress.sub_phone_number)
async def get_sub_phone_number(message: Message, state: FSMContext):
    phone_number = message.text
    chat_id = message.chat.id
    lang = db_users.get_lang(chat_id)

    await state.update_data(sub_phone_number=phone_number)
    await message.answer('Введите адрес доставки' if lang == 'RU' else 'Yetkazib berish manzilini kiriting')
    await state.set_state(ShippingAddress.address)


@client_call_router.message(ShippingAddress.address)
async def get_address(message: Message, bot: Bot, state: FSMContext):
    chat_id = message.chat.id
    lang = db_users.get_lang(chat_id)

    address = message.text
    data = await state.get_data()
    cart_id = data['cart_id']
    sub_phone_number = data['sub_phone_number']
    await state.clear()

    await message.answer('В течении минуты с вами свяжется администратор' if lang == 'RU' else
                         "Bir daqiqa ichida administrator siz bilan bog'lanadi")

    user_id, fio, email, phone_number = db_users.get_user(chat_id)[:4]
    total_price, total_quantity = db_carts.get_cart_info(user_id)
    db_carts.add_shipping_address(user_id, cart_id, address, sub_phone_number)

    text = text_cart_for_admin(fio, email, phone_number, sub_phone_number,
                               address, total_quantity, total_price, lang)

    list_tg_id = db_users.get_list_tg_id_admin()
    for tg_id in list_tg_id:
        await bot.send_message(chat_id=int(tg_id), text=text, reply_markup=btn_is_pay(cart_id, lang))




