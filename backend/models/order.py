# backend/models/order.py

from datetime import datetime
from bson.objectid import ObjectId
from .base_model import BaseModel
from .enums import OrderStatus

class Order(BaseModel):
    """Order model for storing order information."""
    collection_name = 'orders'
    
    @classmethod
    def create_order(cls, customer_id, vendor_id, total_amount, delivery_address, **kwargs):
        """Create a new order."""
        data = {
            'customer_id': customer_id,
            'vendor_id': vendor_id,
            'total_amount': total_amount,
            'delivery_address': delivery_address,
            'courier_id': kwargs.get('courier_id'),
            'delivery_latitude': kwargs.get('delivery_latitude'),
            'delivery_longitude': kwargs.get('delivery_longitude'),
            'status': kwargs.get('status', 'pending')
        }
        return cls.create(**data)
    
    @classmethod
    def find_by_customer_id(cls, customer_id):
        """Find all orders for a specific customer."""
        return cls.find({'customer_id': customer_id})
    
    @classmethod
    def find_by_vendor_id(cls, vendor_id):
        """Find all orders for a specific vendor."""
        return cls.find({'vendor_id': vendor_id})
    
    @classmethod
    def find_by_courier_id(cls, courier_id):
        """Find all orders for a specific courier."""
        return cls.find({'courier_id': courier_id})
    
    @classmethod
    def update_status(cls, order_id, status):
        """Update order status."""
        if isinstance(order_id, str):
            order_id = ObjectId(order_id)
        return cls.update(order_id, {'status': status})
    
    @classmethod
    def assign_courier(cls, order_id, courier_id):
        """Assign a courier to an order."""
        if isinstance(order_id, str):
            order_id = ObjectId(order_id)
        return cls.update(order_id, {'courier_id': courier_id})
    
    @staticmethod
    def to_dict(order_data):
        """Convert order document to dictionary format."""
        if not order_data:
            return None
            
        return {
            'id': str(order_data['_id']),
            'customer_id': order_data['customer_id'],
            'vendor_id': order_data['vendor_id'],
            'courier_id': order_data.get('courier_id'),
            'total_amount': float(order_data['total_amount']),
            'delivery_address': order_data['delivery_address'],
            'delivery_latitude': order_data.get('delivery_latitude'),
            'delivery_longitude': order_data.get('delivery_longitude'),
            'status': order_data['status'],
            'created_at': order_data['created_at'].isoformat() if order_data.get('created_at') else None,
            'updated_at': order_data['updated_at'].isoformat() if order_data.get('updated_at') else None
        }
