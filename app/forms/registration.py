from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import InputRequired, Length, Email, ValidationError
from app.models import users

class RegistrationForm(FlaskForm):
    login_name = StringField('Login Name', validators=[InputRequired(), Length(min=1, max=50)])
    first_name = StringField('First Name', validators=[InputRequired(), Length(min=1, max=100)])
    last_name = StringField('Last Name', validators=[InputRequired(), Length(min=1, max=100)])
    university_number = StringField('University Number', validators=[InputRequired(), Length(min=1, max=20)])
    university_email = StringField('University Email', validators=[InputRequired(), Email(), Length(min=1, max=225)])
    program = StringField('Program', validators=[Length(max=100)])
    password = PasswordField('Password', validators=[InputRequired(), Length(min=1, max=100)])
    register = SubmitField('Register')


    #perform checks if the login_name and email already exist in the database
    def validate_login_name(self, field):
        if users.Users.is_login_name_taken(field.data):
            raise ValidationError('This Login Name is already taken. Please choose another one or Login.')
        
    def validate_university_email(self, field):
        if users.Users.is_university_email_taken(field.data):
            raise ValidationError('This email is already registered. Please use a different email address or Login.')