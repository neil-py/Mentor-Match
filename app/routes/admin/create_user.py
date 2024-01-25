from flask import Blueprint, render_template, redirect, url_for, flash
from app.forms import registration
from app.extensions import db, bcrypt
from app.forms.admin import admin_create_user
from app.models import users, activity_logs
from wtforms.validators import ValidationError as WTFormsValidationError  # Rename to avoid confusion
from flask_login import current_user
from datetime import datetime


admin_creation_route = Blueprint("admin_creation_route", __name__, template_folder="app/templates", static_folder="app/static")

@admin_creation_route.route("/admin/create-user", methods=['POST', 'GET'])
#TODO: add login_required decorator after testing
def create_user():
    
    form = admin_create_user.AdminCreateUserForm()
    check_form = form.validate_on_submit()
    if check_form:
        login_name = form.login_name.data
        university_email = form.university_email.data
        try:
            password = bcrypt.generate_password_hash(form.password.data)
            new_user = users.Users(
                login_name=login_name,
                first_name=form.first_name.data,
                last_name=form.last_name.data,
                university_number=form.university_number.data,
                university_email=university_email,
                program=form.program.data,
                password=password,
                account_status=form.account_status.data,  # default for creating a student account (tutee)
                tags="",
                profile_pic=""
            )
            db.session.add(new_user)
            db.session.commit()

            # Log the activity
            activity_log = activity_logs.ActivityLog(
                user_id=current_user.id,
                description="New User Created",
                activity_type="USER CREATION"
            )

            db.session.add(activity_log)
            db.session.commit()
            
            flash('Account Created', 'Success')
            return redirect(url_for("admin_redirects.manage_users"))
        
        except Exception as e:
            flash(str(e), 'ERROR')
            db.session.rollback()
    else:
        try:
            login_name = form.login_name.data
            university_email = form.university_email.data
            form.validate_login_name(form.login_name)
            form.validate_university_email(form.university_email)
        except WTFormsValidationError as e:
            flash(str(e))


    return render_template("admin_create_user.html", form=form)