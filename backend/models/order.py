# backend/models/order.py

from .. import db
import enum
from datetime import datetime

class OrderStatus(enum.Enum):
    PENDING = 'pending'
    ACCEPTED_BY_VENDOR = 'accepted_by_vendor'
    READY_FOR_PICKUP = 'ready_for_pickup'
    PICKED_UP = 'picked_up'
    OUT_FOR_DELIVERY = 'out_for_delivery'
    DELIVERED = 'delivered'
    CANCELLED = 'cancelled'

class Order(db.Model):
    __tablename__ = 'orders'

    id = db.Column(db.Integer, primary_key=True)
    customer_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    vendor_id = db.Column(db.Integer, db.ForeignKey('vendors.id'), nullable=False)
    courier_id = db.Column(db.Integer, db.ForeignKey('couriers.id'), nullable=True)
    
    total_amount = db.Column(db.Numeric(10, 2), nullable=False)
    delivery_address = db.Column(db.String(255), nullable=False)
    delivery_latitude = db.Column(db.Float, nullable=True)
    delivery_longitude = db.Column(db.Float, nullable=True)
    status = db.Column(db.Enum(OrderStatus), nullable=False, default=OrderStatus.PENDING)
    
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relationships
    customer = db.relationship('User', back_populates='orders', foreign_keys=[customer_id])
    vendor = db.relationship('Vendor', back_populates='orders')
    courier = db.relationship('Courier', back_populates='orders')
    items = db.relationship('OrderItem', back_populates='order', cascade="all, delete-orphan")

    def __repr__(self):
        return f'<Order ID: {self.id} - Status: {self.status.value}>'
