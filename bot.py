import sys
import asyncio
import logging

from os import getenv
from aiogram import Bot, Dispatcher, types, F
from aiogram.filters import CommandStart
from aiogram.types.web_app_info import WebAppInfo

BOT_TOKEN = getenv('BOT_TOKEN')
WEB_APP_URL = getenv('WEB_APP_URL')

dp = Dispatcher()


@dp.message(CommandStart)
async def start(message: types.Message):
    markup = types.ReplyKeyboardMarkup(keyboard=[
        [types.KeyboardButton(text='Старт', web_app=WebAppInfo(url=WEB_APP_URL))],
    ])
    await message.answer(f'Привет, {message.from_user.first_name}!', reply_markup=markup)


async def main():
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    bot = Bot(token=BOT_TOKEN)
    await dp.start_polling(bot)


if __name__ == '__main__':
    asyncio.run(main())
