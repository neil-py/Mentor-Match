from flask import Blueprint, render_template, redirect, url_for, flash
from app.forms.login import LoginForm
from wtforms.validators import ValidationError as WTFormsValidationError  # Rename to avoid confusion
from app.models import users
from app.extensions import bcrypt, db, login_manager
from flask_login import login_user, logout_user, current_user

authentication = Blueprint("authentication", __name__, template_folder="app/templates", static_folder="app/static")

@authentication.route("/login", methods=['POST', 'GET'])
def login():
    # checks if user is already logged in
    if current_user.is_authenticated:
        return redirect(url_for('home.home'))
    
    form = LoginForm()

    if form.validate_on_submit():
        print("valid")
        login_name = form.login_name.data
        password = form.password.data
        user = users.Users.query.filter_by(login_name=login_name).first()

        if user:
            try:
                if bcrypt.check_password_hash(user.password, password):
                    login_user(user)
                    return redirect(url_for('home.home'))
                else:
                    flash("Invalid Username or password!", "danger")
            except Exception as e:
                flash(e, "danger")
        else:
            flash("User Does Not Exist.", "danger")



    return render_template("login.html", form=form)

@authentication.route("/logout")
def logout():
    logout_user()
    return redirect(url_for('authentication.login'))


