from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
from . import db

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(150), unique=True, nullable=False)
    email = db.Column(db.String(150), unique=True, nullable=False)
    password = db.Column(db.String(150), nullable=False)

    goals = db.relationship('Goal', backref='user', lazy=True)
    challenges = db.relationship('ExerciseChallenge', backref='user', lazy=True)
    moods = db.relationship('Mood', backref='user', lazy=True)
    routines = db.relationship('Routine', backref='user', lazy=True)



    def set_password(self, password):
        self.password = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password, password)
