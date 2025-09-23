# backend/models/errand.py

from .. import db
import enum
from datetime import datetime

class ErrandStatus(enum.Enum):
    PENDING = 'pending'
    ACCEPTED = 'accepted'
    IN_PROGRESS = 'in_progress'
    COMPLETED = 'completed'
    CANCELLED = 'cancelled'

class Errand(db.Model):
    __tablename__ = 'errands'

    id = db.Column(db.Integer, primary_key=True)
    customer_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    courier_id = db.Column(db.Integer, db.ForeignKey('couriers.id'), nullable=True)
    
    description = db.Column(db.Text, nullable=False)
    pickup_address = db.Column(db.String(255), nullable=False)
    dropoff_address = db.Column(db.String(255), nullable=False)
    estimated_fee = db.Column(db.Numeric(10, 2), nullable=False)
    status = db.Column(db.Enum(ErrandStatus), nullable=False, default=ErrandStatus.PENDING)
    
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relationships
    customer = db.relationship('User', back_populates='errands')
    courier = db.relationship('Courier', back_populates='errands')

    def __repr__(self):
        return f'<Errand ID: {self.id} - Status: {self.status.value}>'
