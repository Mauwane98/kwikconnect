

from backend.models.order import Order, OrderStatus
from backend.models.courier import Courier, CourierStatus
from backend.models.user import User
from backend.errors import NotFoundError, ConflictError, ForbiddenError, BadRequestError

class CourierService:
    @staticmethod
    def get_available_jobs():
        available_orders_data = Order.orders_collection.find({
            'status': OrderStatus.READY_FOR_PICKUP.value,
            'courier_id': None
        }).sort('created_at', -1) # -1 for descending order
        available_orders = [Order(
            _id=order_data['_id'],
            customer_id=order_data['customer_id'],
            vendor_id=order_data['vendor_id'],
            courier_id=order_data.get('courier_id'),
            total_amount=order_data['total_amount'],
            delivery_address=order_data['delivery_address'],
            delivery_latitude=order_data.get('delivery_latitude'),
            delivery_longitude=order_data.get('delivery_longitude'),
            status=order_data.get('status', 'pending'),
            created_at=order_data.get('created_at'),
            updated_at=order_data.get('updated_at')
        ) for order_data in available_orders_data]
        return available_orders

    @staticmethod
    def accept_job(user_id, order_id):
        courier = Courier.find_by_user_id(user_id)
        if not courier:
            raise ForbiddenError("Courier profile not found.")

        if courier.status != CourierStatus.AVAILABLE.value: # Compare with value
            raise ConflictError(f"Cannot accept job, your status is '{courier.status}'.")

        order = Order.find_by_id(order_id)

        if not order or order.status != OrderStatus.READY_FOR_PICKUP.value or order.courier_id is not None: # Compare with value
            raise ConflictError("Job is no longer available.")

        order.courier_id = str(courier._id) # Store courier's MongoDB _id
        order.status = OrderStatus.PICKED_UP.value # Store status value
        courier.status = CourierStatus.BUSY.value # Store status value

        order.save()
        courier.save()
        return order

    @staticmethod
    def update_job_status(user_id, order_id, new_status_str):
        courier = Courier.find_by_user_id(user_id)
        if not courier:
            raise ForbiddenError("Courier profile not found.")

        order = Order.find_by_id(order_id)

        if not order:
            raise NotFoundError("Order not found.")
        if order.courier_id != str(courier._id): # Compare with string representation of ObjectId
            raise ForbiddenError("You are not assigned to this job.")

        try:
            new_status = OrderStatus(new_status_str)
        except ValueError:
            raise BadRequestError(f"'{new_status_str}' is not a valid order status.")

        valid_transitions = {
            OrderStatus.PICKED_UP.value: [OrderStatus.OUT_FOR_DELIVERY.value],
            OrderStatus.OUT_FOR_DELIVERY.value: [OrderStatus.DELIVERED.value]
        }

        if new_status.value not in valid_transitions.get(order.status, []):
            raise ConflictError(f"Invalid status transition from '{order.status}' to '{new_status.value}'.")

        order.status = new_status.value # Store status value

        if new_status == OrderStatus.DELIVERED:
            courier.status = CourierStatus.AVAILABLE.value # Store status value

        order.save()
        courier.save()
        return order
