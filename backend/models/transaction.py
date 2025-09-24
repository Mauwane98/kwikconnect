# backend/models/transaction.py

from .. import db
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

class Transaction(db.Model, BaseModel): # Inherit from BaseModel
    __tablename__ = 'transactions'

    id = db.Column(db.Integer, primary_key=True)
    wallet_id = db.Column(db.Integer, db.ForeignKey('wallets.id'), nullable=False)
    amount = db.Column(db.Numeric(10, 2), nullable=False)
    transaction_type = db.Column(db.Enum(TransactionType), nullable=False)
    status = db.Column(db.Enum(TransactionStatus), nullable=False, default=TransactionStatus.PENDING)
    description = db.Column(db.String(255), nullable=True)
    gateway_transaction_id = db.Column(db.String(255), nullable=True, unique=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    # Relationships
    wallet = db.relationship('Wallet', back_populates='transactions')

    def __repr__(self):
        return f'<Transaction ID: {self.id} Type: {self.transaction_type.value}>'

    def to_dict(self):
        return {
            'id': self.id,
            'wallet_id': self.wallet_id,
            'amount': str(self.amount),
            'transaction_type': self.transaction_type.value,
            'status': self.status.value,
            'description': self.description,
            'gateway_transaction_id': self.gateway_transaction_id,
            'created_at': self.created_at.isoformat() if self.created_at else None
        }
