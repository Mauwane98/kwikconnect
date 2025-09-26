# backend/models/order_item.py

from bson.objectid import ObjectId
from .base_model import BaseModel

class OrderItem(BaseModel):
    """Order Item model for storing order line items."""
    collection_name = 'order_items'
    
    @classmethod
    def create_order_item(cls, order_id, product_id, quantity, price_at_purchase):
        """Create a new order item."""
        data = {
            'order_id': order_id,
            'product_id': product_id,
            'quantity': quantity,
            'price_at_purchase': price_at_purchase
        }
        return cls.create(**data)
    
    @classmethod
    def find_by_order_id(cls, order_id):
        """Find all items for a specific order."""
        return cls.find({'order_id': order_id})
    
    @classmethod
    def find_by_product_id(cls, product_id):
        """Find all order items containing a specific product."""
        return cls.find({'product_id': product_id})
    
    @classmethod
    def update_quantity(cls, order_item_id, quantity):
        """Update order item quantity."""
        if isinstance(order_item_id, str):
            order_item_id = ObjectId(order_item_id)
        return cls.update(order_item_id, {'quantity': quantity})
    
    @staticmethod
    def to_dict(item_data):
        """Convert order item document to dictionary format."""
        if not item_data:
            return None
            
        return {
            'id': str(item_data['_id']),
            'order_id': item_data['order_id'],
            'product_id': item_data['product_id'],
            'quantity': item_data['quantity'],
            'price_at_purchase': float(item_data['price_at_purchase'])
        }
