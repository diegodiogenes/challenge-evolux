from unittest import TestCase
from app import app, db


class TestFlaskBase(TestCase):

    def setUp(self):
        """Setup Tests."""
        app.config.from_object('config.TestingConfig')
        app_ctx = app.test_request_context()
        app_ctx.push()
        db.app = app
        db.create_all()

        self.client = app.test_client()
        self.user = {
            'username': 'test',
            'password': '1234'
        }

        self.currency = {
            'name': 'USD',
            'moneySign': 'U$'
        }

        self.phone = {
            "value": "+55 84 95232-4231",
            "monthyPrice": "0.03",
            "setupPrice": "3.40",
            "currency": "U$"
        }

    def tearDown(self):
        """Drop database when tests finish."""
        db.drop_all(app=app)

    def create_user(self):
        self.client.post('/user/', json=self.user)

    def create_token(self):
        login = self.client.post('/user/login', json=self.user)
        return {
            'Authorization':
                'Bearer ' + login.json['access_token']
        }

    def create_currency(self):
        self.create_user()
        token = self.create_token()
        self.client.post('/currency/', json=self.currency, headers=token)

    def create_phone(self):
        self.create_user()
        self.create_currency()
        token = self.create_token()
        self.client.post('/phone/', json=self.phone, headers=token)
