

from backend.models.vendor import Vendor
from backend.models.product import Product
from backend.models.user import User
from backend.errors import NotFoundError, ConflictError, ForbiddenError

class VendorService:
    @staticmethod
    def get_all_vendors():
        # Backwards-compatible: return all approved/open vendors as dicts
        vendors = Vendor.find({'is_approved': True, 'is_open': True})
        return [Vendor.to_dict(v) for v in vendors]

    @staticmethod
    def search_vendors(filters: dict):
        """
        Search vendors using a simple MongoDB query.
        Supported filters: query (text), category, delivery_time (under_30, 30_60)
        """
        query = {'is_approved': True, 'is_open': True}

        text = filters.get('query')
        if text:
            # Case-insensitive regex match against name and description
            regex = {'$regex': text, '$options': 'i'}
            query['$or'] = [{'name': regex}, {'description': regex}, {'business_name': regex}]

        category = filters.get('category')
        if category:
            # support either 'category' or 'vendor_type' fields on the vendor document
            query['$or'] = query.get('$or', []) + [{'category': category}, {'vendor_type': category}]

        delivery_time = filters.get('delivery_time')
        if delivery_time:
            # If vendors store an `avg_delivery_mins` field, use it to filter; otherwise ignore
            if delivery_time == 'under_30':
                query['avg_delivery_mins'] = {'$lte': 30}
            elif delivery_time == '30_60':
                query['avg_delivery_mins'] = {'$gt': 30, '$lte': 60}

        vendors_data = Vendor.get_collection().find(query)
        # Return list of vendor dicts
        return [Vendor.to_dict(v) for v in vendors_data]

    @staticmethod
    def get_vendor_products(vendor_id):
        vendor = Vendor.find_by_id(vendor_id)
        if not vendor: # Assuming is_approved is a property of the Vendor object
            raise NotFoundError("Vendor not found or not approved")
        # Add check for vendor.is_approved if it exists in the MongoDB Vendor model
        # if not vendor.is_approved:
        #     raise NotFoundError("Vendor not found or not approved")

        products_data = Product.products_collection.find({'vendor_id': vendor_id, 'is_available': True})
        return [Product(**data) for data in products_data]

    @staticmethod
    def create_or_update_vendor_profile(user_id, data):
        user = User.find_by_id(user_id)
        if not user or user.role != 'vendor':
            raise ForbiddenError("User is not a vendor")

        vendor = Vendor.find_by_user_id(str(user._id))
        if not vendor:
            vendor = Vendor(user_id=str(user._id), name=data.get('business_name'), description=data.get('description')) # Assuming name and description are required for Vendor init
            # You might need to add more fields to Vendor init or set them after creation
        
        vendor.name = data.get('business_name', vendor.name) # Assuming business_name maps to name
        vendor.description = data.get('description', vendor.description)
        # Add other fields as needed, e.g., address, profile_image_url
        # vendor.address = data.get('address', vendor.address)
        # vendor.profile_image_url = data.get('profile_image_url', vendor.profile_image_url)

        vendor.save()
        return vendor

    @staticmethod
    def create_product(user_id, data):
        vendor = Vendor.find_by_user_id(user_id)
        if not vendor:
            raise ForbiddenError("User is not a vendor")

        new_product = Product(
            vendor_id=str(vendor._id), # Store vendor's MongoDB _id
            name=data['name'],
            description=data.get('description'),
            price=data['price'],
            image_url=data.get('image_url')
        )
        new_product.save()
        return new_product

    @staticmethod
    def update_product(user_id, product_id, data):
        vendor = Vendor.find_by_user_id(user_id)
        if not vendor:
            raise ForbiddenError("User is not a vendor")

        product = Product.find_by_id(product_id)
        if not product:
            raise NotFoundError("Product not found")

        if product.vendor_id != str(vendor._id): # Compare with string representation of vendor._id
            raise ForbiddenError("Unauthorized to edit this product")

        product.name = data.get('name', product.name)
        product.description = data.get('description', product.description)
        product.price = data.get('price', product.price)
        product.image_url = data.get('image_url', product.image_url)
        # Assuming is_available is a property of the Product object
        # product.is_available = data.get('is_available', product.is_available)
        product.save()
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
