from flask import Blueprint, render_template, redirect, url_for, flash
from app.extensions import db, bcrypt
from app.forms.admin import admin_manage_user_form
from app.models import users, activity_logs, sessions
from wtforms.validators import ValidationError as WTFormsValidationError  # Rename to avoid confusion
from flask_login import current_user, login_required
from datetime import datetime, timedelta


tutor_redirects_route =Blueprint("tutor_redirects", __name__, template_folder="app/templates", static_folder="app/static")

@tutor_redirects_route.route('/tutor/schedule')
@login_required
def my_schedule():
    today = datetime.today()
    start_of_week = today - timedelta(days=today.weekday())
    
    # Calculate the end date of the current week (Sunday)
    end_of_week = start_of_week + timedelta(days=4)

    # Assuming you have a list of schedule data, filter it for the current week
    # Replace this with your actual schedule data retrieval logic
    week_range = start_of_week, end_of_week

    # str(start_of_week.strftime('%y-%m-%d')) str(end_of_week.strftime('%y-%m-%d'))
    start_of_week_str = str(start_of_week.strftime('%Y-%m-%d'))
    end_of_week_str = str(end_of_week.strftime('%Y-%m-%d'))
    tutor_sessions = sessions.Sessions.query.filter(
    sessions.Sessions.tutor_id == current_user.id,
    sessions.Sessions.session_date >= start_of_week_str,
    sessions.Sessions.session_date <= end_of_week_str
    ).all()

    
    time_slots = [
        '7:30 AM - 9:00 AM',
        '9:00 AM - 10:30 AM',
        '10:30 AM - 12:00 PM',
        '12:00 PM - 1:30 PM',
        '1:30 PM - 3:00 PM',
        '3:00 PM - 4:30 PM',
    ]

    days = ['monday', 'tuesday', 'wednesday', 'thursday', 'friday']

    days_date = {'monday':str((start_of_week + timedelta(days=0)).strftime('%Y-%m-%d')), 
            'tuesday':str((start_of_week + timedelta(days=1)).strftime('%Y-%m-%d')), 
            'wednesday':str((start_of_week + timedelta(days=2)).strftime('%Y-%m-%d')), 
            'thursday':str((start_of_week + timedelta(days=3)).strftime('%Y-%m-%d')), 
            'friday':str((start_of_week + timedelta(days=4)).strftime('%Y-%m-%d'))
            }
    return render_template("tutor_home.html", 
                           show_my_schedule=True, 
                           show_session_requests=False,
                           show_contact_admin=False,
                           week_range = week_range, 
                           tutor_sessions=tutor_sessions, 
                           time_slots=time_slots, 
                           days=days, days_date=days_date
                           )


@tutor_redirects_route.route('/tutor/requests')
@login_required
def session_requests():
    today = datetime.today()
    start_of_week = today - timedelta(days=today.weekday())
    
    # Calculate the end date of the current week (Sunday)
    end_of_week = start_of_week + timedelta(days=4)

    # str(start_of_week.strftime('%y-%m-%d')) str(end_of_week.strftime('%y-%m-%d'))
    start_of_week_str = str(start_of_week.strftime('%Y-%m-%d'))
    end_of_week_str = str(end_of_week.strftime('%Y-%m-%d'))
    #sessions query
    requests = sessions.Sessions.query.filter(
        sessions.Sessions.tutor_id == current_user.id, 
        sessions.Sessions.session_status=='requested',
        sessions.Sessions.session_date >= start_of_week_str,
        sessions.Sessions.session_date <= end_of_week_str) \
        .join(users.Users, sessions.Sessions.student_id == users.Users.id) \
        .order_by(sessions.Sessions.session_date.asc()) \
        .all()
    
    return render_template("tutor_home.html",
                           show_my_schedule=False, 
                           show_session_requests=True,
                           show_contact_admin=False,
                           requests=requests
                           )


@tutor_redirects_route.route('/session/<id>')
@login_required
def manage_session(id):
    session = sessions.Sessions.query.get(id)
    student = users.Users.query.get(session.student_id)
    tutor = users.Users.query.get(session.tutor_id)
    return render_template("manage_session.html", session=session, student=student, tutor=tutor)

    

@tutor_redirects_route.route('/tutor/accept/session/<id>')
@login_required
def accept_session(id):
    session_update = sessions.Sessions.query.get(id)

    if session_update:
        session_update.session_status = 'accepted'
        db.session.commit()
        return redirect(url_for('tutor_redirects.manage_session', id=id))
    
@tutor_redirects_route.route('/tutor/deny/session/<id>')
@login_required
def deny_session(id):
    session_update = sessions.Sessions.query.get(id)

    if session_update:
        session_update.session_status = 'denied'
        db.session.commit()
        return redirect(url_for('tutor_redirects.manage_session', id=id))