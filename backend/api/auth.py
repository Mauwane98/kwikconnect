from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity, get_jwt, create_access_token # Added create_access_token
import requests
from backend.errors import BadRequestError, NotFoundError
from backend.schemas.auth import UserRegistrationSchema, UserLoginSchema
from .auth_service import AuthService
from backend.models.user import User # Ensure this is the MongoDB User model

auth_bp = Blueprint('auth_bp', __name__)

@auth_bp.route('/google-login', methods=['POST'])
def google_login():
    data = request.get_json()
    if 'access_token' not in data:
        raise BadRequestError('Access token is required')

    user, access_token, refresh_token = AuthService.login_with_google(data['access_token'])

    if isinstance(user, dict):
        user_payload = user
    else:
        try:
            user_payload = user.to_dict()
        except Exception:
            user_payload = {
                'id': str(getattr(user, '_id', None) or getattr(user, 'id', None)),
                'email': getattr(user, 'email', None),
                'full_name': getattr(user, 'full_name', None),
                'role': getattr(user, 'role', None)
            }

    return jsonify({
        "access_token": access_token,
        "refresh_token": refresh_token,
        "user": user_payload
    }), 200

@auth_bp.route('/register', methods=['POST'])
def register():
    schema = UserRegistrationSchema()
    try:
        data = schema.load(request.get_json())
    except Exception as err:
        raise BadRequestError(str(err))

    user, access_token, refresh_token = AuthService.register_user(data)

    return jsonify({
        "message": "User registered successfully",
        "access_token": access_token,
        "refresh_token": refresh_token,
        "user": user.to_dict()
    }), 201

@auth_bp.route('/login', methods=['POST'])
def login():
    schema = UserLoginSchema()
    try:
        data = schema.load(request.get_json())
    except Exception as err:
        raise BadRequestError(str(err))

    user, access_token, refresh_token = AuthService.login_user(data)

    # `user` may be a dict (when using BaseModel.create/find) or an object with `to_dict()`.
    if isinstance(user, dict):
        user_payload = user
    else:
        # objects may implement to_dict()
        try:
            user_payload = user.to_dict()
        except Exception:
            # fallback: expose minimal fields
            user_payload = {
                'id': str(getattr(user, '_id', None) or getattr(user, 'id', None)),
                'email': getattr(user, 'email', None),
                'full_name': getattr(user, 'full_name', None),
                'role': getattr(user, 'role', None)
            }

    return jsonify({
        "access_token": access_token,
        "refresh_token": refresh_token,
        "user": user_payload
    }), 200

@auth_bp.route('/refresh', methods=['POST'])
@jwt_required(refresh=True)
def refresh():
    current_user_id = get_jwt_identity()
    user = User.find_by_id(current_user_id)
    if not user:
        raise NotFoundError("User not found")
    additional_claims = {"role": user.role} # Changed from user.role.value
    new_access_token = create_access_token(identity=current_user_id, additional_claims=additional_claims)
    return jsonify(access_token=new_access_token), 200

@auth_bp.route('/logout', methods=['POST'])
@jwt_required()
def logout():
    jti = get_jwt()["jti"]
    # AuthService.logout_user(jti) # Removed
    return jsonify({"message": "Logout successful"}), 200

@auth_bp.route('/protected', methods=['GET'])
@jwt_required()
def protected():
    current_user_id = get_jwt_identity()
    user = User.find_by_id(current_user_id)
    return jsonify(logged_in_as=user.full_name, user_id=str(user._id), role=user.role), 200 # Updated attributes

@auth_bp.route('/profile', methods=['GET'])
@jwt_required()
def get_profile():
    current_user_id = get_jwt_identity()
    user = User.find_by_id(current_user_id)
    if not user:
        raise NotFoundError("User not found")
    return jsonify(user.to_dict()), 200

@auth_bp.route('/profile', methods=['POST'])
@jwt_required()
def update_profile():
    current_user_id = get_jwt_identity()
    user = User.find_by_id(current_user_id)
    if not user:
        raise NotFoundError("User not found")

    data = request.get_json()
    
    # Update fields if provided
    if 'full_name' in data:
        user.full_name = data['full_name']
    if 'email' in data:
        # You might want to add email validation and uniqueness check here
        user.email = data['email']
    # Add other fields as needed

    user.save() # Save changes to MongoDB
    return jsonify(user.to_dict()), 200