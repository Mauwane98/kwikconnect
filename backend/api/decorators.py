"""
API Decorators

This file contains custom decorators for checking user roles and permissions
based on the JWT token.
"""
from functools import wraps
from flask import jsonify, request, current_app
from flask_jwt_extended import jwt_required, get_jwt_identity
from backend.models.user import User
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

        if not user or user.role != 'vendor':
            raise ForbiddenError("Access denied: Vendor privileges required.")

        vendor = Vendor.find_by_user_id(str(user._id)) # Use user._id as string
        if not vendor:
            raise NotFoundError("Vendor profile not found.")

        # Check for product ownership if product_id is in kwargs
        product_id = kwargs.get('product_id')
        if product_id:
            product = Product.find_by_id(product_id)
            if not product or product.vendor_id != str(vendor._id): # Compare with string representation of vendor._id
                raise ForbiddenError("Unauthorized: Product does not belong to this vendor.")

        return fn(user, vendor, *args, **kwargs)
    return wrapper

# Specific role decorators
def admin_required(fn):
    return role_required('admin')(fn)

def vendor_required(fn):
    return role_required('vendor')(fn)

def courier_required(fn):
    return role_required('courier')(fn)

def customer_required(fn):
    return role_required('customer')(fn)