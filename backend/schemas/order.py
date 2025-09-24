
from marshmallow import Schema, fields, validate
from backend.models import OrderStatus

class OrderItemSchema(Schema):
    product_id = fields.Int(required=True)
    quantity = fields.Int(required=True, validate=validate.Range(min=1))
    price_at_purchase = fields.Decimal(as_string=True, dump_only=True)
    product_name = fields.Str(dump_only=True)

class OrderCreateSchema(Schema):
    vendor_id = fields.Int(required=True)
    delivery_address = fields.Str(required=True)
    items = fields.List(fields.Nested(OrderItemSchema), required=True, validate=validate.Length(min=1))

class OrderSchema(Schema):
    id = fields.Int(dump_only=True)
    customer_id = fields.Int(dump_only=True)
    vendor_id = fields.Int(dump_only=True)
    courier_id = fields.Int(allow_none=True, dump_only=True)
    delivery_address = fields.Str(dump_only=True)
    total_amount = fields.Decimal(as_string=True, dump_only=True)
    status = fields.Enum(OrderStatus, by_value=True, dump_only=True)
    created_at = fields.DateTime(dump_only=True)
    updated_at = fields.DateTime(dump_only=True)
    items = fields.List(fields.Nested(OrderItemSchema), dump_only=True)
    vendor_name = fields.Str(dump_only=True)
