from flask import Blueprint, render_template, redirect
from app.extensions import login_manager, account_type
from flask_login import current_user, login_required
from app.models import users

admin_dashboard_route = Blueprint("admin_dashboard", __name__, template_folder="app/templates", static_folder="app/static")

@admin_dashboard_route.route("/admin")
@login_required
def dashboard():
    users_all = users.Users.query.filter(users.Users.account_status != 1).all()
    return render_template('admin_home.html', users = users_all)