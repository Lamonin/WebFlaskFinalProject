import pandas as pd


def get_car_info(conn, car_id):
    query = '''
    SELECT brand_name || ' ' || model_name,
        year_of_manufacture, color_name, license_plate, cost, experience_requirement
    FROM car
    JOIN model USING(model_id)
    JOIN brand USING(brand_id)
    JOIN color USING(color_id)
    WHERE car_id == :car_id
    '''

    return pd.read_sql_query(query, conn, params={'car_id': car_id})


def get_driver_info(conn, driver_license):
    query = '''
    SELECT *
    FROM client
    WHERE driver_license_number == :driver_license
    '''
    return pd.read_sql_query(query, conn, params={'driver_license': driver_license})


def get_drivers_licenses(conn):
    query = '''
    SELECT full_name, driver_license_number as license_number
    FROM client
    '''

    return pd.read_sql_query(query, conn)


def get_car_damage_list(conn, car_id):
    query = '''
    SELECT defect_name
    FROM car_defect
    JOIN defect USING(defect_id)
    WHERE car_id == :car_id
    '''

    return pd.read_sql_query(query, conn, params={'car_id': car_id})


def get_active_rents(conn):
    query = '''
    SELECT *
    FROM rental_contract
    WHERE state == 0
    '''

    return pd.read_sql_query(query, conn)


def add_driver(conn, second_name, name, patronymic, phone_number, driver_license, drive_experience):
    query = f'''
    INSERT INTO client (full_name, phone_number, driver_license_number, driver_experience)
    VALUES ("{second_name + ' ' + name + (' ' + patronymic if patronymic != '' else '')}",
    "{phone_number}", "{driver_license}", {drive_experience})
    '''

    result = False
    cur = conn.cursor()
    try:
        cur.execute(query)
        conn.commit()
        result = True
    except Exception as e:
        print(e)
    cur.close()

    return result


def make_a_rent(conn, car_id, driver_id, rent_date_start, rent_date_end, total_cost):
    query = f'''
    INSERT INTO rental_contract(car_id, client_id, rental_start_date, rental_end_date, total_cost)
    VALUES ({car_id}, {driver_id}, "{rent_date_start}", "{rent_date_end}", {total_cost})
    '''

    cur = conn.cursor()
    cur.execute(query)
    conn.commit()

    return True
