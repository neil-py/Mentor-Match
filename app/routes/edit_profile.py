from flask import Blueprint, render_template, redirect, url_for, flash
from app.extensions import db, bcrypt
from app.forms import edit_profile_form
from app.models import users, activity_logs, sessions
from wtforms.validators import ValidationError as WTFormsValidationError  # Rename to avoid confusion
from flask_login import current_user, login_required
from datetime import datetime, timedelta


edit_profile_route = Blueprint("edit_profile", __name__, template_folder="app/templates", static_folder="app/static")

@edit_profile_route.route('/edit/profile', methods=['GET', 'POST'])
@login_required
def edit_profile():
    user=users.Users.query.get(current_user.id)
    user_password = user.password
    form = edit_profile_form.EditProfile(obj=user)
    check_form = form.validate_on_submit()
    
    if check_form:
        form.populate_obj(user)
        new_password = form.password.data
        if new_password:  # Check if new password is provided
            hashed_password = bcrypt.generate_password_hash(new_password).decode('utf-8')
            user.password = hashed_password
        # No need for an "else" statement here; if new_password is empty, it won't update the password
        else:
            user.password = user_password
        db.session.commit()
        flash('Profile information updated successfully', 'success')
        return redirect(url_for('edit_profile.edit_profile')) 

    return render_template("edit_profile.html", form=form)