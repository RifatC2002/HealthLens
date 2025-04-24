from datetime import datetime
from models import db

class Streak(db.Model):
    __tablename__ = 'streaks'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    type = db.Column(db.String(50), nullable=False)  # goal, mood, routine, exercise
    current_streak = db.Column(db.Integer, default=0)
    last_updated = db.Column(db.Date, default=datetime.utcnow)
