from flask import render_template, request, url_for, jsonify

from models.index_model import *
from utils import get_db_connection, to_list_of_int

from app import app


@app.route('/', methods=["GET", "POST"])
def index():
    conn = get_db_connection()

    # Получаем значения формы
    selected_states = [0, 1]  # Такое значение по умолчанию
    selected_brands = to_list_of_int(request.form.getlist('car-brand[]'))
    selected_colors = to_list_of_int(request.form.getlist('car-color[]'))
    cost_min = request.form.get("cost-min", "")
    cost_max = request.form.get("cost-max", "")
    year_min = request.form.get("year-min", "")
    year_max = request.form.get("year-max", "")
    grouping = request.form.get("car-grouping", "0")

    if "car-filter" in request.form:
        selected_states = to_list_of_int(request.form.getlist('car-state[]'))

    if "car-filter-clear" in request.form:
        selected_brands = []
        selected_colors = []
        cost_min = ""
        cost_max = ""
        year_min = ""
        year_max = ""
        grouping = "0"

    brands = get_brands(conn)
    colors = get_colors(conn)
    cost_range = get_car_cost_range(conn)
    year_of_manufacture_range = get_car_year_of_manufacture_range(conn)

    return render_template(
        'index.html',
        len=len,
        filtered_cars=[],
        # Form data
        cost_min=cost_min,
        cost_max=cost_max,
        year_min=year_min,
        year_max=year_max,
        grouping=grouping,
        selected_states=selected_states,
        selected_brands=selected_brands,
        selected_colors=selected_colors,
        # Display data
        brands=brands,
        colors=colors,
        cost_range=cost_range,
        year_of_manufacture_range=year_of_manufacture_range
    )
