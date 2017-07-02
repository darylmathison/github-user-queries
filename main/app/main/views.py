from flask import render_template
from flask import redirect
from flask import request
from flask import Blueprint
from flask import url_for
from flask_login import login_required
from flask_login import login_user
from flask_login import logout_user
from .forms import SearchForm
from .forms import LoginForm
from .service import GitHubUserService
from .model import User

main_app = Blueprint('main_app', __name__)


@main_app.route('/', methods=("GET", "POST"))
@login_required
def hello_world():
    form = SearchForm()
    results = []
    if form.validate_on_submit():
        name = form.username.data
        results = GitHubUserService.search_for_users(name)

    return render_template("index.html", results=results, form=form)


@main_app.route('/find/<username>')
@login_required
def display_target(username):
    user = GitHubUserService.search_for_user(username)
    return render_template("user.html", user=user)


@main_app.route("/login", methods=("GET", "POST"))
def login():
    form = LoginForm()
    if form.validate_on_submit():
        github_name = form.login_name.data
        password = form.password.data
        if GitHubUserService.validate_user(github_name, password):
            login_user(User(github_name, password))
            return redirect(request.args.get("next") or url_for(".hello_world"))

    return render_template("login.html", form=form)


@main_app.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for(".login"))
