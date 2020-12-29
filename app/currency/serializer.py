from app import ma
from app.currency.models import Currency
from marshmallow import fields, pre_dump, validate, validates, ValidationError


class CurrencySchema(ma.SQLAlchemySchema):
    money_sign = fields.Str(required=True, validate=validate.Length(min=1, max=3), data_key="moneySign")
    name = fields.Str(required=True)

    class Meta:
        fields = ('id', 'name', 'money_sign')
        dump_only = ['id']
        load_instance = True
        model = Currency

    @validates('money_sign')
    def validate_money_sign(self, value: str):
        currency = Currency.query.filter_by(money_sign=value).first()
        if currency:
            raise ValidationError('Currency with money sign {} already exists'.format(value))
