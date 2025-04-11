from datetime import datetime
from . import db

class Mood(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    mood_type = db.Column(db.String(20), nullable=False)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
