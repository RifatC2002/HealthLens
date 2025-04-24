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
        try:
            title = request.form['title']
            category = request.form['category']
            notes = request.form['notes']
            datetime_str = request.form['timeslot']
            dt = datetime.strptime(datetime_str, "%Y-%m-%d %H:%M")
            deadline = dt.date()
            start_time = dt.time()
            priority = int(request.form.get('priority', 1))

            goal = Goal(
                title=title,
                category=category,
                deadline=deadline,
                notes=notes,
                priority=priority,
                user_id=current_user.id,
                start_time=start_time
            )

            db.session.add(goal)
            db.session.commit()
            flash("Goal added successfully!", "success")
            return redirect(url_for('goal.view_goals'))

        except Exception as e:
            db.session.rollback()
            flash(f"Error adding goal: {str(e)}", "danger")

    return render_template('goal/declare.html')


@goal_bp.route('/view')
@login_required
def view_goals():
    user_goals = Goal.query.filter_by(user_id=current_user.id).order_by(Goal.priority.asc(), Goal.created_at.desc()).all()

    completed_goals = sum(1 for g in user_goals if g.completion)
    total_goals = len(user_goals)
    completion_rate = (completed_goals / total_goals * 100) if total_goals > 0 else 0

    return render_template(
        'goal/view_goals.html',
        goals=user_goals,
        completed_goals=completed_goals,
        total_goals=total_goals,
        completion_rate=completion_rate
    )


@goal_bp.route('/update/<int:goal_id>', methods=['POST'])
@login_required
def update_goal(goal_id):
    goal = Goal.query.get_or_404(goal_id)
    if goal.user_id != current_user.id:
        flash("You can't update this goal", "danger")
        return redirect(url_for('goal.view_goals'))

    goal.completion = request.form.get('completion') == 'True'
    db.session.commit()
    flash("Goal updated!", "success")
    return redirect(url_for('goal.view_goals'))


@goal_bp.route('/progress/<int:goal_id>')
@login_required
def goal_progress(goal_id):
    goal = Goal.query.get_or_404(goal_id)
    if goal.user_id != current_user.id:
        return render_template('login.html')

    total_tasks = len(goal.tasks) if hasattr(goal, 'tasks') else 0
    completed_tasks = len([t for t in goal.tasks if t.is_completed]) if total_tasks > 0 else 0
    remaining_tasks = total_tasks - completed_tasks
    completion_rate = (completed_tasks / total_tasks * 100) if total_tasks > 0 else 0

    return render_template(
        'goal/progress.html',
        goal=goal,
        total_tasks=total_tasks,
        completed_tasks=completed_tasks,
        remaining_tasks=remaining_tasks,
        completion_rate=completion_rate
    )
