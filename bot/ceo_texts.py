from aiogram import Router, F
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, CallbackQuery, FSInputFile

from ghostwriter import *
from keyboards.btn_text import *
from keyboards.btn_inline import *
from support import write_excel_sales_info
from utils import DeleteEmployee, EditEmployee, YearSelas
from database.database_manager import SQLActionManager as SAM

txt_ceo_router = Router()

db_products = SAM().products
db_users = SAM().users
db_carts = SAM().carts


@txt_ceo_router.message(F.text.in_(['Назад к меню 🔙', 'Menyuga qaytish 🔙']))
async def react_btn_back_menu(message: Message):
    chat_id = message.chat.id
    lang = db_users.get_lang(chat_id)
    await message.answer('Хорошо' if lang == 'RU' else 'Yaxshi', reply_markup=btn_start_menu(lang, chat_id))


@txt_ceo_router.message(F.text.in_(['Работа с персоналом 🛠', 'Xodimlar bilan ishlash 🛠']))
async def react_btn_work_employee(message: Message):
    chat_id = message.chat.id
    lang = db_users.get_lang(chat_id)
    status = db_users.staff_manager(chat_id)
    if status == 'CLIENT' or status == '404':
        await message.answer('Ошибка' if lang == 'RU' else 'Xato', reply_markup=btn_start_menu(lang, chat_id))
    else:
        await message.answer('Выберите действия' if lang == 'RU' else 'Harakatlarni tanlang',
                             reply_markup=btn_action_employee(lang))


@txt_ceo_router.message(F.text.in_(['Список сотрудника 📃', "Xodimlar ro'yxati 📃"]))
async def react_btn_list_employee(message: Message):
    chat_id = message.chat.id
    lang = db_users.get_lang(chat_id)
    status = db_users.staff_manager(chat_id)
    if status == 'CLIENT' or status == '404':
        await message.answer('Ошибка' if lang == 'RU' else 'Xato', reply_markup=btn_start_menu(lang, chat_id))
    else:
        list_employee = db_users.get_list_employee()
        for employee in list_employee:
            fio, phone_number = employee
            text = text_list_employee(lang, fio, phone_number)
            await message.answer(text, reply_markup=btn_action_employee(lang))


@txt_ceo_router.message(F.text.in_(['Удалить сотрудника ❌', 'Xodimni olib tashlang ❌']))
async def react_btn_delete_employee(message: Message, state: FSMContext):
    chat_id = message.chat.id
    lang = db_users.get_lang(chat_id)
    status = db_users.staff_manager(chat_id)
    if status == 'CLIENT' or status == '404':
        await message.answer('Ошибка' if lang == 'RU' else 'Xato', reply_markup=btn_start_menu(lang, chat_id))
    else:
        kb_back = ReplyKeyboardMarkup(resize_keyboard=True, keyboard=[
            [KeyboardButton(text='Назад к меню 🔙' if lang == 'RU' else 'Menyuga qaytish 🔙')]
        ])
        await message.answer('Введите имя сотрудника' if lang == 'RU' else 'Xodimning ismini kiriting',
                             reply_markup=kb_back)
        await state.set_state(DeleteEmployee.name_employee)


@txt_ceo_router.message(DeleteEmployee.name_employee)
async def get_name_employee(message: Message, state: FSMContext):
    chat_id = message.chat.id
    lang = db_users.get_lang(chat_id)
    if message.text == 'Назад к меню 🔙' or message.text == 'Menyuga qaytish 🔙':
        await message.answer('Хорошо' if lang == 'RU' else 'Yaxshi', reply_markup=btn_start_menu(lang, chat_id))
        await state.clear()
    else:
        await state.update_data(name_employee=message.text)
        kb_back = ReplyKeyboardMarkup(resize_keyboard=True, keyboard=[
            [KeyboardButton(text='Назад к меню 🔙' if lang == 'RU' else 'Menyuga qaytish 🔙')]
        ])
        await message.answer('Введите номер телефона сотрудника, пример: +998999999999'
                             if lang == 'RU' else 'Xodimning telefon raqamini kiriting, masalan: +998999999999',
                             reply_markup=kb_back)
        await state.set_state(DeleteEmployee.phone_number)


@txt_ceo_router.message(DeleteEmployee.phone_number)
async def get_phone_number(message: Message, state: FSMContext):
    chat_id = message.chat.id
    lang = db_users.get_lang(chat_id)
    if message.text == 'Назад к меню 🔙' or message.text == 'Menyuga qaytish 🔙':
        await message.answer('Хорошо' if lang == 'RU' else 'Yaxshi', reply_markup=btn_start_menu(lang, chat_id))
        await state.clear()
    else:
        data = await state.get_data()
        await state.clear()

        phone_number = message.text
        state_code = db_users.delete_employee(data['name_employee'], phone_number)
        if state_code == 404:
            await message.answer('Вы ввели неправильно ФИО или номер телефона, попробуйте ещё раз' if lang == 'RU' else
                                 "Siz noto'g'ri ism yoki telefon raqamini kiritdingiz, qayta urinib ko'ring",
                                 reply_markup=btn_action_employee(lang))
        else:
            await message.answer('Сотрудник удален' if lang == 'RU' else 'Xodim olib tashlandi',
                                 reply_markup=btn_start_menu(lang, chat_id))


@txt_ceo_router.message(F.text.in_(['Изменить данный сотрудника ✏', "Ushbu xodimni o'zgartiring ✏"]))
async def react_btn_edit_employee(message: Message, state: FSMContext):
    chat_id = message.chat.id
    lang = db_users.get_lang(chat_id)
    status = db_users.staff_manager(chat_id)
    if status == 'CLIENT' or status == '404':
        await message.answer('Ошибка' if lang == 'RU' else 'Xato', reply_markup=btn_start_menu(lang, chat_id))
    else:
        kb_back = ReplyKeyboardMarkup(resize_keyboard=True, keyboard=[
            [KeyboardButton(text='Назад к меню 🔙' if lang == 'RU' else 'Menyuga qaytish 🔙')]
        ])
        await message.answer('Введите имя сотрудника' if lang == 'RU' else 'Xodimning ismini kiriting',
                             reply_markup=kb_back)
        await state.set_state(EditEmployee.name_employee)


@txt_ceo_router.message(EditEmployee.name_employee)
async def get_name_employee(message: Message, state: FSMContext):
    chat_id = message.chat.id
    lang = db_users.get_lang(chat_id)
    if message.text == 'Назад к меню 🔙' or message.text == 'Menyuga qaytish 🔙':
        await message.answer('Хорошо' if lang == 'RU' else 'Yaxshi', reply_markup=btn_start_menu(lang, chat_id))
        await state.clear()
    else:
        await state.update_data(name_employee=message.text)
        kb_back = ReplyKeyboardMarkup(resize_keyboard=True, keyboard=[
            [KeyboardButton(text='Назад к меню 🔙' if lang == 'RU' else 'Menyuga qaytish 🔙')]
        ])
        await message.answer('Введите номер телефона сотрудника, пример: +998999999999'
                             if lang == 'RU' else 'Xodimning telefon raqamini kiriting, masalan: +998999999999',
                             reply_markup=kb_back)
        await state.set_state(EditEmployee.phone_number)


@txt_ceo_router.message(EditEmployee.phone_number)
async def get_phone_number(message: Message, state: FSMContext):
    chat_id = message.chat.id
    lang = db_users.get_lang(chat_id)
    if message.text == 'Назад к меню 🔙' or message.text == 'Menyuga qaytish 🔙':
        await message.answer('Хорошо' if lang == 'RU' else 'Yaxshi', reply_markup=btn_start_menu(lang, chat_id))
        await state.clear()
    else:
        await state.update_data(phone_number=message.text)
        await message.answer('Выберите должность' if lang == 'RU' else 'Lavozimni tanlang', reply_markup=btn_post(lang))


@txt_ceo_router.callback_query(lambda call: 'employee_change_admin' in call.data)
async def react_btn_change_admin(callback: CallbackQuery, state: FSMContext):
    chat_id = callback.message.chat.id
    lang = db_users.get_lang(chat_id)

    data = await state.get_data()
    fio = data['name_employee']
    phone_number = data['phone_number']
    await state.clear()

    state_code = db_users.change_post(fio, phone_number, (True, False, True))
    if state_code == 404:
        text = error_text_fio_and_phone[lang]
        await callback.message.answer(text,
                                      reply_markup=btn_action_employee(lang))
    else:
        await callback.message.answer('Изменения прошло успешно' if lang == 'RU' else
                                      "O'zgarishlar muvaffaqiyatli bo'ldi", reply_markup=btn_start_menu(lang, chat_id))


@txt_ceo_router.callback_query(lambda call: 'employee_change_ceo' in call.data)
async def react_btn_change_ceo(callback: CallbackQuery, state: FSMContext):
    chat_id = callback.message.chat.id
    lang = db_users.get_lang(chat_id)

    data = await state.get_data()
    fio = data['name_employee']
    phone_number = data['phone_number']
    await state.clear()

    state_code = db_users.change_post(fio, phone_number, (True, True, True))
    if state_code == 404:
        text = error_text_fio_and_phone[lang]
        await callback.message.answer(text, reply_markup=btn_action_employee(lang))
    else:
        await callback.message.answer('Изменения прошло успешно' if lang == 'RU' else
                                      "O'zgarishlar muvaffaqiyatli bo'ldi", reply_markup=btn_start_menu(lang, chat_id))


@txt_ceo_router.message(F.text.in_(['Информация по продажам 📖', "Savdo haqida ma'lumot 📖"]))
async def react_btn_info_sales(message: Message, state: FSMContext):
    chat_id = message.chat.id
    lang = db_users.get_lang(chat_id)
    status = db_users.staff_manager(chat_id)
    if status == 'CLIENT' or status == '404':
        await message.answer('Ошибка' if lang == 'RU' else 'Xato', reply_markup=btn_start_menu(lang, chat_id))
    else:
        kb_back = ReplyKeyboardMarkup(resize_keyboard=True, keyboard=[
            [KeyboardButton(text='Назад к меню 🔙' if lang == 'RU' else 'Menyuga qaytish 🔙')]
        ])
        await message.answer('Введите год продаж, пример 2025' if lang == 'RU' else 'Savdo kodini kiriting, misol 2025',
                             reply_markup=kb_back)
        await state.set_state(YearSelas.year)


@txt_ceo_router.message(YearSelas.year)
async def get_year_for_sales(message: Message, state: FSMContext):
    chat_id = message.chat.id
    lang = db_users.get_lang(chat_id)
    year = message.text
    if message.text == 'Назад к меню 🔙' or message.text == 'Menyuga qaytish 🔙':
        await message.answer('Хорошо' if lang == 'RU' else 'Yaxshi', reply_markup=btn_start_menu(lang, chat_id))
        await state.clear()
    else:
        if year.isdigit():
            await state.clear()
            sales_list = db_carts.get_sales(year)
            action = 'информация по продажам'
            path = write_excel_sales_info(sales_list, action, chat_id)
            await message.answer_document(text=f'Информация по продажам за {year}' if lang == 'RU'
            else f"Savdo haqida ma'lumot  {year}", document=FSInputFile(path))
        else:
            await message.answer('Вы ввели некорректные данные, попробуйте ещё раз' if lang == 'RU' else
                                 "Siz noto'g'ri ma'lumotlarni kiritdingiz, yana urinib ko'ring")
            await state.set_state(YearSelas.year)
