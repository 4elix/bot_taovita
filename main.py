import os
import asyncio
import logging
from dotenv import load_dotenv
from aiogram import Dispatcher, Bot

from bot.texts import txt_router
from bot.commands import cmd_router
from bot.ceo_texts import txt_ceo_router
from bot.admin_texts import txt_admin_router
from bot.admin_callbacks import admin_call_router
from bot.client_callbacks import client_call_router

# Настроим логирование
logging.basicConfig(
    level=logging.INFO,  # Уровень логирования
    format="%(asctime)s - %(levelname)s - %(name)s - %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
    handlers=[
        logging.FileHandler("bot.log", encoding="utf-8"),  # Лог в файл
        logging.StreamHandler()  # Вывод в консоль
    ]
)

logger = logging.getLogger(__name__)

async def main():
    load_dotenv()
    token = os.getenv('TOKEN')

    if not token:
        logger.critical("TOKEN не найден! Убедитесь, что .env файл настроен правильно.")
        return

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
        logger.info("Бот запускается...")
        await bot.delete_webhook(drop_pending_updates=True)
        await dp.start_polling(bot)
    except Exception as e:
        logger.exception(f"Произошла ошибка в работе бота: {e}")
    finally:
        await bot.session.close()
        logger.info("Бот остановлен.")

if __name__ == '__main__':
    logger.info("=== START BOT ===")
    try:
        asyncio.run(main())
    except (KeyboardInterrupt, SystemExit):
        logger.warning("Бот принудительно остановлен (KeyboardInterrupt, SystemExit).")
    except Exception as e:
        logger.critical(f"Непредвиденная ошибка при запуске: {e}", exc_info=True)
