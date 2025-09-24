
from backend import db
from backend.models import Order, OrderItem, Product, Vendor, User, UserRole, OrderStatus
from backend.errors import NotFoundError, ForbiddenError, BadRequestError, ConflictError
from decimal import Decimal

class OrderService:
    @staticmethod
    def create_order(customer_id, data):
        user = User.find_by_id(customer_id)
        if not user or user.role != UserRole.CUSTOMER:
            raise ForbiddenError("Only customers can create orders.")

        vendor_id = data.get('vendor_id')
        delivery_address = data.get('delivery_address')
        items_data = data.get('items')

        vendor = Vendor.query.get(vendor_id)
        if not vendor or not vendor.is_approved or not vendor.is_open:
            raise NotFoundError("Vendor is not available or does not exist.")

        total_amount = Decimal('0.00')
        order_items_to_create = []

        for item_data in items_data:
            product = Product.query.get(item_data.get('product_id'))
            quantity = item_data.get('quantity', 0)

            if not product or product.vendor_id != vendor.id or not product.is_available:
                raise BadRequestError(f"Product with ID {item_data.get('product_id')} is invalid or unavailable.")
            
            if quantity <= 0:
                raise BadRequestError(f"Invalid quantity for product ID {product.id}.")

            price_at_purchase = product.price
            total_amount += price_at_purchase * quantity
            
            order_items_to_create.append(OrderItem(
                product_id=product.id,
                quantity=quantity,
                price_at_purchase=price_at_purchase
            ))

        if not order_items_to_create:
            raise BadRequestError("Order must contain at least one item.")

        new_order = Order(
            customer_id=customer_id,
            vendor_id=vendor_id,
            delivery_address=delivery_address,
            total_amount=total_amount
        )
        
        new_order.items.extend(order_items_to_create)
        
        db.session.add(new_order)
        db.session.commit()
        
        return new_order

    @staticmethod
    def get_order_details(user_id, order_id):
        order = Order.query.get(order_id)
        if not order:
            raise NotFoundError("Order not found.")
        
        user = User.find_by_id(user_id)

        # Authorization check
        if order.customer_id != user_id and user.role != UserRole.ADMIN and \
           not (user.role == UserRole.VENDOR and order.vendor_id == user.vendor.id) and \
           not (user.role == UserRole.COURIER and order.courier_id == user.courier.id):
            raise ForbiddenError("You are not authorized to view this order.")

        return order
