import datetime
import logging
from aiogram import F, Router
from aiogram.types import Message, CallbackQuery, PollAnswer
from aiogram.filters import CommandStart, Command
from aiogram.filters.callback_data import CallbackData
from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.context import FSMContext
from database import models
from app.keyboards import main, get_number, YoN, my_callback_data
from database.requests import select_users, select_user, insert_user_from_register, NewsLetterStart, edited_text_with_first_name
from main import bot, log_file_printer, log_file, dp
from confidential import admin_id

router = Router()
logger = logging.getLogger(__name__)

class Register(StatesGroup):
    first_name = State()
    last_name = State()
    father_name = State()
    user_tg_id = State()


class NewsLetter(StatesGroup):
    text = State()


@router.message(CommandStart())
async def cmd_start(message: Message):
    await message.answer('Выбер пункт', reply_markup=main)
    log_file_printer(f"{message.from_user.id} - /start: ", log_file)


@router.message(F.text == 'qawsed')
async def NewsLetter_(message: Message, state: FSMContext):
    await state.set_state(NewsLetter.text)
    await message.answer('Введи сообщение для рассылки: ')
    log_file_printer(f"{message.from_user.id} - NewsLetter: ", log_file)


@router.message(NewsLetter.text)
async def NewsLetter_text(message: Message, state: FSMContext):
    text = message.text
    user_tg_id = message.from_user.id
    #print(text, type(text))
    text = edited_text_with_first_name(text, user_tg_id)
    await message.answer(f"Это все, отправляем?: \n {text}", reply_markup=YoN)
    await state.update_data(text=text)
    await state.set_state(NewsLetter.text)
    log_file_printer(f"{message.from_user.id} - NewsLetter - text: " + text, log_file)


@router.callback_query(my_callback_data.filter(F.data == "Yes"), NewsLetter.text)
async def NewsLetter_Yes(query: CallbackQuery, state: FSMContext):
    data = await state.get_data()
    print(data, type(data))
    try:
        await query.answer("Отправил, проверяй.")
        await NewsLetterStart(data['text'], models.path)
        log_file_printer(f"{query.from_user.id} - NewsLetter - fine: ", log_file)
    except:
        print("Ошибка в отправке")
        log_file_printer(f"{query.from_user.id} - NewsLetter - unfine: ", log_file)


@router.callback_query(my_callback_data.filter(F.data == "No"))
async def NewsLetter_No(query: CallbackQuery):
    await query.answer("Не отправляю, давай по новой.")
    log_file_printer(f"{query.from_user.id} - NewsLetter - unfine, not send: ", log_file)


@router.message(F.text == 'Регистрация')
async def registracia(message: Message, state: FSMContext):
    await state.set_state(Register.first_name)
    await message.answer('Напишите ваше ИМЯ, пожалуйста:')
    log_file_printer(f"{message.from_user.id} - Registration: ", log_file)


@router.message(Register.first_name)
async def register_first_name(message: Message, state: FSMContext):
    await state.update_data(first_name=message.text)
    await state.set_state(Register.last_name)
    await message.answer('Напишите вашу ФАМИЛИЮ, пожалуйста:')
    log_file_printer(f"{message.from_user.id} - Registration - first_name: " + message.text, log_file)

@router.message(Register.last_name)
async def register_first_name(message: Message, state: FSMContext):
    await state.update_data(last_name=message.text)
    await state.set_state(Register.father_name)
    await message.answer('Напишите ваше ОТЧЕСТВО, пожалуйста:')
    log_file_printer(f"{message.from_user.id} - Registration - last_name: " + message.text, log_file)

@router.message(Register.father_name)
async def register_name(message: Message, state: FSMContext):
    await state.update_data(father_name=message.text)
    await state.set_state(Register.user_tg_id)
    await message.answer('Нажмите на кнопку чтобы передать контакт боту', reply_markup=get_number)
    log_file_printer(f"{message.from_user.id} - Registartion - father_name: " + message.text, log_file)


@router.message(Register.user_tg_id, F.contact)
async def register_number(message: Message, state: FSMContext):
    await state.update_data(user_tg_id=message.contact.user_id)
    data = await state.get_data()
    priority = 0
    for i in range(admin_id):
        if data["user_tg_id"] == admin_id[i]:
            priority = 1
        else:
            priority = 0
    insert_user_from_register(data["first_name"], data["last_name"], data["father_name"], priority, data["user_tg_id"], message.contact.phone_number)
    user = select_user(models.path, data["user_tg_id"])
    await message.answer(f"Вы теперь юзер: {user[0][0] + user[0][1]}")
    await state.clear()
    await message.edit_reply_markup()
    log_file_printer(f"{message.from_user.id} - Registration fine - contact: " + str((data["first_name"],
                                                                                         data["last_name"],
                                                                                         data["father_name"],
                                                                                         priority,
                                                                                         data["user_tg_id"],
                                                                                         message.contact.phone_number)), log_file)
