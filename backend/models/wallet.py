# backend/models/wallet.py

from .. import db
from datetime import datetime
from decimal import Decimal
from .base_model import BaseModel # Import BaseModel

class Wallet(db.Model, BaseModel): # Inherit from BaseModel
    __tablename__ = 'wallets'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), unique=True, nullable=False)
    balance = db.Column(db.Numeric(10, 2), nullable=False, default=Decimal('0.00'))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relationships
    user = db.relationship('User', back_populates='wallet')
    transactions = db.relationship('Transaction', back_populates='wallet', lazy='dynamic')

    def __repr__(self):
        return f'<Wallet UserID: {self.user_id} Balance: {self.balance}>'

    def to_dict(self):
        return {
            'id': self.id,
            'user_id': self.user_id,
            'balance': str(self.balance),
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None
        }
