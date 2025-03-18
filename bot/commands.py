from aiogram import Router
from aiogram.types import Message
from aiogram.filters import Command

from ghostwriter import text_start
from keyboards.btn_text import btn_lang_option, btn_start_menu
from database.database_manager import SQLActionManager as SAM
cmd_router = Router()


@cmd_router.message(Command('start'))
async def react_start(message: Message):
    db_user = SAM().users
    user = db_user.get_user(message.chat.id)
    if user[0] == '404':
        await message.answer('Добрый день, для начала выберете язык / Xayrli kun, boshlash uchun tilni tanlang',
                             reply_markup=btn_lang_option)
    else:
        chat_id = message.chat.id
        role = db_user.staff_manager(chat_id)
        lang = db_user.get_lang(chat_id)
        text = text_start(lang, role)
        await message.answer(text, reply_markup=btn_start_menu(lang, chat_id))

