from flask import render_template, request, redirect, url_for, jsonify
from flask_login import login_required, current_user
from models.exercise import ExerciseChallenge
from models import db
from flask import Blueprint
from gemini import generate_fitness_challenge

challenge_bp = Blueprint('challenge', __name__, url_prefix='/challenge')

@challenge_bp.route("/view")
@login_required
def view_challenges():
    challenges = ExerciseChallenge.query.filter_by(user_id=current_user.id, completed=False).all()  # ✅ only incomplete ones
    return render_template("challenge/challenges.html", challenges=challenges)


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


@challenge_bp.route('/generate', methods=['POST'])
@login_required
def generate_challenge():
    challenge = generate_fitness_challenge()
    if challenge:
        new_challenge = ExerciseChallenge(
            title=challenge['title'],
            description=challenge['description'],
            user_id=current_user.id
        )
        db.session.add(new_challenge)
        db.session.flush()
        db.session.commit()
        
        return {
            'status': 'success',
            'title': challenge['title'],
            'description': challenge['description'],
            'id': new_challenge.id
        }


    return {'status': 'error'}, 500


@challenge_bp.route('/challenge/complete/<int:id>', methods=['POST'])
@login_required
def complete_challenge(id):
    print(f"Received completion request for challenge ID: {id}")
    challenge = ExerciseChallenge.query.get_or_404(id)
    challenge.completed = True
    db.session.commit()
    return jsonify({"status": "completed"})
