
from marshmallow import Schema, fields, validate
from backend.models import OrderStatus, CourierStatus

class OrderSchema(Schema):
    id = fields.Int(dump_only=True)
    customer_id = fields.Int(required=True)
    vendor_id = fields.Int(required=True)
    courier_id = fields.Int(allow_none=True)
    delivery_address = fields.Str(required=True)
    total_amount = fields.Decimal(as_string=True, required=True)
    status = fields.Enum(OrderStatus, by_value=True, dump_only=True)
    created_at = fields.DateTime(dump_only=True)
    updated_at = fields.DateTime(dump_only=True)

class CourierSchema(Schema):
    id = fields.Int(dump_only=True)
    user_id = fields.Int(required=True)
    status = fields.Enum(CourierStatus, by_value=True, dump_only=True)
    current_location = fields.Str(allow_none=True)
    vehicle_details = fields.Str(allow_none=True)
    is_approved = fields.Bool(dump_only=True)
    created_at = fields.DateTime(dump_only=True)
    updated_at = fields.DateTime(dump_only=True)

class JobUpdateSchema(Schema):
    status = fields.Str(required=True, validate=validate.OneOf([s.value for s in OrderStatus]))
