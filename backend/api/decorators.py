# backend/api/decorators.py

from functools import wraps
from flask import jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from backend.models import User, UserRole

def vendor_required(fn):
    """
    A decorator to protect routes that should only be accessible by vendors.
    """
    @wraps(fn)
    @jwt_required()
    def wrapper(*args, **kwargs):
        user_id = get_jwt_identity()
        user = User.query.get(user_id)
        
        if not user or user.role != UserRole.VENDOR:
            return jsonify(msg="Vendor access required"), 403
            
        if not user.vendor_profile:
             return jsonify(msg="Vendor profile not found. Please create one."), 404

        return fn(*args, **kwargs)

def courier_required(fn):
    """
    A decorator to protect routes that should only be accessible by couriers.
    """
    @wraps(fn)
    @jwt_required()
    def wrapper(*args, **kwargs):
        user_id = get_jwt_identity()
        user = User.query.get(user_id)
        
        if not user or user.role != UserRole.COURIER:
            return jsonify(msg="Courier access required"), 403

        if not user.courier_profile or not user.courier_profile.is_approved:
             return jsonify(msg="Courier profile not found or not approved."), 403

        return fn(*args, **kwargs)
