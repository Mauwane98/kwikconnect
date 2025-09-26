# backend/models/enums.py

"""Collection of enums used across the application."""

import enum

class CourierStatus(enum.Enum):
    """Enumeration for courier statuses."""
    OFFLINE = 'offline'
    AVAILABLE = 'available'
    BUSY = 'busy'
    ON_BREAK = 'on_break'
    MAINTENANCE = 'maintenance'  # For vehicle maintenance/repairs

class OrderStatus(enum.Enum):
    """Enumeration for order statuses."""
    PENDING = 'pending'
    ACCEPTED_BY_VENDOR = 'accepted_by_vendor'
    READY_FOR_PICKUP = 'ready_for_pickup'
    PICKED_UP = 'picked_up'
    OUT_FOR_DELIVERY = 'out_for_delivery'
    DELIVERED = 'delivered'
    CANCELLED = 'cancelled'

class ErrandStatus(enum.Enum):
    """Enumeration for errand statuses."""
    PENDING = 'pending'
    ACCEPTED = 'accepted'
    IN_PROGRESS = 'in_progress'
    COMPLETED = 'completed'
    CANCELLED = 'cancelled'

class TransactionType(enum.Enum):
    """Enumeration for transaction types."""
    DEPOSIT = 'deposit'
    WITHDRAWAL = 'withdrawal'
    PAYMENT = 'payment'
    REFUND = 'refund'
    FEE = 'fee'

class TransactionStatus(enum.Enum):
    """Enumeration for transaction statuses."""
    PENDING = 'pending'
    COMPLETED = 'completed'
    FAILED = 'failed'
    CANCELLED = 'cancelled'

class VehicleType(enum.Enum):
    """Enumeration for vehicle types."""
    BICYCLE = 'bicycle'
    MOTORCYCLE = 'motorcycle'
    CAR = 'car'
    VAN = 'van'
    TRUCK = 'truck'