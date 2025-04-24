from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_required, current_user
from datetime import date
from datetime import date, timedelta
from models.social import SocialContact
from models import db

social_bp = Blueprint('social', __name__, url_prefix='/social')

# View all contacts
@social_bp.route('/contacts')
@login_required
def view_contacts():
    contacts = SocialContact.query.filter_by(user_id=current_user.id).order_by(SocialContact.last_contacted.asc()).all()
    today = date.today()
    return render_template('social/contacts.html', contacts=contacts, today=today)

# Add a new contact
@social_bp.route('/add', methods=['GET', 'POST'])
@login_required
def add_contact():
    if request.method == 'POST':
        name = request.form.get('name')
        relationship = request.form.get('relationship')
        reminder_days = request.form.get('reminder_days')
        notes = request.form.get('notes')
        days_ago = request.form.get('days_ago')

        if not name or not reminder_days:
            flash("Name and reminder frequency are required.")
            return redirect(url_for('social.add_contact'))

        # Convert days ago to actual date
        if days_ago and days_ago.isdigit():
            last_contacted = date.today() - timedelta(days=int(days_ago))
        else:
            last_contacted = date.today()

        new_contact = SocialContact(
            user_id=current_user.id,
            name=name,
            relationship=relationship,
            reminder_days=int(reminder_days),
            last_contacted=last_contacted,
            notes=notes
        )
        db.session.add(new_contact)
        db.session.commit()
        return redirect(url_for('social.view_contacts'))

    return render_template('social/add.html')

# Reset last contacted date
@social_bp.route('/reset/<int:id>', methods=['POST'])
@login_required
def reset_contact(id):
    contact = SocialContact.query.get_or_404(id)
    if contact.user_id != current_user.id:
        flash("Access denied.")
        return redirect(url_for('social.view_contacts'))

    contact.last_contacted = date.today()
    db.session.commit()
    flash(f"Marked {contact.name} as contacted today.")
    return redirect(url_for('social.view_contacts'))

# Optional: Delete a contact
@social_bp.route('/delete/<int:id>', methods=['POST'])
@login_required
def delete_contact(id):
    contact = SocialContact.query.get_or_404(id)
    if contact.user_id == current_user.id:
        db.session.delete(contact)
        db.session.commit()
    return redirect(url_for('social.view_contacts'))
