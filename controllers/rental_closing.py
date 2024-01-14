from flask import render_template

from app import app
from utils import get_db_connection


@app.route('/rental/closing')
def rental_closing():
    return render_template(
        'rental_closing.html',
        len=len
    )
