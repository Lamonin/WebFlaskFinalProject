from flask import Flask, render_template

app = Flask(__name__)
app.secret_key = b'_5#y2L"F4Q8z\n\xec]/'

import controllers.index
import controllers.rental
import controllers.rental_conclusion
import controllers.rental_closing

if __name__ == '__main__':
    app.run()
