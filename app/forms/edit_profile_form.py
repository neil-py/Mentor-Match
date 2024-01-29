from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, IntegerField, SelectField
from wtforms.validators import InputRequired, Length, Email, ValidationError
from app.models import users

class EditProfile(FlaskForm):
    login_name = StringField('Login Name', validators=[InputRequired(), Length(min=1, max=50)])
    first_name = StringField('First Name', validators=[InputRequired(), Length(min=1, max=100)])
    last_name = StringField('Last Name', validators=[InputRequired(), Length(min=1, max=100)])
    university_number = StringField('University Number', validators=[InputRequired(), Length(min=1, max=20)])
    university_email = StringField('University Email', validators=[InputRequired(), Email(), Length(min=1, max=225)])
    program = StringField('Program', validators=[Length(max=100)])
    password = PasswordField('Password', validators=[Length(min=0, max=100)])
    tags = StringField('Tags', validators=[Length(max=100)])
    account_status = SelectField("Account Type", choices=[(1, "ADMIN"), (2, "TUTOR"), (3, "STUDENT")])
    edit_user = SubmitField('APPLY CHANGES')