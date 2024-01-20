import pandas as pd


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


def get_brands(conn, cost_min: int | None, cost_max: int | None, year_min: int | None, year_max: int | None):
    query = '''
    WITH car_brand_count AS (
        SELECT brand_id, brand_name, COUNT(car_id) as car_count
        FROM car
            JOIN model USING(model_id)
            JOIN brand USING(brand_id)
        WHERE
            (:cost_min IS NULL OR cost >= :cost_min)
            AND (:cost_max IS NULL OR cost <= :cost_max)
            AND (:year_min IS NULL OR year_of_manufacture >= :year_min)
            AND (:year_max IS NULL OR year_of_manufacture <= :year_max)
        GROUP BY brand_id
    )
    SELECT b.brand_id, b.brand_name, ifnull(car_count, 0) as car_count
    FROM brand b
        LEFT JOIN car_brand_count USING(brand_id)
    ORDER BY b.brand_name;
    '''

    params = {
        'cost_min': cost_min,
        'cost_max': cost_max,
        'year_min': year_min,
        'year_max': year_max
    }

    return pd.read_sql_query(query, conn, params=params)


def get_colors(conn, cost_min: int | None, cost_max: int | None, year_min: int | None, year_max: int | None):
    query = '''
    WITH car_brand_count AS (
        SELECT color_id, color_name, COUNT(car_id) as car_count
        FROM car
            JOIN color USING(color_id)
        WHERE
            (:cost_min IS NULL OR cost >= :cost_min)
            AND (:cost_max IS NULL OR cost <= :cost_max)
            AND (:year_min IS NULL OR year_of_manufacture >= :year_min)
            AND (:year_max IS NULL OR year_of_manufacture <= :year_max)
        GROUP BY color_id
    )
    SELECT c.color_id, c.color_name, ifnull(car_count, 0) as car_count
    FROM color c
        LEFT JOIN car_brand_count USING(color_id)
    ORDER BY c.color_name;
    '''

    params = {
        'cost_min': cost_min,
        'cost_max': cost_max,
        'year_min': year_min,
        'year_max': year_max
    }

    return pd.read_sql_query(query, conn, params=params)


def get_car_damage_list(conn, car_id):
    query = '''
    SELECT defect_name
    FROM car_defect
    JOIN defect USING(defect_id)
    WHERE car_id == :car_id
    '''

    return pd.read_sql_query(query, conn, params={'car_id': car_id})


def get_filtered_cars(conn, selected_brands: list[int], selected_colors: list[int], cost_min: int | None,
                      cost_max: int | None, year_min: int | None, year_max: int | None,
                      experience_min: int | None, experience_max: int | None, grouping: int):
    sb_as_string = ", ".join([str(t) for t in selected_brands])
    sc_as_string = ", ".join([str(t) for t in selected_colors])

    query = f'''
    SELECT
        c.car_id,
        b.brand_name,
        m.model_name,
        col.color_name,
        c.year_of_manufacture,
        c.license_plate,
        c.cost,
        strftime('%d.%m.%Y', rental_end_date) as rental_end_date,
        experience_requirement
    FROM
        car c
    JOIN model m ON c.model_id = m.model_id
    JOIN brand b ON m.brand_id = b.brand_id
    JOIN color col ON c.color_id = col.color_id
    LEFT JOIN rental_contract USING(car_id)
    WHERE
        {f"b.brand_id IN ({sb_as_string})" if len(selected_brands) > 0 else "TRUE"}
        AND {f"col.color_id IN ({sc_as_string})" if len(selected_colors) > 0 else "TRUE"}
        AND (:cost_min IS NULL OR c.cost >= :cost_min)
        AND (:cost_max IS NULL OR c.cost <= :cost_max)
        AND (:year_min IS NULL OR c.year_of_manufacture >= :year_min)
        AND (:year_max IS NULL OR c.year_of_manufacture <= :year_max)
        AND (:experience_min IS NULL OR experience_requirement >= :experience_min)
        AND (:experience_max IS NULL OR experience_requirement <= :experience_max)
    ORDER BY
        CASE
            WHEN :grouping = 1 THEN b.brand_name
            WHEN :grouping = 2 THEN c.year_of_manufacture
            ELSE c.car_id
        END;
    '''

    params = {
        'cost_min': cost_min,
        'cost_max': cost_max,
        'year_min': year_min,
        'year_max': year_max,
        'experience_min': experience_min,
        'experience_max': experience_max,
        'grouping': grouping
    }

    return pd.read_sql_query(query, conn, params=params)


def get_rent_cars(conn):
    query = '''
    SELECT car_id
    FROM rental_contract
    WHERE state == 0
    '''

    return pd.read_sql_query(query, conn)
