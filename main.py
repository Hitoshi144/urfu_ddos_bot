import asyncio
from os import getenv
from dotenv import load_dotenv

from aiogram import Bot, Dispatcher, F
from aiogram.types import Message, CallbackQuery
from aiogram.filters.command import Command

from keyboards import main_kb
from db.database import init_db, print_tables, create, delete_all, get, get_date, SessionLocal, load_all_data, need_db_update

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
    
@dp.callback_query(F.data.startswith("subject_"))
async def on_subject_select(callback: CallbackQuery):
    program_id = callback.data.split('_')[1] # type: ignore

    async with SessionLocal() as session:
        result = await get(session, int(program_id))
        await callback.message.answer(f'{len(result)}') # type: ignore


@dp.message(Command("test_row"))
async def create_test_row(message: Message):
    if message.from_user.id != 1325869215: # type: ignore
        await message.answer('Это функция разработчика :(')
    else:
        async with SessionLocal() as session:
            try:
                user = await create(
                    session,
                    regnum=123,
                    speciality="Math",
                    compensation="Full",
                    priority=1,
                    marks="A",
                    total_mark=95,
                )

                await message.answer(f'создана запись: {user}')
            except Exception as e:
                await message.answer(f'Чет пошло не так {e}')

@dp.message(Command('test_first'))
async def test(message: Message):
    if message.from_user.id != 1325869215: # type: ignore
        await message.answer('Это функция разработчика :(')
    else:
        async with SessionLocal() as session:
            try:
                result = await load_all_data(session)
                await message.answer(str(result))
            except Exception as e:
                await message.answer(f'Ошибка: {e}')

@dp.message(Command('date'))
async def get_latest_date(message: Message):
    if message.from_user.id != 1325869215: # type: ignore
        await message.answer('Это функция разработчика :(')
    else:
        result = await need_db_update()
        await message.answer(str(result))
            

@dp.message()
async def any_msg(message: Message):
    username = message.from_user.username if message.from_user and message.from_user.username else 'unknown'
    userid = message.from_user.id if message.from_user and message.from_user.id else "unknown"
    await bot.send_message(1325869215, f'{username} ({userid}): \n{message.text}')

async def main():
    await init_db()
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())