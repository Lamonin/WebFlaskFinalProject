import pandas as pd


def get_brands(conn):
    query = "SELECT * FROM brand ORDER BY brand_name"
    return pd.read_sql_query(query, conn)


def get_car_cost_range(conn):
    query = '''
    SELECT MIN(cost) FROM car
    UNION ALL
    SELECT MAX(cost) FROM car
    '''
    return pd.read_sql_query(query, conn)


def get_car_year_of_manufacture_range(conn):
    query = '''
    SELECT MIN(year_of_manufacture) FROM car
    UNION ALL
    SELECT MAX(year_of_manufacture) FROM car
    '''
    return pd.read_sql_query(query, conn)


def get_colors(conn):
    query = "SELECT * FROM color"
    return pd.read_sql_query(query, conn)


def get_filtered_cars(conn):
    pass
