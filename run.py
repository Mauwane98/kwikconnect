from flask_cors import CORS
from flask_jwt_extended import JWTManager
from flask_migrate import Migrate
import os
from dotenv import load_dotenv
from flask import send_from_directory

# Load environment variables from .env file
load_dotenv()

from backend import create_app, db
from backend.api import auth, couriers, orders, vendors, payments, errands
from backend.models.token_blocklist import TokenBlocklist

# Create Flask app
app = create_app()

# Initialize extensions
jwt = JWTManager(app)
CORS(app) # Enables CORS for all routes
migrate = Migrate(app, db)

# Register blueprints for API endpoints
app.register_blueprint(auth.auth_bp, url_prefix='/api/v1/auth')
app.register_blueprint(vendors.vendors_bp, url_prefix='/api/v1/vendors')
app.register_blueprint(couriers.jobs_bp, url_prefix='/api/v1/couriers')
app.register_blueprint(orders.orders_bp, url_prefix='/api/v1/orders')
app.register_blueprint(payments.payments_bp, url_prefix='/api/v1/payments')
app.register_blueprint(errands.errands_bp, url_prefix='/api/v1/errands')

@jwt.token_in_blocklist_loader
def check_if_token_in_blocklist(jwt_header, jwt_payload):
    jti = jwt_payload["jti"]
    token = TokenBlocklist.query.filter_by(jti=jti).first()
    return token is not None

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
    # Using a debug mode for development
    app.run(host='0.0.0.0', port=5000, debug=True)