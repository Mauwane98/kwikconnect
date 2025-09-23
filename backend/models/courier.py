# backend/models/courier.py

from .. import db
import enum
from datetime import datetime

class CourierStatus(enum.Enum):
    OFFLINE = 'offline'
    AVAILABLE = 'available'
    ON_DELIVERY = 'on_delivery'

class Courier(db.Model):
    __tablename__ = 'couriers'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), unique=True, nullable=False)
    vehicle_type = db.Column(db.String(50), nullable=True) # e.g., 'motorcycle', 'bicycle'
    license_plate = db.Column(db.String(20), nullable=True)
    status = db.Column(db.Enum(CourierStatus), nullable=False, default=CourierStatus.OFFLINE)
    current_latitude = db.Column(db.Float, nullable=True)
    current_longitude = db.Column(db.Float, nullable=True)
    is_approved = db.Column(db.Boolean, default=False, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relationships
    user = db.relationship('User', back_populates='courier_profile')
    orders = db.relationship('Order', back_populates='courier', lazy=True)
    errands = db.relationship('Errand', back_populates='courier', lazy=True)

    def __repr__(self):
        return f'<Courier User ID: {self.user_id}>'
