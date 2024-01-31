from flask import Blueprint, render_template, redirect, url_for, flash
from app.extensions import db, bcrypt
from app.forms.admin import admin_manage_user_form
from app.models import users, activity_logs, sessions, tutor_applications
from wtforms.validators import ValidationError as WTFormsValidationError  # Rename to avoid confusion
from flask_login import current_user, login_required
from sqlalchemy.orm import aliased


admin_redirects_route = Blueprint("admin_redirects", __name__, template_folder="app/templates", static_folder="app/static")

@admin_redirects_route.route("/admin/manage/users", methods=['POST', 'GET'])
@login_required
def manage_users():
    users_all = users.Users.query.filter(users.Users.account_status != 1).all()
    return render_template("admin_home.html", users= users_all, show_manage_users=True, show_manage_logs=False, show_session_requests=False, show_tutor_applications=False)

@admin_redirects_route.route("/admin/manage/logs", methods=['POST', 'GET'])
@login_required
def manage_activity_logs():
    logs = db.session.query(activity_logs.ActivityLog, users.Users) \
    .join(users.Users, activity_logs.ActivityLog.user_id == users.Users.id) \
    .order_by(activity_logs.ActivityLog.timestamp.desc()) \
    .all()
    return render_template("admin_home.html", activity_logs= logs, show_manage_users=False, show_manage_logs=True, show_session_requests=False, show_tutor_applications=False)

@admin_redirects_route.route("/admin/manage/sessions", methods=['POST', 'GET'])
@login_required
def admin_manage_sessions():
    student_users = aliased(users.Users)
    # Alias for tutor users
    tutor_users = aliased(users.Users)

    requests = sessions.Sessions.query \
        .join(student_users, sessions.Sessions.student_id == student_users.id) \
        .join(tutor_users, sessions.Sessions.tutor_id == tutor_users.id) \
        .order_by(sessions.Sessions.session_date.asc()) \
        .all()
    return render_template("admin_home.html", requests= requests, show_manage_users=False, show_manage_logs=False, show_session_requests=True, show_tutor_applications=False)

@admin_redirects_route.route('/admin/manage/sessions/s/<id>')
@login_required
def manage_session(id):
    session = sessions.Sessions.query.get(id)
    student = users.Users.query.get(session.student_id)
    tutor = users.Users.query.get(session.tutor_id)
    return render_template("manage_session.html", session=session, student=student, tutor=tutor)


@admin_redirects_route.route('/admin/manage/applications')
@login_required
def manage_tutor_applications():
    applications = tutor_applications.TutorApplications.query.join(users.Users, tutor_applications.TutorApplications.student_id == users.Users.id).all()
    return render_template("admin_home.html", applications= applications, show_manage_users=False, show_manage_logs=False, show_session_requests=False, show_tutor_applications=True)

@admin_redirects_route.route('/admin/manage/applications/u/<id>')
@login_required
def manage_tutor_application_page(id: int):
    application_information = tutor_applications.TutorApplications.query.join(users.Users, tutor_applications.TutorApplications.student_id == id).all()
    return render_template("admin_manage_applications.html", application_information=application_information)