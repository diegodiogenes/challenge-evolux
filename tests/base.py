from json import loads
from unittest import TestCase
from app.conf_test import db, app_test
from flask import url_for
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from app import conf_test


class TestFlaskBase(TestCase):

    def create_app(self):
        return app_test

    def setUp(self):
        """Setup Tests."""
        self.app = self.create_app()
        self.client = self.app.test_client()
        db.create_all()

        self.app.db = db
        self.user = {
            'username': 'test',
            'password': '1234'
        }

        self.currency = {
            'name': 'USD',
            'moneySign': 'U$'
        }

    def tearDown(self):
        """Drop database when tests finish."""
        db.session.remove()
        db.drop_all()

    def create_user(self):
        self.client.post('/user/', json=self.user)

    def create_token(self):
        login = self.client.post('/user/login', json=self.user)
        return {
            'Authorization':
                'Bearer ' + login.json['access_token']
        }

    def create_currency(self):
        token = self.create_token()
        self.client.post('/currency/', json=self.currency, headers=token)
