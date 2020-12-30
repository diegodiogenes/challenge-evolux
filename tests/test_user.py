from base import TestFlaskBase
import unittest


class TestUser(TestFlaskBase):
    user = {
        'username': 'test',
        'password': '1234'
    }

    def test_create_user(self):
        assert_equal = {
            'id': '1',
            'username': 'test'
        }
        response = self.client.post('/user/', json=self.user)

        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.json['username'], assert_equal['username'])

    def test_invalid_payload_create_user(self):
        user = {
            'username': 'test',
        }

        expected = {'password': ['Missing data for required field.']}

        response = self.client.post('/user/', json=user)
        self.assertEqual(response.status_code, 400)

        self.assertEqual(response.json, expected)

    def test_login_user(self):
        self.create_user()
        response = self.client.post('/user/login', json=self.user)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json['user']['username'], self.user['username'])


if __name__ == '__main__':
    unittest.main()
