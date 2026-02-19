from marshmallow import Schema, fields, validate


class RegisterSchema(Schema):
    name = fields.Str(
        required=True,
        validate=validate.Length(min=3, max=100)
    )

    email = fields.Email(required=True)

    phone = fields.Str(required=False, allow_none=True, validate=validate.Length(max=20))

    password = fields.Str(
        required=True,
        validate=validate.Length(min=6)
    )

    role_id = fields.Int(required=True)


class LoginSchema(Schema):
    email = fields.Email(required=True)
    password = fields.Str(required=True)
