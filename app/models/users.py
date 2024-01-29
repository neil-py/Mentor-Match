from flask_login import UserMixin
from app.extensions import db
from app.extensions import bcrypt

class Users(UserMixin, db.Model):
    __tablename__ = "USERS"
    id = db.Column(db.Integer, primary_key=True)
    login_name = db.Column(db.String(50), unique=True, nullable=False)
    first_name = db.Column(db.String(100), unique=False, nullable=False)
    last_name = db.Column(db.String(100), unique=False, nullable=False)
    university_number = db.Column(db.String(20), unique=True, nullable=False)
    university_email = db.Column(db.String(225), unique=True, nullable=False)
    program = db.Column(db.String(100), nullable=True)
    password = db.Column(db.String(200), nullable=False)
    account_status = db.Column(db.Integer)
    tags = db.Column(db.String(200), nullable=True)
    #profile_pic = db.Column(db.String(200), nullable=True)

    @classmethod
    def is_login_name_taken(cls, login_name):
        return db.session.query(db.exists().where(Users.login_name==login_name)).scalar()
    
    @classmethod
    def is_university_email_taken(cls, university_email):
        return db.session.query(db.exists().where(Users.university_email==university_email)).scalar()