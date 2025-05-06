from flask import Flask, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
import os
import google.generativeai as genai
from models import db


app = Flask(__name__)
app.config['SECRET_KEY'] = 'devkey'
app.config['SQLALCHEMY_DATABASE_URI'] = f"sqlite:///{os.path.join(os.path.abspath(os.path.dirname(__file__)), 'instance', 'database.db')}"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)

login_manager = LoginManager()
login_manager.login_view = 'auth.login'
login_manager.init_app(app)

from models.user import User
from models import goal, exercise

from routes.auth import auth_bp
from routes.main import main_bp
from routes.goal import goal_bp
from routes.challenge import challenge_bp
from routes.distraction import distraction_bp
from routes.mood import mood_bp
from routes.routine import routine_bp
from routes.finance import finance_bp
from routes.microsave import microsave_bp
from routes.social import social_bp
from routes.streak import streak_bp
from dotenv import load_dotenv


app.register_blueprint(distraction_bp)  
app.register_blueprint(routine_bp)
app.register_blueprint(main_bp)
app.register_blueprint(mood_bp)
app.register_blueprint(auth_bp)
app.register_blueprint(goal_bp)
app.register_blueprint(challenge_bp)
app.register_blueprint(finance_bp)
app.register_blueprint(microsave_bp)
app.register_blueprint(social_bp)
app.register_blueprint(streak_bp)

load_dotenv()
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

@app.route('/')
def home():
    return redirect(url_for('auth.login'))

if __name__ == '__main__':
    os.makedirs('instance', exist_ok=True)
    with app.app_context():
        db.create_all()
    app.run(port=1063, debug=True)
