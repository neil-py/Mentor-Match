from flask import Flask
from app.extensions import db, migrate, login_manager, account_type
from app.models.users import Users
from app.routes import home
from app.routes.student import booking
from app.routes.student import booking



def create_app():

    app = Flask(__name__)
    app.secret_key = "fortnite"
    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///mentormatch.db"
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = True #for testing

    from app.routes import register, auth
    from app.routes.student import booking as student_booking
    from app.routes.student import dashboard as student_dashboard
    from app.routes.admin import dashboard as admin_dashboard
    from app.routes.tutor import dashboard as tutor_dashboard


    app.register_blueprint(home.home_route)
    app.register_blueprint(auth.authentication)
    app.register_blueprint(register.registration_route)
    app.register_blueprint(register.admin_creation_route)
    app.register_blueprint(student_booking.booking_route)
    app.register_blueprint(student_dashboard.student_dashboard_route)
    app.register_blueprint(admin_dashboard.admin_dashboard_route)
    app.register_blueprint(tutor_dashboard.tutor_dashboard_route)

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