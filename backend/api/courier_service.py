
from backend import db
from backend.models import Order, Courier, User, OrderStatus, CourierStatus
from backend.errors import NotFoundError, ConflictError, ForbiddenError, BadRequestError

class CourierService:
    @staticmethod
    def get_available_jobs():
        available_orders = Order.query.filter_by(
            status=OrderStatus.READY_FOR_PICKUP,
            courier_id=None
        ).order_by(Order.created_at.desc()).all()
        return available_orders

    @staticmethod
    def accept_job(user_id, order_id):
        courier = Courier.query.filter_by(user_id=user_id).first()
        if not courier:
            raise ForbiddenError("Courier profile not found.")

        if courier.status != CourierStatus.AVAILABLE:
            raise ConflictError(f"Cannot accept job, your status is '{courier.status.value}'.")

        order = Order.query.get(order_id)

        if not order or order.status != OrderStatus.READY_FOR_PICKUP or order.courier_id is not None:
            raise ConflictError("Job is no longer available.")

        order.courier_id = courier.id
        order.status = OrderStatus.PICKED_UP
        courier.status = CourierStatus.BUSY
        
        db.session.commit()
        return order

    @staticmethod
    def update_job_status(user_id, order_id, new_status_str):
        courier = Courier.query.filter_by(user_id=user_id).first()
        if not courier:
            raise ForbiddenError("Courier profile not found.")

        order = Order.query.get(order_id)

        if not order:
            raise NotFoundError("Order not found.")
        if order.courier_id != courier.id:
            raise ForbiddenError("You are not assigned to this job.")

        try:
            new_status = OrderStatus(new_status_str)
        except ValueError:
            raise BadRequestError(f"'{new_status_str}' is not a valid order status.")

        valid_transitions = {
            OrderStatus.PICKED_UP: [OrderStatus.OUT_FOR_DELIVERY],
            OrderStatus.OUT_FOR_DELIVERY: [OrderStatus.DELIVERED]
        }

        if new_status not in valid_transitions.get(order.status, []):
            raise ConflictError(f"Invalid status transition from '{order.status.value}' to '{new_status.value}'.")

        order.status = new_status

        if new_status == OrderStatus.DELIVERED:
            courier.status = CourierStatus.AVAILABLE

        db.session.commit()
        return order
