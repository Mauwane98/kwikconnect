
from flask import Blueprint, request, jsonify
from backend.errors import BadRequestError, NotFoundError, ForbiddenError, ConflictError
from backend.schemas.errand import ErrandSchema, ErrandUpdateStatusSchema
from .errand_service import ErrandService
from .decorators import customer_required, courier_required
from flask_jwt_extended import jwt_required, get_jwt_identity
from backend.models import User

errands_bp = Blueprint('errands_api', __name__, url_prefix='/api/v1/errands')

@errands_bp.route('/', methods=['POST'])
@customer_required
def create_errand(current_user):
    """
    Allows a customer to create a new errand.
    """
    schema = ErrandSchema(exclude=['id', 'customer_id', 'courier_id', 'status', 'created_at', 'updated_at'])
    try:
        data = schema.load(request.get_json())
    except Exception as err:
        raise BadRequestError(str(err))

    errand = ErrandService.create_errand(current_user.id, data)
    return jsonify({
        "message": "Errand created successfully",
        "errand": ErrandSchema().dump(errand)
    }), 201

@errands_bp.route('/', methods=['GET'])
@jwt_required()
def get_all_errands():
    """
    Retrieves all errands. Accessible by admins, or filtered for customers/couriers.
    """
    current_user_id = get_jwt_identity()
    current_user = User.find_by_id(current_user_id)
    errands = ErrandService.get_all_errands(current_user)
    return jsonify(ErrandSchema(many=True).dump(errands)), 200

@errands_bp.route('/<int:errand_id>', methods=['GET'])
@jwt_required()
def get_errand_details(errand_id):
    """
    Retrieves details of a specific errand.
    """
    current_user_id = get_jwt_identity()
    current_user = User.find_by_id(current_user_id)
    errand = ErrandService.get_errand_details(current_user, errand_id)
    return jsonify(ErrandSchema().dump(errand)), 200

@errands_bp.route('/<int:errand_id>/accept', methods=['POST'])
@courier_required
def accept_errand(current_user, errand_id):
    """
    Allows an available courier to accept a pending errand.
    """
    errand = ErrandService.accept_errand(current_user.id, errand_id)
    return jsonify({
        "message": f"Errand {errand.id} accepted successfully.",
        "errand": ErrandSchema().dump(errand)
    }), 200

@errands_bp.route('/<int:errand_id>/update_status', methods=['PUT'])
@courier_required
def update_errand_status(current_user, errand_id):
    """
    Allows the assigned courier to update the status of an errand.
    """
    schema = ErrandUpdateStatusSchema()
    try:
        data = schema.load(request.get_json())
    except Exception as err:
        raise BadRequestError(str(err))

    new_status_str = data['status']
    errand = ErrandService.update_errand_status(current_user.id, errand_id, new_status_str)
    return jsonify({
        "message": f"Errand status updated to '{errand.status.value}'.",
        "errand": ErrandSchema().dump(errand)
    }), 200

@errands_bp.route('/<int:errand_id>', methods=['DELETE'])
@customer_required
def delete_errand(current_user, errand_id):
    """
    Allows a customer to delete their own pending errand.
    """
    ErrandService.delete_errand(current_user.id, errand_id)
    return jsonify({"message": "Errand deleted successfully"}), 200
