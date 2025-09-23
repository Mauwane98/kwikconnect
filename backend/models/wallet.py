# backend/models/wallet.py

from .. import db
from datetime import datetime
from decimal import Decimal

class Wallet(db.Model):
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
