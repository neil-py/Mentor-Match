from app.extensions import db

class TutorApplications(db.Model):
    __tablename__ = "TUTOR_APPLICATIONS"
    id = db.Column(db.Integer, primary_key=True)
    student_id = db.Column(db.Integer, db.ForeignKey('USERS.id'))  # Use 'users.id' since 'users' is the tablename of Users model
    student = db.relationship('Users', foreign_keys=[student_id], backref='tutor_applications')
    description = db.Column(db.String, nullable=False)