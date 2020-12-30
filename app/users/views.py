from flask import Blueprint, make_response, Response, jsonify, request, current_app
from marshmallow import ValidationError

from .models import User
from .serializer import UserSchema, LoginSchema
from flask.views import MethodView
from flask_jwt_extended import create_access_token

user_bp = Blueprint('user', __name__)
login_schema = LoginSchema()


class UserView(MethodView):
    user_schema = UserSchema()

    def post(self):
        try:
            try:
                user = self.user_schema.load(request.json)
            except ValidationError as err:
                return jsonify(err.messages), 400

            current_app.db.session.add(user)
            current_app.db.session.commit()
            return self.user_schema.jsonify(user), 201
        except Exception:
            return jsonify(error='An unexpected error has occurred, please try again'), 500


@user_bp.route('/login', methods=['POST'])
def login():
    """
    Handle requests to make login
    """
    try:
        try:
            data = login_schema.load(request.get_json())
        except ValidationError as err:
            return jsonify(err.messages), 400

        user = User.get_by_login(data['username'], data['password'])
        if not user:
            return jsonify(error='Invalid credentials, please try again'), 401

        return jsonify(user=user.as_dict(), access_token=create_access_token(user.as_dict())), 200
    except Exception:
        return jsonify(error='An unexpected error has occurred, please try again'), 500


user_view = UserView.as_view('user_view')
user_bp.add_url_rule('/', view_func=user_view, methods=['GET', 'POST'])
