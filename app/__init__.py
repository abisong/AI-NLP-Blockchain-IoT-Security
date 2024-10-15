import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager

db = SQLAlchemy()
login_manager = LoginManager()

def create_app():
    app = Flask(__name__)
    
    app.config['SECRET_KEY'] = os.environ.get("FLASK_SECRET_KEY") or "a secret key"
    app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get("DATABASE_URL")
    app.config['SQLALCHEMY_ENGINE_OPTIONS'] = {
        "pool_recycle": 300,
        "pool_pre_ping": True,
    }
    
    db.init_app(app)
    login_manager.init_app(app)
    login_manager.login_view = 'main.login'
    
    with app.app_context():
        from . import models
        db.create_all()
    
    from .routes import main
    app.register_blueprint(main)
    
    return app
