# backend/models/order_item.py

from .. import db
from .base_model import BaseModel # Import BaseModel

class OrderItem(db.Model, BaseModel): # Inherit from BaseModel
    __tablename__ = 'order_items'

    id = db.Column(db.Integer, primary_key=True)
    order_id = db.Column(db.Integer, db.ForeignKey('orders.id'), nullable=False)
    product_id = db.Column(db.Integer, db.ForeignKey('products.id'), nullable=False)
    quantity = db.Column(db.Integer, nullable=False)
    price_at_purchase = db.Column(db.Numeric(10, 2), nullable=False)

    # Relationships
    order = db.relationship('Order', back_populates='items')
    product = db.relationship('Product')

    def __repr__(self):
        return f'<OrderItem OrderID: {self.order_id} ProductID: {self.product_id}>'
