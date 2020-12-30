from base import TestFlaskBase
import unittest


class TestCurrency(TestFlaskBase):

    def test_create_currency(self):
        self.create_user()
        token = self.create_token()

        currency = {
            'name': 'BRL',
            'moneySign': 'R$'
        }

        expected = {
            'moneySign': 'R$'
        }

        response = self.client.post('/currency/', json=currency, headers=token)

        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.json['moneySign'], expected['moneySign'])

    def test_invalid_payload_create_currency(self):
        self.create_user()
        token = self.create_token()

        currency = {
            "name": "BRL"
        }

        expected = {
            "moneySign": [
                "Missing data for required field."
            ]
        }

        response = self.client.post('/currency/', json=currency, headers=token)
        self.assertEqual(response.status_code, 400)

        self.assertEqual(response.json, expected)

    def test_create_currency_without_credentials(self):
        response = self.client.post('/currency/', json=self.currency)

        self.assertEqual(response.status_code, 401)

    def test_get_currency(self):
        self.create_currency()
        token = self.create_token()

        response = self.client.get('/currency/1', headers=token)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json['name'], self.currency['name'])

    def test_get_currency_with_id_not_exists(self):
        self.create_currency()
        token = self.create_token()

        response = self.client.get('/currency/3', headers=token)

        self.assertEqual(response.status_code, 404)

    def test_put_currency(self):
        self.create_currency()
        token = self.create_token()

        currency = {
            'name': 'BRL',
            'moneySign': 'R$'
        }

        response = self.client.put('/currency/1', json=currency, headers=token)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json['name'], currency['name'])

    def test_put_currency_with_id_not_exists(self):
        self.create_currency()
        token = self.create_token()

        currency = {
            'name': 'BRL',
            'moneySign': 'R$'
        }

        response = self.client.put('/currency/3', json=currency, headers=token)

        self.assertEqual(response.status_code, 404)

    def test_create_currency_with_same_money_sign(self):
        self.create_currency()
        token = self.create_token()

        currency = {
            'name': 'USD',
            'moneySign': 'U$'
        }

        expected = {
            "moneySign": [
                "Currency with money sign U$ already exists"
            ]
        }

        response = self.client.post('/currency/', json=currency, headers=token)

        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json, expected)


if __name__ == '__main__':
    unittest.main()
