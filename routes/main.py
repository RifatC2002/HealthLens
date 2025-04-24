from flask import render_template, Blueprint
from flask_login import login_required, current_user
from datetime import date, timedelta, datetime
from collections import defaultdict

from models.mood import Mood
from models.goal import Goal
from models.finance import FinanceRecord
from models.exercise import ExerciseChallenge
from models.social import SocialContact

main_bp = Blueprint('main', __name__)

@main_bp.route('/dashboard')
@login_required
def dashboard():
    today = datetime.utcnow().date()
    week_days = [today - timedelta(days=i) for i in range(7)]

    # === Latest Mood & Routine Suggestion ===
    latest_mood = Mood.query.filter_by(user_id=current_user.id).order_by(Mood.timestamp.desc()).first()
    mood_routines = {
        "Happy": "Do 10 jumping jacks, 30 seconds plank, and a 5-minute yoga stretch.",
        "Sad": "Take a 10-minute walk, do 15 squats, and 10 deep breaths.",
        "Angry": "Try 20 push-ups, 30 seconds wall sit, and 1-minute breathing meditation.",
        "Excited": "Do 20 high knees, 20 mountain climbers, and 10 burpees.",
        "Tired": "Perform 10 leg stretches, 10 arm circles, and a 30-second child’s pose."
    }
    routine = mood_routines.get(latest_mood.mood_type) if latest_mood else None

    # === Goals and Challenges ===
    goal_list = Goal.query.filter_by(user_id=current_user.id).order_by(Goal.created_at.desc()).all()
    challenge = ExerciseChallenge.query.filter_by(user_id=current_user.id).order_by(ExerciseChallenge.created_at.desc()).first()

    # === Finance Chart Data ===
    finance_records = FinanceRecord.query.filter_by(user_id=current_user.id).order_by(FinanceRecord.date.desc()).all()
    category_totals = defaultdict(float)
    for record in finance_records:
        category_totals[record.category] += record.amount
    chart_labels = list(category_totals.keys())
    chart_values = [round(category_totals[k], 2) for k in chart_labels]

    # === Social Sync Contacts ===
    contacts = SocialContact.query.filter_by(user_id=current_user.id).all()

    # === Streak Calculation Helpers ===
    def streak_percent(data):
        return round((sum(1 for d in data if d) / len(data)) * 100) if data else 0

    # === Mood Check-In Streak ===
    mood_entries = Mood.query.filter(
        Mood.user_id == current_user.id,
        Mood.timestamp >= today - timedelta(days=6)
    ).all()
    mood_days = set(m.timestamp.date() for m in mood_entries)
    mood_pct = round((len(mood_days) / 7) * 100)

    # === Goal Completion Streak ===
    recent_goals = Goal.query.filter_by(user_id=current_user.id).order_by(Goal.created_at.desc()).limit(7).all()
    goal_pct = streak_percent([g.completion for g in recent_goals])

    # === Exercise Challenge Streak ===
    recent_challenges = ExerciseChallenge.query.filter_by(user_id=current_user.id).order_by(ExerciseChallenge.created_at.desc()).limit(7).all()
    challenge_days = set(c.created_at.date() for c in recent_challenges if c.created_at.date() in week_days)
    challenge_pct = round((len(challenge_days) / 7) * 100)

    # === Routine Follow-through Streak (simulate or replace later) ===
    routine_pct ="Pending"

    # === Streak Summary for Template ===
    streaks = {
        "Goal Completion": goal_pct,
        "Routine Follow-Through": routine_pct,
        "Exercise Challenges": challenge_pct,
        "Mood Check-Ins": mood_pct
    }

    return render_template(
        "dashboard.html",
        user=current_user,
        mood=latest_mood,
        routine=routine,
        goals=goal_list,
        challenge=challenge,
        finances=finance_records,
        chart_labels=chart_labels,
        chart_values=chart_values,
        contacts=contacts,
        today=today,
        streaks=streaks
    )
