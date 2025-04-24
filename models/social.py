from datetime import date
from models import db

class SocialContact(db.Model):
    __tablename__ = 'social_contacts'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    name = db.Column(db.String(100), nullable=False)
    relationship = db.Column(db.String(50))
    reminder_days = db.Column(db.Integer, default=7)  # Number of days between check-ins
    last_contacted = db.Column(db.Date, default=date.today)
    notes = db.Column(db.String(255))  # Optional notes field

