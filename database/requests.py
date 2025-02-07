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
        first_name, phone_number 
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


async def NewsLetterStart(text, path):
    connection = models.create_connection(path)
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
        print(tg_id)
        await bot.send_message(chat_id=tg_id, text=text)
