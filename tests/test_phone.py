from base import TestFlaskBase
import unittest


class TestPhone(TestFlaskBase):
    payload = {
        "value": "+55 84 95232-4231",
        "monthyPrice": "0.03",
        "setupPrice": "3.40",
        "currency": "U$"
    }

    def test_create_phone(self):
        self.create_currency()
        token = self.create_token()

        expected = {
            "id": 1,
            "value": "+55 84 95232-4231",
            "monthyPrice": "0.03",
            "setupPrice": "3.40",
            "currency": "U$"
        }

        response = self.client.post('/phone/', json=self.payload, headers=token)

        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.json, expected)

    def test_create_phone_with_not_currency_registered(self):
        self.create_currency()
        token = self.create_token()

        payload = {
            "value": "+55 84 95232-4231",
            "monthyPrice": "0.03",
            "setupPrice": "3.40",
            "currency": "D$"
        }

        expected = {
            "currency": [
                "There is no currency with D$"
            ]
        }

        response = self.client.post('/phone/', json=payload, headers=token)

        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json, expected)

    def test_create_phone_with_same_value_phone_number(self):
        self.create_phone()
        token = self.create_token()

        expected = {
            "value": [
                "DID with value +55 84 95232-4231 already exists"
            ]
        }

        response = self.client.post('/phone/', json=self.phone, headers=token)

        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json, expected)

    def test_invalid_payload_create_phone(self):
        self.create_currency()
        token = self.create_token()

        phone = {
            "monthyPrice": "0.03",
            "setupPrice": "3.40",
            "currency": "U$"
        }

        expected = {
            "value": [
                "Missing data for required field."
            ]
        }

        response = self.client.post('/phone/', json=phone, headers=token)
        self.assertEqual(response.status_code, 400)

        self.assertEqual(response.json, expected)

    def test_invalid_payload_with_negative_numbers_create_phone(self):
        self.create_currency()
        token = self.create_token()

        phone = {
            "value": "+55 84 91232-4321",
            "monthyPrice": "-0.03",
            "setupPrice": "-3.40",
            "currency": "U$"
        }

        expected = {
            "monthyPrice": [
                "Value must be greater than 0"
            ],
            "setupPrice": [
                "Value must be greater than 0"
            ]
        }

        response = self.client.post('/phone/', json=phone, headers=token)
        self.assertEqual(response.status_code, 400)

        self.assertEqual(response.json, expected)

    def test_create_phone_without_credentials(self):
        response = self.client.post('/phone/', json=self.payload)

        self.assertEqual(response.status_code, 401)

    def test_get_phone(self):
        self.create_phone()
        token = self.create_token()

        response = self.client.get('/phone/1', headers=token)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json['value'], self.payload['value'])

    def test_put_phone(self):
        self.create_phone()
        token = self.create_token()

        phone = {
            "value": "+55 84 91232-1111",
            "monthyPrice": "0.03",
            "setupPrice": "3.40",
            "currency": "U$"
        }

        response = self.client.put('/phone/1', json=phone, headers=token)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json['value'], phone['value'])

    def test_delete_phone(self):
        self.create_phone()
        token = self.create_token()

        response = self.client.delete('/phone/1', headers=token)

        self.assertEqual(response.status_code, 204)


if __name__ == '__main__':
    unittest.main()
