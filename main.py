import asyncio
from os import getenv
from dotenv import load_dotenv

from aiogram import Bot, Dispatcher, F
from aiogram.types import Message, CallbackQuery, FSInputFile
from aiogram.filters.command import Command
from aiogram.utils.chat_action import ChatActionSender
from aiogram.enums import  ParseMode
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup


from keyboards import main_kb
from db.database import init_db, print_tables, create, delete_all, get, get_date, SessionLocal, load_all_data, need_db_update, save_to_xlsx
from helper import get_marks, SUBJECTS, get_regid, write_regid, change_regid
from background import keep_alive

load_dotenv()
TOKEN = getenv("TOKEN")

if (TOKEN):
    bot = Bot(token=TOKEN)
else:
    print('Чёт не так пошло(')

dp = Dispatcher()

class ENTERREFID(StatesGroup):
    regid = State()
    bot_latest_message_id = State()
    current_username = State()

@dp.message(Command("start"))
async def start(message: Message, state: FSMContext):
    userId = message.from_user.id
    regid = get_regid(userId)
    await state.update_data(current_username=message.from_user.username)
    username = await state.get_value("current_username")

    if not regid:
        bot_message =  await message.answer(f'''Привет-привет, {username}-тяяян~! ✨

Я — твоя няшная помощница-бот, которая будет следить за твоим местом в конкурсных списках~ 📝💕
                         
Но сначала отправь, пожалуйста, свой <b>регистрационный номер</b> - без него я не смогу ничего сделать (つ﹏<。)
                         
Не волнуйся, это нужно всего один раз~
Ты всегда сможешь поменять его позже, если что! (*≧ω≦)''', parse_mode=ParseMode.HTML)
        await message.delete()

        await state.update_data(bot_latest_message_id=str(bot_message.message_id))
        await state.set_state(ENTERREFID.regid)
    else:
        bot_message = await message.answer(f'''Привет-привет, {username}-тяяян~! ✨

Я — твоя няшная помощница-бот, которая будет следить за твоим местом в конкурсных списках~ 📝💕

Твой регистрационный номер <b>{regid}</b>

Выбери образовательную программу, чтобы я могла показать тебе самую актуальную информацию! 💻📊

Не волнуйся, всё будет хорошо, я всегда рядом! 🍀''', parse_mode=ParseMode.HTML, reply_markup=main_kb)
        await state.update_data(bot_latest_message_id=str(bot_message.message_id))
        await message.delete()

@dp.callback_query(F.data == 'change-regid')
async def change_user_regid(callback: CallbackQuery, state: FSMContext):
    action_kb = InlineKeyboardMarkup(inline_keyboard=[
        [
            InlineKeyboardButton(
                text='На главную 🌸',
                callback_data='main_menu'
            )
        ]
    ])
    await callback.message.edit_text('Хорошо-хорошо~ (｡･ω･｡)ﾉ♡\nТеперь введи, пожалуйста, новый регистрационный номер~ ✨\nЯ всё аккуратненько запишу! 📒💫', reply_markup=action_kb)
    await state.set_state(ENTERREFID.regid)

@dp.message(F.text, ENTERREFID.regid)
async def enter_regid(message: Message, state: FSMContext):
    latest_msg_id = await state.get_value("bot_latest_message_id")
    if not message.text.strip().isdigit():
        await message.delete()
        await bot.edit_message_text(chat_id=message.chat.id, text='Айяйяй, вводи только цифрочки, плиииз~ >w< 💦 Давай, попробуй ещё раз! ✨', message_id=latest_msg_id)
        await state.set_state(ENTERREFID.regid)
    else:
        await state.update_data(regid=message.text.strip())

        userid = message.from_user.id
        regid = await state.get_value("regid")
        have_regid = get_regid(userid)

        if regid and not have_regid:
            write_regid(userid, regid)
            await state.clear()
        elif regid and have_regid:
            change_regid(userid, regid)
            await state.clear()
        else:
            await message.answer('Что-то пошло не так, давай по новой')
            await state.set_state(ENTERREFID.regid)
        
        await message.delete()
        await bot.edit_message_text(
            chat_id=message.chat.id, message_id=latest_msg_id,
            text=f'''Отличненько. 
Твой текущий регстрационный номер: <b>{regid}</b>

Выбери образовательную программу, чтобы я могла показать тебе самую актуальную информацию! 💻📊

Не волнуйся, всё будет хорошо, я всегда рядом! 🍀
''',
        reply_markup=main_kb, parse_mode=ParseMode.HTML)
    
@dp.callback_query(F.data.startswith("select-action_"))
async def action_selecting(callback: CallbackQuery, state: FSMContext):
    program_id = callback.data.split('_')[1] # type: ignore

    regid = get_regid(callback.message.chat.id)

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
    ],
    [
        InlineKeyboardButton(
            text='На главную 🌸',
            callback_data='main_menu'
        )
    ],
])
    username = await state.get_value("current_username")

    await callback.message.edit_text(f'''<b>{SUBJECTS[program_id]}</b>
Регистрационный номер: <b>{regid}</b>

Выбери, что будем делать дальше, {username}-тяян~! 💕

Хочешь узнать своё заветное местечко в списке абитуриентов? 📋✨
Или, может быть, хочешь скачать всю волшебную табличку целиком, чтобы изучить её в уютной обстановке? 💻☕

🌟 Просто нажми на кнопочку, а остальное я сделаю за тебя, как настоящая заботливая помощница~! (≧◡≦) ♡
''', parse_mode=ParseMode.HTML, reply_markup=action_kb) 
    
@dp.callback_query(F.data.startswith("subject_"))
async def on_subject_select(callback: CallbackQuery, state: FSMContext):
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
            userId = callback.message.chat.id
            print(userId)
            regid = get_regid(userId)

            for user in result:
                count += 1
                if user.regnum == int(regid): # type: ignore
                    katya = user
                    break
            if not katya:
                std_message = f'''Ничего не удалось найти... (；ω；)
Возможно, в регистрационном номере есть ошибочка, или тебя пока нет в списке~
Проверь ещё раз свой номер: <b>{regid}</b> 💌'''

                end_kb = InlineKeyboardMarkup(inline_keyboard=[
                    [
                        InlineKeyboardButton(
                            text='На главную 🌸',
                            callback_data='main_menu'
                        )
                    ],
                    [
                        InlineKeyboardButton(
                            text='Изменить регистрационный номер',
                            callback_data='change-regid'
                        )
                    ]
                ])
            elif katya:
                username = await state.get_value("current_username")
                std_message = f'''Вот что мне удалось найти для тебя, {username}-тяян~! 💖📊

<b>{SUBJECTS[program_id]}</b>
Регистрационный номер: <b>{regid}</b>
                
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
async def show_main_menu(callback: CallbackQuery, state: FSMContext):
    await state.set_state(None)
    regid = get_regid(callback.message.chat.id)
    username = await state.get_value("current_username")

    bot_message = await callback.message.edit_text(f'''Я снова с тобой, {username}-тяян~! 💞
Напоминаю, твой регистрационный номер: <b>{regid}</b>
                                                   
Готова помочь тебе с конкурсными списками, как и раньше~! 📝✨
Выбери образовательную программу, и я всё покажу~ 💻📊
''', reply_markup=main_kb, parse_mode=ParseMode.HTML)
    await state.update_data(bot_latest_message_id=str(bot_message.message_id))

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

keep_alive()
if __name__ == "__main__":
    asyncio.run(main())