
from backend import db
from backend.models import Wallet, Transaction, TransactionType, User
from backend.errors import NotFoundError, BadRequestError, ForbiddenError, ConflictError
from decimal import Decimal

class PaymentService:
    @staticmethod
    def get_user_wallet(user_id):
        wallet = Wallet.query.filter_by(user_id=user_id).first()
        if not wallet:
            raise NotFoundError("Wallet not found")
        return wallet

    @staticmethod
    def get_wallet_transactions(user_id):
        wallet = PaymentService.get_user_wallet(user_id)
        transactions = Transaction.query.filter_by(wallet_id=wallet.id).order_by(Transaction.created_at.desc()).all()
        return transactions

    @staticmethod
    def deposit_funds(user_id, amount):
        if not isinstance(amount, (int, float)) or amount <= 0:
            raise BadRequestError("Invalid amount")

        wallet = PaymentService.get_user_wallet(user_id)
        wallet.balance += Decimal(str(amount))
        
        transaction = Transaction(
            wallet_id=wallet.id,
            amount=Decimal(str(amount)),
            transaction_type=TransactionType.DEPOSIT,
            description="User deposit"
        )
        
        db.session.add(transaction)
        db.session.commit()
        return wallet, transaction

    @staticmethod
    def withdraw_funds(user_id, amount):
        if not isinstance(amount, (int, float)) or amount <= 0:
            raise BadRequestError("Invalid amount")

        wallet = PaymentService.get_user_wallet(user_id)
        if wallet.balance < Decimal(str(amount)):
            raise ConflictError("Insufficient funds")

        wallet.balance -= Decimal(str(amount))
        
        transaction = Transaction(
            wallet_id=wallet.id,
            amount=Decimal(str(amount)),
            transaction_type=TransactionType.WITHDRAWAL,
            description="User withdrawal"
        )
        
        db.session.add(transaction)
        db.session.commit()
        return wallet, transaction

    @staticmethod
    def transfer_funds(sender_id, receiver_id, amount):
        if not isinstance(amount, (int, float)) or amount <= 0:
            raise BadRequestError("Invalid amount")

        sender_wallet = PaymentService.get_user_wallet(sender_id)
        receiver_wallet = PaymentService.get_user_wallet(receiver_id)

        if sender_wallet.balance < Decimal(str(amount)):
            raise ConflictError("Insufficient funds")

        sender_wallet.balance -= Decimal(str(amount))
        receiver_wallet.balance += Decimal(str(amount))

        sender_transaction = Transaction(
            wallet_id=sender_wallet.id,
            amount=Decimal(str(amount)),
            transaction_type=TransactionType.TRANSFER,
            description=f"Transfer to user {receiver_id}"
        )
        receiver_transaction = Transaction(
            wallet_id=receiver_wallet.id,
            amount=Decimal(str(amount)),
            transaction_type=TransactionType.TRANSFER,
            description=f"Transfer from user {sender_id}"
        )

        db.session.add_all([sender_transaction, receiver_transaction])
        db.session.commit()
        return sender_wallet, receiver_wallet, sender_transaction, receiver_transaction
