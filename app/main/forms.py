from flask_wtf import Form
from wtforms import StringField
from wtforms import SubmitField
from wtforms.validators import DataRequired

class SearchForm(Form):
    username = StringField("Name", validators=[DataRequired()])
    submit = SubmitField("Search")
