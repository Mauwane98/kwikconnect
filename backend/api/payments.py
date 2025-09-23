# backend/api/payments.py

from flask import Blueprint, request, jsonify
from backend import db
from backend.models import Order, Transaction, Wallet, User, OrderStatus, TransactionType, TransactionStatus
from flask_jwt_extended import jwt_required, get_jwt_identity
import uuid # To generate mock gateway IDs
from decimal import Decimal

payments_bp = Blueprint('payments_api', __name__, url_prefix='/api/payments')

@payments_bp.route('/initialize', methods=['POST'])
@jwt_required()
def initialize_payment():
    """
    Initializes a payment for a specific order.
    The customer must be the one who placed the order.
    """
    current_user_id = get_jwt_identity()
    data = request.get_json()
    order_id = data.get('order_id')

    if not order_id:
        return jsonify(msg="Order ID is required."), 400

    order = Order.query.get(order_id)

    # Validations
    if not order:
        return jsonify(msg="Order not found."), 404
    if order.customer_id != current_user_id:
        return jsonify(msg="You are not authorized to pay for this order."), 403
    if order.status != OrderStatus.PENDING:
        return jsonify(msg="This order is not pending payment."), 409
    
    user = User.query.get(current_user_id)
    wallet = user.wallet
    if not wallet:
         return jsonify(msg="User wallet not found."), 500

    # Create a new transaction record
    new_transaction = Transaction(
        wallet_id=wallet.id,
        amount=order.total_amount,
        transaction_type=TransactionType.PAYMENT,
        status=TransactionStatus.PENDING,
        description=f"Payment for Order #{order.id}"
    )

    db.session.add(new_transaction)
    db.session.commit()

    # --- MOCK PAYMENT GATEWAY INTERACTION ---
    # In a real application, you would call the payment gateway's API here
    # with the order details and get a payment URL or reference ID.
    # For now, we simulate this.
    mock_payment_gateway_url = f"https://mock-payment-gateway.com/pay?transaction_id={new_transaction.id}&amount={order.total_amount}"

    return jsonify({
        "msg": "Payment initialized.",
        "transaction_id": new_transaction.id,
        "payment_url": mock_payment_gateway_url # Frontend would redirect to this URL
    }), 200


@payments_bp.route('/webhook', methods=['POST'])
def payment_webhook():
    """
    Webhook endpoint for the payment gateway to send payment status updates.
    This endpoint is public but should be secured in production (e.g., via signature verification).
    """
    data = request.get_json()
    # In a real scenario, the gateway would send its own transaction ID,
    # which we would have stored. Here, we'll use our internal ID for simplicity.
    transaction_id = data.get('transaction_id')
    payment_status = data.get('status') # e.g., 'success' or 'failed'
    gateway_id = data.get('gateway_transaction_id', str(uuid.uuid4()))

    if not transaction_id or not payment_status:
        return jsonify(msg="Missing transaction_id or status."), 400

    transaction = Transaction.query.get(transaction_id)
    if not transaction or transaction.status != TransactionStatus.PENDING:
        return jsonify(msg="Transaction not found or already processed."), 404

    # Find the associated order via the transaction description
    # This is a simple way; a direct link (e.g., order_id on Transaction model) would be more robust.
    if "Payment for Order #" in transaction.description:
        try:
            order_id = int(transaction.description.split('#')[-1])
            order = Order.query.get(order_id)
        except (ValueError, IndexError):
            order = None
    else:
        order = None

    if payment_status == 'success':
        transaction.status = TransactionStatus.COMPLETED
        transaction.gateway_transaction_id = gateway_id
        
        # Update order status if it's an order payment
        if order and order.status == OrderStatus.PENDING:
            order.status = OrderStatus.ACCEPTED_BY_VENDOR
            print(f"Order {order.id} status updated to ACCEPTED_BY_VENDOR.")
        
    elif payment_status == 'failed':
        transaction.status = TransactionStatus.FAILED
        transaction.gateway_transaction_id = gateway_id
        
        # Optionally, update order status to 'cancelled' or 'payment_failed'
        if order:
            order.status = OrderStatus.CANCELLED
            print(f"Order {order.id} status updated to CANCELLED due to failed payment.")
    else:
        return jsonify(msg="Invalid payment status received."), 400

    db.session.commit()
    
    # Respond to the webhook to acknowledge receipt
    return jsonify(msg="Webhook received."), 200
