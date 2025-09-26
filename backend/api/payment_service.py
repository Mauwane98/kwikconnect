

from backend.models.wallet import Wallet
from backend.models.transaction import Transaction, TransactionType
from backend.models.user import User
from backend.errors import NotFoundError, BadRequestError, ForbiddenError, ConflictError
from decimal import Decimal

class PaymentService:
    @staticmethod
    def get_user_wallet(user_id):
        wallet = Wallet.find_by_user_id(user_id)
        if not wallet:
            raise NotFoundError("Wallet not found")
        return wallet

    @staticmethod
    def get_wallet_transactions(user_id):
        wallet = PaymentService.get_user_wallet(user_id)
        transactions = Transaction.find_by_wallet_id(str(wallet._id))
        # Sort transactions by created_at in descending order
        transactions.sort(key=lambda x: x.created_at, reverse=True)
        return transactions

    @staticmethod
    def deposit_funds(user_id, amount):
        if not isinstance(amount, (int, float)) or amount <= 0:
            raise BadRequestError("Invalid amount")

        wallet = PaymentService.get_user_wallet(user_id)
        wallet.balance += Decimal(str(amount))
        wallet.save() # Save updated wallet balance

        transaction = Transaction(
            wallet_id=str(wallet._id), # Store wallet's MongoDB _id
            amount=Decimal(str(amount)),
            transaction_type=TransactionType.DEPOSIT.value, # Store enum value
            description="User deposit"
        )
        transaction.save() # Save new transaction
        return wallet, transaction

    @staticmethod
    def withdraw_funds(user_id, amount):
        if not isinstance(amount, (int, float)) or amount <= 0:
            raise BadRequestError("Invalid amount")

        wallet = PaymentService.get_user_wallet(user_id)
        if wallet.balance < Decimal(str(amount)):
            raise ConflictError("Insufficient funds")

        wallet.balance -= Decimal(str(amount))
        wallet.save() # Save updated wallet balance

        transaction = Transaction(
            wallet_id=str(wallet._id), # Store wallet's MongoDB _id
            amount=Decimal(str(amount)),
            transaction_type=TransactionType.WITHDRAWAL.value, # Store enum value
            description="User withdrawal"
        )
        transaction.save() # Save new transaction
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
        sender_wallet.save() # Save updated sender wallet balance
        receiver_wallet.save() # Save updated receiver wallet balance

        sender_transaction = Transaction(
            wallet_id=str(sender_wallet._id), # Store wallet's MongoDB _id
            amount=Decimal(str(amount)),
            transaction_type=TransactionType.PAYOUT.value, # Use PAYOUT for sender
            description=f"Transfer to user {receiver_id}"
        )
        receiver_transaction = Transaction(
            wallet_id=str(receiver_wallet._id), # Store wallet's MongoDB _id
            amount=Decimal(str(amount)),
            transaction_type=TransactionType.PAYMENT.value, # Use PAYMENT for receiver
            description=f"Transfer from user {sender_id}"
        )

        sender_transaction.save()
        receiver_transaction.save()
        return sender_wallet, receiver_wallet, sender_transaction, receiver_transaction
