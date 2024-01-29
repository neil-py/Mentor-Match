from app.extensions import db
from datetime import datetime

class Sessions(db.Model):
    __tablename__ = "SESSIONS"
    id = db.Column(db.Integer, primary_key=True)
    tutor_id = db.Column(db.Integer, db.ForeignKey('USERS.id'))  # Use 'users.id' since 'users' is the tablename of Users model
    student_id = db.Column(db.Integer, db.ForeignKey('USERS.id'))  # Use 'users.id' since 'users' is the tablename of Users model
    tutor = db.relationship('Users', foreign_keys=[tutor_id], backref='tutor_sessions')
    student = db.relationship('Users', foreign_keys=[student_id], backref='student_sessions')
    
    session_date = db.Column(db.Date, nullable=False)
    session_time = db.Column(db.String(50))
    course_code = db.Column(db.String(50))
    course_name = db.Column(db.String(100))
    description = db.Column(db.String(500))
    session_type = db.Column(db.String(20)) # either online, face to face.
    communication_channel = db.Column(db.String(200)) # either by sending email, facebook link.
    session_status = db.Column(db.String(20), default='scheduled')
    session_rating = db.Column(db.Integer)