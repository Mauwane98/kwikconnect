
from marshmallow import Schema, fields, validate

class ProductSchema(Schema):
    id = fields.Int(dump_only=True)
    name = fields.Str(required=True)
    description = fields.Str()
    price = fields.Decimal(as_string=True, required=True)
    image_url = fields.Str()
    is_available = fields.Bool()

class VendorSchema(Schema):
    id = fields.Int(dump_only=True)
    business_name = fields.Str(required=True)
    description = fields.Str()
    address = fields.Str(required=True)
    profile_image_url = fields.Str()
    is_open = fields.Bool()
    products = fields.Nested(ProductSchema, many=True, dump_only=True)
