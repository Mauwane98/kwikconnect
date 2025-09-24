"""
Payments API Endpoints

This blueprint handles wallet and transaction-related operations.
"""
from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from backend.errors import BadRequestError, NotFoundError, ConflictError
from backend.schemas.payment import WalletSchema, TransactionSchema, DepositWithdrawSchema, TransferSchema
from .payment_service import PaymentService

payments_bp = Blueprint('payments', __name__, url_prefix='/api/v1/payments')

@payments_bp.route('/wallet', methods=['GET'])
@jwt_required()
def get_wallet():
    """Get the current user's wallet balance."""
    current_user_id = get_jwt_identity()
    wallet = PaymentService.get_user_wallet(current_user_id)
    return jsonify(WalletSchema().dump(wallet)), 200

@payments_bp.route('/wallet/transactions', methods=['GET'])
@jwt_required()
def get_transactions():
    """
    Get the current user's transaction history.
    """
    current_user_id = get_jwt_identity()
    transactions = PaymentService.get_wallet_transactions(current_user_id)
    return jsonify(TransactionSchema(many=True).dump(transactions)), 200

@payments_bp.route('/wallet/deposit', methods=['POST'])
@jwt_required()
def deposit():
    """
    Deposit funds into a wallet.
    """
    current_user_id = get_jwt_identity()
    schema = DepositWithdrawSchema()
    try:
        data = schema.load(request.get_json())
    except Exception as err:
        raise BadRequestError(str(err))

    amount = data['amount']
    wallet, transaction = PaymentService.deposit_funds(current_user_id, amount)
    return jsonify({
        "message": "Deposit successful",
        "new_balance": str(wallet.balance),
        "transaction": TransactionSchema().dump(transaction)
    }), 200

@payments_bp.route('/wallet/withdraw', methods=['POST'])
@jwt_required()
def withdraw():
    """
    Withdraw funds from a wallet.
    """
    current_user_id = get_jwt_identity()
    schema = DepositWithdrawSchema()
    try:
        data = schema.load(request.get_json())
    except Exception as err:
        raise BadRequestError(str(err))

    amount = data['amount']
    wallet, transaction = PaymentService.withdraw_funds(current_user_id, amount)
    return jsonify({
        "message": "Withdrawal successful",
        "new_balance": str(wallet.balance),
        "transaction": TransactionSchema().dump(transaction)
    }), 200

@payments_bp.route('/wallet/transfer', methods=['POST'])
@jwt_required()
def transfer():
    """
    Transfer funds to another user's wallet.
    """
    current_user_id = get_jwt_identity()
    schema = TransferSchema()
    try:
        data = schema.load(request.get_json())
    except Exception as err:
        raise BadRequestError(str(err))

    receiver_id = data['receiver_id']
    amount = data['amount']

    sender_wallet, receiver_wallet, sender_transaction, receiver_transaction = PaymentService.transfer_funds(current_user_id, receiver_id, amount)
    return jsonify({
        "message": "Transfer successful",
        "sender_new_balance": str(sender_wallet.balance),
        "sender_transaction": TransactionSchema().dump(sender_transaction),
        "receiver_new_balance": str(receiver_wallet.balance),
        "receiver_transaction": TransactionSchema().dump(receiver_transaction)
    }), 200
