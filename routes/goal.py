from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_required, current_user
from models import db
from models.goal import Goal
from datetime import datetime

goal_bp = Blueprint('goal', __name__, url_prefix='/goals')

@goal_bp.route('/declare', methods=['GET', 'POST'])
@login_required
def declare_goal():
    if request.method == 'POST':
        title = request.form['title']
        category = request.form['category']
        notes = request.form['notes']
        deadline = datetime.strptime(request.form['deadline'], "%Y-%m-%d").date()

        goal = Goal(title=title, category=category, deadline=deadline, notes=notes, user_id=current_user.id)
        db.session.add(goal)
        db.session.commit()
        flash("Goal added!")
        return redirect(url_for('goal.declare_goal'))

    return render_template('goal/declare.html')
@goal_bp.route('/view')
@login_required
def view_goals():
    user_goals = Goal.query.filter_by(user_id=current_user.id).order_by(Goal.created_at.desc()).all()
    return render_template('goal/view_goals.html', goals=user_goals)
