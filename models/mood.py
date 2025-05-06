from models import db
from datetime import datetime

class Mood(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    mood_type = db.Column(db.String(50))
    routine = db.Column(db.Text)  # ← New field
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
