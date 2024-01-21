from flask import Blueprint, render_template, redirect, url_for
from app.extensions import login_manager, account_type
from flask_login import current_user, login_required

home_route = Blueprint("home", __name__, template_folder="app/templates", static_folder="app/static")

@home_route.route("/")
@login_required
def home():
    account_status = current_user.account_status
    if account_status == 1: # admin account type
        return redirect(url_for('admin_dashboard.dashboard'))
    elif account_status == 2: # tutor account type
        return redirect(url_for('tutor_dashboard.dashboard'))
    else: # student account type
        return redirect(url_for('student_dashboard.dashboard'))