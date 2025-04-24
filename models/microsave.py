from datetime import datetime
from models import db  # central import from models/__init__.py

class MicroSaving(db.Model):
    __tablename__ = 'microsavings'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    amount = db.Column(db.Float, nullable=False)
    description = db.Column(db.String(255))
    date = db.Column(db.DateTime, default=datetime.utcnow)

    # These fields are only used when this entry is a monthly goal
    is_goal = db.Column(db.Boolean, default=False)
    goal_month = db.Column(db.String(7))  # e.g., "2025-04"
