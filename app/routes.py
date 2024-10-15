from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_user, login_required, logout_user, current_user
from werkzeug.security import check_password_hash
from . import db, login_manager
from .models import User
from .blockchain import Blockchain
from .iot_simulator import IoTSimulator
from .nlp_utils import analyze_sentiment
from .security import encrypt_data

main = Blueprint('main', __name__)

blockchain = Blockchain()
iot_simulator = IoTSimulator()

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

@main.route('/')
def index():
    return render_template('index.html')

@main.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        user = User.query.filter_by(username=username).first()
        if user and check_password_hash(user.password_hash, password):
            login_user(user)
            return redirect(url_for('main.dashboard'))
        else:
            flash('Invalid username or password')
    return render_template('login.html')

@main.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('main.index'))

@main.route('/dashboard')
@login_required
def dashboard():
    iot_data = iot_simulator.get_sensor_data()
    return render_template('dashboard.html', iot_data=iot_data)

@main.route('/analyze_sentiment', methods=['POST'])
@login_required
def analyze_text_sentiment():
    text = request.form.get('text')
    sentiment = analyze_sentiment(text)
    encrypted_sentiment = encrypt_data(str(sentiment))
    blockchain.add_block(encrypted_sentiment)
    return {'sentiment': sentiment}
