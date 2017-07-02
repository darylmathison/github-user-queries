from flask_wtf import Form
from wtforms import StringField
from wtforms import SubmitField
from wtforms import PasswordField
from wtforms.validators import DataRequired


class LoginForm(Form):
    login_name = StringField("GitHub username", validators=(DataRequired(),))
    password = PasswordField("Password", validators=(DataRequired(),))
    submit = SubmitField("Login")


class SearchForm(Form):
    username = StringField("Name", validators=[DataRequired()])
    submit = SubmitField("Search")
