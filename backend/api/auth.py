# backend/api/auth.py

from flask import Blueprint, request, jsonify
from backend.models import User, Wallet
from backend import db
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity

auth_bp = Blueprint('auth_api', __name__, url_prefix='/api/auth')

@auth_bp.route('/register', methods=['POST'])
def register():
    data = request.get_json()

    # Basic input validation
    required_fields = ['email', 'password', 'firstName', 'lastName', 'phoneNumber']
    if not all(field in data for field in required_fields):
        return jsonify({"msg": "Missing required fields"}), 400

    email = data.get('email')
    phone_number = data.get('phoneNumber')

    # Check for existing user
    if User.query.filter_by(email=email).first() is not None:
        return jsonify({"msg": "Email already registered"}), 409
    if User.query.filter_by(phone_number=phone_number).first() is not None:
        return jsonify({"msg": "Phone number already registered"}), 409

    # Create new user
    new_user = User(
        email=email,
        first_name=data.get('firstName'),
        last_name=data.get('lastName'),
        phone_number=phone_number,
        # Role can be assigned based on registration flow in the future
        # For now, defaults to CUSTOMER
    )
    new_user.set_password(data.get('password'))

    # Create a wallet for the new user
    new_wallet = Wallet(user=new_user)
    
    db.session.add(new_user)
    db.session.add(new_wallet)
    db.session.commit()

    return jsonify({"msg": "User registered successfully"}), 201


@auth_bp.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    email = data.get('email', None)
    password = data.get('password', None)

    if not email or not password:
        return jsonify({"msg": "Missing email or password"}), 400

    user = User.query.filter_by(email=email).first()

    if user and user.check_password(password):
        access_token = create_access_token(identity=user.id)
        return jsonify(access_token=access_token, user_role=user.role.value), 200
    
    return jsonify({"msg": "Bad email or password"}), 401


@auth_bp.route('/profile', methods=['GET'])
@jwt_required()
def profile():
    current_user_id = get_jwt_identity()
    user = User.query.get(current_user_id)

    if not user:
        return jsonify({"msg": "User not found"}), 404

    return jsonify({
        "id": user.id,
        "email": user.email,
        "firstName": user.first_name,
        "lastName": user.last_name,
        "phoneNumber": user.phone_number,
        "role": user.role.value,
        "createdAt": user.created_at.isoformat()
    }), 200
