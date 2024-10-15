from flask import Blueprint, render_template, request, redirect, url_for, flash, jsonify
from flask_login import login_user, login_required, logout_user, current_user
from werkzeug.security import check_password_hash, generate_password_hash
from . import db, login_manager
from .models import User
from .blockchain import blockchain
from .iot_simulator import IoTSimulator
from .nlp_utils import analyze_sentiment
from .security import encrypt_data

main = Blueprint('main', __name__)

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

@main.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form.get('username')
        email = request.form.get('email')
        password = request.form.get('password')
        
        user = User.query.filter_by(username=username).first()
        if user:
            flash('Username already exists')
            return redirect(url_for('main.register'))
        
        user = User.query.filter_by(email=email).first()
        if user:
            flash('Email already exists')
            return redirect(url_for('main.register'))
        
        new_user = User(username=username, email=email, password_hash=generate_password_hash(password))
        db.session.add(new_user)
        db.session.commit()
        
        flash('Registration successful. Please log in.')
        return redirect(url_for('main.login'))
    
    return render_template('register.html')

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
    
    # Add transaction to blockchain instead of directly adding a block
    blockchain.add_transaction(current_user.username, "SentimentAnalysis", encrypted_sentiment)
    
    return {'sentiment': sentiment}

@main.route('/mine', methods=['GET'])
@login_required
def mine():
    block = blockchain.mine_block(current_user.username)
    response = {
        'message': "New Block Mined",
        'index': block.index,
        'transactions': block.transactions,
        'nonce': block.nonce,
        'previous_hash': block.previous_hash
    }
    return jsonify(response), 200

@main.route('/transactions/new', methods=['POST'])
@login_required
def new_transaction():
    values = request.get_json()
    required = ['recipient', 'amount']
    if not all(k in values for k in required):
        return 'Missing values', 400

    index = blockchain.add_transaction(current_user.username, values['recipient'], values['amount'])
    response = {'message': f'Transaction will be added to Block {index}'}
    return jsonify(response), 201

@main.route('/chain', methods=['GET'])
def full_chain():
    response = {
        'chain': [vars(block) for block in blockchain.chain],
        'length': len(blockchain.chain),
    }
    return jsonify(response), 200

@main.route('/nodes/register', methods=['POST'])
@login_required
def register_nodes():
    values = request.get_json()
    nodes = values.get('nodes')
    if nodes is None:
        return "Error: Please supply a valid list of nodes", 400

    for node in nodes:
        blockchain.register_node(node)

    response = {
        'message': 'New nodes have been added',
        'total_nodes': list(blockchain.nodes),
    }
    return jsonify(response), 201

@main.route('/nodes/resolve', methods=['GET'])
@login_required
def consensus():
    replaced = blockchain.resolve_conflicts()
    if replaced:
        response = {
            'message': 'Our chain was replaced',
            'new_chain': [vars(block) for block in blockchain.chain]
        }
    else:
        response = {
            'message': 'Our chain is authoritative',
            'chain': [vars(block) for block in blockchain.chain]
        }
    return jsonify(response), 200
