from flask import render_template, request, redirect, url_for, flash
from flask_login import login_required, current_user
from datetime import datetime
from models.finance import FinanceRecord
from models import db
from flask import Blueprint

finance_bp = Blueprint('finance', __name__, url_prefix='/finance')

@finance_bp.route('/view')
@login_required
def view_finances():
    records = FinanceRecord.query.filter_by(user_id=current_user.id).order_by(FinanceRecord.date.desc()).all()

    total_income = sum(r.amount for r in records if r.type == 'income')
    total_expense = sum(r.amount for r in records if r.type == 'expense')
    savings = total_income - total_expense

    return render_template('finance/view_records.html', records=records,
                           total_income=total_income,
                           total_expense=total_expense,
                           savings=savings)


@finance_bp.route('/add', methods=['GET', 'POST'])
@login_required
def add_finance():
    if request.method == 'POST':
        type = request.form.get('type')
        category = request.form.get('category')
        amount = request.form.get('amount')
        date_str = request.form.get('date')  # This is still a string
        description = request.form.get('description')

        if type and category and amount and date_str:
            try:
                amount = float(amount)
                date_obj = datetime.strptime(date_str, '%Y-%m-%d').date()  # Convert string to date

                new_record = FinanceRecord(
                    type=type,
                    category=category,
                    amount=amount,
                    date=date_obj,
                    description=description,
                    user_id=current_user.id
                )

                db.session.add(new_record)
                db.session.commit()
                return redirect(url_for('finance.view_finances'))

            except ValueError:
                flash('Amount must be a valid number.')
        else:
            flash('Please fill all required fields.')

    return render_template('finance/add_record.html')

@finance_bp.route('/delete/<int:record_id>', methods=['POST'])
@login_required
def delete_finance(record_id):
    record = FinanceRecord.query.get_or_404(record_id)
    if record.user_id == current_user.id:
        db.session.delete(record)
        db.session.commit()
    return redirect(url_for('finance.view_finances'))
