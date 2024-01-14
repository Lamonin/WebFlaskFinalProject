from flask import render_template

from app import app
from utils import get_db_connection


@app.route('/rental')
def rental():
    return render_template(
        'rental.html',
        len=len
    )
