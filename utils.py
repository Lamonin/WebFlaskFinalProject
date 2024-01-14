import sqlite3


def get_db_connection():
    return sqlite3.connect('carsharing.sqlite')


def to_list_of_int(list_of_str):
    return [int(n) for n in list_of_str]
