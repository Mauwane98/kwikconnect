
from backend import db
from backend.models import Vendor, Product, User, UserRole
from backend.errors import NotFoundError, ConflictError, ForbiddenError

class VendorService:
    @staticmethod
    def get_all_vendors():
        return Vendor.query.filter_by(is_approved=True, is_open=True).all()

    @staticmethod
    def get_vendor_products(vendor_id):
        vendor = Vendor.query.get(vendor_id)
        if not vendor or not vendor.is_approved:
            raise NotFoundError("Vendor not found or not approved")
        return Product.query.filter_by(vendor_id=vendor_id, is_available=True).all()

    @staticmethod
    def create_or_update_vendor_profile(user_id, data):
        user = User.query.get(user_id)
        if user.role != UserRole.VENDOR:
            raise ForbiddenError("User is not a vendor")

        vendor = user.vendor
        if not vendor:
            vendor = Vendor(user_id=user_id)
            db.session.add(vendor)

        vendor.business_name = data.get('business_name')
        vendor.description = data.get('description')
        vendor.address = data.get('address')
        vendor.profile_image_url = data.get('profile_image_url')
        db.session.commit()
        return vendor

    @staticmethod
    def create_product(user_id, data):
        vendor = Vendor.query.filter_by(user_id=user_id).first()
        if not vendor:
            raise ForbiddenError("User is not a vendor")

        new_product = Product(
            vendor_id=vendor.id,
            name=data['name'],
            description=data.get('description'),
            price=data['price'],
            image_url=data.get('image_url')
        )
        db.session.add(new_product)
        db.session.commit()
        return new_product

    @staticmethod
    def update_product(user_id, product_id, data):
        vendor = Vendor.query.filter_by(user_id=user_id).first()
        if not vendor:
            raise ForbiddenError("User is not a vendor")

        product = Product.query.get(product_id)
        if not product:
            raise NotFoundError("Product not found")

        if product.vendor_id != vendor.id:
            raise ForbiddenError("Unauthorized to edit this product")

        product.name = data.get('name', product.name)
        product.description = data.get('description', product.description)
        product.price = data.get('price', product.price)
        product.image_url = data.get('image_url', product.image_url)
        product.is_available = data.get('is_available', product.is_available)
        db.session.commit()
        return product

    @staticmethod
    def delete_product(user_id, product_id):
        vendor = Vendor.query.filter_by(user_id=user_id).first()
        if not vendor:
            raise ForbiddenError("User is not a vendor")

        product = Product.query.get(product_id)
        if not product:
            raise NotFoundError("Product not found")

        if product.vendor_id != vendor.id:
            raise ForbiddenError("Unauthorized to delete this product")

        db.session.delete(product)
        db.session.commit()
