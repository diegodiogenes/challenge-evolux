from base import TestFlaskBase


class TestPhone(TestFlaskBase):
    phone = {
        "value": "+55 84 91232-4231",
        "monthyPrice": "0.03",
        "setupPrice": "3.40",
        "currency": "U$"
    }

    def test_create_phone(self):
        self.create_user()
        self.create_currency()
        token = self.create_token()

        expected = {
            "value": "+55 84 91232-4321",
            "monthyPrice": "0.03",
            "setupPrice": "3.40",
            "currency": "U$"
        }

        response = self.client.post('/phone/', json=self.phone, headers=token)

        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.json['monthyPrice'], expected['monthyPrice'])

    def test_invalid_payload_create_currency(self):
        self.create_user()
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

    def test_invalid_payload_with_negative_numbers_create_currency(self):
        self.create_user()
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
        response = self.client.post('/phone/', json=self.phone)

        self.assertEqual(response.status_code, 401)

    def test_get_phone(self):
        token = self.create_token()

        response = self.client.get('/phone/1', headers=token)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json['value'], self.phone['value'])

    def test_put_phone(self):
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
