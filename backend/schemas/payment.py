
from marshmallow import Schema, fields, validate
from backend.models import TransactionType

class WalletSchema(Schema):
    id = fields.Int(dump_only=True)
    user_id = fields.Int(dump_only=True)
    balance = fields.Decimal(as_string=True, dump_only=True)
    created_at = fields.DateTime(dump_only=True)
    updated_at = fields.DateTime(dump_only=True)

class TransactionSchema(Schema):
    id = fields.Int(dump_only=True)
    wallet_id = fields.Int(dump_only=True)
    amount = fields.Decimal(as_string=True, dump_only=True)
    transaction_type = fields.Enum(TransactionType, by_value=True, dump_only=True)
    description = fields.Str(dump_only=True)
    created_at = fields.DateTime(dump_only=True)

class DepositWithdrawSchema(Schema):
    amount = fields.Decimal(required=True, validate=validate.Range(min=0.01))

class TransferSchema(Schema):
    receiver_id = fields.Int(required=True)
    amount = fields.Decimal(required=True, validate=validate.Range(min=0.01))
