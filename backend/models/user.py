"""
User Model

This file defines the User model, representing a user in the Kwik Connect platform.
It includes fields for user authentication, personal information, and role management.
"""

from backend import db
from werkzeug.security import generate_password_hash, check_password_hash
import enum
import datetime
from .base_model import BaseModel # Import BaseModel

class UserRole(enum.Enum):
    """Enumeration for user roles."""
    CUSTOMER = 'customer'
    VENDOR = 'vendor'
    COURIER = 'courier'
    ADMIN = 'admin'

class User(db.Model, BaseModel): # Inherit from BaseModel
    """
    User model for storing user data and handling authentication.
    """
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(256), nullable=False)
    first_name = db.Column(db.String(50))
    last_name = db.Column(db.String(50))
    phone_number = db.Column(db.String(20))
    role = db.Column(db.Enum(UserRole), nullable=False, default=UserRole.CUSTOMER)
    created_at = db.Column(db.DateTime, default=db.func.current_timestamp())
    updated_at = db.Column(db.DateTime, default=db.func.current_timestamp(), onupdate=db.func.current_timestamp())
    last_login = db.Column(db.DateTime)
    profile_picture_url = db.Column(db.String(255))
    email_verified = db.Column(db.Boolean, default=False)
    deleted_at = db.Column(db.DateTime, nullable=True)
    reset_password_token = db.Column(db.String(128))
    reset_password_expiration = db.Column(db.DateTime)

    # Relationships
    wallet = db.relationship('Wallet', back_populates='user', uselist=False, cascade="all, delete-orphan")
    orders = db.relationship('Order', back_populates='customer', foreign_keys='Order.customer_id', lazy='dynamic')
    errands = db.relationship('Errand', back_populates='customer', foreign_keys='Errand.customer_id', lazy='dynamic')
    vendor = db.relationship('Vendor', back_populates='user', uselist=False)
    courier = db.relationship('Courier', back_populates='user', uselist=False)

    def set_password(self, password):
        """
        Hashes the user's password and stores it.

        Args:
            password (str): The plaintext password to hash.
        """
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        """
        Verifies the user's password against the stored hash.

        Args:
            password (str): The plaintext password to check.

        Returns:
            bool: True if the password is correct, False otherwise.
        """
        return check_password_hash(self.password_hash, password)

    def to_dict(self, include_sensitive=False):
        """
        Serializes the User object to a dictionary.
        """
        data = {
            'id': self.id,
            'username': self.username,
            'email': self.email,
            'first_name': self.first_name,
            'last_name': self.last_name,
            'phone_number': self.phone_number,
            'role': self.role.value,
            'created_at': self.created_at.isoformat(),
            'profile_picture_url': self.profile_picture_url,
            'last_login': self.last_login.isoformat() if self.last_login else None,
        }
        if include_sensitive:
            data['email_verified'] = self.email_verified
        return data

    def __repr__(self):
        return f'<User {self.username} - {self.role}>'

    @classmethod
    def find_by_email(cls, email):
        return cls.query.filter_by(email=email, deleted_at=None).first()

    @classmethod
    def find_by_id(cls, id):
        return cls.query.filter_by(id=id, deleted_at=None).first()

    def soft_delete(self):
        """Marks a user as deleted."""
        self.deleted_at = datetime.datetime.utcnow()
        self.save_to_db()
