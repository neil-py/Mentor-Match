from flask import Flask
from app.extensions import db, migrate, login_manager
from app.models.users import Users



def create_app():

    app = Flask(__name__)
    app.secret_key = "fortnite"
    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///mentormatch.db"
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = True #for testing

    from app.routes import home, register, auth
    from app.forms import registration

    app.register_blueprint(home.home_route)
    app.register_blueprint(auth.authentication)
    app.register_blueprint(register.registration_route)
    app.register_blueprint(register.admin_creation_route)

    db.init_app(app)
    migrate.init_app(app=app, db=db)
    login_manager.init_app(app)
    login_manager.login_view = "authentication.login"

    @login_manager.user_loader
    def load_user(id):
        return Users.query.get(int(id))

    return app