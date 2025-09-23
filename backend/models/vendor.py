# backend/models/vendor.py

from .. import db
from datetime import datetime

class Vendor(db.Model):
    __tablename__ = 'vendors'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), unique=True, nullable=False)
    store_name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text, nullable=True)
    address = db.Column(db.String(255), nullable=False)
    latitude = db.Column(db.Float, nullable=True)
    longitude = db.Column(db.Float, nullable=True)
    is_approved = db.Column(db.Boolean, default=False, nullable=False)
    is_open = db.Column(db.Boolean, default=True, nullable=False)
    profile_image_url = db.Column(db.String(255), nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relationships
    user = db.relationship('User', back_populates='vendor_profile')
    products = db.relationship('Product', back_populates='vendor', lazy=True, cascade="all, delete-orphan")
    orders = db.relationship('Order', back_populates='vendor', lazy=True)

    def __repr__(self):
        return f'<Vendor {self.store_name}>'
