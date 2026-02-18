from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup, ReplyKeyboardMarkup, KeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder, ReplyKeyboardBuilder

inlineKb = InlineKeyboardMarkup(inline_keyboard=[[
    InlineKeyboardButton(text='Кнопка 1', callback_data='Btn_1'),
    InlineKeyboardButton(text='google', url='https://www.google.com/')
],
[
    InlineKeyboardButton(text='Кнопка 2', callback_data='Btn_2')
]
])

reply_kb = ReplyKeyboardMarkup(keyboard=[[
    KeyboardButton(text='Кнопка 3'),
    KeyboardButton(text='Кнопка 4')
]])

reply_kb2 = ReplyKeyboardBuilder()
reply_kb2.button(text='Кнопка 5')
reply_kb2.button(text='Кнопка 6')
reply_kb2.adjust(2)

inlineKb2 = InlineKeyboardBuilder()
inlineKb2.button(text='Кнопка 7', callback_data='Btn_7')
inlineKb2.button(text='Кнопка 8', callback_data='Btn_8')
inlineKb2.button(text='Кнопка 9', url='https://www.google.com/')
inlineKb2.adjust(2)