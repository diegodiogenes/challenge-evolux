from app import ma
from .models import User
from marshmallow import fields, post_load


class UserSchema(ma.SQLAlchemySchema):
    username = fields.String(required=True)
    password = fields.String(required=True)

    class Meta:
        model = User
        load_instance = True


class LoginSchema(ma.Schema):
    username = fields.String(required=True)
    password = fields.String(required=True)
