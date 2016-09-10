from flask import render_template
from flask import Blueprint
from .forms import SearchForm
from .service import GitHubUserService

main_app = Blueprint('main_app', __name__)


@main_app.route('/', methods=("GET", "POST"))
def hello_world():
    form = SearchForm()
    results = []
    if form.validate_on_submit():
        name = form.username.data
        results = GitHubUserService.search_for_users(name)

    return render_template("index.html", results=results, form=form)


@main_app.route('/find/<username>')
def display_target(username):
    user = GitHubUserService.search_for_user(username)
    return render_template("user.html", user=user)
