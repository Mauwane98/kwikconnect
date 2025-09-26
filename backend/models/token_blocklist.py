"""
Token Blocklist Model

This file defines the TokenBlocklist model, which is used to store revoked JWTs.
"""

from datetime import datetime
from bson.objectid import ObjectId
from .base_model import BaseModel

class TokenBlocklist(BaseModel):
    """TokenBlocklist model for storing revoked JWTs."""
    
    collection_name = 'token_blocklist'
    
    @classmethod
    def create_blocklist_entry(cls, jti):
        """Create a new token blocklist entry."""
        return cls.create(
            jti=jti,
            created_at=datetime.utcnow()
        )
    
    @classmethod
    def find_by_jti(cls, jti):
        """Find a token by JTI."""
        return cls.find_one({'jti': jti})
    
    @staticmethod
    def to_dict(token_data):
        """Convert token document to dictionary format."""
        if not token_data:
            return None
        return {
            'id': str(token_data['_id']),
            'jti': token_data['jti'],
            'created_at': token_data['created_at'].isoformat() if token_data.get('created_at') else None
        }
