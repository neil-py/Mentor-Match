from flask import Blueprint, render_template, redirect
from app.extensions import login_manager, account_type
from flask_login import current_user, login_required
from app.models import users

student_dashboard_route = Blueprint("student_dashboard", __name__, template_folder="app/templates", static_folder="app/static")

@student_dashboard_route.route("/student")
@login_required
def dashboard():
    tutors = users.Users.query.filter(users.Users.account_status == 2).all()
    return render_template("student_home.html", tutors=tutors)