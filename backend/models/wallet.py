# backend/models/wallet.py

from datetime import datetime
from decimal import Decimal
from bson.objectid import ObjectId
from .base_model import BaseModel

class Wallet(BaseModel):
    """Wallet model for storing user balances."""
    collection_name = 'wallets'
    
    @classmethod
    def create_wallet(cls, user_id, balance=Decimal('0.00')):
        """Create a new wallet."""
        data = {
            'user_id': user_id,
            'balance': str(balance)  # Convert Decimal to string for MongoDB
        }
        return cls.create(**data)
    
    @classmethod
    def find_by_user_id(cls, user_id):
        """Find a wallet by user ID."""
        return cls.find_one({'user_id': user_id})
    
    @classmethod
    def update_balance(cls, wallet_id, balance):
        """Update wallet balance."""
        if isinstance(wallet_id, str):
            wallet_id = ObjectId(wallet_id)
        return cls.update(wallet_id, {'balance': str(balance)})
    
    @classmethod
    def adjust_balance(cls, wallet_id, amount):
        """Adjust wallet balance by the given amount (positive or negative)."""
        wallet = cls.find_by_id(wallet_id)
        if not wallet:
            return None
            
        current_balance = Decimal(wallet['balance'])
        new_balance = current_balance + Decimal(str(amount))
        
        return cls.update_balance(wallet_id, new_balance)
    
    @staticmethod
    def to_dict(wallet_data):
        """Convert wallet document to dictionary format."""
        if not wallet_data:
            return None
            
        return {
            'id': str(wallet_data['_id']),
            'user_id': wallet_data['user_id'],
            'balance': str(wallet_data['balance']),
            'created_at': wallet_data['created_at'].isoformat() if wallet_data.get('created_at') else None,
            'updated_at': wallet_data['updated_at'].isoformat() if wallet_data.get('updated_at') else None
        }
