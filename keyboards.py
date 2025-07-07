from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

main_kb = InlineKeyboardMarkup(inline_keyboard=[
    [
        InlineKeyboardButton(
            text='37.05.01\nКлиническая психология',
            callback_data='select-action_1'
        )
    ],
    [
        InlineKeyboardButton(
            text='38.03.02\nМенеджмент',
            callback_data='select-action_2'
        )
    ],
    [
        InlineKeyboardButton(
            text='38.03.01\nЭкономика',
            callback_data='select-action_3'
        )
    ],
    [
        InlineKeyboardButton(
            text='05.03.06\nЭкология и природопользование',
            callback_data='select-action_4'
        )
    ]
])

