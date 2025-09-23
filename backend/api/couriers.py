# backend/api/couriers.py

from flask import Blueprint, request, jsonify
from backend import db
from backend.models import Order, Courier, User, OrderStatus, CourierStatus
from flask_jwt_extended import get_jwt_identity
from .decorators import courier_required

jobs_bp = Blueprint('jobs_api', __name__, url_prefix='/api/jobs')

#@jobs_bp.route('/available', methods=['GET'])
#@courier_required
#def available_jobs():
#    """
#    Lists all orders that are ready for pickup and have not been assigned a courier.
#    """
#    # Orders are "available jobs" when a vendor marks them as ready.
#    available_orders = Order.query.filter_by(
#        status=OrderStatus.READY_FOR_PICKUP,
#        courier_id=None
#    ).order_by(Order.created_at.desc()).all()
#
#    jobs_list = [{
#        "order_id": order.id,
#        "vendor_name": order.vendor.store_name,
#        "pickup_address": order.vendor.address,
#        "delivery_address": order.delivery_address,
#        "total_amount": str(order.total_amount),
#        "placed_at": order.created_at.isoformat()
#    } for order in available_orders]
#
#    return jsonify(jobs_list), 200


#@jobs_bp.route('/<int:order_id>/accept', methods=['POST'])
#@courier_required
#def accept_job(order_id):
#    """
#    Allows an authenticated courier to accept an available job.
#    """
#    user_id = get_jwt_identity()
#    courier = User.query.get(user_id).courier_profile
#    
#    if courier.status != CourierStatus.AVAILABLE:
#        return jsonify(msg=f"Cannot accept job, your status is '{courier.status.value}'."), 409
#
#    order = Order.query.get(order_id)
#
#    # Atomic check: Ensure the order is still available
#    if not order or order.status != OrderStatus.READY_FOR_PICKUP or order.courier_id is not None:
#        return jsonify(msg="Job is no longer available."), 404
#
#    # Assign the job to the courier
#    order.courier_id = courier.id
#    order.status = OrderStatus.PICKED_UP
#    courier.status = CourierStatus.ON_DELIVERY
#    
#    db.session.commit()
#
#    return jsonify(msg=f"Job {order.id} accepted successfully."), 200
#
#
#@jobs_bp.route('/<int:order_id>/update', methods=['POST'])
#@courier_required
#def update_job_status(order_id):
#    """
#    Allows the assigned courier to update the status of an order.
#    e.g., from 'picked_up' to 'out_for_delivery' or 'delivered'.
#    """
#    user_id = get_jwt_identity()
#    courier = User.query.get(user_id).courier_profile
#
#    data = request.get_json()
#    new_status_str = data.get('status')
#    
#    if not new_status_str:
#        return jsonify(msg="New status is required."), 400
#
#    order = Order.query.get(order_id)
#
#    # Security and logic checks
#    if not order:
#        return jsonify(msg="Order not found."), 404
#    if order.courier_id != courier.id:
#        return jsonify(msg="You are not assigned to this job."), 403
#
#    # Validate the new status
#    try:
#        new_status = OrderStatus(new_status_str)
#    except ValueError:
#        return jsonify(msg=f"'{new_status_str}' is not a valid order status."), 400
#
#    # Basic state machine logic
#    valid_transitions = {
#        OrderStatus.PICKED_UP: [OrderStatus.OUT_FOR_DELIVERY],
#        OrderStatus.OUT_FOR_DELIVERY: [OrderStatus.DELIVERED]
#    }
#
#    if new_status not in valid_transitions.get(order.status, []):
#        return jsonify(msg=f"Invalid status transition from '{order.status.value}' to '{new_status.value}'."), 409
#
#    order.status = new_status
#
#    # If the job is done, the courier becomes available again
#    if new_status == OrderStatus.DELIVERED:
#        courier.status = CourierStatus.AVAILABLE
#
#    db.session.commit()
#
#    return jsonify(msg=f"Job status updated to '{new_status.value}'."), 200