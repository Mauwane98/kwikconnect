# backend/__init__.py

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from .config.config import Config
from .errors import register_error_handlers # Import the function
import os

# Initialize extensions
db = SQLAlchemy()

def create_app(config_class=Config):
    """
    Creates and configures an instance of the Flask application.
    """
    app = Flask(__name__, static_folder=os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'frontend'), static_url_path='/')
    app.config.from_object(config_class)

    # Initialize extensions with the app
    db.init_app(app)

    # Register error handlers
    register_error_handlers(app)

    return app