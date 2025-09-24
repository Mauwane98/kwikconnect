from marshmallow import Schema, fields, validate

class UserRegistrationSchema(Schema):
    username = fields.String(required=True, validate=validate.Length(min=3, max=80))
    email = fields.Email(required=True)
    password = fields.String(required=True, validate=validate.Length(min=6))
    role = fields.String(validate=validate.OneOf(['customer', 'vendor', 'courier']), missing='customer')

class UserLoginSchema(Schema):
    email = fields.Email(required=True)
    password = fields.String(required=True)
