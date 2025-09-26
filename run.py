from flask_cors import CORS
from flask_jwt_extended import JWTManager
# from flask_migrate import Migrate # Removed
import os
from datetime import datetime
from dotenv import load_dotenv
from flask import send_from_directory

# Load environment variables from .env file
load_dotenv()

from backend import create_app # Removed db import
# from backend.models.token_blocklist import TokenBlocklist # Removed
from backend.api import auth, couriers, orders, vendors, payments, errands, messaging # Added messaging

# Example: Import current_app for MongoDB usage
from flask import current_app, jsonify

# Create Flask app
app = create_app()

# Initialize extensions
jwt = JWTManager(app)
CORS(app) # Enables CORS for all routes
# migrate = Migrate(app, db) # Removed

# Register blueprints for API endpoints
app.register_blueprint(auth.auth_bp, url_prefix='/api/v1/auth')
app.register_blueprint(vendors.vendors_bp, url_prefix='/api/v1/vendors')
app.register_blueprint(couriers.jobs_bp, url_prefix='/api/v1/couriers')
app.register_blueprint(orders.orders_bp, url_prefix='/api/v1/orders')
app.register_blueprint(payments.payments_bp, url_prefix='/api/v1/payments')
app.register_blueprint(errands.errands_bp, url_prefix='/api/v1/errands')
app.register_blueprint(messaging.messaging, url_prefix='/api/v1/messaging') # Registered messaging blueprint

@jwt.token_in_blocklist_loader
def check_if_token_in_blocklist(jwt_header, jwt_payload):
    jti = jwt_payload["jti"]
    # token = TokenBlocklist.query.filter_by(jti=jti).first() # Commented out
    # return token is not None # Commented out
    return False # For now, always return False as TokenBlocklist is not implemented with MongoDB

# Serve React App
@app.route('/')
def serve_index():
    return send_from_directory(app.static_folder, 'index.html')

@app.route('/<path:path>')
def serve_static(path):
    if path != "" and os.path.exists(os.path.join(app.static_folder, path)):
        return send_from_directory(app.static_folder, path)
    else:
        return send_from_directory(app.static_folder, 'index.html')

if __name__ == '__main__':
    try:
        print("Starting Flask server...")
        print(f"MongoDB URI: {app.config['MONGO_URI']}")
        print(f"MongoDB Database: {app.config['MONGO_DB']}")
        
        # Test MongoDB connection before starting server
        with app.app_context():
            db = app.mongo_db
            db.command('ping')
            print("MongoDB connection successful!")
        
        # Using debug mode for development with reloader disabled
        app.run(
            host='127.0.0.1',
            port=5000,
            debug=True,
            use_reloader=False
        )
    except Exception as e:
        print(f"Error starting server: {str(e)}")
        import traceback
        traceback.print_exc()


# Example route to test MongoDB connection
@app.route('/api/v1/mongo-test')
def mongo_test():
    try:
        db = current_app.mongo_db
        # Insert a test document
        result = db.test_collection.insert_one({'msg': 'Hello from MongoDB!', 'timestamp': str(datetime.now())})
        
        # Find all documents
        docs = list(db.test_collection.find({}, {'_id': 0}))
        
        return jsonify({
            'status': 'success',
            'message': 'MongoDB connection successful',
            'data': docs
        }), 200
    except Exception as e:
        return jsonify({
            'status': 'error',
            'message': f'MongoDB connection failed: {str(e)}'
        }), 500
