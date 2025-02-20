from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.filters.callback_data import CallbackData


class my_callback_data(CallbackData, prefix='my'):
    data: str


Assortment = InlineKeyboardMarkup(
    inline_keyboard=[[InlineKeyboardButton(text='Крем-мед',
                                           callback_data=my_callback_data(
                                               data='cream_honey').pack())],
                     [InlineKeyboardButton(text='Прополис',
                                           callback_data=my_callback_data(
                                               data='propolis').pack())],
                     [InlineKeyboardButton(text='Крем-мед',
                                           callback_data=my_callback_data(
                                               data='cream_honey').pack())],
                     [InlineKeyboardButton(text='Трутневое молочко',
                                           callback_data=my_callback_data(
                                               data='drone_jelly').pack())],
                     [InlineKeyboardButton(text='Вино на меду',
                                           callback_data=my_callback_data(
                                               data='wine_with_honey').pack())],
                     [InlineKeyboardButton(text='Медовуха',
                                           callback_data=my_callback_data(
                                               data='mead').pack())],
                     [InlineKeyboardButton(text='Пчелиная пыльца',
                                           callback_data=my_callback_data(
                                               data='bee_pollen').pack())],
                     [InlineKeyboardButton(text='Забрус',
                                           callback_data=my_callback_data(
                                               data='lining').pack())],
                     [InlineKeyboardButton(text='Мед',
                                           callback_data=my_callback_data(
                                               data='honey').pack())],
                     [InlineKeyboardButton(text='Вернуться к главному меню',
                                           callback_data=my_callback_data(
                                               data='main').pack())]])

Back_to_assortment = InlineKeyboardMarkup(inline_keyboard=[[InlineKeyboardButton(text='Вернуться к ассортименту',
                                                                                 callback_data=my_callback_data(
                                                                                     data='assortment').pack()
                                                                                 )]])

main = ReplyKeyboardMarkup(keyboard=[[KeyboardButton(text='Регистрация')],
                                     [KeyboardButton(text='Ассортимент')]],
                           resize_keyboard=True,
                           input_field_placeholder='Выбери пункт меню',
                           one_time_keyboard=True)

get_number = ReplyKeyboardMarkup(keyboard=[[KeyboardButton(text='Номер тык', request_contact=True)]],
                                 resize_keyboard=True,
                                 one_time_keyboard=True)

YoN = InlineKeyboardMarkup(
    inline_keyboard=[[InlineKeyboardButton(text='ДА', callback_data=my_callback_data(data="Yes").pack())],
                     [InlineKeyboardButton(text='НЕТ', callback_data=my_callback_data(data="No").pack())]])
