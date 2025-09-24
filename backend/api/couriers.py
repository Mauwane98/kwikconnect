
# backend/api/couriers.py

from flask import Blueprint, request, jsonify
from backend.errors import BadRequestError, ConflictError, NotFoundError
from backend.schemas.courier import OrderSchema, JobUpdateSchema
from .courier_service import CourierService
from .decorators import courier_required

jobs_bp = Blueprint('jobs_api', __name__, url_prefix='/api/v1/couriers')

@jobs_bp.route('/available', methods=['GET'])
@courier_required
def available_jobs(current_user):
    """
    Lists all orders that are ready for pickup and have not been assigned a courier.
    """
    available_orders = CourierService.get_available_jobs()
    return jsonify(OrderSchema(many=True).dump(available_orders)), 200


@jobs_bp.route('/<int:order_id>/accept', methods=['POST'])
@courier_required
def accept_job(current_user, order_id):
    """
    Allows an authenticated courier to accept an available job.
    """
    order = CourierService.accept_job(current_user.id, order_id)
    return jsonify({
        "message": f"Job {order.id} accepted successfully.",
        "order": OrderSchema().dump(order)
    }), 200


@jobs_bp.route('/<int:order_id>/update', methods=['POST'])
@courier_required
def update_job_status(current_user, order_id):
    """
    Allows the assigned courier to update the status of an order.
    """
    schema = JobUpdateSchema()
    try:
        data = schema.load(request.get_json())
    except Exception as err:
        raise BadRequestError(str(err))

    new_status_str = data['status']
    order = CourierService.update_job_status(current_user.id, order_id, new_status_str)
    return jsonify({
        "message": f"Job status updated to '{order.status.value}'.",
        "order": OrderSchema().dump(order)
    }), 200
