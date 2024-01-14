from flask import render_template

from app import app
from utils import get_db_connection


@app.route('/rental/conclusion')
def rental_conclusion():
    return render_template(
        'rental_conclusion.html',
        len=len
    )
