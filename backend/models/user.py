# backend/models/user.py

from werkzeug.security import generate_password_hash, check_password_hash
from bson.objectid import ObjectId
from .base_model import BaseModel

class User(BaseModel):
    collection_name = 'users'
    
    @classmethod
    def create_user(cls, email, password, full_name, role='customer'):
        """Create a new user with hashed password."""
        return cls.create(
            email=email,
            password_hash=generate_password_hash(password),
            full_name=full_name,
            role=role
        )
    
    @classmethod
    def find_by_email(cls, email):
        """Find a user by email address."""
        return cls.find_one({'email': email})
    
    @classmethod
    def find_by_id(cls, user_id):
        """Find a user by ID."""
        if isinstance(user_id, str):
            user_id = ObjectId(user_id)
        return cls.find_one({'_id': user_id})
    
    @staticmethod
    def check_password(password_hash, password):
        """Check if the password matches the hash."""
        return check_password_hash(password_hash, password)
    
    @staticmethod
    def to_dict(user_data):
        """Convert user document to dictionary format."""
        if not user_data:
            return None
        return {
            'id': str(user_data['_id']),
            'email': user_data['email'],
            'full_name': user_data['full_name'],
            'role': user_data['role']
        }