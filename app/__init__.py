import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from flask_jwt_extended import JWTManager


def create_app() -> Flask:
    app = Flask(__name__)
    app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL')
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['JSON_SORT_KEYS'] = False
    app.config['JWT_SECRET_KEY'] = os.getenv('JWT_SECRET_KEY', 'My precious')

    JWTManager(app)

    db = SQLAlchemy(app)
    ma = Marshmallow(app)

    from currency.models import Currency
    from phone.models import Phone
    from users.models import User
    from app.currency.views import currency_bp
    from phone.views import phone_bp
    from users.views import user_bp

    app.register_blueprint(currency_bp, url_prefix='/currency')
    app.register_blueprint(phone_bp, url_prefix='/phone')
    app.register_blueprint(user_bp, url_prefix='/user')

    db.create_all()
    app.db = db
    return app
