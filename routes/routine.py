from flask import Blueprint, render_template, request, redirect, url_for, session, jsonify
from flask_login import login_required, current_user
from models import db
from models.routine import Routine
from datetime import date
from gemini import generate_routine_based_on_inputs

routine_bp = Blueprint('routine', __name__, url_prefix='/routine')


@routine_bp.route('/input', methods=['GET', 'POST'])
@login_required
def routine_input():
    if request.method == 'POST':
        action = request.form.get('action')

        if action == 'manual':
            return redirect(url_for('routine.manual_routine_input'))

        # Get user inputs
        height = request.form.get('height')
        weight = request.form.get('weight')
        goal_weight = request.form.get('goal_weight')
        duration = int(request.form.get('duration'))
        daily_hours = int(request.form.get('daily_hours'))

        # NEW: Generate with Gemini
        sample = generate_routine_based_on_inputs(height, weight, goal_weight, duration, daily_hours)

        session['routine'] = sample
        session.modified = True
        return redirect(url_for('routine.view_custom_routine'))

    return render_template('routine/input.html')

@routine_bp.route('/calendar')
@login_required
def routine_calendar():
    routines = Routine.query.filter_by(user_id=current_user.id).all()
    return render_template('routine/routine_calendar.html', routines=routines)


@routine_bp.route('/manual', methods=['GET', 'POST'])
@login_required
def manual_routine_input():
    if 'manual_routine' not in session:
        session['manual_routine'] = []

    if request.method == 'POST':
        if request.form.get('finalize'):
            sample = session.pop('manual_routine', [])
            session['routine'] = sample
            return redirect(url_for('routine.view_custom_routine'))


        day = request.form.get('day')
        time = request.form.get('time')
        activity = request.form.get('activity')

        if day and time and activity:
            session['manual_routine'].append([day, time, activity])
            session.modified = True

    return render_template('routine/manual_input.html', routine=session.get('manual_routine', []))


@routine_bp.route('/custom/result')
@login_required
def view_custom_routine():
    routine = session.get('routine', [])
    return render_template('routine/result.html', sample=routine)


@routine_bp.route('/update_entry', methods=['POST'])
@login_required
def update_entry():
    data = request.json
    idx = int(data['index'])
    new_activity = data['new_activity']

    if 'routine' in session:
        routine = session['routine']
        if 0 <= idx < len(routine):
            # Update activity in-place
            routine[idx][2] = new_activity
            session['routine'] = routine  # Reassign to trigger session update
            session.modified = True
            return jsonify(success=True, routine=routine)
    return jsonify(success=False)


@routine_bp.route('/delete_entry', methods=['POST'])
@login_required
def delete_entry():
    data = request.json
    idx = int(data['index'])
    if 'routine' in session:
        routine = session['routine']
        if 0 <= idx < len(routine):
            routine.pop(idx)
            session['routine'] = routine
            return jsonify(success=True)
    return jsonify(success=False)
