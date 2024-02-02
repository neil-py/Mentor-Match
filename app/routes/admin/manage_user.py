from flask import Blueprint, render_template, redirect, url_for, flash
from app.extensions import db, bcrypt
from app.forms.admin import admin_manage_user_form
from app.models import users, activity_logs
from wtforms.validators import ValidationError as WTFormsValidationError  # Rename to avoid confusion
from flask_login import current_user, login_required


admin_manage_route = Blueprint("admin_manage_route", __name__, template_folder="app/templates", static_folder="app/static")

@admin_manage_route.route("/admin/manage/users/u/<id>", methods=['POST', 'GET'])
@login_required
def manage_user(id):
    user = users.Users.query.filter_by(id = id).first()
    form = admin_manage_user_form.AdminManageUserForm(obj=user)
    check_form = form.validate_on_submit()

    if check_form:
        oldUserPass = user.password
        form.populate_obj(user)
        new_password = form.password.data
        if new_password:
            print(new_password)
            hashed_password = bcrypt.generate_password_hash(new_password).decode('utf-8')
            print(hashed_password)
            user.password = hashed_password
        db.session.commit()
        # Revert the override from the form's empty password field
        if user.password == "":
            user.password = oldUserPass
            db.session.commit()


        flash('User information updated successfully', 'success')
        return redirect(url_for('admin_manage_route.manage_user', id=id)) 
    
    return render_template("admin_manage_user.html", user=user, form=form)

@admin_manage_route.route("/admin/delete/user/<id>", methods=['POST', 'GET'])
@login_required
def delete_user(id):
    user = users.Users.query.filter_by(id=id).first()
    db.session.delete(user)
    db.session.commit()

    activity_log = activity_logs.ActivityLog(
                user_id=current_user.id,
                description="User Deleted",
                activity_type="USER DELETION"
            )

    db.session.add(activity_log)
    db.session.commit()
    #flash('User deleted successfully', 'success')
    return redirect(url_for("admin_redirects.manage_users"))