from flask import render_template, Blueprint
from flask_login import login_required, current_user
from models.mood import Mood
from models.goal import Goal
from models.finance import FinanceRecord
from models.exercise import ExerciseChallenge
from collections import defaultdict

main_bp = Blueprint('main', __name__)

@main_bp.route('/dashboard')
@login_required
def dashboard():
    # Latest Mood
    latest_mood = Mood.query.filter_by(user_id=current_user.id).order_by(Mood.timestamp.desc()).first()

    # Routine Suggestion
    routine = None
    if latest_mood:
        mood_routines = {
            "Happy": "Do 10 jumping jacks, 30 seconds plank, and a 5-minute yoga stretch.",
            "Sad": "Take a 10-minute walk, do 15 squats, and 10 deep breaths.",
            "Angry": "Try 20 push-ups, 30 seconds wall sit, and 1-minute breathing meditation.",
            "Excited": "Do 20 high knees, 20 mountain climbers, and 10 burpees.",
            "Tired": "Perform 10 leg stretches, 10 arm circles, and a 30-second child’s pose."
        }
        routine = mood_routines.get(latest_mood.mood_type)

    # Latest Goal
    goal_list = Goal.query.filter_by(user_id=current_user.id).order_by(Goal.created_at.desc()).all()

    # Latest Challenge
    challenge = ExerciseChallenge.query.filter_by(user_id=current_user.id).order_by(ExerciseChallenge.created_at.desc()).first()

    # Finance Records and Chart Data
    finance_records = FinanceRecord.query.filter_by(user_id=current_user.id).order_by(FinanceRecord.date.desc()).all()
    category_totals = defaultdict(float)
    for record in finance_records:
        category_totals[record.category] += record.amount

    chart_labels = list(category_totals.keys())
    chart_values = [round(category_totals[label], 2) for label in chart_labels]

    return render_template(
        "dashboard.html",
        user=current_user,
        mood=latest_mood,
        routine=routine,
        goals=goal_list,
        challenge=challenge,
        finances=finance_records,
        chart_labels = list(category_totals.keys()),
        chart_values = [round(category_totals[k], 2) for k in chart_labels]
    )
