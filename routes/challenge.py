from flask import render_template, request, redirect, url_for
from flask_login import login_required, current_user
from models.exercise import ExerciseChallenge
from models import db
from flask import Blueprint

challenge_bp = Blueprint('challenge', __name__, url_prefix='/challenge')

@challenge_bp.route('/view')
@login_required
def view_challenges():
    challenges = ExerciseChallenge.query.all()
    return render_template('challenge/challenges.html', challenges=challenges)

@challenge_bp.route('/add', methods=['GET', 'POST'])
@login_required
def add_challenge():
    if request.method == 'POST':
        title = request.form.get('title')
        description = request.form.get('description')
        if title and description:
            new_challenge = ExerciseChallenge(title=title, description=description, user_id=current_user.id)
            db.session.add(new_challenge)
            db.session.commit()
            return redirect(url_for('challenge.view_challenges'))
    return render_template('challenge/add_challenge.html')
