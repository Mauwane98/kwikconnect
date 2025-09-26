# backend/models/__init__.py

"""
Models package initialization.
Load only the base model and enums at the module level.
Other models will be loaded lazily by the app context.
"""

from .base_model import BaseModel

# Import enums directly as they don't need app context
from .enums import (
    CourierStatus,
    OrderStatus,
    ErrandStatus,
    TransactionType,
    TransactionStatus,
    VehicleType
)

# Export enums and BaseModel for immediate use
__all__ = [
    'BaseModel',
    'CourierStatus',
    'OrderStatus',
    'ErrandStatus',
    'TransactionType',
    'TransactionStatus',
    'VehicleType'
]

def init_models():
    """Initialize all models after app context is created."""
    
    # Import models here to avoid circular dependencies
    from .token_blocklist import TokenBlocklist
    from .user import User
    from .vendor import Vendor
    from .product import Product
    from .courier import Courier
    from .order import Order
    from .order_item import OrderItem
    from .errand import Errand
    from .wallet import Wallet
    from .transaction import Transaction
    
    # Return initialized models
    return {
        'BaseModel': BaseModel,
        'User': User,
        'Vendor': Vendor,
        'Product': Product,
        'Courier': Courier,
        'CourierStatus': CourierStatus,
        'Order': Order,
        'OrderStatus': OrderStatus,
        'OrderItem': OrderItem,
        'Errand': Errand,
        'ErrandStatus': ErrandStatus,
        'Wallet': Wallet,
        'Transaction': Transaction,
        'TransactionType': TransactionType,
        'TransactionStatus': TransactionStatus,
        'TokenBlocklist': TokenBlocklist,
        'VehicleType': VehicleType
    }
