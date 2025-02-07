
# Вручную бдшка
import sqlite3
from sqlite3 import Error

path = "C://Users/barys/PycharmProjects/BeeGardenBot/bd.sqlite3"


def create_connection(path):
    connection = None
    try:
        connection = sqlite3.connect(path)  # connection
        return connection
    except Error as e:
        print(f"The error {e} occured")

def execute_read_query(connection, query):
    cursor = connection.cursor()
    result = None
    try:
        cursor.execute(query)
        result = cursor.fetchall()
        # print(result)
        return result
    except Error as e:
        print(f"The error::  {e}   occured!")

def execute_query(connection, query):
    cursor = connection.cursor()
    try:
        cursor.execute(query)
        connection.commit()
        print("Query executed successfuly.")
    except Error as e:
        print(f"Error - {e} - was occured!")


create_users_table = """
CREATE TABLE IF NOT EXISTS users (
    user_id INTEGER PRIMARY KEY AUTOINCREMENT,
    first_name TEXT NOT NULL,
    last_name TEXT NOT NULL,
    father_name TEXT NOT NULL,
    priority INTEGER DEFAULT 0,
    user_tg_id INTEGER,
    phone_number TEXT DEFAULT fuck
);
"""
#first_name, last_name, father_name, priority, user_tg_id, phone_number: