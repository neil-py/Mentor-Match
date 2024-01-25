from app.extensions import db
from datetime import datetime

class ActivityLog(db.Model):
    __tablename__ = "ACTIVITY_LOGS"
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('USERS.id'))  # Use 'users.id' since 'users' is the tablename of Users model
    user = db.relationship('Users', backref='activity_logs')
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)
    activity_type = db.Column(db.String(100))
    description = db.Column(db.String(500))