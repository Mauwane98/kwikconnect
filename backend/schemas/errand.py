
from marshmallow import Schema, fields, validate
from backend.models import ErrandStatus

class ErrandSchema(Schema):
    id = fields.Int(dump_only=True)
    customer_id = fields.Int(dump_only=True)
    courier_id = fields.Int(allow_none=True, dump_only=True)
    description = fields.Str(required=True, validate=validate.Length(min=1, max=255))
    pickup_address = fields.Str(required=True, validate=validate.Length(min=1, max=255))
    dropoff_address = fields.Str(required=True, validate=validate.Length(min=1, max=255))
    estimated_fee = fields.Decimal(as_string=True, required=True, validate=validate.Range(min=0.01))
    status = fields.Enum(ErrandStatus, by_value=True, dump_only=True)
    created_at = fields.DateTime(dump_only=True)
    updated_at = fields.DateTime(dump_only=True)

class ErrandUpdateStatusSchema(Schema):
    status = fields.Str(required=True, validate=validate.OneOf([s.value for s in ErrandStatus]))
