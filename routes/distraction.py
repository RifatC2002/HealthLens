from flask import Blueprint, render_template
from flask_login import login_required
from gemini import get_focus_tip  # ← your Gemini helper

distraction_bp = Blueprint('distraction', __name__, url_prefix='/distraction')

@distraction_bp.route('/techniques')
@login_required
def show_techniques():
    tip = get_focus_tip()  # get the Gemini-generated response
    return render_template("distraction/techniques.html", tip=tip)
