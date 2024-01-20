import pandas as pd


def get_filtered_rents(conn, rent_states, rent_start_date, rent_end_date, client_full_name, auto_number_plate):
    query = f'''
    SELECT
        rental_contract_id,
        brand_name || ' ' || model_name AS car_name,
        license_plate,
        full_name AS driver_name,
        strftime('%d.%m.%Y', rental_start_date) AS rental_start_date,
        strftime('%d.%m.%Y', rental_end_date) AS rental_end_date,
        total_cost,
        fine_amount,
        state,
        floor(MAX(julianday('now') - julianday(rental_end_date), 0)) AS days_overdue
    FROM rental_contract
    JOIN client USING(client_id)
    JOIN car USING(car_id)
    JOIN model USING(model_id)
    JOIN brand USING(brand_id)
    WHERE TRUE
        {f"AND state IN ({', '.join([str(rs) for rs in rent_states])})" if len(rent_states) > 0 else ""}
        AND rental_start_date >= "{rent_start_date}"
        AND rental_end_date <= "{rent_end_date}"
        AND instr(full_name, "{client_full_name}")
        AND instr(license_plate, "{auto_number_plate}")
    '''

    return pd.read_sql_query(query, conn)


def get_rental_date_range(conn):
    query = '''
    SELECT min(rental_start_date) as date
    FROM rental_contract
    UNION ALL
    SELECT max(rental_end_date) as date
    FROM rental_contract
    '''

    return pd.read_sql_query(query, conn)


def get_clients(conn):
    query = '''
    SELECT
            client_id,
            full_name,
            driver_license_number as license_number
    FROM client
    ORDER BY full_name
    '''

    return pd.read_sql_query(query, conn)
