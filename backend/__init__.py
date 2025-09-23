# backend/__init__.py

from flask import Flask, send_from_directory # Added send_from_directory
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_cors import CORS
from flask_jwt_extended import JWTManager
from .config.config import Config
import os # Added os for path joining

# Initialize extensions
db = SQLAlchemy()
migrate = Migrate()
jwt = JWTManager()

def create_app(config_class=Config):
    """
    Creates and configures an instance of the Flask application.
    """
    app = Flask(__name__)
    app.config.from_object(config_class)

    # Initialize extensions with the app
    db.init_app(app)
    migrate.init_app(app, db)
    jwt.init_app(app)
    
    # Enable CORS for all domains on all routes
    CORS(app, resources={r"/api/*": {"origins": "*"}})

    # Import and register blueprints
    from .api.auth import auth_bp
    from .api.vendors import vendors_bp
    from .api.orders import orders_bp
    from .api.payments import payments_bp
    from .api.couriers import jobs_bp # <-- IMPORT NEW BLUEPRINT
    
    app.register_blueprint(auth_bp)
    #app.register_blueprint(vendors_bp)
    app.register_blueprint(orders_bp)
    app.register_blueprint(payments_bp)
    app.register_blueprint(jobs_bp) # <-- REGISTER NEW BLUEPRINT

    # Serve frontend files
    @app.route('/')
    def serve_index():
        return send_from_directory(os.path.join(app.root_path, '..', 'frontend'), 'index.html')

    @app.route('/<path:path>')
    def serve_static(path):
        return send_from_directory(os.path.join(app.root_path, '..', 'frontend'), path)


    return app
