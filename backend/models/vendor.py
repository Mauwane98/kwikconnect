"""
Vendor Model

This file defines the Vendor model, representing a vendor or business on the platform.
It includes details about the vendor's business, location, and relationship to a user account.
"""

from backend import db
from .base_model import BaseModel # Import BaseModel

class Vendor(db.Model, BaseModel): # Inherit from BaseModel
    """
    Vendor model for storing business-specific data.
    """
    __tablename__ = 'vendors'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), unique=True, nullable=False)
    business_name = db.Column(db.String(120), nullable=False)
    description = db.Column(db.Text)
    address = db.Column(db.String(255))
    latitude = db.Column(db.Float)
    longitude = db.Column(db.Float)
    is_approved = db.Column(db.Boolean, default=False) # New field
    is_open = db.Column(db.Boolean, default=True) # New field
    profile_image_url = db.Column(db.String(255), nullable=True) # New field
    operating_hours = db.Column(db.String(255)) # e.g., "Mon-Fri 9:00-17:00"

    # Relationships
    user = db.relationship('User', back_populates='vendor', uselist=False)
    products = db.relationship('Product', back_populates='vendor', lazy=True, cascade="all, delete-orphan")
    orders = db.relationship('Order', back_populates='vendor', lazy='dynamic')

    def to_dict(self):
        """
        Serializes the Vendor object to a dictionary.
        """
        return {
            'id': self.id,
            'user_id': self.user_id,
            'business_name': self.business_name,
            'description': self.description,
            'address': self.address,
            'latitude': self.latitude,
            'longitude': self.longitude,
            'is_approved': self.is_approved,
            'is_open': self.is_open,
            'profile_image_url': self.profile_image_url,
            'operating_hours': self.operating_hours,
            'user_info': self.user.to_dict() if self.user else None
        }

    def __repr__(self):
        return f'<Vendor {self.business_name}>'
