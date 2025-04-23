from models import db
from datetime import datetime

class FocusTechnique(db.Model):
    __tablename__ = 'focus_techniques'

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text, nullable=False)
    category = db.Column(db.String(50))  # e.g., Pomodoro, Mindfulness, Breathing
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
