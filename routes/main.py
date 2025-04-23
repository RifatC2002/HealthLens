from flask import render_template, Blueprint
from flask_login import login_required, current_user
from models.mood import Mood
from models.goal import Goal
#from models.task import Task
from models.finance import FinanceRecord


main_bp = Blueprint('main', __name__)

@main_bp.route('/dashboard')
@login_required
def dashboard():
    # Fetch latest mood
    latest_mood = Mood.query.filter_by(user_id=current_user.id).order_by(Mood.timestamp.desc()).first()

    # Suggest routine based on mood
    routine = None
    if latest_mood:
        mood = latest_mood.mood_type
        mood_routines = {
            "Happy": "Do 10 jumping jacks, 30 seconds plank, and a 5-minute yoga stretch.",
            "Sad": "Take a 10-minute walk, do 15 squats, and 10 deep breaths.",
            "Angry": "Try 20 push-ups, 30 seconds wall sit, and 1-minute breathing meditation.",
            "Excited": "Do 20 high knees, 20 mountain climbers, and 10 burpees.",
            "Tired": "Perform 10 leg stretches, 10 arm circles, and a 30-second child’s pose."
        }
        routine = mood_routines.get(mood, "No specific routine available for this mood.")

    # Fetch declared goals
    goal_list = Goal.query.filter_by(user_id=current_user.id).order_by(Goal.created_at.desc()).all()

    # Fetch tasks
    #task_list = Task.query.filter_by(user_id=current_user.id).order_by(Task.due_date.desc()).all()

    # Fetch finance records
    finance_records = FinanceRecord.query.filter_by(user_id=current_user.id).order_by(FinanceRecord.date.desc()).all()

    return render_template(
        "dashboard.html",
        user=current_user,
        mood=latest_mood,
        routine=routine,
        goals=goal_list,
        #tasks=task_list,
        finances=finance_records
    )
