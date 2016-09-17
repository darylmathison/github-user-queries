from flask import Flask
from flask_bootstrap import Bootstrap
from flask_login import LoginManager
from .main.model import User

bootstrap = Bootstrap()
login_manager = LoginManager()
login_manager.session_protection = "strong"
login_manager.login_view = "main_app.login"


@login_manager.user_loader
def get_user(user_id):
    return User.get(user_id)


def create_app():
    app = Flask(__name__)
    bootstrap.init_app(app)
    login_manager.init_app(app)
    from .main.views import main_app
    app.register_blueprint(main_app)
    return app