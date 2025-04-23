from flask import Blueprint, render_template
import random

distraction_bp = Blueprint('distraction', __name__, url_prefix='/distraction')

techniques = [
    {"title": "Pomodoro Technique", "description": "Work 25 mins, break 5 mins.", "category": "Time Management"},
    {"title": "Remove Phone", "description": "Put your phone in another room.", "category": "Environment"},
    {"title": "Website Blockers", "description": "Use extensions to block distracting sites.", "category": "Digital"},
    {"title": "Mindful Breathing", "description": "Breathe deeply for 2 minutes to regain focus.", "category": "Mental"},
    {"title": "Task Batching", "description": "Group similar tasks to avoid switching focus.", "category": "Efficiency"}
]

@distraction_bp.route('/techniques')
def show_techniques():
    tip = random.choice(techniques)
    return render_template('distraction/techniques.html', tip=tip, techniques=techniques)
