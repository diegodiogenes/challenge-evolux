import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from flask_jwt_extended import JWTManager


app = Flask(__name__)
app.config.from_object('config.BaseConfig')

JWTManager(app)

db = SQLAlchemy(app)
ma = Marshmallow(app)

from app.currency.views import currency_bp
from phone.views import phone_bp
from users.views import user_bp

app.register_blueprint(currency_bp, url_prefix='/currency')
app.register_blueprint(phone_bp, url_prefix='/phone')
app.register_blueprint(user_bp, url_prefix='/user')

db.create_all()
app.db = db
