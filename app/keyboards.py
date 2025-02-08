from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.filters.callback_data import CallbackData


class my_callback_data(CallbackData, prefix='my'):
    data: str


main = ReplyKeyboardMarkup(keyboard=[[KeyboardButton(text='Регистрация')]],
                           resize_keyboard=True,
                           input_field_placeholder='Выбери пункт меню',
                           one_time_keyboard=True)

get_number = ReplyKeyboardMarkup(keyboard=[[KeyboardButton(text='Номер тык', request_contact=True)]],
                                 resize_keyboard=True,
                                 one_time_keyboard=True)

YoN = InlineKeyboardMarkup(
    inline_keyboard=[[InlineKeyboardButton(text='ДА', callback_data=my_callback_data(data="Yes").pack())],
                     [InlineKeyboardButton(text='НЕТ', callback_data=my_callback_data(data="No").pack())]])
