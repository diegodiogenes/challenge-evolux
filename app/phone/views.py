from flask import Blueprint, make_response, Response, jsonify, request, current_app
from flask_jwt_extended import jwt_required
from marshmallow import ValidationError

from .models import Phone
from .serializer import PhoneSchema
from flask.views import MethodView

phone_bp = Blueprint('phone', __name__)


class PhoneView(MethodView):
    phone_schema = PhoneSchema()

    @jwt_required
    def get(self, pk: int = None, page=1):
        if not pk:
            phones_schema = PhoneSchema(many=True)
            phones = Phone.query.paginate(page, 10).items
            res = jsonify(phones_schema.dump(phones))
        else:
            phone = Phone.query.filter_by(id=pk).first()
            if not phone:
                return jsonify(error="DID not found with this ID"), 404
            res = self.phone_schema.jsonify(phone)
        return make_response(res, 200)

    @jwt_required
    def post(self):
        try:
            phone = self.phone_schema.load(request.json)
        except ValidationError as err:
            return jsonify(err.messages), 400

        current_app.db.session.add(phone)
        current_app.db.session.commit()
        return self.phone_schema.jsonify(phone), 201

    @jwt_required
    def put(self, pk: int = None):
        phone = Phone.get_by_id(pk)
        if not phone:
            return jsonify(error="DID not found with this ID"), 404

        try:
            obj = self.phone_schema.load(request.json)
        except ValidationError as err:
            return jsonify(err.messages), 400

        delattr(obj, '_sa_instance_state')

        for key, value in obj.__dict__.items():
            setattr(phone, key, value)

        current_app.db.session.commit()

        return self.phone_schema.dump(phone), 200

    @jwt_required
    def delete(self, pk: int = None):
        phone = Phone.get_by_id(pk)

        if not phone:
            return jsonify(error="DID not found with this ID"), 404

        current_app.db.session.delete(phone)
        current_app.db.session.commit()

        return jsonify(''), 204


phone_view = PhoneView.as_view('phone_view')
phone_bp.add_url_rule('/', view_func=phone_view, methods=['GET', 'POST'])
phone_bp.add_url_rule(
    '/<int:pk>', view_func=phone_view, methods=['GET', 'PUT', 'DELETE']
)
