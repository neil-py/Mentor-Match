from flask import Blueprint, render_template, redirect
from app.extensions import login_manager, account_type
from flask_login import current_user, login_required
from app.models import users

booking_route = Blueprint("booking", __name__, template_folder="app/templates", static_folder="app/static")

@booking_route.route("/booking/tutor/<id>")
@login_required
def booking(id):
    account_status = current_user.account_status
    if account_status == 1 or account_status == 2:
        return "Access Denied"
    else:
        tutor = users.Users.query.get(id)
        tutor_info = {
            "first_name": tutor.first_name,
            "last_name": tutor.last_name,
            "program": tutor.program.upper()
            }
        return render_template("booking_page.html", tutor_info = tutor_info)