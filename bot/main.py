import os
import asyncio

from aiogram import Bot, Dispatcher, types
from aiogram.filters.command import Command
from aiogram.enums.parse_mode import ParseMode

from dotenv import load_dotenv

from answers import START_ANSWER
from exceptions import BotTokenNotSet

load_dotenv()

CWD = os.path.dirname(__file__)

BOT_TOKEN = os.getenv('BOT_TOKEN')

if not BOT_TOKEN:
    raise BotTokenNotSet()

kb = types.InlineKeyboardMarkup(inline_keyboard=[
    [
        types.InlineKeyboardButton(
            text='Открыть приложение',
            web_app=types.WebAppInfo(url='https://2e2541.creatium.site/bagon_main')
        ),
    ]
])

dp = Dispatcher()
bot = Bot(token=BOT_TOKEN, parse_mode=ParseMode.MARKDOWN_V2)


@dp.message(Command('start'))
async def start(message: types.Message):
    open_app = types.FSInputFile(f'{CWD}/photos/open_app.jpg')
    await message.answer_photo(open_app, caption=START_ANSWER, reply_markup=kb)


async def main():
    await dp.start_polling(bot)


if __name__ == '__main__':
    asyncio.run(main())
