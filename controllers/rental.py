from flask import render_template, request, session, redirect, url_for

from app import app
from models.rental_model import *
from utils import get_db_connection, to_list_of_int


@app.route('/rental')
def rental():
    conn = get_db_connection()

    rental_date_range = get_rental_date_range(conn)

    # Получаем значения формы
    selected_states = [0, 1]  # Такое значение по умолчанию
    rental_start_date = request.values.get("rental-start-date", rental_date_range.date[0])
    rental_end_date = request.values.get("rental-end-date", rental_date_range.date[1])
    client_name = request.values.get("client-name", "")
    auto_number_plate = request.values.get("auto-number-plate", "")

    if "rental-filter" in request.values:
        selected_states = to_list_of_int(request.values.getlist('rental_state[]'))

    # Сброс фильтров
    if "rental-filter-clear" in request.values:
        selected_states = [0, 1]
        rental_start_date = rental_date_range.date[0]
        rental_end_date = rental_date_range.date[1]
        client_name = ""
        auto_number_plate = ""

    rents = get_filtered_rents(conn, selected_states, rental_start_date, rental_end_date, client_name, auto_number_plate)
    clients = get_clients(conn)

    if "end-rental" in request.values:
        session["rental_contract_id"] = request.values.get("rental-contract-id")
        return redirect(url_for("rental_closing"))

    return render_template(
        'rental.html',
        len=len,
        int=int,
        rents=rents,
        clients=clients,
        selected_states=selected_states,
        rental_start_date=rental_start_date,
        rental_end_date=rental_end_date,
        rental_min_date=rental_date_range.date[0],
        rental_max_date=rental_date_range.date[1],
        client_name=client_name,
        auto_number_plate=auto_number_plate
    )
