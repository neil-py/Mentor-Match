from flask import Blueprint, render_template, redirect, url_for, flash
from app.extensions import db, bcrypt
from app.forms.admin import admin_manage_user_form
from app.models import users, activity_logs, sessions
from wtforms.validators import ValidationError as WTFormsValidationError  # Rename to avoid confusion
from flask_login import current_user, login_required
from datetime import datetime, timedelta


student_requests_route = Blueprint("student_requests", __name__, template_folder="app/templates", static_folder="app/static")

@student_requests_route.route('/student/requests')
@login_required
def my_requests():
    my_id = current_user.id
    my_requests = sessions.Sessions.query.filter(sessions.Sessions.student_id == my_id).join(users.Users, sessions.Sessions.student_id == users.Users.id).all()
    print(my_requests)
    return render_template("student_my_requests.html", requests=my_requests)