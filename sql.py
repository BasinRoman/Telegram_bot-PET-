"""База данных"""

import sqlite3
from sqlite3 import Error


def create_connection(path):
    my_connection = None
    try:
        my_connection = sqlite3.connect(path)
        my_connection.row_factory = sqlite3.Row
        print("Connection to SQLite DB successful")
    except Error as e:
        print(f"The error '{e}' occurred")

    return my_connection


connection = create_connection("/projects/sb_bot/sql/bot_bd.db")


def execute_query(my_connection, query, my_data):

    cursor = my_connection.cursor()

    try:
        cursor.executemany(query, my_data)
        my_connection.commit()
        print("Query executed successfully")
    except Error as e:
        print(f"The error '{e}' occurred")


def execute_read_query(my_connection, query):

    cursor = my_connection.cursor()

    try:
        cursor.execute(query)
        result = cursor.fetchall()
        return result
    except Error as e:
        print(f"The error '{e}' occurred")


def execute_read_query_with_par(my_connection, query, my_data):

    cursor = my_connection.cursor()

    try:
        cursor.execute(query, my_data)
        result = cursor.fetchall()
        return result
    except Error as e:
        print(f"The error '{e}' occurred")


if __name__ == "__main__":
    print('hello world!')
