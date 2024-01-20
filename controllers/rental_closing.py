from datetime import datetime

from flask import render_template, session, request, url_for, redirect

from app import app
from models.rental_closing_model import *
from utils import get_db_connection, get_years_declension, to_list_of_int, get_days_declension


@app.route('/rental/closing')
def rental_closing():
    conn = get_db_connection()

    if not session.get("rental_contract_id", None):
        return redirect(url_for("rental"))

    rental_contract_id = session["rental_contract_id"]

    contract_info = get_contract_info(conn, rental_contract_id)
    rent_start_date = contract_info.rental_start_date[0]
    rent_end_date = contract_info.rental_end_date[0]

    current_date = datetime.now().date()
    rent_end_date_obj = datetime.strptime(rent_end_date, "%Y-%m-%d").date()
    days_difference = (current_date - rent_end_date_obj).days
    fine_days = max(days_difference, 0)

    driver_info = get_driver_info(conn, rental_contract_id)
    driver_info[['second_name', 'name', 'patronymic']] = driver_info['full_name'].str.split(expand=True)
    driver_info.drop('full_name', axis=1, inplace=True)

    car_info = get_car_info(conn, rental_contract_id)
    car_damage_list = get_car_damage_list(conn, int(car_info.car_id[0]))

    damage_list = get_damage_list(conn)
    new_damages_list = request.values.getlist("new_damages[]")

    if "new_damage" in request.values:
        new_damages_list.append(request.values.get("new_damage_id"))

    if "remove_new_damage" in request.values:
        del new_damages_list[int(request.values.get("remove_new_damage"))]

    fine_amount = sum([damage_list.iloc[(int(i) - 1, 2)] for i in new_damages_list]) + fine_days * car_info.cost[0]
    total_cost = contract_info.total_cost[0] + fine_amount

    if "close-a-rent" in request.values:
        if len(new_damages_list) > 0:
            update_car_damages_list(conn, car_info.car_id[0], new_damages_list)
        close_a_rent(conn, rental_contract_id, total_cost, fine_amount)
        return redirect(url_for("rental"))

    return render_template(
        'rental_closing.html',
        len=len,
        driver_info=driver_info,
        car_info=car_info,
        car_damage_list=car_damage_list,
        rent_start_date=rent_start_date,
        rent_end_date=rent_end_date,
        damage_list=damage_list,
        new_damages_list=to_list_of_int(new_damages_list),
        total_cost=total_cost,
        fine_amount=fine_amount,
        fine_days=fine_days,
        # Utils
        get_years_declension=get_years_declension,
        get_days_declension=get_days_declension
    )
