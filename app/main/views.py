from flask import render_template
from flask import Blueprint

main_app = Blueprint('main_app', __name__)

@main_app.route('/', methods=("GET",))
def hello_world():
    return render_template("index.html", name="Daryl")
