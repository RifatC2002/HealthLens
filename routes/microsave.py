from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_required, current_user
from datetime import datetime
from models.microsave import MicroSaving
from models import db


microsave_bp = Blueprint('microsave', __name__, url_prefix='/microsave')


@microsave_bp.route('/log')
@login_required
def view_micro_savings():
    from datetime import datetime


    entries = MicroSaving.query.filter_by(user_id=current_user.id, is_goal=False).order_by(MicroSaving.date.desc()).all()
    total_saved = sum(e.amount for e in entries)


    current_month = datetime.utcnow().strftime('%Y-%m')
    goal_entry = MicroSaving.query.filter_by(user_id=current_user.id, is_goal=True, goal_month=current_month).first()
    goal_amount = goal_entry.amount if goal_entry else 0
    progress_percent = round((total_saved / goal_amount) * 100, 2) if goal_amount > 0 else 0


    return render_template(
        'microsave/log.html',
        entries=entries,
        total_saved=total_saved,
        goal_amount=goal_amount,
        progress_percent=progress_percent
    )




@microsave_bp.route('/add', methods=['GET', 'POST'])
@login_required
def add_micro_saving():
    from models.finance import FinanceRecord  # Import here to avoid circular import
    if request.method == 'POST':
        amount = request.form.get('amount')
        description = request.form.get('description')


        if amount:
            try:
                amount = float(amount)


                # Step 1: Calculate current savings
                finance_records = FinanceRecord.query.filter_by(user_id=current_user.id).all()
                total_income = sum(r.amount for r in finance_records if r.type == 'income')
                total_expense = sum(r.amount for r in finance_records if r.type == 'expense')
                net_balance = total_income - total_expense


                # Step 2: Check if user has enough savings
                if amount > net_balance:
                    flash(f"Insufficient balance. You only have {net_balance:.2f} BDT available.")
                    return redirect(url_for('microsave.add_micro_saving'))


                # Step 3: Save to MicroSaving
                new_entry = MicroSaving(
                    user_id=current_user.id,
                    amount=amount,
                    description=description
                )
                db.session.add(new_entry)


                # Step 4: Simulate deduction in FinanceRecord
                deduction = FinanceRecord(
                    user_id=current_user.id,
                    type='expense',
                    category='Micro-Saving',
                    amount=amount,
                    date=datetime.utcnow().date(),
                    description='Transferred to Micro-Saving'
                )
                db.session.add(deduction)


                db.session.commit()
                return redirect(url_for('microsave.view_micro_savings'))


            except ValueError:
                flash('Amount must be a valid number.')
        else:
            flash('Amount is required.')


    return render_template('microsave/add.html')




@microsave_bp.route('/delete/<int:entry_id>', methods=['POST'])
@login_required
def delete_micro_saving(entry_id):
    entry = MicroSaving.query.get_or_404(entry_id)
    if entry.user_id == current_user.id:
        db.session.delete(entry)
        db.session.commit()
    return redirect(url_for('microsave.view_micro_savings'))


@microsave_bp.route('/set-goal', methods=['POST'])
@login_required
def set_goal():
    current_month = datetime.utcnow().strftime('%Y-%m')
    amount = request.form.get('goal_amount')


    try:
        amount = float(amount)
        goal_entry = MicroSaving.query.filter_by(user_id=current_user.id, is_goal=True, goal_month=current_month).first()
        if goal_entry:
            goal_entry.amount = amount
        else:
            goal_entry = MicroSaving(
                user_id=current_user.id,
                amount=amount,
                description='Monthly savings goal',
                is_goal=True,
                goal_month=current_month
            )
            db.session.add(goal_entry)
        db.session.commit()
        flash("Monthly goal set successfully.")
    except ValueError:
        flash("Invalid amount.")
    return redirect(url_for('microsave.view_micro_savings'))