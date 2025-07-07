import asyncio
from os import getenv
from dotenv import load_dotenv

from aiogram import Bot, Dispatcher, F
from aiogram.types import Message, CallbackQuery, FSInputFile
from aiogram.filters.command import Command
from aiogram.utils.chat_action import ChatActionSender
from aiogram.enums import  ParseMode
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton


from keyboards import main_kb
from db.database import init_db, print_tables, create, delete_all, get, get_date, SessionLocal, load_all_data, need_db_update, save_to_xlsx
from helper import get_marks, SUBJECTS

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
    await message.delete()
    
@dp.callback_query(F.data.startswith("select-action_"))
async def action_selecting(callback: CallbackQuery):
    program_id = callback.data.split('_')[1] # type: ignore

    action_kb = InlineKeyboardMarkup(inline_keyboard=[
    [
        InlineKeyboardButton(
            text='Узнать место в списке 📋',
            callback_data=f'subject_{program_id}'
        )
    ],
    [
        InlineKeyboardButton(
            text='Скачать полную таблицу 💻',
            callback_data=f'table_{program_id}'
        )
    ]
])

    await callback.message.edit_text(f'''<b>{SUBJECTS[program_id]}</b>
Выбери, что будем делать дальше, Катюша-тяян~! 💕

Хочешь узнать своё заветное местечко в списке абитуриентов? 📋✨
Или, может быть, хочешь скачать всю волшебную табличку целиком, чтобы изучить её в уютной обстановке? 💻☕

🌟 Просто нажми на кнопочку, а остальное я сделаю за тебя, как настоящая заботливая помощница~! (≧◡≦) ♡
''', parse_mode=ParseMode.HTML, reply_markup=action_kb) 
    
@dp.callback_query(F.data.startswith("subject_"))
async def on_subject_select(callback: CallbackQuery):
    program_id = callback.data.split('_')[1] # type: ignore

    async with SessionLocal() as session:
        need_update = await need_db_update()

        if need_update:
            async with ChatActionSender.typing(bot=callback.message.bot, chat_id=callback.message.chat.id): # type: ignore
                await init_db()
                await callback.message.edit_text('Получаю актуальные данные... (･ω<)☆') # type: ignore
                await load_all_data(session)

        async with ChatActionSender.typing(bot=callback.message.bot, chat_id=callback.message.chat.id): # type: ignore
            await callback.message.edit_text('Шуршу байтами... ( = ⩊ = )') # type: ignore
            result = await get(session, int(program_id)) # type: ignore
            count = 0
            katya = False
            for user in result:
                count += 1
                if user.regnum == 3766402: # type: ignore
                    katya = user
                    break
            
            if katya:
                std_message = f'''Вот что мне удалось найти для тебя, Катюша-тяян~! 💖📊

<b>{SUBJECTS[program_id]}</b>
                
🪄 Твоё место в списке: {count}
👥 Всего участников в списке: {len(result)}
'''

                marks = get_marks(katya.marks) # type: ignore

                if marks != []:
                    std_message += '''\n📚 Оценки по предметам:\n'''
                    for mark in marks:
                        std_message += f"* {mark}\n"
                    std_message += f"\n💯 Общий балл: {katya.total_mark}" # type: ignore
                else:
                    std_message += "\nУвы, оценочек пока нету (╥﹏╥)"
                
                std_message += f'''\n\nТы молодчинка! Я горжусь тобой~ (๑˃ᴗ˂)ﻭ
Если нужно, я могу всё повторить или показать тебе что-то ещё~! 💌✨'''
                
            end_kb = InlineKeyboardMarkup(inline_keyboard=[
                [
                    InlineKeyboardButton(
                        text='На главную 🌸',
                        callback_data='main_menu'
                    )
                ],
                [
                    InlineKeyboardButton(
                        text='Скачать полную таблицу 💻',
                        callback_data=f'table_{program_id}'
                    )
                ]
            ])


            await callback.message.edit_text(std_message, reply_markup=end_kb, parse_mode=ParseMode.HTML) # type: ignore


@dp.callback_query(F.data == 'main_menu')
async def show_main_menu(callback: CallbackQuery):
    await callback.message.edit_text('''Я снова с тобой, Катюша-тяян~! 💞

Готова помочь тебе с конкурсными списками, как и раньше~! 📝✨
Выбери образовательную программу, и я всё покажу~ 💻📊
''', reply_markup=main_kb)

@dp.callback_query(F.data.startswith('table_'))
async def get_table(callback: CallbackQuery):
     async with SessionLocal() as session:
        need_update = await need_db_update()

        if need_update:
            async with ChatActionSender.typing(bot=callback.message.bot, chat_id=callback.message.chat.id): # type: ignore
                await init_db()
                await callback.message.edit_text('Получаю актуальные данные... (･ω<)☆') # type: ignore
                await load_all_data(session)

        program_id = callback.data.split('_')[1]

        async with ChatActionSender.upload_document(bot=callback.message.bot, chat_id=callback.message.chat.id):
            file_path = await save_to_xlsx(int(program_id))
    
            file = FSInputFile(file_path)
        
            await callback.message.delete()
            await callback.message.answer_document(file, caption='Вот твоя табличка~ 📊💖')
    
            action_kb = InlineKeyboardMarkup(inline_keyboard=[
                [
                    InlineKeyboardButton(
                        text='На главную 🌸',
                        callback_data='main_menu'
                    )
                ],
                [
                    InlineKeyboardButton(
                        text='Узнать место в списке 📋',
                        callback_data=f'subject_{program_id}'
                    )
                ]
            ])
    
            await callback.message.answer('Что будем делать дальше? (っ╹ᆺ╹)っ', reply_markup=action_kb)


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