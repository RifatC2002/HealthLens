from flask import Blueprint, render_template, request, redirect, url_for
from flask_login import login_required, current_user
from models import db
from models.mood import Mood
from gemini import get_mood_routine
mood_bp = Blueprint('mood', __name__, url_prefix='/mood')

@mood_bp.route('/adjust', methods=['GET', 'POST'])
@login_required
def adjust_mood():
    if request.method == 'POST':
        mood_type = request.form.get('mood')
        if mood_type:
            routine = get_mood_routine(mood_type)
            mood_entry = Mood(mood_type=mood_type, user_id=current_user.id, routine=routine)
            db.session.add(mood_entry)
            db.session.commit()
            return redirect(url_for('mood.adjust_mood'))

    moods = Mood.query.filter_by(user_id=current_user.id).order_by(Mood.timestamp.desc()).limit(5).all()
    return render_template('mood/adjust_mood.html', moods=moods)