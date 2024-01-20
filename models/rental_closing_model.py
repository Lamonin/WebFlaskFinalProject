import pandas as pd


def get_contract_info(conn, contract_id):
    query = '''
    SELECT *
    FROM rental_contract
    WHERE rental_contract_id == :contract_id
    '''

    return pd.read_sql_query(query, conn, params={'contract_id': contract_id})


def get_driver_info(conn, contract_id):
    query = '''
    SELECT *
    FROM client
    JOIN rental_contract USING(client_id)
    WHERE rental_contract_id == :contract_id
    '''

    return pd.read_sql_query(query, conn, params={'contract_id': contract_id})


def get_car_info(conn, contract_id):
    query = '''
    SELECT
        car.car_id,
        brand_name || ' ' || model_name AS car_name,
        license_plate,
        year_of_manufacture as year,
        color_name as color,
        experience_requirement as experience,
        cost
    FROM car
    JOIN rental_contract USING(car_id)
    JOIN color USING(color_id)
    JOIN model USING(model_id)
    JOIN brand USING(brand_id)
    WHERE rental_contract_id == :contract_id
    '''

    return pd.read_sql_query(query, conn, params={'contract_id': contract_id})


def get_car_damage_list(conn, car_id):
    query = '''
    SELECT defect_name
    FROM car_defect
    JOIN defect USING(defect_id)
    WHERE car_id == :car_id
    '''

    return pd.read_sql_query(query, conn, params={'car_id': car_id})


def get_damage_list(conn):
    query = '''
    SELECT *
    FROM defect
    '''

    return pd.read_sql_query(query, conn)


def update_car_damages_list(conn, car_id, new_damages_list):
    values = ", ".join([f"({car_id}, {defect_id})" for defect_id in new_damages_list])
    query = f'''
    INSERT INTO car_defect(car_id, defect_id)
    VALUES
        {values};
    '''

    cur = conn.cursor()
    cur.execute(query)
    conn.commit()

    return True


def close_a_rent(conn, contract_id, total_cost, fine_amount):
    query = f'''
    UPDATE rental_contract
    SET state = 1, total_cost = {total_cost}, fine_amount = {fine_amount}
    WHERE rental_contract_id == {contract_id}
    '''

    cur = conn.cursor()
    cur.execute(query)
    conn.commit()

    return True
