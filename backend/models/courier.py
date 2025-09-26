"""
Courier Model

This file defines the Courier model, representing a delivery person on the platform.
It includes information about the courier's status, vehicle, and location.
"""

from bson.objectid import ObjectId
from datetime import datetime
from .base_model import BaseModel
from .vehicle_types import VEHICLE_CONFIGS
from .enums import CourierStatus, VehicleType

class Courier(BaseModel):
    """Courier model for storing courier-specific data."""
    collection_name = 'couriers'
    
    @classmethod
    def create_courier(cls, user_id, vehicle_type, **kwargs):
        """Create a new courier."""
        data = {
            'user_id': user_id,
            'vehicle_type': vehicle_type,
            'status': kwargs.get('status', 'offline'),
            'license_plate': kwargs.get('license_plate'),
            'latitude': kwargs.get('latitude'),
            'longitude': kwargs.get('longitude'),
            'active_area': kwargs.get('active_area'),
            'availability_hours': kwargs.get('availability_hours'),
            'rating': kwargs.get('rating', 5.0),
            'total_deliveries': kwargs.get('total_deliveries', 0),
            'total_distance': kwargs.get('total_distance', 0.0),
            'current_load': kwargs.get('current_load', 0.0),
            'vehicle_docs': kwargs.get('vehicle_docs'),
            'insurance_info': kwargs.get('insurance_info'),
            'delivery_preferences': kwargs.get('delivery_preferences'),
            'is_verified': kwargs.get('is_verified', False),
            'last_maintenance': kwargs.get('last_maintenance')
        }
        return cls.create(**data)
    
    @classmethod
    def find_by_user_id(cls, user_id):
        """Find a courier by user ID."""
        return cls.find_one({'user_id': user_id})
    
    @classmethod
    def update_status(cls, courier_id, status):
        """Update courier status."""
        if isinstance(courier_id, str):
            courier_id = ObjectId(courier_id)
        return cls.update(courier_id, {'status': status})
    
    @classmethod
    def update_location(cls, courier_id, latitude, longitude):
        """Update courier location."""
        if isinstance(courier_id, str):
            courier_id = ObjectId(courier_id)
        return cls.update(courier_id, {
            'latitude': latitude,
            'longitude': longitude
        })
    
    @staticmethod
    def to_dict(courier_data):
        """Convert courier document to dictionary format."""
        if not courier_data:
            return None
            
        vehicle_config = VEHICLE_CONFIGS.get(courier_data.get('vehicle_type'))
        
        return {
            'id': str(courier_data['_id']),
            'user_id': courier_data['user_id'],
            'status': courier_data['status'],
            'vehicle_type': courier_data['vehicle_type'],
            'vehicle_info': vehicle_config,
            'license_plate': courier_data.get('license_plate'),
            'latitude': courier_data.get('latitude'),
            'longitude': courier_data.get('longitude'),
            'active_area': courier_data.get('active_area'),
            'availability_hours': courier_data.get('availability_hours'),
            'rating': courier_data.get('rating', 5.0),
            'total_deliveries': courier_data.get('total_deliveries', 0),
            'total_distance': courier_data.get('total_distance', 0.0),
            'current_load': courier_data.get('current_load', 0.0),
            'is_verified': courier_data.get('is_verified', False),
            'last_maintenance': courier_data['last_maintenance'].isoformat() if courier_data.get('last_maintenance') else None
        }
