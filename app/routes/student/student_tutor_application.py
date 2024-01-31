from flask import Blueprint, render_template, redirect, url_for, flash
from app.extensions import db, bcrypt
from app.forms.student import tutor_application as application_form
from app.models import tutor_applications
from wtforms.validators import ValidationError as WTFormsValidationError  # Rename to avoid confusion
from flask_login import current_user, login_required
from datetime import datetime, timedelta


student_tutor_application_route = Blueprint("student_tutor_application", __name__, template_folder="app/templates", static_folder="app/static")

@student_tutor_application_route.route('/student/tutor-application', methods=['POST', 'GET'])
@login_required
def tutor_application():
    application = tutor_applications.TutorApplications.query.filter_by(student_id=current_user.id).first()
    form = application_form.TutorApplicationForm()

    if form.validate_on_submit():
        new_application = tutor_applications.TutorApplications(student_id=current_user.id, description=form.description.data)
        db.session.add(new_application)
        db.session.commit()
        flash("Tutor Application Submitted", "Success")
        return redirect(url_for("student_tutor_application.tutor_application"))
    
    return render_template("student_tutor_application.html", form=form, application=application)