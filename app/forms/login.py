from flask_wtf import FlaskForm
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import InputRequired, Length, ValidationError
from app.models import users
from app.extensions import bcrypt

class LoginForm(FlaskForm):
    login_name = StringField("Login Name", validators=[InputRequired(), Length(min=1, max=50)])
    password = PasswordField("Password", validators=[InputRequired(), Length(min=1, max=100)])
    login = SubmitField("Login")
