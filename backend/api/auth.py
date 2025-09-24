from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity, get_jwt
from backend.errors import BadRequestError, NotFoundError
from backend.schemas.auth import UserRegistrationSchema, UserLoginSchema
from .auth_service import AuthService
from backend.models.user import User

auth_bp = Blueprint('auth_bp', __name__)

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

    return jsonify({
        "access_token": access_token,
        "refresh_token": refresh_token,
        "user": user.to_dict()
    }), 200

@auth_bp.route('/refresh', methods=['POST'])
@jwt_required(refresh=True)
def refresh():
    current_user_id = get_jwt_identity()
    user = User.find_by_id(current_user_id)
    if not user:
        raise NotFoundError("User not found")
    additional_claims = {"role": user.role.value}
    new_access_token = create_access_token(identity=current_user_id, additional_claims=additional_claims)
    return jsonify(access_token=new_access_token), 200

@auth_bp.route('/logout', methods=['POST'])
@jwt_required()
def logout():
    jti = get_jwt()["jti"]
    AuthService.logout_user(jti)
    return jsonify({"message": "Logout successful"}), 200

@auth_bp.route('/protected', methods=['GET'])
@jwt_required()
def protected():
    current_user_id = get_jwt_identity()
    user = User.find_by_id(current_user_id)
    return jsonify(logged_in_as=user.username, user_id=user.id, role=user.role.value), 200