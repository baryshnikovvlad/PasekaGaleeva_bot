from database import models
from database.models import create_connection
from aiogram.methods.send_message import SendMessage
import time, datetime
from main import bot

# типо создали таблицы, далее ебашим INSERT
create_user = lambda first_name, last_name, father_name, priority, user_tg_id, phone_number: f"""
INSERT INTO users (first_name, last_name, father_name, priority, user_tg_id, phone_number) 
VALUES ('{first_name}', '{last_name}', '{father_name}', '{priority}', '{user_tg_id}', '{phone_number}');
"""


# SELECT
def select_users(path):
    select = "SELECT * FROM users"
    users = models.execute_read_query(create_connection(path), select)
    return users


def select_user(path, tg_id):
    select = f"""
    SELECT 
        first_name, last_name, father_name, priority, user_tg_id, phone_number
    FROM 
        users 
    WHERE 
        user_tg_id = '{tg_id}'"""
    user = models.execute_read_query(create_connection(path), select)
    return user


def insert_user_from_register(first_name, second_name, father_name, priority, user_tg_id, phone_number):
    # ---вручную---
    connection = models.create_connection(models.path)
    models.execute_query(connection, delete_previous_users(user_tg_id))
    models.execute_query(connection, create_user(first_name, second_name, father_name, priority, user_tg_id, phone_number))


delete_previous_users = lambda user_tg_id: f"""
DELETE FROM users WHERE user_tg_id = {user_tg_id};
"""

def edited_text_with_first_name(text, user_tg_id):
    edited_text = text
    first_name = select_user(models.path, user_tg_id)[0][0]
    father_name = select_user(models.path, user_tg_id)[0][2]
    #print(first_name, father_name)
    edited_text = edited_text.replace('{first_name}', str(first_name))
    edited_text = edited_text.replace('{father_name}', str(father_name))
    #print(edited_text)
    #edited_text = {'text': str(edited_text)}
    return edited_text

async def NewsLetterStart(text, path):
    connection = models.create_connection(path)
    await bot.send_message(chat_id=641371845, text=text) # - разкомментить для дебага
    all_rows_id = """
    SELECT user_id AS all_rows
    FROM users;
    """
    all_rows = models.execute_read_query(connection, all_rows_id)
    length = len(models.execute_read_query(connection, all_rows_id))
    for i in range(length):
        select = (f"""
        SELECT
            user_tg_id
        FROM
            users
        WHERE
            user_id = '{models.execute_read_query(connection, all_rows_id)[0][0] + i}'
""")
        tg_id = models.execute_read_query(connection, select)[0][0]
        #print(tg_id)  # - закомментить для дебага
        #await bot.send_message(chat_id=tg_id, text=text)  # - закомментить для дебага
