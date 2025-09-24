"""
Admin API Endpoints

This blueprint provides administrative functionalities, such as viewing stats and managing users.
Access is restricted to users with the ADMIN role.
"""
from flask import Blueprint, jsonify
from backend.models.user import User
from backend.models.vendor import Vendor
from backend.models.courier import Courier
from backend.models.order import Order
from .decorators import admin_required

admin_bp = Blueprint('admin', __name__)

@admin_bp.route('/stats', methods=['GET'])
@admin_required
def get_stats(current_user):
    """
    Retrieves platform-wide statistics for the admin dashboard.
    """
    total_users = User.query.count()
    total_vendors = Vendor.query.count()
    total_couriers = Courier.query.count()
    total_orders = Order.query.count()

    stats = {
        'total_users': total_users,
        'total_vendors': total_vendors,
        'total_couriers': total_couriers,
        'total_orders': total_orders
    }
    return jsonify(stats), 200

@admin_bp.route('/users', methods=['GET'])
@admin_required
def list_users(current_user):
    """
    Lists all users on the platform.
    """
    users = User.query.all()
    return jsonify([user.to_dict() for user in users]), 200
