from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, IntegerField, SelectField
from wtforms.validators import InputRequired, Length, Email, ValidationError
from app.models import sessions, users

class SessionRequestForm(FlaskForm):
    time_slot = StringField("Time Slot")
    session_date = StringField("Date")
    course_code = StringField("Course Code", validators=[InputRequired()])
    course_name = StringField("Course Name", validators=[InputRequired()])
    description = StringField("Description", validators=[InputRequired()])
    session_type = SelectField("Session Type", choices=["Online", "In-Person"], default="In-Person")
    communication_channel = StringField("Communication Means (Email, FB Link, Teams Email)", validators=[InputRequired()])
    request = SubmitField("Request")