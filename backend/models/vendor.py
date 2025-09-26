# backend/models/vendor.py

from bson.objectid import ObjectId
from .base_model import BaseModel

class Vendor(BaseModel):
    collection_name = 'vendors'
    
    @classmethod
    def create_vendor(cls, name, description, whatsapp_number):
        """Create a new vendor."""
        return cls.create(
            name=name,
            description=description,
            whatsapp_number=whatsapp_number
        )
    
    @classmethod
    def find_all(cls):
        """Get all vendors."""
        return cls.find()
    
    @classmethod
    def find_by_user_id(cls, user_id):
        """Find a vendor by user ID."""
        return cls.find_one({'user_id': user_id})
    
    @staticmethod
    def to_dict(vendor_data):
        """Convert vendor document to dictionary format."""
        if not vendor_data:
            return None
        return {
            'id': str(vendor_data['_id']),
            'name': vendor_data['name'],
            'description': vendor_data['description'],
            'whatsapp_number': vendor_data['whatsapp_number']
        }