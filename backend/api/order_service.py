

from backend.models.order import Order, OrderStatus
from backend.models.order_item import OrderItem
from backend.models.product import Product
from backend.models.vendor import Vendor
from backend.models.user import User
from backend.errors import NotFoundError, ForbiddenError, BadRequestError, ConflictError
from decimal import Decimal

class OrderService:
    @staticmethod
    def create_order(customer_id, data):
        user = User.find_by_id(customer_id)
        if not user or user.role != 'customer':
            raise ForbiddenError("Only customers can create orders.")

        vendor_id = data.get('vendor_id')
        delivery_address = data.get('delivery_address')
        items_data = data.get('items')

        vendor = Vendor.find_by_id(vendor_id)
        if not vendor: # Assuming is_approved and is_open are properties of the Vendor object
            raise NotFoundError("Vendor is not available or does not exist.")
        # Add checks for is_approved and is_open if they exist in the MongoDB Vendor model
        # if not vendor.is_approved or not vendor.is_open:
        #     raise NotFoundError("Vendor is not available or does not exist.")


        total_amount = Decimal('0.00')
        order_item_ids = [] # Store ObjectIds of created order items

        for item_data in items_data:
            product = Product.find_by_id(item_data.get('product_id'))
            quantity = item_data.get('quantity', 0)

            if not product or product.vendor_id != str(vendor._id): # Compare with string representation of vendor._id
                raise BadRequestError(f"Product with ID {item_data.get('product_id')} is invalid or unavailable.")
            # Add check for product.is_available if it exists in the MongoDB Product model
            # if not product.is_available:
            #     raise BadRequestError(f"Product with ID {item_data.get('product_id')} is invalid or unavailable.")

            if quantity <= 0:
                raise BadRequestError(f"Invalid quantity for product ID {str(product._id)}.")

            price_at_purchase = product.price
            total_amount += price_at_purchase * quantity

            new_order_item = OrderItem(
                order_id=None, # Will be updated after order is saved
                product_id=str(product._id),
                quantity=quantity,
                price_at_purchase=price_at_purchase
            )
            new_order_item.save() # Save order item first
            order_item_ids.append(str(new_order_item._id)) # Store its ObjectId

        if not order_item_ids:
            raise BadRequestError("Order must contain at least one item.")

        new_order = Order(
            customer_id=str(user._id),
            vendor_id=str(vendor._id),
            delivery_address=delivery_address,
            total_amount=total_amount,
            # Add order_item_ids to the order
            items=order_item_ids
        )

        new_order.save() # Save the order

        # Update order_id in each order item
        for item_id in order_item_ids:
            order_item = OrderItem.find_by_id(item_id)
            if order_item:
                order_item.order_id = str(new_order._id)
                order_item.save()

        return new_order

    @staticmethod
    def get_order_details(user_id, order_id):
        order = Order.find_by_id(order_id)
        if not order:
            raise NotFoundError("Order not found.")
        
        user = User.find_by_id(user_id)

        # Authorization check
        # Assuming user.vendor_id and user.courier_id are stored in the User model if applicable
        if order.customer_id != str(user._id) and user.role != 'admin' and \
           not (user.role == 'vendor' and order.vendor_id == str(user._id)) and \
           not (user.role == 'courier' and order.courier_id == str(user._id)):
            raise ForbiddenError("You are not authorized to view this order.")

        return order
