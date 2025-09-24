# backend/models/product.py

from .. import db
from datetime import datetime
from .base_model import BaseModel # Import BaseModel

class Product(db.Model, BaseModel): # Inherit from BaseModel
    __tablename__ = 'products'

    id = db.Column(db.Integer, primary_key=True)
    vendor_id = db.Column(db.Integer, db.ForeignKey('vendors.id'), nullable=False)
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text, nullable=True)
    price = db.Column(db.Numeric(10, 2), nullable=False)
    image_url = db.Column(db.String(255), nullable=True)
    is_available = db.Column(db.Boolean, default=True, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relationships
    vendor = db.relationship('Vendor', back_populates='products')
    order_items = db.relationship('OrderItem', back_populates='product', lazy='dynamic')

    def __repr__(self):
        return f'<Product {self.name}>'
