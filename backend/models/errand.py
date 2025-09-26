# backend/models/errand.py

from datetime import datetime
from bson.objectid import ObjectId
from .base_model import BaseModel
from .enums import ErrandStatus

class Errand(BaseModel):
    """Errand model for storing errand information."""
    collection_name = 'errands'
    
    @classmethod
    def create_errand(cls, customer_id, description, pickup_address, dropoff_address, estimated_fee, **kwargs):
        """Create a new errand."""
        data = {
            'customer_id': customer_id,
            'description': description,
            'pickup_address': pickup_address,
            'dropoff_address': dropoff_address,
            'estimated_fee': estimated_fee,
            'courier_id': kwargs.get('courier_id'),
            'status': kwargs.get('status', 'pending')
        }
        return cls.create(**data)
    
    @classmethod
    def find_by_customer_id(cls, customer_id):
        """Find all errands for a specific customer."""
        return cls.find({'customer_id': customer_id})
    
    @classmethod
    def find_by_courier_id(cls, courier_id):
        """Find all errands for a specific courier."""
        return cls.find({'courier_id': courier_id})
    
    @classmethod
    def update_status(cls, errand_id, status):
        """Update errand status."""
        if isinstance(errand_id, str):
            errand_id = ObjectId(errand_id)
        return cls.update(errand_id, {'status': status})
    
    @classmethod
    def assign_courier(cls, errand_id, courier_id):
        """Assign a courier to an errand."""
        if isinstance(errand_id, str):
            errand_id = ObjectId(errand_id)
        return cls.update(errand_id, {'courier_id': courier_id})
    
    @staticmethod
    def to_dict(errand_data):
        """Convert errand document to dictionary format."""
        if not errand_data:
            return None
            
        return {
            'id': str(errand_data['_id']),
            'customer_id': errand_data['customer_id'],
            'courier_id': errand_data.get('courier_id'),
            'description': errand_data['description'],
            'pickup_address': errand_data['pickup_address'],
            'dropoff_address': errand_data['dropoff_address'],
            'estimated_fee': float(errand_data['estimated_fee']),
            'status': errand_data['status'],
            'created_at': errand_data['created_at'].isoformat() if errand_data.get('created_at') else None,
            'updated_at': errand_data['updated_at'].isoformat() if errand_data.get('updated_at') else None
        }
