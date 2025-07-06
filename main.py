import asyncio
from os import getenv
from dotenv import load_dotenv

from aiogram import Bot, Dispatcher, F
from aiogram.types import Message, CallbackQuery
from aiogram.filters.command import Command

from keyboards import main_kb

load_dotenv()
TOKEN = getenv("TOKEN")

if (TOKEN):
    bot = Bot(token=TOKEN)
else:
    print('Чёт не так пошло(')

dp = Dispatcher()

@dp.message(Command("start"))
async def start(message: Message):
    await message.answer('''Привет-привет, Катюша-тяяян~! ✨

Я — твоя няшная помощница-бот, которая будет следить за твоим местом в конкурсных списках~ 📝💕
Выбери образовательную программу, чтобы я могла показать тебе самую актуальную информацию! 💻📊

Не волнуйся, всё будет хорошо, я всегда рядом! 🍀''', 
reply_markup=main_kb)
    
@dp.callback_query(F.data == 'First')
async def psychology(callback: CallbackQuery):
    await callback.answer("ya", show_alert=True)


async def main():
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())