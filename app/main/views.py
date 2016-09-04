from flask import render_template
from flask import Blueprint
from .forms import SearchForm
from .service import GithubUserService

main_app = Blueprint('main_app', __name__)

@main_app.route('/', methods=("GET","POST"))
def hello_world():
    form = SearchForm()
    results = []
    if form.validate_on_submit():
        name = form.username.data
        results = GithubUserService.search_for_user(name)

    return render_template("index.html", results=results, form=form)
