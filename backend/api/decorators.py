"""
API Decorators

This file contains custom decorators for checking user roles and permissions
based on the JWT token.
"""
from functools import wraps
from flask import jsonify, request, current_app
from flask_jwt_extended import jwt_required, get_jwt_identity
from backend.models.user import User, UserRole
from backend.models.vendor import Vendor
from backend.models.product import Product
from backend.errors import UnauthorizedError, ForbiddenError, NotFoundError

def role_required(required_role):
    """
    A decorator to restrict access to users with a specific role.
    """
    def decorator(fn):
        @wraps(fn)
        @jwt_required()
        def wrapper(*args, **kwargs):
            user_id = get_jwt_identity()
            user = User.find_by_id(user_id)

            if not user:
                raise UnauthorizedError("User not found")

            if user.role != required_role:
                raise ForbiddenError("Insufficient permissions")

            return fn(user, *args, **kwargs)
        return wrapper
    return decorator

def vendor_owner_required(fn):
    """
    A decorator to ensure the authenticated user is a vendor and owns the resource (e.g., product).
    Assumes the resource ID (e.g., product_id) is passed as a keyword argument.
    """
    @wraps(fn)
    @jwt_required()
    def wrapper(*args, **kwargs):
        user_id = get_jwt_identity()
        user = User.find_by_id(user_id)

        if not user or user.role != UserRole.VENDOR:
            raise ForbiddenError("Access denied: Vendor privileges required.")

        vendor = Vendor.query.filter_by(user_id=user.id).first()
        if not vendor:
            raise NotFoundError("Vendor profile not found.")

        # Check for product ownership if product_id is in kwargs
        product_id = kwargs.get('product_id')
        if product_id:
            product = Product.query.get(product_id)
            if not product or product.vendor_id != vendor.id:
                raise ForbiddenError("Unauthorized: Product does not belong to this vendor.")

        return fn(user, vendor, *args, **kwargs)
    return wrapper

# Specific role decorators
def admin_required(fn):
    return role_required(UserRole.ADMIN)(fn)

def vendor_required(fn):
    return role_required(UserRole.VENDOR)(fn)

def courier_required(fn):
    return role_required(UserRole.COURIER)(fn)

def customer_required(fn):
    return role_required(UserRole.CUSTOMER)(fn)