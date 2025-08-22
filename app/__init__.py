from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_wtf.csrf import CSRFProtect

db = SQLAlchemy()
login_manager = LoginManager()
csrf = CSRFProtect()

def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'your-secret-key'
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///yourdb.sqlite3'

    db.init_app(app)
    login_manager.init_app(app)
    csrf.init_app(app)
    
    # Import models and create tables
    with app.app_context():
        from . import models
        db.create_all()

    login_manager.login_view = 'main.login'  # Correct blueprint view name

    from .routes import main
    app.register_blueprint(main)

    return app