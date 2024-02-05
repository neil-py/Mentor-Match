from flask import Blueprint, render_template, redirect, url_for, flash
from app.forms import registration
from app.extensions import db, bcrypt
from app.forms.admin import admin_create_user
from app.models import users
from wtforms.validators import ValidationError as WTFormsValidationError  # Rename to avoid confusion
from flask_login import current_user


registration_route = Blueprint("registration", __name__, template_folder="app/templates", static_folder="app/static")

# simple account creation
@registration_route.route("/registration", methods = ["POST", "GET"])
def register():
    # checks if user is already logged in
    if current_user.is_authenticated:
        return redirect(url_for('home.home'))
    
    form = registration.RegistrationForm()
    check_form = form.validate_on_submit()
    print(check_form)
    if check_form:
        print("test")
        login_name = form.login_name.data
        university_email = form.university_email.data
        try:
            password = bcrypt.generate_password_hash(form.password.data)
            new_user = users.Users(
                login_name=login_name.lower(),
                first_name=form.first_name.data,
                last_name=form.last_name.data,
                university_number=form.university_number.data,
                university_email=university_email,
                program=form.program.data,
                password=password,
                account_status=3,  # default for creating a student account (tutee)
                tags="",
                #profile_pic=""
            )

            db.session.add(new_user)
            db.session.commit()
            
            flash('Account Created', 'Success')
            return redirect(url_for("authentication.login"))

        
        except Exception as e:
            flash(str(e), 'ERROR')
            db.session.rollback()
    else:
        print("error")
        try:
            login_name = form.login_name.data
            university_email = form.university_email.data
            form.validate_login_name(form.login_name)
            form.validate_university_email(form.university_email)
        except WTFormsValidationError as e:
            flash(str(e))


    return render_template("registration.html", form=form)