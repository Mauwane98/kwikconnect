# backend/models/user.py

from .. import db
from werkzeug.security import generate_password_hash, check_password_hash
import enum
from datetime import datetime

class UserRole(enum.Enum):
    CUSTOMER = 'customer'
    VENDOR = 'vendor'
    COURIER = 'courier'
    ADMIN = 'admin'

class User(db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(256), nullable=False)
    first_name = db.Column(db.String(50), nullable=False)
    last_name = db.Column(db.String(50), nullable=False)
    phone_number = db.Column(db.String(20), unique=True, nullable=False)
    role = db.Column(db.Enum(UserRole), nullable=False, default=UserRole.CUSTOMER)
    is_active = db.Column(db.Boolean, default=True, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relationships
    wallet = db.relationship('Wallet', back_populates='user', uselist=False, cascade="all, delete-orphan")
    orders = db.relationship('Order', back_populates='customer', foreign_keys='Order.customer_id')
    errands = db.relationship('Errand', back_populates='customer')
    vendor_profile = db.relationship('Vendor', back_populates='user', uselist=False, cascade="all, delete-orphan")
    courier_profile = db.relationship('Courier', back_populates='user', uselist=False, cascade="all, delete-orphan")

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def __repr__(self):
        return f'<User {self.email} - {self.role.value}>'
