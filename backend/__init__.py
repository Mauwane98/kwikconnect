# backend/__init__.py

from flask import Flask
# from flask_sqlalchemy import SQLAlchemy
from .config.config import Config
from .errors import register_error_handlers # Import the function
import os

# Initialize extensions
# db = SQLAlchemy()

def create_app(config_class=Config):
    """
    Creates and configures an instance of the Flask application.
    """
    app = Flask(__name__, 
                static_folder=os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 
                                         'frontend'), 
                static_url_path='/')
    
    # Load config
    app.config.from_object(config_class)
    
    with app.app_context():
        # Initialize MongoDB connection
        try:
            from .mongo import get_mongo_client
            app.mongo_db = get_mongo_client()
            print("MongoDB connected successfully!")
            
            # Initialize models after MongoDB connection
            from .models import init_models
            app.models = init_models()
            print("Models initialized successfully!")
            
        except Exception as e:
            print(f"Error during app initialization: {e}")
            raise
        
        # Register error handlers
        register_error_handlers(app)
    
    return app