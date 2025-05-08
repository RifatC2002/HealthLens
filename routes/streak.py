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

    mood_count = len(mood_entries)
    mood_pct = round((mood_count / 7) * 100)
    mood_desc = f"You’ve checked in your mood {mood_count} time(s) this week."

    # === Goal Completion Streak ===
    recent_goals = Goal.query.filter_by(user_id=current_user.id).order_by(Goal.created_at.desc()).limit(7).all()
    goal_pct = streak_percent([g.completion for g in recent_goals])
    completed_goals = sum(1 for g in recent_goals if g.completion)
    goal_desc = f"You've completed your goals for {completed_goals} out of {len(recent_goals)} days this week!"


    recent_challenges = ExerciseChallenge.query.filter(
        ExerciseChallenge.user_id == current_user.id,
        ExerciseChallenge.created_at >= today - timedelta(days=6)
    ).all()

    challenge_count = sum(1 for c in recent_challenges if c.completed)
    total_generated = len(recent_challenges)

    challenge_pct = round((challenge_count / total_generated) * 100) if total_generated else 0
    challenge_desc = f"You’ve completed {challenge_count} out of {total_generated} challenges this week!"




 

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
            "title": "Exercise Challenge Streak",
            "percentage": challenge_pct,
            "description": challenge_desc
        }
    ]

    return render_template("streak/streaks.html", streaks=streaks)
