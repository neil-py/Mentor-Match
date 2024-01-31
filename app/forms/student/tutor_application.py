from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, IntegerField, SelectField, TextAreaField
from wtforms.validators import InputRequired, Length, Email, ValidationError
from app.models import sessions, users

class TutorApplicationForm(FlaskForm):
    description = TextAreaField("Provide a brief explanation on why you want to become a tutor", validators=[InputRequired()])
    request = SubmitField("SUBMIT")