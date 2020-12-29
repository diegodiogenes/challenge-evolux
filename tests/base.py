from json import loads
from unittest import TestCase
from app import create_app
from flask import url_for


class TestFlaskBase(TestCase):
    def setUp(self):
        """Roda antes de todos os testes."""
        self.app = create_app()
        self.app.testing = True
        self.app_context = self.app.test_request_context()
        self.app_context.push()
        self.client = self.app.test_client()
        self.app.db.create_all()
        self.user = {
            'username': 'test',
            'password': '1234'
        }

        self.currency = {
            'name': 'USD',
            'moneySign': 'U$'
        }

    def tearDown(self):
        """Roda depois de todos os testes."""
        self.app.db.drop_all()

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
