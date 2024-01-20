from flask import render_template, session, redirect, request, url_for, flash
from datetime import datetime, timedelta

from app import app
from models.rental_conclusion_model import *
from utils import get_db_connection, get_years_declension


@app.route('/rental_conclusion', methods=["GET", "POST"])
def rental_conclusion():
    conn = get_db_connection()

    if not session.get("selected_car_id", None):
        return redirect(url_for("index"))

    driver_info = None
    driver_license = request.values.get("driver-license", "")

    if "add-driver" in request.values:
        second_name = request.values.get("second-name", "")
        name = request.values.get("name", "")
        patronymic = request.values.get("patronymic", "")
        phone_number = request.values.get("phone-number", "")
        is_error = False

        if len(second_name) < 2:
            flash("Фамилия должна содержать более двух букв!", "warning")
            is_error = True

        if len(name) < 2:
            flash("Имя должно содержать более двух букв!", "warning")
            is_error = True

        # if len(phone_number) != 11 or not phone_number.isdigit():

        if len(driver_license) != 9:
            flash("Номер водительского удостоверения должен содержать 9 символов!", "warning")
            is_error = True

        if not is_error:
            is_error = not add_driver(
                conn,
                second_name,
                name,
                patronymic,
                phone_number,
                driver_license,
                int(request.values.get("driver-experience", "0")) if request.values.get("driver-experience", "0") != "" else 0
            )
            if is_error:
                flash("Водитель не добавлен! Возможно водитель с таким номером телефона или номером водительского "
                      "удостоверения уже существует!", "warning")
            else:
                driver_info = get_driver_info(conn, driver_license.upper())

    if driver_license != "":
        driver_info = get_driver_info(conn, driver_license.upper())
        if len(driver_info) == 0:
            driver_info = None
            flash("Водитель не найден!", "warning")

    if driver_info is not None:
        driver_info[['second_name', 'name', 'patronymic']] = driver_info['full_name'].str.split(expand=True)
        driver_info.drop('full_name', axis=1, inplace=True)

    selected_car_id = session.get("selected_car_id")
    car_info = get_car_info(conn, selected_car_id)
    car_damage_list = get_car_damage_list(conn, selected_car_id)

    rent_date_start = request.values.get("rent-date-start", datetime.now().strftime("%Y-%m-%d"))
    rent_date_end = request.values.get("rent-date-end", (datetime.now() + timedelta(days=1)).strftime("%Y-%m-%d"))

    if "make-a-rent" in request.values:
        selected_driver_id = request.values.get("selected_driver_id")
        tt = datetime.strptime(rent_date_end, "%Y-%m-%d") - datetime.strptime(rent_date_start, "%Y-%m-%d")
        make_a_rent(
            conn,
            session.get("selected_car_id"),
            selected_driver_id,
            rent_date_start,
            rent_date_end,
            tt.days * car_info.cost[0]
        )
        return redirect(url_for("rental"))

    active_rents = get_active_rents(conn)

    is_can_rent_a_car = (driver_info is not None
                         and driver_info.client_id[0] not in active_rents.client_id.values
                         and driver_info.driver_experience[0] >= car_info.experience_requirement[0])

    if driver_info is not None and driver_info.client_id[0] in active_rents.client_id.values:
        flash("Водитель уже арендует другую машину.", "warning")

    if driver_info is not None and driver_info.driver_experience[0] < car_info.experience_requirement[0]:
        flash("У водителя недостаточно водительского стажа для аренды этой машины.", "warning")

    driver_licenses = get_drivers_licenses(conn)

    return render_template(
        'rental_conclusion.html',
        len=len,
        car_info=car_info,
        car_damage_list=car_damage_list,
        driver_info=driver_info,
        driver_license=driver_license,
        driver_licenses=driver_licenses,
        rent_date_start=rent_date_start,
        rent_date_end=rent_date_end,
        is_can_rent_a_car=is_can_rent_a_car,
        get_years_declension=get_years_declension
    )
