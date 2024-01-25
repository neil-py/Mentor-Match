from flask import Blueprint, render_template, redirect, url_for, flash
from app.extensions import db, bcrypt
from app.forms.admin import admin_manage_user_form
from app.models import users, activity_logs
from wtforms.validators import ValidationError as WTFormsValidationError  # Rename to avoid confusion
from flask_login import current_user, login_required


admin_redirects_route = Blueprint("admin_redirects", __name__, template_folder="app/templates", static_folder="app/static")

@admin_redirects_route.route("/admin/manage/users", methods=['POST', 'GET'])
@login_required
def manage_users():
    users_all = users.Users.query.filter(users.Users.account_status != 1).all()
    return render_template("admin_home.html", users= users_all, show_manage_users=True, show_manage_logs=False)

@admin_redirects_route.route("/admin/manage/logs", methods=['POST', 'GET'])
@login_required
def manage_activity_logs():
    logs = db.session.query(activity_logs.ActivityLog, users.Users) \
    .join(users.Users, activity_logs.ActivityLog.user_id == users.Users.id) \
    .order_by(activity_logs.ActivityLog.timestamp.desc()) \
    .all()
    return render_template("admin_home.html", activity_logs= logs, show_manage_users=False, show_manage_logs=True)