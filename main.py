import os
import asyncio
from dotenv import load_dotenv
from aiogram import Dispatcher, Bot

from bot.texts import txt_router
from bot.commands import cmd_router
from bot.ceo_texts import txt_ceo_router
from bot.admin_texts import txt_admin_router
from bot.admin_callbacks import admin_call_router
from bot.client_callbacks import client_call_router


async def main():
    load_dotenv()
    token = os.getenv('TOKEN')
    bot = Bot(token=token)
    dp = Dispatcher()

    dp.include_routers(
        txt_admin_router,
        admin_call_router,
        cmd_router,
        txt_ceo_router,
        txt_router,
        client_call_router,
    )

    try:
        await bot.delete_webhook(drop_pending_updates=True)
        await dp.start_polling(bot)
    finally:
        await bot.session.close()

if __name__ == '__main__':
    print('START BOT')
    try:
        asyncio.run(main())
    except (KeyboardInterrupt, SystemExit):
        print('BOT STOPPED')
    except Exception as e:
        print(f'Unexpected error: {e}')