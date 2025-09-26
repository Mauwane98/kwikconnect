# backend/models/product.py

from bson.objectid import ObjectId
from .base_model import BaseModel

class Product(BaseModel):
    collection_name = 'products'
    
    @classmethod
    def create_product(cls, name, description, price, vendor_id):
        """Create a new product."""
        if isinstance(vendor_id, str):
            vendor_id = ObjectId(vendor_id)
        return cls.create(
            name=name,
            description=description,
            price=price,
            vendor_id=vendor_id
        )
    
    @classmethod
    def find_by_vendor(cls, vendor_id):
        """Find all products for a specific vendor."""
        if isinstance(vendor_id, str):
            vendor_id = ObjectId(vendor_id)
        return cls.find({'vendor_id': vendor_id})
    
    @staticmethod
    def to_dict(product_data):
        """Convert product document to dictionary format."""
        if not product_data:
            return None
        return {
            'id': str(product_data['_id']),
            'name': product_data['name'],
            'description': product_data['description'],
            'price': product_data['price'],
            'vendor_id': str(product_data['vendor_id'])
        }