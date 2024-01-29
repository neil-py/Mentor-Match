from flask import Blueprint, render_template, redirect, url_for, flash
from app.extensions import login_manager, account_type, db
from flask_login import current_user, login_required
from app.models import users, sessions, activity_logs
from datetime import datetime, timedelta
from app.forms.student import session_request

booking_route = Blueprint("booking", __name__, template_folder="app/templates", static_folder="app/static")

@booking_route.route("/student/booking/tutor/<id>", methods=["POST", "GET"])
@login_required
def booking(id):

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
    sessions.Sessions.tutor_id == id,
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
    
    #form
    request_form = session_request.SessionRequestForm()
    
    tutor = users.Users.query.get(id)
    tutor_info = {
            "id": tutor.id,
            "first_name": tutor.first_name,
            "last_name": tutor.last_name,
            "program": tutor.program.upper(),
            "tags": tutor.tags.split(",")
        }
    
    if request_form.validate_on_submit():
        date_format = '%Y-%m-%d'
        session_date = datetime.strptime(request_form.session_date.data, date_format)
        new_session = sessions.Sessions(
            tutor_id=id, 
            student_id=current_user.id,
            session_date=session_date,
            session_time=request_form.time_slot.data,
            course_code=request_form.course_code.data,
            course_name=request_form.course_name.data,
            description=request_form.description.data,
            session_type=request_form.session_type.data,
            communication_channel=request_form.communication_channel.data,
            session_status="requested"
            )
        db.session.add(new_session)
        db.session.commit()

        activity_log = activity_logs.ActivityLog(
                user_id=current_user.id,
                description="Tutor Session Requested",
                activity_type="SESSION REQUEST"
            )

        db.session.add(activity_log)
        db.session.commit()
            
        flash('Session Requested', 'Success')
        return redirect(url_for('booking.booking', id=id))
    
    return render_template("booking_page.html", 
                           tutor_info = tutor_info, 
                           week_range = week_range, 
                           tutor_sessions=tutor_sessions, 
                           time_slots=time_slots, 
                           days=days, days_date=days_date,
                           form=request_form)