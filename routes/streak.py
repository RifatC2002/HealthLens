from flask import Blueprint, render_template
from flask_login import login_required, current_user
from datetime import datetime, timedelta
from models.goal import Goal
from models.mood import Mood
from models.exercise import ExerciseChallenge

streak_bp = Blueprint('streak', __name__, url_prefix='/streak')

def streak_percent(data):
    return round((sum(1 for d in data if d) / len(data)) * 100) if data else 0

@streak_bp.route('/view')
@login_required
def view_streaks():
    today = datetime.utcnow().date()
    week_days = [today - timedelta(days=i) for i in range(7)]

    # === Mood Streak ===
    mood_entries = Mood.query.filter(
        Mood.user_id == current_user.id,
        Mood.timestamp >= today - timedelta(days=6)
    ).all()
    mood_days = set(m.timestamp.date() for m in mood_entries)
    mood_pct = round((len(mood_days) / 7) * 100)
    mood_desc = f"You’ve checked in your mood {len(mood_days)} times this week."

    # === Goal Completion Streak ===
    recent_goals = Goal.query.filter_by(user_id=current_user.id).order_by(Goal.created_at.desc()).limit(7).all()
    goal_pct = streak_percent([g.completion for g in recent_goals])
    completed_goals = sum(1 for g in recent_goals if g.completion)
    goal_desc = f"You've completed your goals for {completed_goals} out of {len(recent_goals)} days this week!"


    # === Challenge Streak ===
    recent_challenges = ExerciseChallenge.query.filter_by(user_id=current_user.id).order_by(ExerciseChallenge.created_at.desc()).limit(7).all()
    challenge_days = set(c.created_at.date() for c in recent_challenges if c.created_at.date() in week_days)
    challenge_pct = round((len(challenge_days) / 7) * 100)
    challenge_desc = f"You’ve completed challenges on {len(challenge_days)} days this week!"

    # === Routine Follow-through (placeholder) ===
    routine_pct = "Pending"  
    routine_desc = "You followed through on X days’ worth of routines." 

    streaks = [
        {
            "title": "Goal Completion Streak",
            "percentage": goal_pct,
            "description": goal_desc
        },
        {
            "title": "Mood Check-In Streak",
            "percentage": mood_pct,
            "description": mood_desc
        },
        {
            "title": "Routine Follow-Through",
            "percentage": routine_pct,
            "description": routine_desc
        },
        {
            "title": "Exercise Challenge Streak",
            "percentage": challenge_pct,
            "description": challenge_desc
        }
    ]

    return render_template("streak/streaks.html", streaks=streaks)
