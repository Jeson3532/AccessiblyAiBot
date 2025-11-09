import asyncio
import logging

from aiogram import Dispatcher, Bot
from bot.handlers.message import router as message_router
from bot.handlers import routers
from bot.entry.config import BOT_TOKEN, DEBUG_MODE

bot = Bot(BOT_TOKEN)
dp = Dispatcher()


async def bot_start_polling():
    dp.include_routers(*routers)
    await dp.start_polling(bot)


if __name__ == "__main__":
    if DEBUG_MODE:
        logging.basicConfig(level=logging.DEBUG)
    else:
        logging.basicConfig(level=logging.INFO)
    try:
        asyncio.run(bot_start_polling())
    except KeyboardInterrupt:
        print("Exit")
