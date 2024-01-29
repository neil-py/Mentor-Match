from flask import Blueprint, render_template, redirect
from app.extensions import login_manager, account_type, account_type
from flask_login import current_user, login_required
from app.models import users


tutor_dashboard_route = Blueprint("tutor_dashboard", __name__, template_folder="app/templates", static_folder="app/static")

@tutor_dashboard_route.route("/tutor")
@login_required
def dashboard():
    return render_template("tutor_home.html", 
                           show_my_schedule=False, 
                           show_session_requests=False,
                           show_contact_admin=False)