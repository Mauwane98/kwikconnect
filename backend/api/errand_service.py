
from backend import db
from backend.models import Errand, ErrandStatus, User, UserRole, CourierStatus
from backend.errors import NotFoundError, ForbiddenError, BadRequestError, ConflictError

class ErrandService:
    @staticmethod
    def create_errand(customer_id, data):
        description = data.get('description')
        pickup_address = data.get('pickup_address')
        dropoff_address = data.get('dropoff_address')
        estimated_fee = data.get('estimated_fee')

        new_errand = Errand(
            customer_id=customer_id,
            description=description,
            pickup_address=pickup_address,
            dropoff_address=dropoff_address,
            estimated_fee=estimated_fee
        )
        db.session.add(new_errand)
        db.session.commit()
        return new_errand

    @staticmethod
    def get_all_errands(current_user):
        if current_user.role == UserRole.ADMIN:
            errands = Errand.query.all()
        elif current_user.role == UserRole.CUSTOMER:
            errands = Errand.query.filter_by(customer_id=current_user.id).all()
        elif current_user.role == UserRole.COURIER:
            errands = Errand.query.filter(
                (Errand.status == ErrandStatus.PENDING) | (Errand.courier_id == current_user.courier.id)
            ).all()
        else:
            raise ForbiddenError("Unauthorized")
        return errands

    @staticmethod
    def get_errand_details(current_user, errand_id):
        errand = Errand.query.get(errand_id)
        if not errand:
            raise NotFoundError("Errand not found.")

        # Authorization check
        if current_user.role == UserRole.CUSTOMER and errand.customer_id != current_user.id:
            raise ForbiddenError("Unauthorized to view this errand")
        if current_user.role == UserRole.COURIER and errand.courier_id != current_user.courier.id and errand.status != ErrandStatus.PENDING:
            raise ForbiddenError("Unauthorized to view this errand")
        if current_user.role not in [UserRole.ADMIN, UserRole.CUSTOMER, UserRole.COURIER]:
            raise ForbiddenError("Unauthorized")
        
        return errand

    @staticmethod
    def accept_errand(user_id, errand_id):
        courier = User.query.get(user_id).courier
        if courier.status != CourierStatus.AVAILABLE:
            raise ConflictError(f"Cannot accept errand, your status is '{courier.status.value}'.")

        errand = Errand.query.get(errand_id)
        if not errand:
            raise NotFoundError("Errand not found.")

        if errand.status != ErrandStatus.PENDING or errand.courier_id is not None:
            raise ConflictError("Errand is no longer available or already accepted.")

        errand.courier_id = courier.id
        errand.status = ErrandStatus.ACCEPTED
        courier.status = CourierStatus.BUSY
        db.session.commit()
        return errand

    @staticmethod
    def update_errand_status(user_id, errand_id, new_status_str):
        courier = User.query.get(user_id).courier
        errand = Errand.query.get(errand_id)

        if not errand:
            raise NotFoundError("Errand not found.")

        if errand.courier_id != courier.id:
            raise ForbiddenError("You are not assigned to this errand.")

        try:
            new_status = ErrandStatus(new_status_str)
        except ValueError:
            raise BadRequestError(f"'{new_status_str}' is not a valid errand status.")

        valid_transitions = {
            ErrandStatus.ACCEPTED: [ErrandStatus.IN_PROGRESS, ErrandStatus.CANCELLED],
            ErrandStatus.IN_PROGRESS: [ErrandStatus.COMPLETED, ErrandStatus.CANCELLED]
        }

        if new_status not in valid_transitions.get(errand.status, []):
            raise ConflictError(f"Invalid status transition from '{errand.status.value}' to '{new_status.value}'.")

        errand.status = new_status
        if new_status == ErrandStatus.COMPLETED or new_status == ErrandStatus.CANCELLED:
            courier.status = CourierStatus.AVAILABLE
        
        db.session.commit()
        return errand

    @staticmethod
    def delete_errand(user_id, errand_id):
        errand = Errand.query.get(errand_id)
        if not errand:
            raise NotFoundError("Errand not found.")

        if errand.customer_id != user_id:
            raise ForbiddenError("Unauthorized to delete this errand")
        
        if errand.status != ErrandStatus.PENDING:
            raise BadRequestError("Only pending errands can be deleted")

        db.session.delete(errand)
        db.session.commit()
