from flask import Flask
from app.extensions import db, migrate, login_manager, account_type
from app.models.users import Users
from app.models.activity_logs import ActivityLog
from app.models.sessions import Sessions
from app.models.tutor_applications import TutorApplications
from app.routes import home
from app.routes.student import booking
from app.routes.student import booking



def create_app():

    app = Flask(__name__)
    app.secret_key = "fortnite"
    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///mentormatch.db"
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = True #for testing

    from app.routes import register, auth, edit_profile
    #student modules
    from app.routes.student import booking as student_booking
    from app.routes.student import dashboard as student_dashboard
    from app.routes.student import requests as student_requests
    from app.routes.student import student_tutor_application
    #admin modules
    from app.routes.admin import dashboard as admin_dashboard
    from app.routes.admin import create_user as admin_create_user
    from app.routes.admin import manage_user as admin_manage_user
    from app.routes.admin import admin_redirects as admin_redirects
    #tutor modules
    from app.routes.tutor import dashboard as tutor_dashboard
    from app.routes.tutor import tutor_redirects


    app.register_blueprint(home.home_route)
    app.register_blueprint(auth.authentication)
    app.register_blueprint(register.registration_route)
    app.register_blueprint(admin_create_user.admin_creation_route)
    app.register_blueprint(student_booking.booking_route)
    app.register_blueprint(student_dashboard.student_dashboard_route)
    app.register_blueprint(admin_dashboard.admin_dashboard_route)
    app.register_blueprint(tutor_dashboard.tutor_dashboard_route)
    app.register_blueprint(admin_manage_user.admin_manage_route)
    app.register_blueprint(admin_redirects.admin_redirects_route)
    app.register_blueprint(tutor_redirects.tutor_redirects_route)
    app.register_blueprint(student_requests.student_requests_route)
    app.register_blueprint(edit_profile.edit_profile_route)
    app.register_blueprint(student_tutor_application.student_tutor_application_route)


    db.init_app(app)
    migrate.init_app(app=app, db=db)
    login_manager.init_app(app)
    login_manager.login_view = "authentication.login"

    @login_manager.user_loader
    def load_user(id):
        return Users.query.get(int(id))
    
    @app.context_processor
    def account_type_dict():
        return dict(account_type=account_type)

    return app