from flask import render_template, request, url_for, session, redirect

from models.index_model import *
from utils import get_db_connection, to_list_of_int, c_int, get_years_declension

from app import app


@app.route('/', methods=["GET", "POST"])
def index():
    conn = get_db_connection()

    if "car-rent" in request.values:
        session["selected_car_id"] = request.values.get("car-id")
        return redirect(url_for("rental_conclusion"))

    # Получаем значения формы
    selected_states = [0, 1]  # Такое значение по умолчанию
    selected_brands = to_list_of_int(request.values.getlist('car-brand[]'))
    selected_colors = to_list_of_int(request.values.getlist('car-color[]'))
    cost_min = request.values.get("cost-min", "")
    cost_max = request.values.get("cost-max", "")
    year_min = request.values.get("year-min", "")
    year_max = request.values.get("year-max", "")
    experience_min = request.values.get("experience-min", "")
    experience_max = request.values.get("experience-max", "")
    grouping = request.values.get("car-grouping", "0")

    if "car-filter" in request.values:
        selected_states = to_list_of_int(request.values.getlist('car-state[]'))

    if "car-filter-clear" in request.values:
        selected_states = [0, 1]
        selected_brands = []
        selected_colors = []
        cost_min = ""
        cost_max = ""
        year_min = ""
        year_max = ""
        experience_min = ""
        experience_max = ""
        grouping = "0"

    filtered_cars = get_filtered_cars(
        conn,
        selected_brands,
        selected_colors,
        c_int(cost_min),
        c_int(cost_max),
        c_int(year_min),
        c_int(year_max),
        c_int(experience_min),
        c_int(experience_max),
        c_int(grouping)
    )

    rent_cars = get_rent_cars(conn)

    cars_damage_list = [get_car_damage_list(conn, car_id) for car_id in filtered_cars.car_id]

    brands = get_brands(conn, c_int(cost_min), c_int(cost_max), c_int(year_min), c_int(year_max))
    colors = get_colors(conn, c_int(cost_min), c_int(cost_max), c_int(year_min), c_int(year_max))
    cost_range = get_car_cost_range(conn)
    year_of_manufacture_range = get_car_year_of_manufacture_range(conn)

    return render_template(
        'index.html',
        len=len,
        get_years_declension=get_years_declension,
        # Form data
        cost_min=cost_min,
        cost_max=cost_max,
        year_min=year_min,
        year_max=year_max,
        experience_min=experience_min,
        experience_max=experience_max,
        grouping=grouping,
        selected_states=selected_states,
        selected_brands=selected_brands,
        selected_colors=selected_colors,
        # Display data
        cars=filtered_cars,
        rent_cars=rent_cars,
        cars_damage_list=cars_damage_list,
        brands=brands,
        colors=colors,
        cost_range=cost_range,
        year_of_manufacture_range=year_of_manufacture_range
    )
