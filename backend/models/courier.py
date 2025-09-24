"""
Courier Model

This file defines the Courier model, representing a delivery person on the platform.
It includes information about the courier's status, vehicle, and location.
"""

from backend import db
import enum
from .base_model import BaseModel # Import BaseModel

class CourierStatus(enum.Enum):
    """
    Enumeration for courier statuses.
    """
    OFFLINE = 'offline'
    AVAILABLE = 'available'
    BUSY = 'busy'

class VehicleType(enum.Enum):
    """
    Enumeration for vehicle types.
    """
    BICYCLE = 'bicycle'
    MOTORCYCLE = 'motorcycle'
    CAR = 'car'

class Courier(db.Model, BaseModel): # Inherit from BaseModel
    """
    Courier model for storing courier-specific data.
    """
    __tablename__ = 'couriers'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), unique=True, nullable=False)
    status = db.Column(db.Enum(CourierStatus), default=CourierStatus.OFFLINE)
    vehicle_type = db.Column(db.Enum(VehicleType))
    license_plate = db.Column(db.String(20))
    latitude = db.Column(db.Float)
    longitude = db.Column(db.Float)

    # Relationships
    user = db.relationship('User', back_populates='courier', uselist=False)
    errands = db.relationship('Errand', back_populates='courier', lazy='dynamic')
    orders = db.relationship('Order', back_populates='courier', lazy='dynamic')

    def to_dict(self):
        """
        Serializes the Courier object to a dictionary.
        """
        return {
            'id': self.id,
            'user_id': self.user_id,
            'status': self.status.value,
            'vehicle_type': self.vehicle_type.value if self.vehicle_type else None,
            'license_plate': self.license_plate,
            'latitude': self.latitude,
            'longitude': self.longitude,
            'user_info': self.user.to_dict() if self.user else None
        }

    def __repr__(self):
        return f'<Courier {self.user.username}>'
