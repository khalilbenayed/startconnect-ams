import unittest
from app import create_app
from tests.utils import use_test_database


class StudentResourceTest(unittest.TestCase):
    def setUp(self):
        app, _ = create_app('TESTING')
        self.app = app.test_client()

    @use_test_database
    def test_post_1(self):
        test_payload_1 = {
            'first_name': 'test',
            'last_name': 'test_test',
            'email': 'test@test.com',
            'password': 'test',
            'state': 'test'
        }

        resp = self.app.post('api/students/', data=test_payload_1)
        resp_data = resp.json
        self.assertEqual(resp_data.get('first_name'), test_payload_1.get('first_name'))
        self.assertEqual(resp_data.get('last_name'), test_payload_1.get('last_name'))
        self.assertEqual(resp_data.get('email'), test_payload_1.get('email'))
        self.assertEqual(resp_data.get('state'), test_payload_1.get('state'))


if __name__ == '__main__':
    unittest.main()
