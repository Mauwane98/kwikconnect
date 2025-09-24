# backend/api/orders.py

from flask import Blueprint, request, jsonify
from backend.errors import BadRequestError, NotFoundError, ForbiddenError
from backend.schemas.order import OrderCreateSchema, OrderSchema
from .order_service import OrderService
from flask_jwt_extended import jwt_required, get_jwt_identity

orders_bp = Blueprint('orders_api', __name__, url_prefix='/api/v1/orders')

@orders_bp.route('/', methods=['POST'])
@jwt_required()
def create_order():
    """
    Creates a new order. Authenticated customers only.
    """
    customer_id = get_jwt_identity()
    schema = OrderCreateSchema()
    try:
        data = schema.load(request.get_json())
    except Exception as err:
        raise BadRequestError(str(err))

    order = OrderService.create_order(customer_id, data)
    return jsonify({
        "message": "Order created successfully.",
        "order": OrderSchema().dump(order)
    }), 201


@orders_bp.route('/<int:order_id>', methods=['GET'])
@jwt_required()
def get_order_details(order_id):
    """
    Retrieves the details and status of a specific order.
    """
    current_user_id = get_jwt_identity()
    order = OrderService.get_order_details(current_user_id, order_id)
    return jsonify(OrderSchema().dump(order)), 200
