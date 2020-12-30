from flask import Blueprint, make_response, Response, jsonify, request, current_app
from flask_jwt_extended import jwt_required
from marshmallow import ValidationError

from .models import Currency
from .serializer import CurrencySchema
from flask.views import MethodView

currency_bp = Blueprint('currency', __name__)


class CurrencyView(MethodView):
    currency_schema = CurrencySchema()

    @jwt_required
    def get(self, pk: int = None, page=1):
        if not pk:
            currencies_schema = CurrencySchema(many=True)
            currencies = Currency.query.all()
            res = jsonify(currencies_schema.dump(currencies))
        else:
            currency = Currency.get_by_id(pk)
            if not currency:
                return jsonify(error="Currency not found with this ID"), 404
            res = self.currency_schema.jsonify(currency)
        return res

    @jwt_required
    def post(self):
        try:
            currency = self.currency_schema.load(request.json)
        except ValidationError as err:
            return jsonify(err.messages), 400
        current_app.db.session.add(currency)
        current_app.db.session.commit()
        return self.currency_schema.jsonify(currency), 201

    @jwt_required
    def put(self, pk: int = None):
        currency = Currency.get_by_id(pk)
        if not currency:
            return jsonify(error="Currency not found with this ID"), 404

        try:
            obj = self.currency_schema.load(request.json)
        except ValidationError as err:
            return jsonify(err.messages), 400

        delattr(obj, '_sa_instance_state')

        for key, value in obj.__dict__.items():
            setattr(currency, key, value)

        current_app.db.session.commit()

        return self.currency_schema.jsonify(currency), 200

    @jwt_required
    def delete(self, pk: int = None):
        currency = Currency.get_by_id(pk)

        if not currency:
            return jsonify(error="Currency not found with this ID"), 404

        current_app.db.session.delete(currency.first())
        current_app.db.session.commit()

        return jsonify(''), 204


currency_view = CurrencyView.as_view('currency_view')
currency_bp.add_url_rule('/', view_func=currency_view, methods=['GET', 'POST'])
currency_bp.add_url_rule(
    '/<int:pk>', view_func=currency_view, methods=['GET', 'PUT', 'DELETE']
)
