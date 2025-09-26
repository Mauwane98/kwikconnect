# backend/models/transaction.py


from backend.mongo import get_mongo_client
from bson.objectid import ObjectId

db = get_mongo_client()
transactions_collection = db.transactions

import enum
from datetime import datetime
from .base_model import BaseModel # Import BaseModel

class TransactionType(enum.Enum):
    DEPOSIT = 'deposit'
    WITHDRAWAL = 'withdrawal'
    PAYMENT = 'payment'
    PAYOUT = 'payout'
    REFUND = 'refund'

class TransactionStatus(enum.Enum):
    PENDING = 'pending'
    COMPLETED = 'completed'
    FAILED = 'failed'

class Transaction(BaseModel):
    def __init__(self, wallet_id, amount, transaction_type, status='pending', description=None,
                 gateway_transaction_id=None, created_at=None, _id=None):
        self.wallet_id = wallet_id
        self.amount = amount
        self.transaction_type = transaction_type
        self.status = status
        self.description = description
        self.gateway_transaction_id = gateway_transaction_id
        self.created_at = created_at if created_at else datetime.utcnow()
        self._id = _id if _id else ObjectId()

    def save(self):
        transaction_data = {
            'wallet_id': self.wallet_id,
            'amount': self.amount,
            'transaction_type': self.transaction_type,
            'status': self.status,
            'description': self.description,
            'gateway_transaction_id': self.gateway_transaction_id,
            'created_at': self.created_at
        }
        if self._id:
            transactions_collection.update_one({'_id': self._id}, {'$set': transaction_data}, upsert=True)
        else:
            result = transactions_collection.insert_one(transaction_data)
            self._id = result.inserted_id
        return self

    @staticmethod
    def find_by_id(transaction_id):
        transaction_data = transactions_collection.find_one({'_id': ObjectId(transaction_id)})
        if transaction_data:
            return Transaction(
                _id=transaction_data['_id'],
                wallet_id=transaction_data['wallet_id'],
                amount=transaction_data['amount'],
                transaction_type=transaction_data['transaction_type'],
                status=transaction_data.get('status', 'pending'),
                description=transaction_data.get('description'),
                gateway_transaction_id=transaction_data.get('gateway_transaction_id'),
                created_at=transaction_data.get('created_at')
            )
        return None

    @staticmethod
    def find_by_wallet_id(wallet_id):
        transactions_data = transactions_collection.find({'wallet_id': wallet_id})
        return [Transaction(
            _id=data['_id'],
            wallet_id=data['wallet_id'],
            amount=data['amount'],
            transaction_type=data['transaction_type'],
            status=data.get('status', 'pending'),
            description=data.get('description'),
            gateway_transaction_id=data.get('gateway_transaction_id'),
            created_at=data.get('created_at')
        ) for data in transactions_data]

    def to_dict(self):
        return {
            'id': str(self._id),
            'wallet_id': self.wallet_id,
            'amount': float(self.amount), # Convert Decimal to float for JSON serialization
            'transaction_type': self.transaction_type,
            'status': self.status,
            'description': self.description,
            'gateway_transaction_id': self.gateway_transaction_id,
            'created_at': self.created_at.isoformat() if self.created_at else None
        }

    def __repr__(self):
        return f'<Transaction ID: {self._id} Type: {self.transaction_type}>'
