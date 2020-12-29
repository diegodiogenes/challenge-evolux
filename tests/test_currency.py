from base import TestFlaskBase


class TestCurrency(TestFlaskBase):

    def test_create_currency(self):
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

