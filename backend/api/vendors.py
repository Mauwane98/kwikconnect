
# backend/api/vendors.py

from flask import Blueprint, request, jsonify
from backend.errors import BadRequestError, ConflictError, UnauthorizedError, NotFoundError, ForbiddenError
from backend.schemas.vendor import VendorSchema, ProductSchema
from .vendor_service import VendorService
from .decorators import vendor_required, vendor_owner_required

vendors_bp = Blueprint('vendors_api', __name__, url_prefix='/api/v1/vendors')

# ===========================================================================
# PUBLIC ENDPOINTS (for Customers browsing)
# ===========================================================================

@vendors_bp.route('/', methods=['GET'])
def list_vendors():
    """Returns a list of all approved vendors."""
    # Read supported filters from query params
    q = request.args.get('query')
    category = request.args.get('category')
    delivery_time = request.args.get('delivery_time')

    if q or category or delivery_time:
        filters = {}
        if q:
            filters['query'] = q
        if category:
            filters['category'] = category
        if delivery_time:
            filters['delivery_time'] = delivery_time

        vendors = VendorService.search_vendors(filters)
        return jsonify(vendors), 200

    vendors = VendorService.get_all_vendors()
    # VendorService.get_all_vendors returns raw vendor dicts; ensure schema compatibility when possible
    return jsonify(VendorSchema(many=True).dump(vendors)), 200

@vendors_bp.route('/<int:vendor_id>/products', methods=['GET'])
def list_vendor_products(vendor_id):
    """
    Returns a list of available products for a specific vendor.
    """
    products = VendorService.get_vendor_products(vendor_id)
    return jsonify(ProductSchema(many=True).dump(products)), 200

# ===========================================================================
# PROTECTED VENDOR ENDPOINTS (for store management)
# ===========================================================================

@vendors_bp.route('/profile', methods=['POST'])
@vendor_required
def create_or_update_vendor_profile(user):
    """
    Creates or updates a vendor's profile.
    """
    schema = VendorSchema(partial=True) # Allow partial updates
    try:
        data = schema.load(request.get_json())
    except Exception as err:
        raise BadRequestError(str(err))

    vendor = VendorService.create_or_update_vendor_profile(user.id, data)
    return jsonify({
        "message": "Vendor profile updated successfully. Awaiting admin approval." if not vendor.is_approved else "Vendor profile updated successfully.",
        "vendor": VendorSchema().dump(vendor)
    }), 200


@vendors_bp.route('/products', methods=['POST'])
@vendor_required
def create_product(user):
    """
    Creates a new product for the authenticated vendor.
    """
    schema = ProductSchema()
    try:
        data = schema.load(request.get_json())
    except Exception as err:
        raise BadRequestError(str(err))

    product = VendorService.create_product(user.id, data)
    return jsonify({
        "message": "Product created successfully",
        "product": ProductSchema().dump(product)
    }), 201


@vendors_bp.route('/products/<int:product_id>', methods=['PUT'])
@vendor_owner_required
def update_product(user, vendor, product_id):
    """
    Updates an existing product for the authenticated vendor.
    """
    schema = ProductSchema(partial=True) # Allow partial updates
    try:
        data = schema.load(request.get_json())
    except Exception as err:
        raise BadRequestError(str(err))

    product = VendorService.update_product(user.id, product_id, data)
    return jsonify({
        "message": "Product updated successfully",
        "product": ProductSchema().dump(product)
    }), 200


@vendors_bp.route('/products/<int:product_id>', methods=['DELETE'])
@vendor_owner_required
def delete_product(user, vendor, product_id):
    """
    Deletes a product for the authenticated vendor.
    """
    VendorService.delete_product(user.id, product_id)
    return jsonify({"message": "Product deleted successfully"}), 200
