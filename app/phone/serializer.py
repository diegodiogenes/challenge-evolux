from app.utils import ma
from app.currency.serializer import CurrencySchema, Currency
from marshmallow import fields, pre_dump, pre_load, post_load, validate, validates, ValidationError, post_dump
from .models import Phone


class PhoneSchema(ma.SQLAlchemySchema):
    id = fields.Integer()
    value = fields.Str(required=True,
                       validate=validate.Regexp(regex='^(\+\d{1,2}\s)?\d{2,3}?[\s.-]\d{3,5}[\s.-]\d{4}$'))
    monthy_price = fields.Decimal(required=True, as_string=True, data_key="monthyPrice",
                                  validate=[validate.Range(min=0, error="Value must be greater than 0")])
    setup_price = fields.Decimal(required=True, as_string=True, data_key="setupPrice",
                                 validate=[validate.Range(min=0, error="Value must be greater than 0")])
    currency = fields.Nested(lambda: CurrencySchema(only=("name", "money_sign",)))

    class Meta:
        fields = ('id', 'value', 'monthy_price', 'setup_price', 'currency', 'currency.money_sign')
        model = Phone
        include_relationships = True
        load_instance = True
        ordered = True
        dump_only = ['currency.money_sign', 'id']

    @pre_load
    def set_currency(self, in_data: dict, many, **kwargs):
        currency = Currency.query.filter_by(money_sign=in_data['currency']).first_or_404(
            description='There is no data with {}'.format(in_data['currency']))
        in_data['currency'] = {'moneySign': currency.money_sign, 'name': currency.name}
        return in_data

    @validates('currency')
    def validate_currency(self, value: Currency):
        currency = Currency.query.filter_by(money_sign=value.money_sign).first()
        if not currency:
            ValidationError('There is no data with {}'.format(value.money_sign))

    @post_load
    def set_currency_object(self, in_data: Phone, many, **kwargs):
        currency = Currency.query.filter_by(money_sign=in_data.currency_id.money_sign).first()
        in_data.currency_id = currency.id
        return in_data

    @pre_dump
    def set_data_key(self, data: dict, many, **kwargs):
        self.fields.get("currency.money_sign").data_key = "currency"
        return data
