# backend/api/vendors.py

from flask import Blueprint, request, jsonify
from backend import db
from backend.models import Vendor, Product, User, UserRole
from flask_jwt_extended import jwt_required, get_jwt_identity
from .decorators import vendor_required

vendors_bp = Blueprint('vendors_api', __name__, url_prefix='/api/vendors')

# ===========================================================================
# PUBLIC ENDPOINTS (for Customers browsing)
# ===========================================================================

@vendors_bp.route('/', methods=['GET'])
def list_vendors():
    """Returns a list of all approved vendors."""
    vendors = Vendor.query.filter_by(is_approved=True, is_open=True).all()
    vendor_list = [
        {
            "id": vendor.id,
            "storeName": vendor.store_name,
            "description": vendor.description,
            "address": vendor.address,
            "profileImageUrl": vendor.profile_image_url
        } for vendor in vendors
    ]
    return jsonify(vendor_list), 200

@vendors_bp.route('/<int:vendor_id>/products', methods=['GET'])
def list_vendor_products(vendor_id):
    """Returns a list of available products for a specific vendor."""
    vendor = Vendor.query.get_or_404(vendor_id)
    if not vendor.is_approved:
        return jsonify(msg="Vendor not found or not approved"), 404
        
    products = Product.query.filter_by(vendor_id=vendor_id, is_available=True).all()
    product_list = [
        {
            "id": product.id,
            "name": product.name,
            "description": product.description,
            "price": str(product.price), # Convert Decimal to string for JSON
            "imageUrl": product.image_url
        } for product in products
    ]
    return jsonify(product_list), 200

# ===========================================================================
# PROTECTED VENDOR ENDPOINTS (for store management)
# ===========================================================================

@vendors_bp.route('/profile', methods=['POST'])
@jwt_required() # User must be logged in, but not necessarily a vendor yet
def create_or_update_vendor_profile():
    """
    Creates or updates a vendor's profile.
    This is the first step for a user with 'vendor' role.
    """
    user_id = get_jwt_identity()
    user = User.query.get(user_id)

    if user.role != UserRole.VENDOR:
        return jsonify(msg="User is not a vendor"), 403

    data = request.get_json()
    if not data or 'storeName' not in data or 'address' not in data:
        return jsonify(msg="Missing storeName or address"), 400

    vendor = user.vendor_profile
    if not vendor:
        # Create new profile
        vendor = Vendor(
            user_id=user_id,
            store_name=data.get('storeName'),
            description=data.get('description'),
            address=data.get('address'),
            profile_image_url=data.get('profileImageUrl')
        )
        db.session.add(vendor)
        msg = "Vendor profile created successfully. Awaiting admin approval."
    else:
        # Update existing profile
        vendor.store_name = data.get('storeName', vendor.store_name)
        vendor.description = data.get('description', vendor.description)
        vendor.address = data.get('address', vendor.address)
        vendor.profile_image_url = data.get('profileImageUrl', vendor.profile_image_url)
        vendor.is_open = data.get('isOpen', vendor.is_open)
        msg = "Vendor profile updated successfully."

    db.session.commit()
    return jsonify(msg=msg), 200


@vendors_bp.route('/products', methods=['POST'])
@vendor_required
def create_product():
    """Creates a new product for the authenticated vendor."""
    user_id = get_jwt_identity()
    vendor = Vendor.query.filter_by(user_id=user_id).first_or_404()
    
    data = request.get_json()
    required_fields = ['name', 'price']
    if not all(field in data for field in required_fields):
        return jsonify(msg="Missing name or price"), 400

    new_product = Product(
        vendor_id=vendor.id,
        name=data['name'],
        description=data.get('description'),
        price=data['price'],
        image_url=data.get('imageUrl')
    )
    db.session.add(new_product)
    db.session.commit()
    
    return jsonify({
        "msg": "Product created successfully",
        "product": {
            "id": new_product.id,
            "name": new_product.name,
            "price": str(new_product.price)
        }
    }), 201


@vendors_bp.route('/products/<int:product_id>', methods=['PUT'])
@vendor_required
def update_product(product_id):
    """Updates an existing product for the authenticated vendor."""
    user_id = get_jwt_identity()
    vendor = Vendor.query.filter_by(user_id=user_id).first_or_404()
    
    product = Product.query.get_or_404(product_id)

    # Security check: Ensure the product belongs to the vendor
    if product.vendor_id != vendor.id:
        return jsonify(msg="Unauthorized to edit this product"), 403

    data = request.get_json()
    product.name = data.get('name', product.name)
    product.description = data.get('description', product.description)
    product.price = data.get('price', product.price)
    product.image_url = data.get('imageUrl', product.image_url)
    product.is_available = data.get('isAvailable', product.is_available)
    
    db.session.commit()
    
    return jsonify(msg="Product updated successfully"), 200


@vendors_bp.route('/products/<int:product_id>', methods=['DELETE'])
@vendor_required
def delete_product(product_id):
    """Deletes a product for the authenticated vendor."""
    user_id = get_jwt_identity()
    vendor = Vendor.query.filter_by(user_id=user_id).first_or_404()
    
    product = Product.query.get_or_404(product_id)

    # Security check: Ensure the product belongs to the vendor
    if product.vendor_id != vendor.id:
        return jsonify(msg="Unauthorized to delete this product"), 403
    
    db.session.delete(product)
    db.session.commit()
    
    return jsonify(msg="Product deleted successfully"), 200