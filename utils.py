import sqlite3


def get_db_connection():
    return sqlite3.connect('carsharing.sqlite')


def to_list_of_int(list_of_str):
    return [int(n) for n in list_of_str]


def c_int(value: str) -> int | None:
    return int(value) if value != "" else None


def get_years_declension(years):
    if years % 100 in [11, 12, 13, 14]:
        return "лет"
    elif years % 10 == 1:
        return "год"
    elif 2 <= years % 10 <= 4:
        return "года"
    else:
        return "лет"


def get_days_declension(days):
    if days % 100 in [11, 12, 13, 14]:
        return "дней"
    elif days % 10 == 1:
        return "день"
    elif 2 <= days % 10 <= 4:
        return "дня"
    else:
        return "дней"