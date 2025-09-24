"""
Token Blocklist Model

This file defines the TokenBlocklist model, which is used to store revoked JWTs.
"""

from backend import db
from .base_model import BaseModel # Import BaseModel

class TokenBlocklist(db.Model, BaseModel): # Inherit from BaseModel
    """
    TokenBlocklist model for storing revoked JWTs.
    """
    __tablename__ = 'token_blocklist'

    id = db.Column(db.Integer, primary_key=True)
    jti = db.Column(db.String(36), nullable=False, unique=True)
    created_at = db.Column(db.DateTime, nullable=False, default=db.func.current_timestamp())

    def __repr__(self):
        return f'<TokenBlocklist {self.jti}>'

    # Removed save_to_db as it is inherited from BaseModel
