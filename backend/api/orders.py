# backend/api/orders.py

from flask import Blueprint, request, jsonify
from backend import db
from backend.models import Order, OrderItem, Product, Vendor, User, UserRole
from flask_jwt_extended import jwt_required, get_jwt_identity
from decimal import Decimal

orders_bp = Blueprint('orders_api', __name__, url_prefix='/api/orders')

@orders_bp.route('/', methods=['POST'])
@jwt_required()
def create_order():
    """
    Creates a new order. Authenticated customers only.
    Expects a JSON payload with:
    {
        "vendor_id": 1,
        "delivery_address": "123 Main St, Anytown, USA",
        "items": [
            {"product_id": 1, "quantity": 2},
            {"product_id": 3, "quantity": 1}
        ]
    }
    """
    customer_id = get_jwt_identity()
    user = User.query.get(customer_id)
    
    # Ensure the user is a customer
    if not user or user.role != UserRole.CUSTOMER:
        return jsonify(msg="Only customers can create orders."), 403

    data = request.get_json()
    vendor_id = data.get('vendor_id')
    delivery_address = data.get('delivery_address')
    items_data = data.get('items')

    # Basic validation
    if not all([vendor_id, delivery_address, items_data]):
        return jsonify(msg="Missing vendor_id, delivery_address, or items."), 400

    # Validate vendor
    vendor = Vendor.query.get(vendor_id)
    if not vendor or not vendor.is_approved or not vendor.is_open:
        return jsonify(msg="Vendor is not available or does not exist."), 404

    total_amount = Decimal('0.00')
    order_items_to_create = []

    # Validate products and calculate total amount
    for item in items_data:
        product = Product.query.get(item.get('product_id'))
        
        # Check if product exists, belongs to the correct vendor, and is available
        if not product or product.vendor_id != vendor.id or not product.is_available:
            return jsonify(msg=f"Product with ID {item.get('product_id')} is invalid or unavailable."), 400
        
        quantity = item.get('quantity', 0)
        if quantity <= 0:
            return jsonify(msg=f"Invalid quantity for product ID {product.id}."), 400

        price_at_purchase = product.price
        total_amount += price_at_purchase * quantity
        
        order_items_to_create.append(OrderItem(
            product_id=product.id,
            quantity=quantity,
            price_at_purchase=price_at_purchase
        ))

    if not order_items_to_create:
        return jsonify(msg="Order must contain at least one item."), 400

    # Create the order and its items within a transaction
    try:
        new_order = Order(
            customer_id=customer_id,
            vendor_id=vendor_id,
            delivery_address=delivery_address,
            total_amount=total_amount
        )
        
        new_order.items.extend(order_items_to_create)
        
        db.session.add(new_order)
        db.session.commit()
        
        return jsonify({
            "msg": "Order created successfully.",
            "order_id": new_order.id,
            "total_amount": str(new_order.total_amount)
        }), 201

    except Exception as e:
        db.session.rollback()
        # In a real app, log the error e
        return jsonify(msg="An error occurred while creating the order."), 500


@orders_bp.route('/<int:order_id>', methods=['GET'])
@jwt_required()
def get_order_status(order_id):
    """
    Retrieves the details and status of a specific order.
    Accessible by the customer who placed it, or other relevant roles (TBD).
    """
    current_user_id = get_jwt_identity()
    order = Order.query.get_or_404(order_id)
    
    # Security check: Ensure the user is authorized to view this order
    # For now, only the customer who placed the order can view it.
    if order.customer_id != current_user_id:
        return jsonify(msg="You are not authorized to view this order."), 403

    items = [{
        "product_id": item.product_id,
        "product_name": item.product.name,
        "quantity": item.quantity,
        "price_at_purchase": str(item.price_at_purchase)
    } for item in order.items]

    return jsonify({
        "order_id": order.id,
        "status": order.status.value,
        "total_amount": str(order.total_amount),
        "delivery_address": order.delivery_address,
        "created_at": order.created_at.isoformat(),
        "vendor": {
            "id": order.vendor.id,
            "store_name": order.vendor.store_name
        },
        "items": items
    }), 200
